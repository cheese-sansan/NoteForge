# NoteForge Public Roadmap

NoteForge is an evidence-aware research report pipeline for topics and documents. The roadmap prioritizes inspectable provenance, stable interfaces, and explicit capability boundaries over feature count.

## Product principles

- Retrieved metadata, source-document facts, model inference, simulated data, and unverified content remain distinguishable.
- A real-provider failure stays visible and never becomes an implicit simulated fallback.
- CLI, TUI, API, Docker, and Python integrations share one semantic SDK contract.
- Reports expose uncertainty and evidence gaps instead of hiding them behind polished prose.

## v0.3: Engineering foundation

The current baseline provides:

- An installable `src/noteforge` package for Python 3.10–3.13.
- A unified `noteforge` command and typed dataclass SDK.
- Semantic schema-v3 context, explicit Job/Stage state machines, and structured errors.
- Transactional, idempotent migration of persisted v0.2 jobs.
- Crossref, deterministic Mock, and explicitly simulated provider modes.
- Wheel-first CI with Ruff, Pyright, coverage, OpenAPI, privacy, API, and Docker gates.

## v0.4: Report quality

The current unreleased increment implements specific claim attribution,
DOI/URL citation deduplication and completeness warnings, literal/reference-only
evidence grades, JSON/HTML exports, offline real-source fixtures, and local
cross-process recovery/locking. See [report quality](report_quality.md) for
contracts and verification limits.

The next release is reserved for report-level trust and portability:

- Citation numbering, DOI/URL deduplication, and citation completeness checks (implemented).
- Evidence grades (implemented), plus scientific conflict and obsolescence detection (planned).
- Report presets for technical research, literature review, industry analysis, policy analysis, and product comparison.
- JSON and HTML exports (implemented) before DOCX and PDF.
- Representative real-source fixtures for technical-case and policy-assessment validation (implemented as minimal offline excerpts).

## v1.0 release conditions

- Stable CLI, HTTP API v1, and small top-level Python SDK.
- At least one production-ready real literature provider.
- Complete provenance labels on every report section.
- Citation traceability and documented verification limits.
- Reproducible wheel and Docker delivery with all release gates passing.

## Outside the pre-v1 scope

GraphRAG, heavy vector databases, large knowledge graphs, multi-tenant authorization, complex browser frontends, hosted SaaS, and open-ended multi-agent orchestration are intentionally deferred.
