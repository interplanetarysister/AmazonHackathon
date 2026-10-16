# AGENTS.md — Delivery Guardian hackathon operating rules

These instructions govern all contributors, AI coding agents (including Kiro/Codex), scripts, PRs, deployments, and production decisions in this repository. Read `docs/product-scope.md` and `docs/hackathon-requirements.md` before making changes. If instructions conflict, honor official hackathon rules, then the owner's approved scope, then this file. Proposed work outside scope requires explicit owner approval.

## Mission / target
Build **Delivery Guardian** (working name), combining #11 Delivery Guardian, #1 DoneProof and #5 Ring Resolution. Primary submission track: **Alexa+**, implemented as a real MCP (2025-11-25 or later) Streamable HTTP server and an independent working web MCP client. Ring sandbox/integration is a gated supplementary capability, NOT grounds to claim real Ring device connectivity. Deadline: **October 23, 2026 at 12:00 p.m. PDT**, with a submission buffer. Real functionality and judge-reproducible setup beat breadth.

## Nonnegotiables
1. **Zero-dollar total development budget.** Do not enable paid plans, AWS resources that can bill, pay-as-you-go, paid hosting, carrier contracts, or required hardware. Do not assume promo AWS credits.
2. **Kiro credits: protect the final credit.** Never launch Kiro work unless remaining balance is verified and there is a conservative margin above at least one reserved credit. A single request can use more than one credit. Use free tools and prewritten specifications first; combine well-defined coding/testing/documentation work. Never start unattended Kiro agents, credit-consuming loops, or schedules without owner approval.
3. **Truthful claims.** Distinguish authentic Ring Playground calls, local fixtures, imported messages, manual user confirmation, and live service integrations in code, UI, logs, and demo. No fake 'connected', 'verified delivered', 'AI analyzed' or 'claim submitted'. Ring documentation MCP is not live customer device API access. Do not claim access to private Alexa+ tooling.
4. **DoneProof invariant.** A requested action is not complete solely because an agent or API says so. Persist the action request, attempt, evidence/source and actual read-back/verification where possible; use `unknown`, `needs-review` or `failed` when verification is absent. API accepted != outcome verified; carrier-marked delivered != customer confirmed receipt; Ring activity != proof of a particular parcel.
5. **Safety, user agency and privacy.** Consent before connecting accounts; no secrets, raw credentials, private email, addresses or tracking numbers in Git, screenshots, fixture recordings or logs. Human review before contacting anyone, posting publicly, making payments, purchases or filing complaints. Provide data deletion controls for real users. Never suggest footage or silence proves theft.
6. **Functional, not mockup.** Test real MCP `initialize`, `tools/list` and `tools/call` through Streamable HTTP, app/database state, repeated requests, failures and follow-up sessions. A labeled sample event is fine but processing/verification must execute for real.
7. **Don't destabilize the submission.** Prioritize critical path; avoid new dependencies and major rewrites after Oct 20 unless needed to fix a blocker. No 'complete' label until tests and clean-room demo pass. No unapproved automatic production deployment.
8. **Accessibility.** Mobile-first (Android/Termux-friendly), plain-language labels, readable contrast, obvious outcome/status and controls. A nontechnical person should understand the app in seconds.
9. **Document changes.** When an interaction changes, update relevant help/README, tests, demo script, and developer friction log when a real issue occurs. Tell the truth about what was actually tested.
10. **No false Amazon affiliation.** Present as an independent hackathon project, not an official Amazon/Ring partnership. Follow logo/trademark and open-source license restrictions.

## Scope gates
- **P0 submission-critical:** working MCP HTTP server + web MCP client, import/manual package records, persisted package timeline, evidence/provenance, DoneProof action ledger, trustworthy issue detection, user confirmation, prepared support guidance, responsive demo, automated tests, clean-room setup, Devpost materials.
- **P1 only after P0 passes:** verified Ring Playground integration/official API testing, limited context preference suggestions, optional meaningful AWS Builder/Open Source mini challenge.
- **Post-hackathon:** full Gmail OAuth syncing, UPS/FedEx/USPS/Amazon account integrations, autonomous camera watching, paid cloud, scheduling, household multiaccount, automatic purchases/complaints, predictive personalization.

## Engineering directions
Favor simple local-first architecture (Python 3.11+; MCP Python SDK + FastAPI/Starlette where useful; SQLite; simple accessible web client). Choose exact implementation after checking environment. Tests must run without third-party credentials, proprietary hardware, paid APIs or a Kiro subscription. Use parameterized SQL, dependency pins, input validation, idempotency keys, bounded retries, source timestamps, time zones, clear errors, and secure handling of any secrets. Public demo must use only synthetic data and avoid open writes to shared private data.

The app should show provenance per claim (`source_type`, `observed_at`, `verified_at`, `verification_method`, `confidence/uncertainty`). Do not mislabel deterministic rules as a live AI model. Make actual agent/tool orchestration inspectable.

## Judging and release gates
Official judges score technical implementation, design, potential impact and originality equally; an honest friction log can add up to 10%. Deliver a public under-three-minute video; complete source/setup/test instructions; product feedback; licensed GitHub repo; no undisclosed restricted accounts. A live deployment is optional under official Alexa+ FAQ, but judge-reproducible local execution is required. Demo-only code is not automatically consumer-production ready: production requires authorized OAuth, secure data separation, privacy controls, real integration tests, and operational support.
