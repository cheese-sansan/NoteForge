# Evidence Modes and Literature Providers

Provider selection controls where literature records come from. It is independent from the optional LLM used to analyze those records.

| Provider | Data origin | Network | Valid citation source | Failure behavior |
| --- | --- | --- | --- | --- |
| `crossref` | Crossref REST API metadata | Required | Metadata only; verify through the DOI or publisher | Empty results plus warning |
| `mock` | Deterministic local fixtures | No | No | Always labelled `simulated` |
| `llm-simulated` | LLM-generated demonstration data | LLM endpoint | No | Remains labelled as simulated output |

Crossref is the default. It may return records without abstracts; NoteForge keeps the abstract empty and does not fabricate methods, findings, metrics, or limitations. Table, figure, reference-entry, issue, and volume components are filtered before the result limit is applied.

Simulated modes must be selected explicitly:

```bash
noteforge run --topic "AI evaluation" --provider mock
noteforge run --topic "AI evaluation" --provider llm-simulated
```

Reports show the active data mode near the top. A real-provider outage never triggers an automatic Mock fallback because mixing simulated records into a retrieval run would make the report's provenance ambiguous.

## Provider versus analysis model

The literature provider supplies source records. An optional OpenAI-compatible model can assist with extraction and synthesis after retrieval, but model credentials do not change the selected literature provider and cannot turn simulated records into real evidence.

## Verification boundary

Crossref supplies bibliographic metadata, not guaranteed full text. Verify DOI records, abstracts, claims, and quantitative findings through the publisher or another authoritative source before relying on them.
