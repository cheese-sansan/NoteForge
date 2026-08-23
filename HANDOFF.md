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
| Latest engineering commit | `d4f4a5f803be90909427ef96e551039fd7031b19` | `verified-current` |
| Normalized engineering history | 6 linear commits, 0 merges | `verified-current` |
| Package version | `0.3.0` | `verified-current` |
| Latest tag | `v0.3.0` at `e16b4edbc50f5e6bc484452163efa0f54d1be222` | `verified-current` |
| Open issues | 0 | `verified-current` |
| Open pull requests | 0 | `verified-current` |
| GitHub Actions on rewritten `main` | Derive from the current remote HEAD; pre-rewrite runs are historical evidence only | `requires-live-check` |
| Remote branches | `main` only | `verified-current` |

## Status vocabulary

- `verified-current`: checked on 2026-08-24 against the workspace or GitHub
- `verified-historical`: passed at the stated earlier checkpoint; not evidence of a current rerun
- `requires-live-check`: intentionally not self-recorded because the value changes when this handoff commit is pushed
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

No feature implementation is in progress. The CI repair is integrated into engineering `main@d4f4a5f`, the repository has been recreated, and repository attribution has been normalized to the sole maintainer. The next product objective is the v0.4 report-quality milestone in `README_plan.md`.

This handoff follows the six normalized engineering commits and the repository-recreation handoff as a separate attribution documentation commit. Its exact commit hash and corresponding GitHub Actions run are intentionally derived live rather than self-recorded in this file.

## Completed work

### CI recovery and repository recreation

The sixth engineering commit is workflow-only:

| Commit | Subject | Scope |
| --- | --- | --- |
| `d4f4a5f` | `ci: fix Python discovery and update actions` | `.github/workflows/ci.yml` only |

The commit upgrades `actions/checkout` and `actions/setup-python` to v6. The quality job names the setup step and passes `${{ steps.setup-python.outputs.python-path }}` to Pyright instead of the unresolved literal `python` path.

[CI run 32654549249](https://github.com/cheese-sansan/NoteForge/actions/runs/32654549249) passed the wheel quality gate, Python 3.10 through 3.13 wheel jobs, and Docker build before the attribution-only history rewrite. Pyright reported 0 errors and 0 warnings. This run is historical tree evidence; the current rewritten HEAD requires its own live run.

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

### Linear history and sole attribution

The normalized engineering history contains six commits and no merge commits:

| Commit | Primary author | Subject |
| --- | --- | --- |
| `aa4136b` | Hueter | `chore: establish NoteForge v0.1.0 baseline` |
| `d121d08` | Hueter | `feat: release NoteForge v0.2.0 evidence pipeline` |
| `4057621` | Hueter | `feat!: establish NoteForge v0.3.0 engineering foundation` |
| `5c5538b` | Hueter | `docs: correct project attribution` |
| `e16b4ed` | Hueter | `docs: redefine NoteForge project presentation` |
| `d4f4a5f` | Hueter | `ci: fix Python discovery and update actions` |

All reachable commits use `Hueter <w8p1p6t0@gmail.com>` as both author and committer. Reachable commit messages contain no `Co-authored-by`, Bot email, or `Assisted-by` attribution. `CONTRIBUTORS.md` lists Hueter as the sole repository contributor.

GitHub contributor displays are derived from the rewritten default-branch history. GitHub documents that contributor statistics may take about 24 hours to refresh after a force push; live endpoint data is therefore checked after submission rather than frozen in this file.

Tags point to:

- `v0.1.0` -> `aa4136b70081c9b62448d543e3ecb16b5cd3effd`
- `v0.2.0` -> `d121d0854f341a5f015551e5774696bc6a3cb6b3`
- `v0.3.0` -> `e16b4edbc50f5e6bc484452163efa0f54d1be222`

The remote has only `main`. It has no `master`, CI feature branch, or contributor-attribution temporary branch.

## Verification ledger

### Current checks from 2026-08-24

| Check | Result | Status |
| --- | --- | --- |
| Recreated repository | Public ID `1344019864`, default branch `main` | `verified-current` |
| Engineering history before the two handoff commits | `d4f4a5f`, 6 commits, 0 merges | `verified-current` |
| Reachable Git author and committer identities | Hueter only | `verified-current` |
| Reachable co-author trailers | 0 | `verified-current` |
| Remote branch set | `main` only | `verified-current` |
| Open issues and pull requests | 0 and 0 | `verified-current` |
| Pre-rewrite recreated-repository `main` CI | Run 32654549249 passed all six jobs | `verified-historical` |
| Rewritten `main` CI | Query the run whose head SHA equals current remote `main` | `requires-live-check` |
| Rewritten release-tag runs | Query by the rewritten tag targets above | `requires-live-check` |
| Storage concurrency | Thread-level tests exist; locks use process-local `threading.RLock` | `accepted-limitation` |

### Local checks from 2026-08-24

These checks ran against the rewritten history and current tree before submission:

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

The pre-rewrite recreated `main` run is historical tree evidence. The rewritten `v0.3.0` target retains its original workflow tree and is expected to reproduce the old Pyright failure when rerun; current `main` contains the CI repair.

## Unresolved items

| Priority | Item | Evidence | Current treatment |
| --- | --- | --- | --- |
| P1 | v0.3 changelog date differs from the tag timestamp | `CHANGELOG.md` says 2026-07-11; tag and E commit are dated 2026-07-13 | Decide whether the changelog date represents release preparation or publication; edit only after that decision |
| P2 | Tests emit one Starlette dependency warning | FastAPI `TestClient` reports that its `httpx` integration is deprecated | Evaluate the supported FastAPI, Starlette, and HTTP client combination; do not hide the warning without a compatibility decision |
| P2 | Rewritten `v0.3.0` tag CI is expected to remain red | Tag target `e16b4ed` retains the release tree from before the CI repair | Preserve the release snapshot; use green current `main` as release-gate evidence |
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

The latest verified pre-attribution-rewrite backup is:

`E:\NoteForge-backups\20260824-013436-pre-contributor-rewrite`

It contains:

- `noteforge-before-rewrite.bundle`: all refs and complete pre-rewrite history; SHA-256 `BB734C42299EC8D29B562D35C3BBEAFE0F37FA0A5EB37758DC8C6981AE2A6E13`
- `tracked-main-before-rewrite.zip`: the seven-commit tree at `f91da14`; SHA-256 `9B35C6E6150073EFBAF26705382D788075CFF289148D8A397456A5A663EFB59C`
- `HANDOFF-before-rewrite.md`: the committed pre-rewrite handoff; SHA-256 `F1897221462A3ABBB1DFAC0FA6AB76E8CE6E268D25DBFA78B1C813DBA3934BA3`

The verified pre-recreation backup is:

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
