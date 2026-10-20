# Amazon Developer Hackathon: verified research and implementation memory
_Last researched: 2026-10-20. Recheck official sources before decisions; beta SDKs and contest updates change._

## Authority and source priority
1. Official rules: https://amazonappdev2026.devpost.com/rules
2. Official resources: https://amazonappdev2026.devpost.com/resources
3. Official FAQ: https://amazonappdev2026.devpost.com/details/faqs
4. Updates: https://amazonappdev2026.devpost.com/updates
5. Vega latest docs: https://developer.amazon.com/docs/vega/latest/vega-develop
6. Vega SDK setup: https://developer.amazon.com/docs/vega/0.24/install-vega-sdk
7. Vega build guide: https://developer.amazon.com/docs/vega/latest/build-an-app
8. Vega app manifest: https://developer.amazon.com/docs/vega/0.24/app-manifest
9. Ring developer portal: https://developer.ring.com/
10. Ring API docs: navigate from https://developer.ring.com/ ; confirm API entitlement and exact endpoint semantics before implementation.

## Dates, judging, and awards
- Submission due **October 23, 2026, 12:00 PM Pacific**. Judging November 9–20, winner announcement around December 3.
- Stage 1 eligibility pass/fail: real primary-track use required.
- Stage 2, four **equally weighted** dimensions: Technical Implementation, Design, Potential Impact, Quality of the Idea. Tie-breaking follows criterion order.
- Detailed friction logs (task, attempted steps, expected/actual, severity, workaround, actionable suggestion) may earn up to **10% bonus**.
- Free/low-cost development preferred. October 7 rules update says AWS promotional credit codes exhausted; do not count on credits.

## Official primary tracks
- Fire TV: demo-ready running app on **Fire OS OR Vega OS**; show actual device or official simulator in demo. Computer vision is among priority categories. The contest itself does not require Vega in all projects.
- Alexa+: self-hosted MCP server or Agent Skill, MCP spec **2025-11-25 minimum** over Streamable HTTP, OR the rules' permitted simulated Alexa+ experience path. Preview-only Alexa+ add-on SDK/CLI/Web Simulator are not available generally to hackathon entrants.
- Ring: working use of Ring APIs, SDKs, simulator or device; video must show actual Ring simulator or supported device usage. Ring technology must actually execute at runtime; a static mention, mocked webhook, or UI branding alone is insufficient. Priority areas include business systems, access control, accessibility, IoT automation, caretaking.
- Bee: real Bee or Apple Watch with Bee software data through CLI/MCP/Skills; demonstrable user value.
- Optional AWS Builder mini challenge: documented AWS service integration; official rules additionally recognize Kiro Crew as a development tool without runtime AWS service.
- Optional Open Source mini challenge: separately qualifying public contribution/repo/branch/fork/PR in hackathon period; provide contribution URL, project URL, username, explanation.

## Existing repository facts and scope decisions
- Repository: https://github.com/interplanetarysister/AmazonHackathon ; currently public, main branch.
- Its README (checked 2026-10-20) labels the primary track **Alexa+**, with a real local MCP server and Ring as supplementary and not yet live-verified. Do NOT silently rewrite history or claim Ring is integrated. README identifies 14 tools, persistence, local fixtures, signed Ring-format webhook inbox; says independent MCP-SDK proof and official Ring Playground/API proof remain incomplete.
- Owner's **new requirement**: authentic **Vega OS** functionality, not a fake screenshot. Treat as additional accepted product constraint requiring genuine Vega SDK build and simulator/device proof if presenting it as Fire TV entry. Do not assume Vega is required for Alexa+ or Ring eligibility or claim it already runs without test.
- Product: Delivery Guardian / Package P.I.; shipping-status import, delivery evidence, human verification, missed delivery guidance, optional Ring camera evidence, future package-scanning state machine.
- Scope priority with short runway: prove existing primary track and submission first; Vega expansion only if it can be implemented and proven without endangering minimum eligible working submission. If changing track, explicitly reconcile README, application, video, and Devpost selection.
- Future machine vision: states UNSCANNED, HELD_FOR_SCAN, SCANNED; transitions based on motion/hand proximity, confirmed barcode read, and database validation. Must handle ambiguous/unreadable/duplicate scan, identity matching, privacy, audit, and deterministic fallback. Not currently implemented or demonstrated. Do not claim it works.

## Vega OS developer specification
- Vega OS is Amazon's Linux-based TV platform using React Native-based SDK. Vega Developer Tools: Vega Studio VS Code extension, Vega CLI, SDK Manager, Vega Virtual Device.
- Official v0.24 requirements: native macOS 10.15+ (Apple Silicon preferred) or Ubuntu 20.04/22.04/24.04 x86_64; **Windows and WSL unsupported/tested**; around 20 GB disk, Node.js >=16 and platform dependencies. Android Termux is not a verified native supported Vega development host.
- Vega SDK v0.24 generally maps to Vega OS 1.2 and React Native 0.83; older SDK versions can use RN 0.72. Never mix libraries across incompatible SDK/OS/RN versions.
- Root `manifest.toml` required with mandatory `[package]` and OS version; identifier follows reverse DNS. Official build guide: `vega project update-manifest --os-min 1.2 --os-version 1.2` where relevant; `npm install && npm run build:app` after installing SDK. Validate against current docs, don't paste blindly into old projects.
- Vega libraries include runtime permissions, navigation/focus, media playback, WebView and custom native Turbo Modules. React Navigation compatibility is Vega-version-specific. Request only needed system privileges.
- Test D-pad and TV focus navigation, readable TV typography, overscan/safe areas, suspend/resume, crashes, memory/performance, latency, accessible controls. Virtual Device can support early testing; Amazon recommends real Fire TV Stick testing for Appstore submission. Hackathon accepts official TV/Vega simulator demo.
- Avoid claiming an Android APK is itself a Vega OS app. Fire OS Android APK and Vega application packaging are different targets.
- Vega docs open beta; check release notes and API compatibility immediately before coding.

## Ring integration technical constraints
- Ring developer platform describes authenticated developer APIs and MCP support, live video including WebRTC/RTSP, motion and doorbell events, device status and history. Developer Playground/simulator is permitted in competition.
- Confirm account enrollment, API credentials, authorization scopes, available camera/event permissions, webhook signature rules, subscription/retention rules, rate limits, and simulator access from current official Ring docs before coding. Do not invent endpoint URLs or permissions.
- Architecture: server-side OAuth/token storage, least-privilege scopes, signed verified webhooks, deduplication and replay protection, timestamp skew handling, explicit device-to-shipment association, event correlation, retention and consent, audit log. WebRTC/RTSP stream access requires user authorization and technical validation; don't scrape surveillance feeds or conflate a local sample with real Ring footage.
- Preserve separate claims: 'carrier says delivered', 'Ring event observed', 'person confirmed received', and 'AI inference'. AI uncertain evidence must never be labeled established fact.

## Submission must-haves and DOs
- Working code **and** video proof on intended platform (real device or authorized simulator).
- GitHub repository URL with complete source code, dependencies, assets, reproducible setup/test steps. Public repository with discoverable valid open-source LICENSE, or private repo with accepted judge collaborator invitations according to current rules. Verify latest required reviewers in rules; invitation acceptance matters.
- Public YouTube/Vimeo demo **under three minutes**, strongly focused: problem > working solution > actual track technology > result and customer value. Never pass off scripted mockups as working live services.
- Project description and explanation of changes during hackathon window if pre-existing project.
- Detailed **product feedback for each API/SDK/tool used**: tool and use case, strengths, weaknesses, zero-to-hello-world onboarding, would use again + why.
- Specify track(s) and mini-challenges; supply extra fields for AWS Builder/Open Source if entered.
- Useful: feature requests (critical/important/nice-to-have), rigorous friction log.
- Ensure working unrestricted judge access through judging, with safe dedicated demo credentials if login needed; never publish secrets.
- Submission materials in English or include translation.
- Finish and freeze materials by Oct 23 at noon PDT. Official final-stretch update advises no edits to code repo/video/submission after deadline until winner announcement.
- Respect third-party intellectual property, data licensing and camera privacy, API terms; no unapproved trademarks/music.
- Hide secrets in server environment; add .env to .gitignore; use example env template without tokens; scan repository for credentials.
- Preserve zero-dollar development policy and the remaining Kiro credit; avoid paid services, AWS surprise billing and unnecessary GitHub Actions minutes. Batch prompts only after acceptance criteria, tests, and current repository inspection.

## DON’Ts and honesty gates
- Don't say 'using Vega' without actual Vega build and proof.
- Don't say 'Ring connected' on local fixture, a Ring-shaped webhook, or README text.
- Don't claim Amazon partnership/endorsement; permitted technology usage is not partnership.
- Don't spend credits just to add nice-to-have UI before eligibility proof.
- Don't fabricate carrier status, camera events, delivery outcomes, actions or AI model confidence.
- Don't use real customer surveillance data without proper consent and privacy safeguards.
- Don't ship demo-only shortcuts as production-grade OAuth or trust them with user accounts.
- Don't omit required product feedback, video, repo license/access or install instructions.
- Don't present untested machine-learning scanning as implemented.

## Prioritized implementation/runbook
1. Run and document existing FastAPI/MCP tests and **independent** MCP 2025-11-25 SDK interoperability. Prove reachable demo client and persistence.
2. Inspect official Ring Playground availability; integrate and test one real documented flow if feasible; otherwise label Ring as future and keep Alexa+ primary.
3. Evaluate and implement minimal genuine Vega OS TV client with official toolchain only if host environment and deadline permit; prove with SDK build and Vega simulator capture. Else do not claim Fire TV/Vega track.
4. Ensure no secrets, complete LICENSE, clean README and QUICKSTART, judge setup, objective proof matrix.
5. Write friction logs and tool-by-tool product feedback.
6. Record public <3-minute real demo video and upload; submit Devpost before deadline.
7. Freeze submission and repo on deadline per organizer update.

## Research limits
This reference consolidates verified primary official rules, Vega SDK/start/build/manifests, Ring platform overview, Devpost resources/FAQ and current repository README. It is **not a claim that every Amazon API endpoint or SDK document was exhaustively inspected**. Specific Ring endpoints/limits and Vega manifest fields must be rechecked in their canonical API references when implementation requires them.
