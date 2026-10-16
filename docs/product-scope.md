# Delivery Guardian — approved product scope and build gates

**Status:** Product direction approved by owner October 16, 2026. Scope baseline; implementation NOT yet complete.
**Repository:** `interplanetarysister/AmazonHackathon`
**Working product name:** Delivery Guardian (independent third-party hackathon project)
**Selected ideas:** #11 Delivery Guardian + #1 DoneProof + #5 Ring Resolution
**Primary track:** Alexa+; working self-hosted MCP 2025-11-25+ over Streamable HTTP with our own real MCP web client.
**Supplementary integration:** Ring developer APIs/Playground ONLY if verified in a working demo. Do not describe sample events as live Ring device events.
**Deadline:** Friday, October 23, 2026 **12:00 p.m. PDT**. Aim for complete and submitted by Oct 22, with Oct 23 as a buffer.
**Budget:** $0. No mandatory external subscriptions, paid hardware, carrier developer approvals, or paid hosting. Preserve minimum one Kiro credit, plus safety margin.

## 1. Pitch / product promise

**"Know what's coming. Know what actually arrived. Know what to do next."**

Delivery Guardian turns scattered delivery clues into a simple, accountable delivery journey. A user imports a shipping notice or adds a package, sees what a carrier reports, optionally connects compatible Ring evidence, confirms receipt (or reports a missing package), and gets truthful, step-by-step resolution support. Its DoneProof engine tracks what the software actually did and independently verifies stored results, rather than saying "done" without evidence.

**Target users:** ordinary online shoppers, busy households, working adults, small businesses receiving shipments, people whose packages are difficult to monitor. Design for broad appeal, short attention spans, phones, and first-time users.

**Distinctive use case:** "Carrier says delivered, but the package is not confirmed in hand." Ring motion can be a clue, not proof. The app must clearly say `carrier marked delivered`, `doorstep activity observed`, `person confirmed receipt` or `unknown`, according to evidence. It then prepares appropriate next steps without accusing anyone or secretly contacting companies.

**Outcomes for a 3-minute judge demo:** import a delivery, see a tracked ETA, ingest a labeled Ring Playground event or fallback fixture, reveal carrier-delivered versus not-received mismatch, request next steps, watch action log verify its own stored changes, correct a detail, and recover it after refresh.

## 2. Winning constraints / acceptance hierarchy

1. Eligibility: runnable MCP compliant with 2025-11-25 or later and Streamable HTTP, demonstrated by actual `initialize`, `tools/list`, `tools/call`, not decorative UI. Our web app must act as real MCP client.
2. Technical credibility: real persistence, real tool results, explicit post-write checks and failure handling, protocol/integration tests.
3. Design: immediately legible "Coming / Check / Received" overview; accessibility and phone layouts; error states and source attribution.
4. User impact: common household delivery pain; address a tangible unresolved task; show helpful action in <3 minutes.
5. Originality: combining carrier records, optional Ring signals, human confirmation, and independently verified AI actions. NOT another tracking-number entry form, normal package alert or list of carrier hyperlinks.
6. Cost/time: never require payment; submit functioning narrow product by Oct 23 with days available for testing.
7. Truth: never conflate sandbox fixture, API call, carrier assertion, inference, user action or real-world outcome. Publicly label simulation boundaries.
8. Compliance: own code, open-source license, public repo instructions, real demo video (<3 min), product feedback and friction log, free judge testing until Nov 20.

Official rules: https://amazonappdev2026.devpost.com/rules
Official FAQ: https://amazonappdev2026.devpost.com/details/faqs
Ring developer docs: https://developer.ring.com/ and https://developer.amazon.com/docs/ring/develop.html
MCP specification: https://modelcontextprotocol.io/specification/2025-11-25

## 3. Core P0 product scope — must actually work by submission

### P0-A. Easy delivery intake and overview
- An accessible web app usable on phone and desktop, no hardware required.
- User can paste an order/shipping notice, upload a local .eml/.txt file (optional PDF later) or enter delivery manually. Parse carrier/tracking/reference/ETA where explicit; offer an edit confirmation view. Never infer missing details confidently.
- Sample notices included locally, clearly labeled demonstration data.
- Save package records durably; list and open packages across refreshes and restarts.
- Three top-level views: **Expected**, **Needs attention**, **Received**. Every package detail includes source and timestamp.

### P0-B. DoneProof action ledger — real, independent outcomes
- Persist every requested action with idempotency key, attempt(s), tool name, inputs sanitized, result, status, source, timestamp, verification method and errors.
- State machine: `requested -> running -> accepted -> verified` OR `failed/needs_review`. "Accepted" is never automatically "verified".
- Read-after-write verification for local records; externally sourced state is verified only to the level of the source ("carrier reported X").
- Clear on-screen view: "requested / completed and verified / could not verify / needs help" and drill-down proof.
- Inject one deterministic failing operation into a demo test, display failure honestly, safe retry without duplicates.

### P0-C. Delivery evidence and mismatch reasoning
Keep **separate** truth fields (never a single misleading `delivered` flag):
  - `carrier_status`: unknown, expected, in_transit, out_for_delivery, marked_delivered, exception.
  - `doorstep_event`: none, unknown, observed (with real/sandbox/fixture source).
  - `receipt_status`: unknown, user_confirmed_received, user_reported_missing.
  - `resolution_status`: none, needs_attention, guidance_prepared, user_resolved.
- Create a `needs attention` case if carrier marks delivered but the user says not received; do not label theft.
- Ring events within ETA window may be offered for association only with explanation and optional human correction. Motion/doorbell video is not proof of package identity, theft, or physical receipt.
- Show "What we know / What we don't know / Suggested next step." Never fabricate external status.

### P0-D. Resolution guidance, not unauthorized action
- App prepares source-aware, general next steps: check safe location and household, allow for carrier status delay, contact seller/carrier through official channels, preserve tracking/evidence, request refund/replacement when eligible.
- Use a compact user-editable support message draft if appropriate; **no automatic sending, claims, charges or purchasing**.
- Never guarantee a refund, make legal determinations, or misstate customer-service policies. No unverified customer service URLs; do not embed links until verified.

### P0-E. Conversational workflow / tool transparency
- A plain-language input supports at least these demonstrated intentions: "Track this delivery", "What's due today?", "Was my package received?", "What do I do about a missing package?".
- The client invokes real MCP methods over HTTP; server responds with structured data; tool calls and their evidence are inspectable in an optional developer panel.
- If language understanding uses a deterministic planner instead of a live generative model, disclose that plainly. No external paid inference requirement.
- Persistent context across sessions: correct a delivery date, save it, and show source/impact of correction. Do not claim generalized Alexa+ memory editing.

### P0-F. Required runnable MCP tools
Implementation names may be refined with tests, but preserve equivalent semantics:
1. `import_delivery_notice` — validate/persist parsed imported data, idempotent.
2. `list_deliveries` and `get_delivery` — read real records.
3. `update_delivery_status` — accept properly sourced observations.
4. `record_doorstep_event` — accept explicit source/provenance.
5. `confirm_delivery_receipt` — human-asserted received/missing.
6. `find_delivery_issues` — evidence-based mismatch alerts.
7. `prepare_resolution_steps` — proposed human-reviewed guidance.
8. `get_action_proof` — verified ledger and tool evidence.
Each tool must use validation, authorization relevant to demo, idempotency for changes, predictable structured errors, and proper timestamps.

### P0-G. Tests and clean-room proof
- Automated tests for MCP handshake/list/call, status separation, imported data, persistence after restart, duplicate events, missing fields, incorrect data correction, read-after-write verification, failed tools, missing consent and inaccessible credentials.
- E2E judge runbook with exact free startup command, seeded sample records, expected results and a reset command.
- Screenshot and video use synthetic/sample data; no private user email, Ring footage, address or tracking number.
- Optional local test supported on Ubuntu in Termux as feasible; judges on a standard desktop must be able to reproduce independently.
- Clear honest disclosure of non-implemented, future or simulated components.

## 4. P1 gated extras — only after all P0 acceptance tests pass

### P1-A. Actual Ring developer evidence
- Priority: access official Ring Developer Playground; inspect its legitimate developer surfaces and docs; use a real permitted API call / Playground simulation in a repeatable workflow; retain evidence that call actually happened (redacted, no credentials).
- Sandbox may simulate package events inside live view. **Do not assume it sends package webhooks to our application**. A manually imported sandbox event must be labeled sandbox imported; a purely local event is labeled fixture. Official Ring docs describe a separate production app/OAuth process.
- The Ring documentation MCP server at `https://knowledge.appstore-mcp.ring.amazon.dev/mcp` is documentation lookup, NOT actual live Ring device event access.
- Don't claim an eligible Ring-track implementation until the Ring API/SDK/simulator is actually used by app runtime and shown in the video.
- No requirement for consumer Ring hardware, Ring subscription, or Ring certification to run the core Alexa+ entry.

### P1-B. Preferred delivery time (user control)
- From user-provided delivery and availability history, offer an *explainable* recommendation for a preferred window; show example observations and allow opt-out/edit/delete.
- Do not secretly monitor home occupancy or infer work schedules from surveillance. Do not automatically order groceries.

### P1-C. Mini-challenge and presentation upgrades
- Kiro CLI/steering used for implementation can be documented, but do not claim that ordinary Kiro CLI alone meets the AWS Builder mini challenge. Official rules expressly name **Kiro Crew**, which must be actually used and documented before claiming it.
- Optional AWS integration only when demonstrably real, no risk of charges. AWS promo codes exhausted Oct 7; no AWS required for primary.
- Open Source mini challenge only through an additional licensed project or meaningful external contribution with tests, separate from this main repo.
- Capture real reproducible developer friction for up to 10% judging bonus.
- Add one polished explanatory diagram/demo evidence view; don't weaken reliability for decoration.

## 5. Excluded until AFTER the hackathon (not build promises)
- Always-on Gmail, Outlook, Shopify, UPS, FedEx, USPS or Amazon orders connections. OAuth, scope approval, service APIs and account privacy take more than the remaining time.
- Background account/email monitoring, proactive outreach, self-submitted claims, refunds, grocery purchases, financial transactions, and predictive work/home surveillance.
- Full Ring camera footage analytics, real-time video surveillance, face recognition, package identity claims, or working live device links absent actual permission.
- Paid infrastructure, Ring subscriptions, external hardware, subscription handling, multi-household marketplace, native Android/iOS APKs, enterprise accounts, broad international carrier coverage.
- Amazon partnership assertions, Alexa+ production device account linking, gated SDK access.

## 6. Data contract / architecture

Recommended simplest viable implementation: Python >=3.11; official MCP Python SDK capable of Streamable HTTP, minimal FastAPI/Starlette if needed, SQLite, static accessible HTML/CSS/JS front end. Do not overengineer or force new stack until runtime check. Minimize install/compile dependencies to work on Ubuntu/Termux and desktop Linux/macOS/Windows (where dependencies allow).

Entities:
- `Delivery`: id, source reference, carrier, tracking_redacted, ETA/timezone, source status, receipt status, resolution status, created_at, updated_at; synthetic sample fields.
- `Evidence`: id, delivery_id, source_type (user, carrier_notice, ring_playground, local_fixture), observed_at, recorded_at, details sanitized, confidence, verified_scope.
- `Action`: id, idempotency_key, tool, status, result, verified_at, verifier, source_ids, error_code.
- `ResolutionCase`: id, delivery_id, trigger, guidance, draft_status, user_resolution.
- `Preference` (P1): user-entered preferred window and controlled consent.

Data rules:
- Verified API response or read-back confirms that **our database changed**, not that someone physically received a parcel.
- Carrier records, doorbell activity and human acknowledgments must retain distinct provenance and uncertainty.
- Missing camera evidence means `unknown`, not `did not happen`.
- All clocks UTC with display in explicit local time zone; time windows and elapsed time must be tested.
- Keep fixtures deterministic and reproducible; no credentials in repo or terminal history. Sample and real user data never mixed.

Example architecture:
`Responsive Web UI (actual MCP client) -> Streamable HTTP MCP server -> planning/tools -> SQLite evidence/ledger -> verified tool responses`.
`Ring API/Playground` (P1 gated) -> source-aware adapter -> Evidence; `local fixture` separately labeled.
`Shipping confirmation` (user supplied) -> parser/confirmation -> Delivery.
No required online model API. The agent/tool coordination must be genuinely functioning; use truthful description of any rule-based or AI planning.

## 7. Demo path (target 2:30–2:50; must be <3:00)

0:00–0:15: "My package says delivered, but I can't find it." One-sentence pain.
0:15–0:40: Paste/upload sample confirmation; create verified persistent delivery.
0:40–1:10: Show carrier marked delivered and Ring Playground evidence (only if truly integrated and labeled; otherwise a clearly named local fixture).
1:10–1:40: User reports not received. Show evidence vs unknown; request safe resolution steps.
1:40–2:05: Trigger failed tool/action and show DoneProof correctly refusing to label success.
2:05–2:25: Correct expected date or parcel detail; refresh; show reliable persistent context and ledger.
2:25–2:45: Show MCP actual tool calls, open judge instructions and clear next-step benefit.

Record actual product in use; do not substitute animations, static fake terminal output, or fabricated integrations. If live Ring demo is infeasible, invest extra seconds in actual MCP+DoneProof reliability.

## 8. Timeboxed build plan and stop/go gates

- **Oct 16:** Lock scope, owner/agent guardrails; scaffold and locally validate MCP initialize/list/call; eliminate install blockers.
- **Oct 17:** Delivery intake, SQLite model, mobile overview and persistence; baseline tests green.
- **Oct 18:** DoneProof ledger, status/evidence separation, deterministic failure/retry; tests green.
- **Oct 19:** Evaluate Ring Playground access and actual integration. If blocked, label fallback fixture and protect P0.
- **Oct 20:** Resolution guidance, easy UX, provenance UI. Freeze new large features.
- **Oct 21:** Integration tests, accessibility, clean-room judge run, security/secret review, real friction log.
- **Oct 22:** Record/test <3 minute public demo; Devpost text, product feedback, repo cleanup, license verification; submit if ready.
- **Oct 23 before noon PDT:** submission confirmation, emergency buffer only.

**Hard gates**
- G1: protocol authentic and testable.
- G2: complete user journey is working and persisted; DoneProof never lies.
- G3: free fresh install with no real credentials, hardware or Kiro is reproducible; tests pass.
- G4: accurate/demo-safe presentation, licensed public repo, video, Devpost text and tool feedback complete.
- G5: submit on time, verify submitted status.

If time short, CUT P1 and visual extras rather than cut G1–G5.

## 9. Production after competition

Do not call the demo "consumer production-ready." Before accepting real customer email, tracking numbers or Ring footage:
- Per-user isolation, strong authentication, authorized OAuth scopes/revocation, secret storage, privacy notice/terms, retention/deletion, observability and rate limits.
- Test actual carrier and retailer API permissions, delivery-status consistency, webhook authenticity/signatures and retries.
- Privacy-by-design for household occupancy, camera feeds and contact lists; no silent monitoring.
- Security reviews, actual deployment spend checks, backup/recovery and support policy.
- Separate claims of shipment status from human confirmed receipt; consequences require user approval.
This readiness work is outside the Oct 23 hackathon MVP.

## 10. Source and status honesty

Official Ring developer release notes describe Playground simulations for Package/Vehicle/Motion live-view workflows, but documentation also distinguishes this from full production OAuth/webhook integrations. Do not advertise successful event delivery into our own server without showing and testing that path. Same rule for Gmail, carriers, Alexa devices and AI inference.

**Current status at scope creation:** Documentation/README and license exist in GitHub; these scope requirements describe work to build, not features already implemented. Update this status and evidence links only as tests pass.
