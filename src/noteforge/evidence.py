"""Conservative claim attribution and deterministic citation auditing."""

from __future__ import annotations

import re
from copy import deepcopy
from urllib.parse import unquote, urlsplit, urlunsplit


def attribute_claims(output: dict, literature: list, document: dict | None = None) -> dict:
    result = dict(output)
    sources = {str(item["source_id"]): item for item in literature
               if isinstance(item, dict) and item.get("source_id")}
    doc_text = str((document or {}).get("markdown_text") or (document or {}).get("raw_text") or "")
    if doc_text:
        sources["D1"] = {"source_type": "source_document", "abstract": doc_text}
    existing = {str(item.get("text")): item for item in output.get("claim_records", [])
                if isinstance(item, dict) and item.get("text")}
    # These rows were extracted deterministically from the local document.
    from noteforge.stages.synthesis import _document_evidence

    document_claims = _document_evidence(document)[0]
    records = []
    for value in output.get("claims", []):
        text = str(value).strip()
        if not text:
            continue
        raw = existing.get(text, {})
        requested = raw.get("evidence_ids", [])
        requested = requested if isinstance(requested, list) else []
        refs = [str(value) for value in requested if str(value) in sources]
        matches = [key for key, item in sources.items() if
                   text in item.get("key_findings", []) or
                   (text and text in str(item.get("abstract", ""))) or
                   (key == "D1" and text in document_claims)]
        refs = list(dict.fromkeys(refs + matches))
        literal_refs = [key for key in refs if key in matches and
                        sources[key].get("source_type") in {"source_document", "external_api"}]
        simulated = bool(refs) and all(sources[key].get("source_type") == "simulated" for key in refs)
        origin = "simulated" if simulated else ("source_document" if literal_refs == ["D1"] else "llm_inference")
        status = "simulated" if simulated else ("supported" if literal_refs else "referenced" if refs else "unverified")
        records.append({"text": text, "evidence_ids": refs, "source_type": origin,
                        "verification_status": status,
                        "evidence_grade": "simulated" if simulated else "literal" if literal_refs else
                                          "reference_only" if refs else "unverified"})
    result["claim_records"] = records
    return result


def _doi(value) -> str:
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", str(value or "").strip(), flags=re.I).casefold()


def _url(value) -> str:
    try:
        parts = urlsplit(str(value or "").strip())
        if parts.scheme.lower() not in {"http", "https"} or not parts.netloc:
            return ""
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"), parts.query, ""))
    except ValueError:
        return ""


def citation_registry(sources: list[dict]) -> tuple[list[dict], dict[str, str], list[str]]:
    """Deduplicate DOI/URL identities within a provenance type, preserving aliases."""
    canonical: list[dict] = []
    aliases: dict[str, str] = {}
    identities: dict[tuple[str, str], dict] = {}
    warnings = []
    for raw in sources:
        item = deepcopy(raw)
        source_id = str(item.get("source_id") or "")
        if not source_id:
            warnings.append("来源记录缺少 source_id。")
            continue
        if source_id in aliases:
            warnings.append(f"重复 source_id：{source_id}，后续记录未采用。")
            continue
        url = _url(item.get("url"))
        doi = _doi(item.get("doi"))
        if not doi and url:
            parts = urlsplit(url)
            if parts.hostname in {"doi.org", "dx.doi.org"}:
                doi = _doi(unquote(parts.path.lstrip("/")))
        # Never merge real and simulated origins, even when their identifiers match.
        origin = str(item.get("source_type", "unverified"))
        keys = [(origin, "doi:" + doi)] if doi else []
        if url:
            keys.append((origin, "url:" + url))
        # Different explicit DOIs take precedence over a coincident URL.
        match = identities.get(keys[0]) if doi else next((identities[key] for key in keys if key in identities), None)
        if match is None and doi:
            match = next((identities[key] for key in keys[1:] if key in identities and
                          not identities[key].get("doi")), None)
        if match is not None:
            match["aliases"].append(source_id)
            if doi and not match.get("doi"):
                match["doi"] = doi
            aliases[source_id] = match["source_id"]
        else:
            item.update(source_id=source_id, doi=doi or None, citation_number=len(canonical) + 1, aliases=[source_id])
            canonical.append(item)
            aliases[source_id] = source_id
            match = item
        for key in keys:
            identities.setdefault(key, match)
    return canonical, aliases, warnings


def audit_report(synthesis: dict, cases: dict, policies: dict, sources: list[dict]) -> dict:
    canonical, aliases, warnings = citation_registry(sources)
    claims = deepcopy(synthesis.get("extractor_draft", {}).get("claim_records", []))
    dangling: list[str] = []
    uncited: list[str] = []
    used = set()
    metrics = synthesis.get("extractor_draft", {}).get("metrics", [])
    for record in claims + list(metrics) + list(cases.get("cases", [])) + list(policies.get("policies", [])):
        if not isinstance(record, dict):
            warnings.append("忽略非结构化证据记录。")
            continue
        refs = record.get("evidence_ids", [])
        refs = refs if isinstance(refs, list) else []
        label = str(record.get("text") or record.get("case_name") or record.get("policy_name") or "未命名记录")
        valid = [aliases[str(ref)] for ref in refs if str(ref) in aliases]
        used.update(valid)
        dangling.extend(str(ref) for ref in refs if str(ref) not in aliases)
        if not valid:
            uncited.append(label)
    prose = str(synthesis.get("final_report", ""))
    by_number = {str(item["citation_number"]): item["source_id"] for item in canonical}
    for token in re.findall(r"\[([A-Za-z0-9_-]+)\](?!\()", prose):
        if token in aliases:
            used.add(aliases[token])
        elif token in by_number:
            used.add(by_number[token])
        else:
            dangling.append(token)
    # Warn about uncited narrative lines; do not pretend arbitrary prose is a claim graph.
    uncited_lines = [line.strip() for line in prose.splitlines() if
                     line.strip().startswith(("- ", "* ")) and
                     not re.search(r"\[[A-Za-z0-9_-]+\](?!\()", line)]
    if dangling:
        warnings.append("引用不存在的来源：" + ", ".join(dict.fromkeys(dangling)))
    if uncited:
        warnings.append(f"{len(uncited)} 条结构化结论没有有效引用，需回查原文。")
    if uncited_lines:
        warnings.append(f"{len(uncited_lines)} 条正文列表项未附来源编号，需人工检查。")
    insufficient = [item["source_id"] for item in canonical if
                    item.get("source_type") == "external_api" and not item.get("doi") and not _url(item.get("url"))]
    if insufficient:
        warnings.append("外部来源缺少 DOI/有效 URL：" + ", ".join(insufficient))
    return {"sources": canonical, "aliases": aliases, "warnings": warnings,
            "quality": {"scope": "citation traceability; not semantic or full-text verification",
                        "dangling_citations": list(dict.fromkeys(dangling)), "uncited_records": uncited,
                        "uncited_narrative_lines": uncited_lines, "incomplete_sources": insufficient,
                        "unused_sources": [item["source_id"] for item in canonical if item["source_id"] not in used],
                        "claims": claims}}
