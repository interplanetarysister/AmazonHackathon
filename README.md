# Delivery Guardian — Amazon Build, Ship, Shape Hackathon

**Status:** Local working MVP milestone 1 committed and backend-tested; Ring API integration, independent MCP SDK interoperability, browser end-to-end acceptance, and Devpost submission are **not yet complete**.

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

**Implemented and backend-tested (Oct 16):** stateless MCP Streamable HTTP 2025-11-25 JSON-RPC `initialize`, `tools/list`, `tools/call`; eleven real tools; SQLite persistence; a shipping-notice text parser with user review, imported/manual delivery records and verified ETA corrections; user-confirmed receipt and manually entered carrier status; local fixture doorstep events; delivery mismatch detection; human-reviewed support guidance; DoneProof local read-back ledger with idempotency, and five passing backend tests. The UI JavaScript passes syntax validation.

**Not verified yet:** browser end-to-end interaction (test environment blocked Chromium's localhost network), independent MCP SDK interoperability, Ring Playground/API calls, actual third-party carrier or email connections, live Alexa+ device access, authentication/multiuser security, public deployment, and Devpost submission. **This is a local demo, not public production.** Never advertise local fixture activity as a Ring event.

**Next priority:** Validate a local real-browser run on user's Termux environment; test official MCP SDK interoperability; investigate official Ring Playground sandbox permissions; add meaningful actual integration only if feasible before deadline; harden reproducibility, accessibility, and capture a genuine under-three-minute demo.

Official contest: https://amazonappdev2026.devpost.com/
