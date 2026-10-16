# Delivery Guardian — Amazon Build, Ship, Shape Hackathon

**Status:** Local working MVP milestone 1 committed and backend-tested; live Ring Playground/API integration, independent official MCP SDK interoperability, public production readiness, and Devpost submission are **not yet complete**.

**Working name:** Delivery Guardian  
**Selected ideas:** #11 Delivery Guardian + #1 DoneProof + #5 Ring Resolution  
**Primary hackathon track:** Alexa+ (real MCP 2025-11-25+ Streamable HTTP server with a working web MCP client)  
**Additional integration target:** Ring developer Playground/API when honestly testable, otherwise labeled sample evidence.  
**Deadline:** **Friday, October 23, 2026 at 12:00 p.m. PDT**.

> **Know what's coming. Know what actually arrived. Know what to do next.**

Delivery Guardian is a privacy-conscious delivery follow-through application. It aims to combine shipping notices, independently verified software actions, optional Ring doorstep evidence and human package-receipt confirmation. When a delivery is unclear or missing, it prepares transparent customer-service next steps rather than claiming it automatically filed a complaint. Built for zero-cost development and a reproducible working demo, not a static mockup.

## Start here

- [Approved product scope, architecture, acceptance tests and dates](docs/product-scope.md) — **authoritative requirements for the product**.
- [Project-wide agent and development guardrails](AGENTS.md) — applies to contributors, Kiro, Codex and all production/deployment work.
- [Hackathon rules, eligibility, track integrations and submission checklist](docs/hackathon-requirements.md).
- [Customer feedback, unresolved problems and feature research](docs/customer-voice-opportunity-research.md).
- [Kiro steering file](.kiro/steering/hackathon-winning-scope.md).

## Non-negotiables

- No paid plans, services, hardware, or surprise spending. Preserve the final Kiro credit plus safety margin.
- Real, testable, source-cited functionality. Do not call an AI action done without verification.
- Separate carrier reports, Ring device/sandbox/local simulated activity and human-confirmed receipt.
- Distinguish working integrations from proposed ones in screenshots, demo and documentation.
- Scope freeze: prioritize complete Alexa+ MCP implementation first; Ring is a gated supplementary feature.
- An authentic under-three-minute demo, clean-room judge setup, developer product feedback, and a timely Devpost submission are mandatory.

## Run milestone 1

See [QUICKSTART.md](QUICKSTART.md) for setup and demonstration steps.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` in a browser on the same device. No hardware or online API key required.

**Implemented and backend-tested (Oct 16):** stateless MCP Streamable HTTP 2025-11-25 JSON-RPC `initialize`, `tools/list`, `tools/call`; fourteen real tools; SQLite persistence; a shipping-notice text parser with user review, imported/manual delivery records and verified ETA corrections; user-confirmed receipt and manually entered carrier status; local fixture doorstep events; delivery mismatch detection; human-reviewed support guidance; DoneProof local read-back ledger with idempotency, persistently recorded failed mutations, a signed Ring-format webhook inbox (raw-body HMAC-SHA256 verification and replay protection), explicit event-to-delivery association, and seven passing backend tests. JavaScript passes syntax validation.

**Browser proof:** Chromium exercised the running UI JavaScript against the real FastAPI/SQLite application through a local browser test bridge: create sample, enter delivered claim, report missing, show guidance, record failed mutation, and reopen a fresh page with persistent data; no JavaScript exceptions. Direct networked browser-to-localhost communication was blocked by the test environment, so native HTTP browser E2E should still be confirmed in Termux.\n\n**Not verified yet:** official MCP SDK interoperability, Ring Playground/API calls, actual third-party carrier or email connections, live Alexa+ device access, authentication/multiuser security, public deployment, and Devpost submission. **This is a local demo, not public production.** Never advertise local fixture activity as a Ring event.

**Next priority:** Run a real browser-to-localhost demo on Termux, verify independent MCP SDK interoperability, test the official Ring Playground if accessible, then finalize the friction log, demo video, setup validation and Devpost submission. The signed Ring-format test fixture is not a real Ring event. No Kiro credits or paid services were consumed.

Official contest: https://amazonappdev2026.devpost.com/
