"""Portable report artifacts; HTML treats all report content as text."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from noteforge.evidence import audit_report
from noteforge.models import JobStatus
from noteforge.storage.atomic import write_text
from noteforge.storage.context import ContextStore
from noteforge.storage.locking import JobLock
from noteforge.storage.state import StateManager, validate_job_id


def report_payload(topic: str, markdown: str, synthesis: dict, cases: dict, policies: dict,
                   sources: list[dict], warnings: list[str], audit: dict | None = None) -> dict:
    audit = audit or audit_report(synthesis, cases, policies, sources)
    return {"report_version": 1, "topic": topic, "markdown": markdown,
            "sources": audit["sources"], "citation_aliases": audit["aliases"],
            "quality": audit["quality"], "warnings": list(dict.fromkeys(warnings + audit["warnings"])),
            "synthesis": synthesis, "technical_cases": cases.get("cases", []),
            "policy_assessment": policies.get("policies", [])}


def render_html(payload: dict) -> str:
    title = html.escape(str(payload["topic"]))
    body = []
    in_list = False
    in_table = False
    table_header = False
    source_section = False
    numbers = {str(source["citation_number"]) for source in payload.get("sources", [])}

    def inline(text):
        escaped = html.escape(text)
        escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
        return re.sub(r"\[(\d+)\]", lambda match:
                      f'<a href="#citation-{match[1]}">[{match[1]}]</a>' if match[1] in numbers else match[0], escaped)

    for line in str(payload["markdown"]).splitlines():
        text = inline(line)
        table_row = line.startswith("|") and line.endswith("|")
        if in_table and not table_row:
            body.append("</tbody></table></div>")
            in_table = False
        if table_row:
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                continue
            if not in_table:
                body.append('<div class="table-wrap"><table><tbody>')
                in_table = True
                table_header = True
            tag = "th" if table_header else "td"
            body.append("<tr>" + "".join(f"<{tag}>{inline(cell)}</{tag}>" for cell in cells) + "</tr>")
            table_header = False
            continue
        bullet = line.startswith("- ")
        if in_list and not bullet:
            body.append("</ul>")
            in_list = False
        if line.startswith("#") and " " in line:
            marker, heading = line.split(" ", 1)
            if set(marker) == {"#"} and len(marker) <= 6:
                level = len(marker)
                if level == 2:
                    source_section = heading == "数据来源"
                body.append(f"<h{level}>{html.escape(heading)}</h{level}>")
                continue
        if bullet:
            if not in_list:
                body.append("<ul>")
                in_list = True
            number = re.match(r"- \[(\d+)\]", line)
            anchor = f' id="citation-{number[1]}"' if source_section and number else ""
            body.append(f"<li{anchor}>{inline(line[2:])}</li>")
        elif line.startswith("> "):
            body.append(f"<blockquote>{inline(line[2:])}</blockquote>")
        elif line.strip():
            body.append(f"<p>{text}</p>")
    if in_list:
        body.append("</ul>")
    if in_table:
        body.append("</tbody></table></div>")
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'">
<title>{title}</title><style>
body{{font:17px/1.7 system-ui,sans-serif;color:#172635;background:#f5f7fa;margin:0}}
main{{max-width:900px;margin:32px auto;padding:36px;background:white;border-radius:12px}}
h1,h2,h3{{line-height:1.3}} h2{{border-bottom:1px solid #dae0e7;padding-bottom:12px;margin-top:36px}}
p,li{{overflow-wrap:anywhere;white-space:pre-wrap}} blockquote{{border-left:4px solid #426585;padding:12px;background:#eef4f8}}
.table-wrap{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:15px}}
th,td{{border:1px solid #dae0e7;padding:10px;text-align:left}} th{{background:#eef4f8}}
a{{color:#20537c}} li:target{{background:#fff5d6}}
@media print{{body,main{{background:white;margin:0;padding:0}} h2,h3{{break-after:avoid}}}}
</style></head><body><main>{''.join(body)}</main></body></html>\n"""


def write_exports(job_dir: Path, payload: dict) -> dict[str, str]:
    paths = {"json": job_dir / "report.json", "html": job_dir / "report.html"}
    write_text(paths["json"], json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    write_text(paths["html"], render_html(payload))
    return {name: str(path) for name, path in paths.items()}


def export_job(job_id: str, *, format: str = "json", output_root: Path = Path("outputs")) -> Path:
    """Export a completed job without rerunning providers or replacing its Markdown."""
    if format not in {"json", "html"}:
        raise ValueError("export format must be json or html")
    job_id = validate_job_id(job_id)
    manager = StateManager(job_id, output_root)
    if not manager.state_file.exists():
        raise FileNotFoundError(f"job not found: {job_id}")
    with JobLock(job_id, output_root, execution=True):
        if manager.load_state().status is not JobStatus.COMPLETED:
            raise ValueError("only completed jobs can be exported")
        data = ContextStore(job_id, output_root).load_all()
        report = manager.job_dir / "report.md"
        markdown = report.read_text(encoding="utf-8")
        report_data = data.get("report", {})
        audit = None
        if "quality" in report_data:
            audit = {"sources": report_data["sources"], "aliases": report_data["citation_aliases"],
                     "quality": report_data["quality"], "warnings": []}
        payload = report_payload(data.get("input", {}).get("topic", job_id), markdown,
                                 data.get("synthesis", {}), data.get("technical_cases", {}),
                                 data.get("policy_assessment", {}), report_data.get("sources", []),
                                 report_data.get("warnings", []), audit)
        paths = write_exports(manager.job_dir, payload)
        return Path(paths[format])
