"""Behavioral quality checks using versioned real-source excerpts."""

import copy
import json
from pathlib import Path
from unittest.mock import patch

from noteforge.evidence import attribute_claims, audit_report, citation_registry
from noteforge.export import render_html
from noteforge.stages.policy import run as assess_policy
from noteforge.stages.report import run as render_report
from noteforge.stages.technical_cases import run as extract_cases

FIXTURES = Path(__file__).parent / "fixtures" / "real_sources"


def paper():
    return json.loads((FIXTURES / "resnet.json").read_text(encoding="utf-8"))["literature"]


def test_unrelated_claim_does_not_inherit_source_ids_or_support():
    result = attribute_claims({"claims": ["Unrelated invented outcome"]}, [paper()])
    claim = result["claim_records"][0]
    assert claim["evidence_ids"] == []
    assert claim["verification_status"] == "unverified"


def test_valid_id_does_not_prove_claim_semantics():
    draft = {"claims": ["Invented outcome"], "claim_records": [{"text": "Invented outcome",
             "evidence_ids": ["L1", "missing"], "verification_status": "supported"}]}
    claim = attribute_claims(draft, [paper()])["claim_records"][0]
    assert claim["evidence_ids"] == ["L1"]
    assert claim["verification_status"] == "referenced"
    assert claim["evidence_grade"] == "reference_only"


def test_literal_real_abstract_has_specific_support():
    source = paper()
    claim = attribute_claims({"claims": [source["abstract"]]}, [source])["claim_records"][0]
    assert claim["evidence_ids"] == ["L1"]
    assert claim["verification_status"] == "supported"
    assert claim["evidence_grade"] == "literal"


def test_document_literal_and_simulation_keep_distinct_grades():
    doc = json.loads((FIXTURES / "ai_act.json").read_text(encoding="utf-8"))["document"]
    claim = attribute_claims({"claims": [doc["raw_text"]]}, [], doc)["claim_records"][0]
    assert claim["source_type"] == "source_document"
    source = paper()
    source["source_type"] = "simulated"
    claim = attribute_claims({"claims": [source["abstract"]]}, [source])["claim_records"][0]
    assert claim["verification_status"] == "simulated"


def test_title_only_case_and_sparse_policy_do_not_fill_facts():
    source = paper()
    source["abstract"] = ""
    literature = {"provider": "crossref", "literature_results": [source]}
    assert extract_cases("ResNet", literature)["cases"] == []
    doc = json.loads((FIXTURES / "ai_act.json").read_text(encoding="utf-8"))["document"]
    with patch("noteforge.llm.chat", return_value=None):
        assert assess_policy("AI regulation", literature, doc)["policies"] == []


def test_policy_inference_with_real_excerpt_remains_reference_only():
    doc = json.loads((FIXTURES / "ai_act.json").read_text(encoding="utf-8"))["document"]
    response = {"policies": [{"policy_name": "Regulation (EU) 2024/1689",
                              "issuing_body": "Model-supplied authority", "evidence_ids": ["D1"]}]}
    with patch("noteforge.llm.chat", return_value=json.dumps(response)):
        result = assess_policy("AI regulation", {"provider": "crossref"}, doc)
    assert result["policies"][0]["verification_status"] == "referenced"
    assert result["policies"][0]["effective_date"] == ""


def test_doi_and_url_dedup_preserves_alias_references_and_source_types():
    first = paper()
    second = {**first, "source_id": "L2", "doi": "https://doi.org/10.48550/ARXIV.1512.03385"}
    third = {**first, "source_id": "L3", "doi": None, "url": first["url"] + "/#abstract"}
    simulated = {**first, "source_id": "L4", "source_type": "simulated"}
    canonical, aliases, warnings = citation_registry([first, second, third, simulated])
    assert len(canonical) == 2
    assert aliases == {"L1": "L1", "L2": "L1", "L3": "L1", "L4": "L4"}
    assert canonical[0]["citation_number"] == 1
    assert warnings == []
    synthesis = {"final_report": "A result [L2]", "extractor_draft": {"claim_records": [
        {"text": "A result", "evidence_ids": ["L2"]}]}}
    audit = audit_report(synthesis, {}, {}, [first, second])
    assert audit["quality"]["dangling_citations"] == []
    assert audit["quality"]["unused_sources"] == []
    report = render_report("topic", synthesis, sources=[first, second])
    assert "[1] [L2]" in report
    assert report.count(first["title"]) == 1


def test_conflicting_dois_are_not_merged_by_same_url():
    first = paper()
    second = {**first, "source_id": "L2", "doi": "10.1234/different"}
    canonical, _, _ = citation_registry([first, second])
    assert len(canonical) == 2


def test_citation_audit_catches_missing_numeric_and_named_citations():
    synthesis = {"final_report": "- Unknown [L99]\n- Missing numeric [999]\n- Uncited conclusion",
                 "extractor_draft": {"claim_records": [{"text": "No evidence", "evidence_ids": ["bad"]}]}}
    audit = audit_report(synthesis, {}, {}, [paper()])
    assert set(audit["quality"]["dangling_citations"]) == {"bad", "L99", "999"}
    assert audit["quality"]["uncited_records"] == ["No evidence"]
    assert audit["quality"]["uncited_narrative_lines"] == ["- Uncited conclusion"]


def test_duplicate_id_incomplete_metadata_and_invalid_records_warn():
    source = {**paper(), "doi": None, "url": "javascript:alert(1)"}
    audit = audit_report({"extractor_draft": {"metrics": [None]}}, {}, {}, [source, source, {"title": "No id"}])
    assert audit["quality"]["incomplete_sources"] == ["L1"]
    assert len(audit["warnings"]) == 4


def test_html_escapes_active_content_and_has_no_external_dependencies():
    malicious = '<script>alert(1)</script><img src="x" onerror="alert(1)">'
    output = render_html({"topic": malicious, "markdown": "# " + malicious + "\n- " + malicious})
    assert "<script>" not in output
    assert "<img" not in output
    assert "&lt;script&gt;" in output
    assert "Content-Security-Policy" in output


def test_audit_does_not_mutate_inputs():
    source = paper()
    before = copy.deepcopy(source)
    audit_report({}, {}, {}, [source])
    assert source == before


def test_nested_synthesis_keeps_single_document_title_and_heading_hierarchy():
    markdown = render_report("topic", {"final_report": "# Academic report\n\n## Findings\n- Finding [L1]"},
                             sources=[paper()])
    assert sum(line.startswith("# ") for line in markdown.splitlines()) == 1
    assert "### Findings" in markdown
