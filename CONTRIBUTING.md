# Contributing

Contributions should improve NoteForge as an evidence-aware research report pipeline while preserving its source boundaries and stable interfaces.

## Development setup

```bash
git clone https://github.com/cheese-sansan/NoteForge.git
cd NoteForge
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on Linux and macOS:

```bash
source .venv/bin/activate
```

Install the package and development tools:

```bash
python -m pip install --upgrade pip
python -m pip install ".[dev,documents]"
```

## Required checks

Run the focused checks appropriate to the change. Before a release or a change to shared contracts, run the full set:

```bash
python -m build --wheel
ruff check src/noteforge tests scripts
pyright src/noteforge
pytest --cov=noteforge --cov-report=term-missing --cov-fail-under=80
python scripts/check_openapi.py
python scripts/api_smoke.py
python scripts/privacy_audit.py --history
docker compose config
docker compose build api
```

Changes to HTTP API v1 require deliberate review of `tests/snapshots/openapi_v1.json`. Changes to packaging should also install the built wheel in a clean environment and exercise the CLI and SDK outside the checkout.

## Contribution principles

- Keep `mock` deterministic and usable without a network connection or API key.
- Never add an automatic simulated fallback to a real-provider execution path.
- Keep simulated records visibly labelled with `source_type: simulated`.
- Preserve source IDs, warnings, and verification status when transforming evidence.
- Add or update tests for behavior and contract changes.
- Keep focused fixes separate from unrelated refactors.
- Do not commit credentials, `.env`, generated jobs, private documents, local paths, caches, or IDE metadata.

## Pull requests

Describe the problem, the chosen solution, user-visible or compatibility impact, and the checks that passed. Call out evidence-model, API, migration, privacy, or Docker implications explicitly.

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for project attribution and [SECURITY.md](SECURITY.md) for private vulnerability reporting.
