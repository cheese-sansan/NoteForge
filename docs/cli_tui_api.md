# CLI, TUI, and API

All user-facing interfaces call the same typed SDK and persistence layer. Provider selection, job state, warnings, and report behavior should therefore remain consistent across interfaces.

## CLI

Run a topic or document analysis:

```bash
noteforge run --topic "transformer evaluation" --provider crossref
noteforge run --file ./examples/sample_paper_abstract.md --provider mock --job-id paper-demo
```

Resume, inspect, or migrate persisted jobs:

```bash
noteforge run --job-id paper-demo
noteforge jobs list --limit 20
noteforge jobs migrate --all
noteforge report paper-demo
```

Use `--output-root` on `run`, `jobs list`, `jobs migrate`, and `report` when artifacts should not use `outputs/`.

## TUI

```bash
noteforge tui
```

The terminal interface runs topic/file analysis, lists jobs, and displays canonical reports. It does not maintain a separate task engine or data format.

## API

```bash
python -m pip install ".[api]"
noteforge api --host 0.0.0.0 --port 8000
```

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/api/v1/jobs/submit \
  -F "topic=AI safety" -F "provider=crossref"
curl http://localhost:8000/api/v1/jobs/status/{job_id}
curl http://localhost:8000/api/v1/jobs/result/{job_id}
```

The v1 result retains `report`, `context_summary`, `provider_status`, `sources`, `tech_cases`, `policy_assessment`, and `warnings`. Status responses retain legacy `T0–T6` presentation fields for HTTP compatibility even though schema-v3 persistence uses semantic stage names. Structured failures may add `error_code` without removing `detail` or `error`.

Set `API_TOKEN` to require `Authorization: Bearer ...` on `/api/v1/jobs/*`. Keep secrets in environment variables or an untracked `.env` file, and do not expose an unauthenticated service to untrusted networks.

## Capability boundary

Every interface can retrieve metadata and generate an evidence-aware report, but none of them turns metadata into verified full text. Source records, inferred analysis, and policy conclusions still require review against authoritative material.
