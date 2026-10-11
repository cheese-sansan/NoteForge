# NoteForge handoff

Local verification recorded on 2026-10-11 (Asia/Tokyo). GitHub refs and CI must
be checked live for the exact pushed commit. The
[2026-09-26 handoff](docs/history/2026-09-26-handoff.md) preserves the earlier
repository recreation, backup, and verification evidence.

## Working baseline and scope

- Development branch: `codex/report-quality`, based on main
  `50dba34d23ed2042dc4ebf0d7af920a8b5ec1704` (also verified remotely before push).
- Package version and latest release tag remain `0.3.0`; this is an unreleased
  v0.4 increment. Historical tags and attribution are preserved.
- Implementation covers the five approved updates: claim attribution,
  citation completeness/deduplication, JSON/HTML exports, real-source quality
  fixtures, and interrupted-job/local cross-process reliability.
- User authorized implementation and push. This branch has not been merged
  into main as part of this increment.

## Implemented behavior

- Unrelated claims no longer receive every available source ID. Literal input
  support, references alone, missing evidence, and simulation stay distinct.
  LLM case/policy references alone yield `referenced`.
- Citation registry assigns stable numeric labels, deduplicates DOI/URL within
  provenance types, retains aliases, and flags missing references and evidence.
- New jobs write Markdown, JSON, and standalone escaped HTML. CLI `export` and
  SDK `export_job` also export completed historical jobs without provider calls
  or replacing their Markdown.
- Stages persist results before completion. Resume invalidates interrupted or
  missing stage results and downstream dependencies, and checks report hashes.
- Separate execution/storage OS locks coordinate local threads and processes.
  Status reads remain available during analysis. Retention skips locked jobs.
- Schema v3 and HTTP API v1 remain compatible. SDK/artifact export fields are
  additive. See [report quality](docs/report_quality.md) for exact limits.

## Local validation

- Windows Python 3.12.14: 172 tests passed; coverage 84.20% (80% gate).
- Ruff passed; Pyright reported 0 errors and 0 warnings.
- OpenAPI v1 snapshot, API and CLI/export smoke checks passed.
- Current-file and complete Git-history privacy audits passed.
- Docker Compose configuration passed. Local Docker image build/runtime were
  not repeated; remote CI includes Docker build.
- Browser QA verified tables, citation links, and escaped script-like content;
  the QA page had no observed console warnings/errors. A duplicate document
  title found in the report preview was fixed and guarded by a heading test.
- One dependency warning remains: Starlette's use of the httpx test client is
  deprecated. It does not fail the test gate.

CI adds a Windows Python 3.12 wheel job alongside Linux Python 3.10-3.13 and
installed-wheel export smoke checks. Local results are not remote-CI evidence;
check the branch run's `headSha` and conclusion after push.

## Verification limits and remaining roadmap

- Fixture excerpts are from real primary sources but are minimal offline
  snapshots. They do not establish live provider availability or current law.
- Literal support means matching input text, not independent truth or full-text
  verification. Citation checks are not an exhaustive semantic claim audit.
- Scientific conflict/obsolescence detection, presets, and DOCX/PDF exports
  remain planned; see [roadmap](docs/roadmap.md).
- Locks cover cooperating processes on a local filesystem. They do not provide
  a distributed queue or network-filesystem guarantees. Keep `.locks` files
  while any process uses the output root.
- The release-date discrepancy and historical v0.3 CI snapshot remain recorded
  in the archived handoff. No release-history rewrite was performed.

Generated data, previews, package builds, and the local `.venv` are ignored and
must stay out of commits. Prior recovery material remains recorded in the
archived handoffs.
