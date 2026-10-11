# Report quality and exports

This unreleased v0.4 increment adds citation auditing, conservative claim
attribution, portable exports, and interrupted-job recovery. Package version
and release tags remain at v0.3.0 until a release is explicitly prepared.

## Evidence states

| State | Meaning | Limit |
| --- | --- | --- |
| `supported` / `literal` | Claim text occurs in an input abstract or document, matches a supplied finding, or comes from a deterministic document Results-row extraction | Input support, not independent truth or full-text verification |
| `referenced` / `reference_only` | The claim has existing source IDs but no literal match | An identifier alone does not establish support |
| `unverified` | No specific valid source is associated | Requires source review |
| `simulated` | All associated records are simulated | Demonstrations only |

The extractor retains specific model-supplied source IDs after filtering unknown
IDs. It never attaches every available source to an unrelated claim. Technical
cases and policy records extracted by an LLM remain `referenced`; they do not
become verified because the cited ID exists. Existing saved reports keep their
historical contents; exporting one does not retroactively validate it.

## Citation audit

Reports retain source IDs such as `[L1]` and add stable numeric citations such as
`[1]`. Sources with the same normalized DOI or URL are grouped within the same
provenance type. The first occurrence controls display order and metadata;
aliases preserve references to later duplicates. Real and simulated records
are never merged. Different explicit DOIs remain separate even with a shared URL.

Markdown includes warnings; JSON includes a `quality` object with dangling
citations, uncited structured records and narrative list items, incomplete
external-source identifiers, unused sources, and claim evidence grades.
Checks cover claims, quantitative metrics, cases, policy records, and bracketed
citations in the synthesis text. Narrative-list warnings are review hints,
not semantic verification. Prose paragraphs and arbitrary Markdown citation
styles are not an exhaustive claim graph. Conflicting scientific results and
obsolescence still require source review; conflicting DOI identities are kept
distinct.

## Export a report

New jobs write `report.md`, `report.json`, and `report.html` under the job
directory. Their content hashes are saved before report generation is marked
complete. `JobResult.export_paths` exposes the JSON/HTML paths.

```bash
noteforge run --topic "transformer evaluation" --provider mock --job-id demo
noteforge export demo --format json
noteforge export demo --format html
```

```python
from pathlib import Path
from noteforge import export_job

path = export_job("demo", format="html", output_root=Path("outputs"))
```

The export command also supports completed historical jobs. It reads saved
context and Markdown, makes no provider calls, and preserves `report.md`.
JSON has `report_version: 1` (separate from persistence schema v3), Markdown,
sources, citation aliases, quality results, warnings, synthesis, cases, and
policy records. HTML is standalone, printable, and renders headings, lists,
tables, and numeric citation anchors. All document/model text is escaped; raw
HTML and scripts are not executed and no external asset is loaded. Exports may
contain private document text and inherit the job's privacy requirements.

HTTP API v1 paths, response fields, and OpenAPI remain unchanged. Its result
still returns Markdown and sources/warnings; CLI and SDK expose portable files.
Optional export artifact fields are additive within schema v3; old snapshots
remain readable and no release tag is moved.

## Recovery and local concurrency

Every stage saves its context before committing `COMPLETED`. A job execution
lock serializes the same job across threads and processes; shorter storage
locks protect state, context, and migration operations. Status polling uses
the storage lock rather than waiting for analysis to finish. Windows uses
`msvcrt.locking` and Unix uses `fcntl.flock`. Lock waits are bounded to 30
seconds and timeout produces a retryable storage error. A process exit releases
its OS locks. Lock files live under `outputs/.locks/` and must not be deleted
while any process is using that output root. Automatic retention cleanup skips
locked jobs.

On resume, a `RUNNING`/`FAILED` stage, a completed stage without context, or
a missing/mismatched report artifact invalidates that stage and its dependents.
Earlier completed stages are reused. Each artifact is replaced through a unique,
flushed temporary file; the three report files are not a filesystem transaction.
The context manifest and stage state form the completion receipt, so an
interruption before all artifacts commit remains recoverable. Recovered stage
history is retained. A corrupted JSON context/state raises an error and is
preserved instead of silently reset.

Locks coordinate cooperating NoteForge processes on a local filesystem. This
is not a distributed/network-filesystem queue, multi-tenant authorization, or
a guarantee against power-loss behavior of every filesystem.

## Quality fixtures

[Real-source excerpts](../tests/fixtures/real_sources/README.md) cover a ResNet
abstract and the original AI Act text. Tests derive explicitly altered negative
inputs for missing evidence and conflicting identifiers. The tests run offline;
they do not prove live provider availability or legal applicability. Spawned
process tests exercise serialization, concurrent updates, and lock release on
termination. CI runs these on Linux and Windows.
