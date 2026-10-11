"""Crash recovery, artifact integrity, and real spawn-process serialization."""

import hashlib
import json
import multiprocessing
import os
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from noteforge import AnalysisRequest, JobStatus, export_job, run_job
from noteforge.cli import main
from noteforge.errors import NoteForgeError
from noteforge.models import ArtifactSet, JobResult, StageStatus
from noteforge.storage.atomic import write_text
from noteforge.storage.cleanup import cleanup_old_jobs
from noteforge.storage.context import ContextStore
from noteforge.storage.locking import JobLock
from noteforge.storage.state import StateManager


def _save_key(root, key):
    ContextStore("shared", root).save(key, {"written": key})


def _hold_lock(root, ready):
    with JobLock("held", root, execution=True):
        ready.set()
        ready.wait(0.1)
        import time

        time.sleep(30)


def _run_shared(root):
    # All stages are deterministic; this worker makes no network requests.
    with patch("noteforge.llm.chat", return_value=None):
        run_job(AnalysisRequest(topic="bibliographic research", provider="mock", job_id="shared"),
                output_root=Path(root))


def _request():
    return AnalysisRequest(topic="transformer deployment", provider="mock", job_id="recovery")


@pytest.fixture(autouse=True)
def no_llm_network():
    with patch("noteforge.llm.chat", return_value=None):
        yield


def test_all_three_artifacts_agree_and_sdk_round_trips(tmp_path):
    result = run_job(_request(), output_root=tmp_path)
    assert set(result.export_paths) == {"json", "html"}
    payload = json.loads(result.export_paths["json"].read_text(encoding="utf-8"))
    assert payload["markdown"] == result.report_path.read_text(encoding="utf-8")
    assert payload["sources"][0]["source_type"] == "simulated"
    assert JobResult.from_json(result.to_json()) == result
    hashes = ContextStore("recovery", tmp_path).load("report")["artifact_hashes"]
    assert all(hashlib.sha256((result.report_path.parent / name).read_bytes()).hexdigest() == digest
               for name, digest in hashes.items())


@pytest.mark.parametrize("filename", ["report.md", "report.json", "report.html"])
def test_missing_or_corrupt_export_recovers_without_retrieving_again(tmp_path, filename):
    result = run_job(_request(), output_root=tmp_path)
    (result.report_path.parent / filename).write_text("corrupt", encoding="utf-8")
    with patch("noteforge.pipeline.search_literature", side_effect=AssertionError("provider reran")):
        restored = run_job(AnalysisRequest(job_id="recovery"), output_root=tmp_path)
    assert restored.status is JobStatus.COMPLETED
    assert (restored.report_path.parent / filename).read_text(encoding="utf-8") != "corrupt"


def test_persist_failure_never_marks_stage_complete_and_resume_reuses_prior_stages(tmp_path):
    real_save = ContextStore.save

    def fail_synthesis(self, key, value):
        if key == "synthesis":
            raise OSError("injected persistence failure")
        return real_save(self, key, value)

    with patch.object(ContextStore, "save", fail_synthesis), pytest.raises(NoteForgeError):
        run_job(_request(), output_root=tmp_path)
    manager = StateManager("recovery", tmp_path)
    assert manager.load_state().stages["synthesis"].status is StageStatus.FAILED
    with patch("noteforge.pipeline.search_literature", side_effect=AssertionError("provider reran")):
        result = run_job(AnalysisRequest(job_id="recovery"), output_root=tmp_path)
    assert result.status is JobStatus.COMPLETED
    assert manager.load_state().error is None


def test_missing_completed_context_rebuilds_only_dependencies(tmp_path):
    run_job(_request(), output_root=tmp_path)
    ContextStore("recovery", tmp_path).discard(["synthesis"])
    with patch("noteforge.pipeline.search_literature", side_effect=AssertionError("provider reran")):
        result = run_job(AnalysisRequest(job_id="recovery"), output_root=tmp_path)
    assert result.status is JobStatus.COMPLETED
    assert ContextStore("recovery", tmp_path).load("synthesis") is not None


def test_interrupted_running_stage_recovers_after_process_exit(tmp_path):
    run_job(_request(), output_root=tmp_path)
    manager = StateManager("recovery", tmp_path)
    state = manager.load_state()
    state.status = JobStatus.RUNNING
    state.stages["report_generation"].status = StageStatus.RUNNING
    manager.save_state(state)
    result = run_job(AnalysisRequest(job_id="recovery"), output_root=tmp_path)
    assert result.status is JobStatus.COMPLETED


def test_export_failure_does_not_complete_job(tmp_path):
    with patch("noteforge.pipeline.write_exports", side_effect=OSError("injected export failure")), \
         pytest.raises(NoteForgeError):
        run_job(_request(), output_root=tmp_path)
    assert StateManager("recovery", tmp_path).load_state().status is JobStatus.FAILED
    with patch("noteforge.pipeline.search_literature", side_effect=AssertionError("provider reran")):
        assert run_job(AnalysisRequest(job_id="recovery"), output_root=tmp_path).status is JobStatus.COMPLETED


def test_atomic_replace_failure_preserves_previous_bytes_and_cleans_temporary(tmp_path):
    target = tmp_path / "report.md"
    target.write_text("previous", encoding="utf-8")
    with patch("noteforge.storage.atomic.os.replace", side_effect=OSError("injected")), pytest.raises(OSError):
        write_text(target, "replacement")
    assert target.read_text(encoding="utf-8") == "previous"
    assert list(tmp_path.glob("*.tmp")) == []


def test_explicit_export_preserves_markdown_and_does_not_rerun_analysis(tmp_path, capsys):
    result = run_job(_request(), output_root=tmp_path)
    original = result.report_path.read_bytes()
    with patch("noteforge.pipeline.search_literature", side_effect=AssertionError("provider reran")):
        path = export_job("recovery", format="html", output_root=tmp_path)
        assert main(["export", "recovery", "--format", "json", "--output-root", str(tmp_path)]) == 0
    assert path.is_file()
    assert "report.json" in capsys.readouterr().out
    assert result.report_path.read_bytes() == original


def test_export_old_v3_job_with_only_markdown(tmp_path):
    result = run_job(_request(), output_root=tmp_path)
    context = ContextStore("recovery", tmp_path)
    report_data = context.load("report")
    context.save("report", {key: report_data[key] for key in ["sources", "warnings", "report_path"]})
    for path in result.export_paths.values():
        path.unlink()
    original = result.report_path.read_bytes()
    assert export_job("recovery", output_root=tmp_path).is_file()
    assert result.report_path.read_bytes() == original
    assert ArtifactSet.from_dict({"report": "report.md"}).report_json is None


def test_export_rejects_missing_unfinished_and_invalid_format(tmp_path):
    with pytest.raises(FileNotFoundError):
        export_job("missing", output_root=tmp_path)
    with pytest.raises(ValueError):
        export_job("missing", format="pdf", output_root=tmp_path)
    StateManager("pending", tmp_path).init_state()
    with pytest.raises(ValueError):
        export_job("pending", output_root=tmp_path)


def test_multiple_processes_preserve_distinct_context_updates(tmp_path):
    spawn = multiprocessing.get_context("spawn")
    keys = ["document", "keywords", "literature", "synthesis"]
    processes = [spawn.Process(target=_save_key, args=(str(tmp_path), key)) for key in keys]
    try:
        for process in processes:
            process.start()
        for process in processes:
            process.join(20)
            assert process.exitcode == 0
        data = ContextStore("shared", tmp_path).load_all()
        assert all(data[key] == {"written": key} for key in keys)
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(5)


def test_os_lock_exclusion_and_release_after_terminated_holder(tmp_path):
    spawn = multiprocessing.get_context("spawn")
    ready = spawn.Event()
    process = spawn.Process(target=_hold_lock, args=(str(tmp_path), ready))
    process.start()
    try:
        assert ready.wait(10)
        with pytest.raises(NoteForgeError) as caught, JobLock("held", tmp_path, execution=True, timeout=0.05):
            pass
        assert caught.value.retryable
        # Status/context reads have their own lock and remain available.
        assert ContextStore("held", tmp_path).load_all()["schema_version"] == 3
    finally:
        process.terminate()
        process.join(5)
    with JobLock("held", tmp_path, execution=True):
        pass


def test_retention_cleanup_skips_active_jobs(tmp_path):
    manager = StateManager("held", tmp_path)
    manager.init_state()
    old = time.time() - 20 * 86400
    os.utime(manager.job_dir, (old, old))
    spawn = multiprocessing.get_context("spawn")
    ready = spawn.Event()
    process = spawn.Process(target=_hold_lock, args=(str(tmp_path), ready))
    process.start()
    try:
        assert ready.wait(10)
        assert cleanup_old_jobs(retention_days=1, output_root=tmp_path) == (0, 1)
        assert manager.job_dir.is_dir()
    finally:
        process.terminate()
        process.join(5)
    assert cleanup_old_jobs(retention_days=1, output_root=tmp_path) == (1, 1)


def test_same_job_is_executed_once_across_processes(tmp_path):
    spawn = multiprocessing.get_context("spawn")
    processes = [spawn.Process(target=_run_shared, args=(str(tmp_path),)) for _ in range(2)]
    try:
        for process in processes:
            process.start()
        for process in processes:
            process.join(20)
            assert process.exitcode == 0
        state = StateManager("shared", tmp_path).load_state()
        assert state.status is JobStatus.COMPLETED
        assert sum(item["status"] == "RUNNING" for item in state.stages["keyword_extract"].history) == 1
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
                process.join(5)
