# NoteForge

[English](README.md) | [简体中文](README.zh-CN.md)

**Evidence-aware research reports from topics and documents.**

NoteForge turns a research topic or local document into a structured Markdown report. It keeps retrieved metadata, source-document facts, model inference, simulated records, and warnings visibly separated so readers can see what the report is based on.

> NoteForge supports research preparation; it does not provide full-text verification, guarantee citation accuracy, replace authoritative policy review, or operate as a hardened multi-tenant research platform.

## What it delivers

- One installable Python package with a typed SDK and unified CLI.
- Topic and document analysis through CLI, TUI, HTTP API, or Docker.
- Real scholarly metadata retrieval from Crossref without an API key.
- Explicit offline and simulated modes that are never presented as retrieved evidence.
- Inspectable jobs with semantic stage state, sources, warnings, and Markdown reports.
- Transactional migration for persisted v0.2 jobs.

Every interface calls the same `AnalysisRequest` and `run_job` pipeline:

```text
topic or document
    -> document parsing
    -> keyword extraction
    -> literature retrieval
    -> synthesis
    -> technical cases and policy assessment
    -> report.md
```

## Quick start

NoteForge supports Python 3.10–3.13. The core SDK and CLI have no required third-party dependencies.

```bash
python -m pip install .

# Deterministic offline demonstration
noteforge run --topic "evidence-aware research" --provider mock --job-id demo

# Real Crossref metadata retrieval
noteforge run --topic "transformer model evaluation" --provider crossref

# Analyze a local document
noteforge run --file ./examples/sample_paper_abstract.md --provider crossref

noteforge report demo
```

Install optional interfaces and document parsers when needed:

```bash
python -m pip install ".[api]"
python -m pip install ".[documents]"
```

## Choose an interface

| Interface | Purpose | Start here |
| --- | --- | --- |
| CLI | Run, resume, inspect, and migrate jobs | `noteforge --help` |
| Python SDK | Embed the typed pipeline in Python code | `from noteforge import AnalysisRequest, run_job` |
| TUI | Use the pipeline interactively in a terminal | `noteforge tui` |
| HTTP API | Submit and poll jobs through API v1 | `noteforge api` |
| Docker | Run the API with a reproducible image | `docker compose up -d --build` |

## Python SDK

```python
from pathlib import Path

from noteforge import AnalysisRequest, run_job

result = run_job(
    AnalysisRequest(
        topic="LLM deployment evaluation",
        provider="mock",
        job_id="sdk-demo",
    ),
    output_root=Path("outputs"),
)

print(result.status, result.report_path)
print(result.sources, result.warnings)
```

`AnalysisRequest`, `JobResult`, literature/source/case/policy records, state models, enums, and structured errors are standard-library dataclasses. `LiteratureProvider.search(LiteratureQuery)` is the stable provider extension contract.

## Evidence modes

| Provider | Origin | Network | Evidence use | Failure behavior |
| --- | --- | --- | --- | --- |
| `crossref` | Crossref REST metadata | Required | Metadata that should be verified through the DOI or publisher | Empty results with visible warnings |
| `mock` | Deterministic local fixtures | No | Demonstration and tests only | Always labelled `simulated` |
| `llm-simulated` | Model-generated demonstration records | LLM endpoint | Demonstration only | Remains explicitly simulated |

Crossref is the default. A real-provider outage never triggers an automatic simulated fallback. Metadata retrieval is not the same as reading or verifying the full publication.

## Jobs and migration

Canonical job artifacts are stored under `outputs/jobs/{job_id}/`:

```text
task_state.json
context_data.json
resume_log.txt
report.md
```

Version 0.3 removes the old root scripts, `core/tasks/utils` import paths, and requirements files. Existing v0.2 jobs are backed up and migrated transactionally on first read, or in advance with:

```bash
noteforge jobs migrate --all
```

See the [v0.3 migration guide](docs/migration_v0.3.md) for the compatibility details.

## API and Docker

```bash
python -m pip install ".[api]"
noteforge api --host 0.0.0.0 --port 8000
```

```bash
curl -X POST http://localhost:8000/api/v1/jobs/submit \
  -F "topic=AI safety" -F "provider=crossref"
curl http://localhost:8000/api/v1/jobs/status/{job_id}
curl http://localhost:8000/api/v1/jobs/result/{job_id}
```

Set `API_TOKEN` before exposing the API beyond a trusted local environment. The Docker image installs `.[api]`; set `INSTALL_EXTRAS=true` at build time to include document parsers.

## Documentation

- [CLI, TUI, and API](docs/cli_tui_api.md)
- [Python SDK and provider integration](docs/developer_integration.md)
- [Evidence modes and literature providers](docs/mock_vs_real_provider.md)
- [Migrating from v0.2](docs/migration_v0.3.md)
- [Development guide](DEVELOPMENT.md)
- [Public roadmap](README_plan.md)
- [v0.3.0 release notes](docs/releases/v0.3.0.md)
- [Sample Crossref report](examples/sample_crossref_report.md)
- [Sample document report](examples/sample_document_report.md)

## Project status

Version 0.3 establishes the installable package, typed semantic contracts, unified interfaces, migration path, and release gates. Version 0.4 is reserved for citation completeness, evidence grading, report presets, and JSON/HTML exports. See the [roadmap](README_plan.md).

## Contributing and security

See [CONTRIBUTING.md](CONTRIBUTING.md) for development expectations, [CONTRIBUTORS.md](CONTRIBUTORS.md) for project attribution, and [SECURITY.md](SECURITY.md) for the supported security model and private reporting guidance.

## License

MIT
