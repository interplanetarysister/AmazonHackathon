# Delivery Guardian — Amazon Developer Hackathon

Delivery Guardian helps people investigate uncertain deliveries by comparing package events, independently labeled evidence, and reported issues. It provides guided support steps and an interactive demonstration using fictional records.

## Run the demonstration

See [QUICKSTART.md](QUICKSTART.md) for requirements, installation, testing, and the interactive walkthrough.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 on the same device.

**Security:** This local demonstration does not implement production user authentication or multi-user data isolation. Run it only on localhost with fictional data.

## Features demonstrated

- Package histories, example delivery updates, user-confirmed receipt, and discrepancy detection.
- Guided investigation and support information without claiming to contact a carrier.
- Case and action persistence in a local database, with verification and duplicate-action prevention.
- Sample doorstep events with explicit provenance, plus signed-event validation.
- An interactive MCP server and web client using Streamable HTTP and protocol version 2025-11-25 or later.
- Five fictional package scenarios.

**Integration boundaries:** Simulated camera events are not verified footage from Ring hardware. Browser narration is not an authenticated Alexa device connection. Any actual integrations should be demonstrated and described separately from sample content.

## For evaluators

- [Installation and functional walkthrough](QUICKSTART.md)
- [Build and evaluation guide](docs/ring-guardian-build-and-demo.md)
- [Project scope](docs/product-scope.md)
- [Submission requirements](docs/hackathon-requirements.md)

Official contest: https://amazonappdev2026.devpost.com/
