# Security Policy

NoteForge is designed for local research workflows and standalone API deployments. It is not a hardened multi-tenant hosted service.

## Supported versions

Security fixes target the latest tagged release and the current `main` branch. Older releases may receive documentation updates but are not guaranteed code fixes.

## Reporting a vulnerability

Do not open a public issue for suspected credential exposure, path traversal, arbitrary file access, authentication bypass, remote code execution, or disclosure of private document content.

Use GitHub private vulnerability reporting when available, or contact the maintainer directly. Include the affected version or commit, reproduction conditions, potential impact, and the smallest safe proof of concept.

## Operational boundaries

- Set `API_TOKEN` before exposing `/api/v1/jobs/*` beyond a trusted local environment.
- Treat uploaded documents and extracted text as untrusted input.
- Keep `.env` and credentials outside version control.
- Treat `outputs/jobs/{job_id}/` as potentially sensitive and do not publish generated artifacts by default.
- Keep simulated literature visibly labelled; never present it as retrieved evidence.
- Verify DOI metadata, generated analysis, and policy conclusions against authoritative sources before relying on them.

## Pre-publication audit

```bash
python scripts/privacy_audit.py
python scripts/privacy_audit.py --history
python scripts/privacy_audit.py --include-outputs
```

The audit checks for high-confidence credentials, assigned secret-like values, private absolute paths, and phone-like numbers. Findings are redacted in command output.
