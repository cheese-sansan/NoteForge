# NoteForge handoff

This file records the project state for a new agent session on the same development host. It separates current evidence, historical verification, unresolved work, planned work, and accepted limitations.

## Current repository snapshot

| Field | Value | Status |
| --- | --- | --- |
| Snapshot date | 2026-08-24, Asia/Shanghai | `verified-current` |
| Content type | Operational reference | `verified-current` |
| Workspace | `E:\NoteForge` | `verified-current`, `local-only` |
| Repository | `cheese-sansan/NoteForge` | `verified-current` |
| Repository generation | Recreated public repository, ID `1344019864` | `verified-current` |
| Branch | `main` | `verified-current` |
| Latest engineering commit | `53da207b3c96d7cfa4ce2c09cf493fa9e77ea874` | `verified-current` |
| Preserved engineering history | 6 linear commits, 0 merges | `verified-current` |
| Package version | `0.3.0` | `verified-current` |
| Latest tag | `v0.3.0` at `018a094c839b0bb04df41f383dd50b41eb317a0d` | `verified-current` |
| Open issues | 0 | `verified-current` |
| Open pull requests | 0 | `verified-current` |
| GitHub Actions on engineering `main` | Passed at `53da207`; run 32654172553 | `verified-current` |
| Remote branches | `main` only | `verified-current` |

## Status vocabulary

- `verified-current`: checked on 2026-08-24 against the workspace or GitHub
- `verified-historical`: passed at the stated earlier checkpoint; not evidence of a current rerun
- `unresolved`: observed defect, inconsistency, or decision without an applied fix
- `planned`: proposed scope without an implementation claim
- `accepted-limitation`: intentional boundary, not a defect in the current release
- `local-only`: specific to this development host and absent from the repository contract

## Source-of-truth order

Conflicts use this priority:

1. Current Git objects, GitHub Commit and Actions data, executable tests, and `tests/snapshots/openapi_v1.json`
2. `pyproject.toml`, `src/noteforge/`, `Dockerfile`, and `docker-compose.yml`
3. `DEVELOPMENT.md`, `SECURITY.md`, `docs/`, `CONTRIBUTING.md`, and `CHANGELOG.md`
4. This snapshot for session continuity
5. Generated artifacts, caches, ignored directories, and older backup manifests

`README.md` and `README.zh-CN.md` describe the public product. `README_plan.md` is the tracked public roadmap. It is not the deleted pre-v0.3 `NoteForge_Roadmap.md`.

## Current objective

No feature implementation is in progress. The CI repair is integrated into `main@53da207`, the repository has been recreated, and the new `main` workflow is green. The next product objective is the v0.4 report-quality milestone in `README_plan.md`.

This handoff follows the six preserved engineering commits as a separate documentation commit. Its exact commit hash is intentionally derived from Git rather than self-recorded in this file.

## Completed work

### CI recovery and repository recreation

The sixth engineering commit is workflow-only:

| Commit | Subject | Scope |
| --- | --- | --- |
| `53da207` | `ci: fix Python discovery and update actions` | `.github/workflows/ci.yml` only |

The commit upgrades `actions/checkout` and `actions/setup-python` to v6. The quality job names the setup step and passes `${{ steps.setup-python.outputs.python-path }}` to Pyright instead of the unresolved literal `python` path.

[CI run 32654172553](https://github.com/cheese-sansan/NoteForge/actions/runs/32654172553) on the recreated repository passed the wheel quality gate, Python 3.10 through 3.13 wheel jobs, and Docker build. Pyright reported 0 errors and 0 warnings. The run log contains no Node 20 deprecation or forced-runtime warning.

The previous public GitHub repository was deleted after a verified local backup. A new public `cheese-sansan/NoteForge` repository was created on 2026-08-24 at 01:13:40 Asia/Shanghai. Only `main` and the three preserved annotated release tags were submitted. No pull request or secondary branch exists.

### v0.3 engineering foundation

The repository contains an installable `src/noteforge` Python package for Python 3.10 through 3.13. The stable top-level software development kit (SDK) exposes `AnalysisRequest`, `run_job`, `JobResult`, and `LiteratureProvider`.

The `noteforge` command provides:

- `noteforge run`
- `noteforge tui`
- `noteforge api`
- `noteforge jobs list`
- `noteforge jobs migrate`
- `noteforge report`

Command-line interface (CLI), text user interface (TUI), HTTP API, Docker, and SDK execution converge on `AnalysisRequest` and `run_job`.

Persistence uses schema v3 semantic keys:

```text
input -> document -> keywords -> literature -> synthesis
      -> technical_cases -> policy_assessment -> report
```

Jobs use `PENDING`, `RUNNING`, `COMPLETED`, and `FAILED`. Stages also use `SKIPPED`. Invalid transitions raise structured `NoteForgeError` instances.

The v0.2 migration path creates byte-exact backups, validates both migrated JSON files, performs atomic replacement, rolls back on failure, preserves `report_framework.md`, creates canonical `report.md`, and remains idempotent.

### Evidence pipeline

Available literature providers are `crossref`, `mock`, and `llm-simulated`.

- Crossref returns real metadata, not full-text verification
- Mock is deterministic and explicitly simulated
- Real-provider failure produces an empty or degraded evidence result with visible warnings
- Missing Crossref fields remain empty instead of receiving fabricated methods, findings, metrics, or limitations
- Technical cases and policy assessments preserve evidence identifiers
- Reports distinguish retrieved metadata, document facts, model inference, simulation, and warnings

### HTTP API v1 compatibility

The committed OpenAPI snapshot covers:

- `POST /api/v1/jobs/submit`
- `GET /api/v1/jobs/status/{job_id}`
- `GET /api/v1/jobs/result/{job_id}`
- `GET /health`

The HTTP API retains legacy `T0` through `T6` presentation fields where required for v1 compatibility. Schema-v3 storage does not use those keys internally. Structured errors may add `error_code` without removing legacy `detail` or `error` fields.

### Linear history and attribution

The preserved engineering history contains six commits and no merge commits:

| Commit | Primary author | Subject |
| --- | --- | --- |
| `e6882b3` | Hueter | `chore: establish NoteForge v0.1.0 baseline` |
| `9717f9a` | Hueter | `feat: release NoteForge v0.2.0 evidence pipeline` |
| `f220a32` | Hueter | `feat!: establish NoteForge v0.3.0 engineering foundation` |
| `b01c549` | Hueter | `docs: correct project attribution` |
| `018a094` | `chatgpt-codex-connector[bot]` | `docs: redefine NoteForge project presentation` |
| `53da207` | Hueter | `ci: fix Python discovery and update actions` |

A through D contain the Connector Bot as co-author. E contains Hueter as co-author. F is Hueter-authored. Reachable engineering commit messages contain no Claude, Anthropic, DeepSeek, old Bot email, or `Assisted-by` attribution.

Pre-recreation GitHub contributor data from 2026-08-12 is historical only:

| Endpoint | Hueter / `cheese-sansan` | Connector Bot | Other entries |
| --- | ---: | ---: | ---: |
| `/stats/contributors` | 5 | 5 | 0 |
| `/contributors` | 4 primary-author commits | 1 primary-author commit | 0 |

The recreated repository contributor endpoints are allowed to recompute from the submitted Git history. Git objects and commit metadata remain the attribution source of truth.

Tags point to:

- `v0.1.0` -> `e6882b361a0b80009972c441259ec905c1a487cf`
- `v0.2.0` -> `9717f9a48359945188566d1a92e1252650b1df8b`
- `v0.3.0` -> `018a094c839b0bb04df41f383dd50b41eb317a0d`

The remote has only `main`. It has no `master`, CI feature branch, or contributor-attribution temporary branch.

## Verification ledger

### Current checks from 2026-08-24

| Check | Result | Status |
| --- | --- | --- |
| Recreated repository | Public ID `1344019864`, default branch `main` | `verified-current` |
| Engineering `main` alignment before this handoff commit | `53da207` locally and remotely | `verified-current` |
| Preserved engineering history | 6 commits, 0 merges | `verified-current` |
| Remote branch set | `main` only | `verified-current` |
| Open issues and pull requests | 0 and 0 | `verified-current` |
| Recreated-repository `main` CI | Run 32654172553 passed all six jobs | `verified-current` |
| `main` Pyright | 0 errors, 0 warnings | `verified-current` |
| `main` Python matrix | 3.10, 3.11, 3.12, and 3.13 passed | `verified-current` |
| `main` Docker job | Compose validation and image build passed | `verified-current` |
| GitHub-maintained actions | `checkout@v6` and `setup-python@v6`; no Node 20 warning | `verified-current` |
| Recreated `v0.1.0` and `v0.2.0` runs | Runs 32654172628 and 32654172504 passed | `verified-current` |
| Recreated `v0.3.0` run | Run 32654172603 reproduces the old Pyright failure at preserved commit `018a094` | `verified-current` |
| Storage concurrency | Thread-level tests exist; locks use process-local `threading.RLock` | `accepted-limitation` |

### Local checks from 2026-08-24

These checks ran before and after the local fast-forward of `main` to `53da207`:

| Check | Result | Status |
| --- | --- | --- |
| Pyright with absolute validation interpreter | 0 errors, 0 warnings | `verified-current` |
| Ruff | Passed | `verified-current` |
| pytest | 143 passed, 1 dependency deprecation warning | `verified-current` |
| Coverage | 81.66%, threshold 80% | `verified-current` |
| OpenAPI snapshot | Matched | `verified-current` |
| API smoke | Passed | `verified-current` |
| Privacy audit including Git history | Passed | `verified-current` |
| Docker Compose configuration | Valid | `verified-current` |

### Release checks from 2026-08-09

These checks ran against the final v0.3 tree before the atomic `main` and tag update:

| Check | Result | Status |
| --- | --- | --- |
| Wheel build | `noteforge-0.3.0-py3-none-any.whl` built | `verified-historical` |
| Clean wheel installation outside the repository | Installed with `api`, `documents`, and `dev` extras | `verified-historical` |
| Ruff | Passed | `verified-historical` |
| Pyright with absolute interpreter path | 0 errors, 0 warnings | `verified-historical` |
| pytest | 143 passed | `verified-historical` |
| Coverage | 81.66%, threshold 80% | `verified-historical` |
| OpenAPI snapshot | Matched | `verified-historical` |
| API smoke | Passed | `verified-historical` |
| Privacy audit including Git history | Passed | `verified-historical` |
| Installed CLI and SDK outside repository | All documented subcommands and SDK smoke passed | `verified-historical` |
| Docker image build | Passed | `verified-historical` |
| Running container health | `/health` returned `{"status":"ok"}` | `verified-historical` |

The recreated `main` run is current release-gate evidence. The preserved `v0.3.0` tag still contains its original workflow and therefore remains red when rerun; moving the release tag would falsify release history.

## Unresolved items

| Priority | Item | Evidence | Current treatment |
| --- | --- | --- | --- |
| P1 | v0.3 changelog date differs from the tag timestamp | `CHANGELOG.md` says 2026-07-11; tag and E commit are dated 2026-07-13 | Decide whether the changelog date represents release preparation or publication; edit only after that decision |
| P2 | Tests emit one Starlette dependency warning | FastAPI `TestClient` reports that its `httpx` integration is deprecated | Evaluate the supported FastAPI, Starlette, and HTTP client combination; do not hide the warning without a compatibility decision |
| P2 | Preserved `v0.3.0` tag CI is red | Tag points to original commit `018a094`, before the CI repair | Preserve the tag; use green `main` as current release-gate evidence |
| P2 | Release checklist wording exceeds present CI evidence | The matrix installs wheels on Python 3.10 through 3.13; installed CLI/SDK outside-checkout smoke runs only in the Python 3.10 quality job | Preserve the distinction when reporting compatibility |
| P2 | Local ignored legacy directories remain | `core/`, `tasks/`, and `utils/` contain only pre-v0.3 `.pyc` files | Treat as stale local cache, never as tracked compatibility code |
| P2 | Job and migration locks are process-local | Storage modules use `threading.RLock`; concurrency tests use threads | Do not claim cross-process serialization; assess an operating-system lock before supporting concurrent processes on one job |

No open GitHub issue currently tracks these items.

## Proposed next plan

### P1: normalize release metadata and maintenance warnings

1. Decide the canonical v0.3 release date
2. Align `CHANGELOG.md` only if the existing date is incorrect

### P2: start the v0.4 report-quality milestone

The tracked roadmap reserves v0.4 for:

- Citation numbering, DOI and URL deduplication, and citation completeness checks
- Evidence grades, conflict detection, and obsolescence detection
- Report presets for technical research, literature review, industry analysis, policy analysis, and product comparison
- JSON and HTML export before DOCX and PDF
- Representative real-source fixtures for technical-case and policy-assessment validation

The v0.4 work can start from the green `main` release gate. It requires a new plan and compatibility review before implementation.

## Accepted limitations and invariant boundaries

- HTTP `/api/v1` is the compatibility boundary
- New persistence remains schema v3
- v0.2 jobs remain readable through transactional migration
- New jobs write canonical `report.md`
- Crossref metadata is not full-text evidence
- Simulated records never become retrieved evidence
- Real-provider failure never triggers a silent simulated fallback
- Generated analysis and policy content require external verification
- `API_TOKEN` is required before exposing job endpoints outside a trusted local environment
- Uploaded documents and `outputs/jobs/{job_id}/` may contain sensitive data
- NoteForge is not a hardened multi-tenant hosted service
- Job, context, and migration locks serialize threads inside one process; they do not serialize independent processes
- GraphRAG, vector databases, knowledge graphs, hosted software as a service, complex browser frontends, and open-ended multi-agent orchestration remain outside pre-v1 scope

## Repository file map

| Path | Role |
| --- | --- |
| `pyproject.toml` | Package metadata, optional dependencies, entry point, Ruff, Pyright, pytest, and coverage configuration |
| `src/noteforge/__init__.py` | Stable SDK exports |
| `src/noteforge/models.py` | Dataclass and enum contracts, schema version, JSON encoding |
| `src/noteforge/pipeline.py` | Shared job pipeline and `run_job` |
| `src/noteforge/providers/literature.py` | Provider protocol and Crossref, Mock, simulated implementations |
| `src/noteforge/storage/` | State, context, migration, cleanup, process-local locking, and atomic persistence |
| `src/noteforge/api.py` | FastAPI v1 compatibility surface |
| `src/noteforge/cli.py` | Unified CLI |
| `src/noteforge/tui.py` | Standard-library TUI |
| `tests/snapshots/openapi_v1.json` | API v1 compatibility snapshot |
| `tests/fixtures/v0_2_job/` | Realistic v0.2 migration fixture |
| `scripts/check_openapi.py` | OpenAPI snapshot gate |
| `scripts/api_smoke.py` | API submit, status, and result smoke test |
| `scripts/privacy_audit.py` | Current-tree, history, and optional-output privacy scan |
| `.github/workflows/ci.yml` | Wheel-first quality, Python compatibility, and Docker jobs |
| `README.md` and `README.zh-CN.md` | Mirrored public project presentation |
| `README_plan.md` | Public roadmap through v1.0 |
| `DEVELOPMENT.md` | Architecture and engineering invariants |
| `docs/release_checklist.md` | v0.3 release checks |
| `SECURITY.md` | Deployment and disclosure boundaries |
| `CONTRIBUTORS.md` | Human ownership and Connector Bot attribution |

## Development-host state

This section is `local-only` and applies to a new agent session on the same Windows host.

### Reliable executables

| Tool | Path or state |
| --- | --- |
| Git | `D:\Git\cmd\git.exe` |
| GitHub CLI | `C:\Program Files\GitHub CLI\gh.exe` |
| Bundled Python 3.12 | `$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe` |
| Full validation Python | `E:\NoteForge-backups\20260809-225911-bot-attribution-fallback\release-validation\venv\Scripts\python.exe` |
| Docker Desktop | Installed; daemon state requires a fresh check in each session |

Plain `python` may resolve to the Windows Store alias. Pyright interpreter checks require the absolute validation Python path on this host.

### Recovery material

The latest verified pre-recreation backup is:

`E:\NoteForge-backups\20260824-011144-pre-github-recreate`

It contains:

- `noteforge-all.bundle`: all refs and complete Git history; SHA-256 `B37555073266CFEFE2D5B4B27BCF82A8DFFCFD559216DBF2A5F86EE26DEB0E88`
- `tracked-main.zip`: the six-commit `main` tree at `53da207`; SHA-256 `74B56C9E8170EE946CAB81337F764B8893E1D936254C6BBB00E8F7ADBEDF7C49`
- `HANDOFF.md`: the uncommitted pre-recreation handoff; SHA-256 `3A40D32272E4E7D25F51126951F6720C4869CBD1F9C66F7BD26EF5BD53303416`

The previous complete attribution and release-validation backup is:

`E:\NoteForge-backups\20260809-225911-bot-attribution-fallback`

It retains reference manifests, tracked-worktree hashes, the clean wheel, validation environment, and outside-repository smoke outputs.

Older retained backups:

- `E:\NoteForge-backups\20260713-233600`
- `E:\NoteForge-backups\20260714-002516-bot-attribution`

These directories are outside the repository and remain intentionally retained.

### Ignored workspace material

The following paths are not current source and must not influence architecture decisions:

- `core/`, `tasks/`, and `utils/`: stale pre-v0.3 Python bytecode only
- `build/`, `dist/`, and `src/noteforge.egg-info/`: local packaging output
- `.pytest_cache/`, `.ruff_cache/`, `.coverage`, and `__pycache__/`: tool caches
- `outputs/`: generated job data when present

Git does not track the removed legacy Python packages. Their `.pyc` files do not provide a supported import compatibility layer.

## Verification commands

The release gate documented by the repository is:

```powershell
$python = 'E:\NoteForge-backups\20260809-225911-bot-attribution-fallback\release-validation\venv\Scripts\python.exe'
& $python -m build --wheel
& $python -m ruff check src/noteforge tests scripts
& $python -m pyright --pythonpath $python src/noteforge
& $python -m pytest --cov=noteforge --cov-report=term-missing --cov-fail-under=80
& $python scripts/check_openapi.py
& $python scripts/api_smoke.py
& $python scripts/privacy_audit.py --history
docker compose config
docker compose build api
```

Installed-wheel verification runs outside `E:\NoteForge`. Docker completion requires a running container to reach the `healthy` state and return `{"status":"ok"}` from `/health`.

## Handoff integrity rules

- Current evidence and historical evidence remain separate
- Plans never appear as implemented behavior
- Local ignored artifacts never appear as repository source
- Local passing checks never appear as a green GitHub Actions run
- Provider metadata never appears as verified publication content
- Simulated evidence never appears as retrieved evidence
- Runtime, SDK, CLI, API, persistence, and migration changes require corresponding contract tests
- Changes to `/api/v1` require explicit OpenAPI snapshot review
- Changes to persisted fields require schema, round-trip, corruption, rollback, idempotence, and concurrency review
