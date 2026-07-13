# Development Guide

NoteForge has one application pipeline and several delivery interfaces. CLI, TUI, API, Docker, and Python integrations must converge on the same typed request, configuration, state, and report behavior.

## Architecture

The stable entry point is `noteforge.run_job(AnalysisRequest, output_root=...)`. The pipeline persists schema-v3 semantic context:

```text
input -> document -> keywords -> literature -> synthesis
      -> technical_cases -> policy_assessment -> report
```

Job states are `PENDING`, `RUNNING`, `COMPLETED`, and `FAILED`. Stage states add `SKIPPED`. Invalid transitions raise a structured `NoteForgeError`.

The package uses a `src/noteforge` layout. The removed `core`, `tasks`, and `utils` paths are not compatibility packages. HTTP API v1 remains a compatibility boundary and is guarded by `tests/snapshots/openapi_v1.json`.

## Environment

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install ".[dev,documents]"
```

## Verification

```bash
python -m build --wheel
ruff check src/noteforge tests scripts
pyright src/noteforge
pytest --cov=noteforge --cov-report=term-missing --cov-fail-under=80
python scripts/check_openapi.py
python scripts/api_smoke.py
python scripts/privacy_audit.py --history
docker compose config
docker compose build api
```

CI builds and installs a wheel before testing on Python 3.10, 3.11, 3.12, and 3.13. Release validation also exercises the installed CLI and SDK outside the repository and checks a running Docker container through `/health`.

## Persistence and migration

`StateManager` and `ContextStore` validate job IDs and write through atomic replacement. The migration layer backs up v0.2 files byte-for-byte, validates both schema-v3 documents before replacement, and restores the originals if either replacement fails.

New persisted fields require a schema decision, JSON round-trip tests, corruption handling, and concurrent-read coverage. Migration behavior must remain idempotent.

## Evidence invariants

- Keep real retrieval, model inference, simulation, and unverified content distinguishable.
- Never fill missing provider data with fabricated facts.
- Keep provider failures visible through status and warnings.
- Preserve evidence IDs when producing claims, cases, policies, and reports.
- Do not describe metadata retrieval as full-text verification.
