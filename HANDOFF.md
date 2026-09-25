# NoteForge handoff

This page records the repository state checked on 2026-09-26 (Asia/Singapore). Recheck changing GitHub and CI state before relying on it. The [2026-08-24 handoff](docs/history/2026-08-24-handoff.md) preserves the earlier release, migration, attribution, and backup evidence.

## Current baseline

- Project: `cheese-sansan/NoteForge`, recreated public GitHub repository ID `1387866226` (created 2026-09-26 at 00:26:36 Asia/Singapore).
- The maintenance branch was fast-forwarded into local `main` at `b6907f579e4634c5e3ef148bce17e551f8e11a03`, then pushed to the new remote with the annotated `v0.1.0`, `v0.2.0`, and `v0.3.0` tags. The previous remote `main` was `2c0a1ab2f388d834f087c7641cf5931c74fa624a`.
- The latest commit before this maintenance work was on 2026-08-24. No product feature release followed v0.3.0.
- The last checked run on the previous repository, `32655574300`, completed successfully for `2c0a1ab`. It is historical evidence. Check the new repository's run for the current remote `main` before claiming CI success.
- Package version remains `0.3.0`. The next planned product milestone is [v0.4 report quality](docs/roadmap.md).

## Maintenance scope

This maintenance pass groups executable helpers in `scripts/`, moves the roadmap under `docs/`, provides a documentation index, and archives the previous handoff. It does not change the SDK, HTTP API v1, persistence schema v3, evidence behavior, or release tags.

## Repository map

| Path | Role |
| --- | --- |
| `src/noteforge/` | Installable package, SDK, CLI, API, providers, stages, and storage |
| `tests/` | Tests, migration fixtures, and API v1 OpenAPI snapshot |
| `scripts/` | Quality, privacy, OpenAPI, API, and CLI smoke checks |
| `docs/` | [Documentation index](docs/README.md), guides, roadmap, releases, and archived handoffs |
| `examples/` | Sample inputs and reports |
| `README.md`, `README.zh-CN.md` | Public project overview |
| `DEVELOPMENT.md`, `CONTRIBUTING.md`, `SECURITY.md` | Development and project policies |

## Verification and evidence boundaries

The release checks are documented in [DEVELOPMENT.md](DEVELOPMENT.md) and [the v0.3 checklist](docs/release_checklist.md). The earlier handoff records historical wheel, coverage, Docker, API, and migration evidence. A local check does not establish a passing CI run on a new remote commit.

On 2026-09-26, the current checkout passed Ruff, Pyright (0 errors), 143 tests with 81.66% coverage, the OpenAPI snapshot, API and CLI smoke checks, the privacy audit including Git history, wheel build, and Docker Compose configuration. The tests emitted one dependency deprecation warning. Docker image build and a running-container health check were not rerun locally in this maintenance pass.

Crossref supplies metadata, not full-text verification. Mock and LLM-simulated records stay explicitly simulated. Persisted v0.2 jobs use the transactional migration path; HTTP `/api/v1` and schema v3 are compatibility boundaries. Storage locks serialize threads in one process, not independent processes.

## Open items

- `CHANGELOG.md` lists v0.3.0 as 2026-07-11, while the release tag was created from a 2026-07-13 commit. The date's meaning needs a decision before editing release history.
- The historical v0.3.0 tag precedes the CI Python-path fix; retain the tag as an immutable release snapshot.
- Validate multi-process locking before claiming shared-job concurrency across processes.
- Keep generated job data and local ignored cache files out of commits.

## Local recovery material

The pre-recreation backup is `E:\NoteForge-backups\20260926-pre-recreate\`. Its complete `noteforge-all.bundle` passed `git bundle verify` and has SHA-256 `2F9F585A0B81B90917D3741158915739BD44CC78BE7873D215D034715A5DC56F`. The directory also contains the previous GitHub repository metadata and remote refs. The archived handoff lists older backups.
