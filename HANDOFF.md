# NoteForge handoff

This page records the repository state checked on 2026-09-26 (Asia/Singapore). Recheck changing GitHub and CI state before relying on it. The [2026-08-24 handoff](docs/history/2026-08-24-handoff.md) preserves the earlier release, migration, attribution, and backup evidence.

## Current baseline

- Project: `cheese-sansan/NoteForge`, public GitHub repository ID `1344019864` at the time of this check.
- Local and remote `main` started at `2c0a1ab2f388d834f087c7641cf5931c74fa624a`; the remote had only `main` and annotated `v0.1.0`, `v0.2.0`, and `v0.3.0` tags.
- The latest commit before this maintenance work was on 2026-08-24. No product feature release followed v0.3.0.
- The latest checked GitHub Actions run for that commit, `32655574300`, completed successfully. This is historical evidence for that commit, not for subsequent changes.
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

Crossref supplies metadata, not full-text verification. Mock and LLM-simulated records stay explicitly simulated. Persisted v0.2 jobs use the transactional migration path; HTTP `/api/v1` and schema v3 are compatibility boundaries. Storage locks serialize threads in one process, not independent processes.

## Open items

- `CHANGELOG.md` lists v0.3.0 as 2026-07-11, while the release tag was created from a 2026-07-13 commit. The date's meaning needs a decision before editing release history.
- The historical v0.3.0 tag precedes the CI Python-path fix; retain the tag as an immutable release snapshot.
- Validate multi-process locking before claiming shared-job concurrency across processes.
- Keep generated job data and local ignored cache files out of commits.

## Local recovery material

Previous complete Git bundles and manifests are outside the repository under `E:\NoteForge-backups\`. See the archived handoff for their exact paths and SHA-256 values. Create and verify a fresh Git bundle before deleting a GitHub repository.
