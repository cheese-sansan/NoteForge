# Developer Integration

The top-level SDK is intentionally small: construct a typed request, run the shared pipeline, and inspect a typed result. Applications should not reproduce CLI or API orchestration internally.

## Stable SDK

```python
from pathlib import Path

from noteforge import AnalysisRequest, JobResult, run_job

request = AnalysisRequest(
    topic="LLM benchmark evaluation",
    file_path=Path("examples/sample_paper_abstract.md"),
    provider="crossref",
    job_id="my-analysis-job",
)
result: JobResult = run_job(request, output_root=Path("outputs"))
```

`JobResult` contains `job_id`, `status`, `report_path`, `sources`, `warnings`, `tech_cases`, and `policies`. Dataclass models provide `to_dict`, `to_json`, `from_dict`, and `from_json`; incoming schema markers are validated against schema v3.

Resume with persisted input:

```python
result = run_job(AnalysisRequest(job_id="my-analysis-job"))
```

## Provider contract

```python
from noteforge import LiteratureProvider, LiteratureQuery, LiteratureSearchResult


class MyProvider(LiteratureProvider):
    name = "my-provider"

    def search(self, query: LiteratureQuery) -> LiteratureSearchResult:
        ...
```

Provider records must label `source_type` and `source_provider`. Simulated records must never be represented as retrieved evidence. Provider failures should return an explicit status and warnings or raise a structured provider error; they must not silently substitute Mock results.

## Structured errors

`NoteForgeError` exposes `code`, `message`, `retryable`, and `details`. Callers may branch on the error code, but should retain the human-readable message and diagnostic details when reporting failures.

## Operational persistence access

Persistence classes are available for maintenance tools but are not part of the small top-level SDK surface:

```python
from noteforge.storage.context import ContextStore
from noteforge.storage.state import StateManager

state = StateManager("my-analysis-job").load_state()
context = ContextStore("my-analysis-job").load_all()
```

Do not import removed v0.2 paths such as `core.pipeline`, `tasks.t2_literature_search`, or `utils.state_manager`.

## Verification responsibility

Source metadata and model-generated synthesis are useful inputs to a research workflow, not proof that a publication, finding, or policy conclusion has been fully verified. Integrations should preserve NoteForge warnings and source labels in their own user interfaces.
