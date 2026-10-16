# Build, Ship, Shape — Amazon Developer Hackathon

**Requirements research and submission playbook**  
**Last verified:** October 16, 2026  
**Repo:** https://github.com/interplanetarysister/AmazonHackathon  
**Submission deadline:** **Friday, October 23, 2026 at 12:00 p.m. Pacific (PDT)**

> This document distinguishes official requirements from our project recommendations. If anything changes, the official Devpost Rules and Submission Form take precedence. These checkboxes track work and are not evidence that an item is complete.

## Official sources

- [Hackathon home](https://amazonappdev2026.devpost.com/)
- [Official rules (authoritative)](https://amazonappdev2026.devpost.com/rules)
- [FAQ — hardware, simulators, judging access, Alexa+](https://amazonappdev2026.devpost.com/details/faqs)
- [Developer resources and starter samples](https://amazonappdev2026.devpost.com/resources)
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-11-25)

## 1. Dates, eligibility, and entry

| Topic | Official requirement / detail |
| --- | --- |
| Submission period | August 31 – October 23, 2026 at **12:00 p.m. Pacific** |
| Judging | November 9 – November 20, 2026 |
| Expected winners announcement | On or around December 3, 2026 |
| Registration | Join via hackathon Devpost page and submit required fields there |
| Entrants | Eligible adults, teams, and eligible legal entities; see prohibited locations/conflicts in Rules |
| Team size | No stated maximum; teams/organizations require an authorized representative |
| Price to enter | No purchase necessary |
| New versus existing | New work permitted; existing projects must be significantly updated during the hackathon period, and changes described/demonstrated |
| Ownership and permissions | Submission must be original/owned by entrant; authorized usage of third-party APIs, assets and licenses |
| Multiple submissions | Allowed if unique and substantially different |

**Submission is a separate action on Devpost. A GitHub commit alone is not an entry.**

## 2. Primary tracks and platform proof

Build a working product for at least one primary track; describe and demonstrate its actual integration.

### Alexa+ — proposed primary track

Two sanctioned paths:

1. A functional **Agent Skill** or **self-hosted MCP server** implementing **MCP 2025-11-25 or later**; the MCP server uses **Streamable HTTP** transport.
2. Alternatively, a simulated Alexa+ experience built with AI/agentic tools. This alternate path does not require a particular MCP-shaped interface, but **real running simulation code** and a clear demo are required.

A **custom web-based MCP client** that exchanges real MCP initialize, tools/list, and tools/call operations with the server is explicitly accepted. Amazon's official gated Alexa+ Add-on SDK, CLI, Toolkit and Web Simulator are **not open to hackathon participants**. Do not claim real Echo/Alexa+ integration unless actually demonstrated.

Priority creative uses: stateful multi-step work across services, maintaining context across sessions, richer cards/interfaces, real-world task execution; **not** a one-turn FAQ assistant or superficial API wrapper.

### Fire TV

- Demo-ready app **running on Fire OS or Vega OS**.
- Real Fire TV hardware or supported simulator/emulator accepted.
- Any appropriate framework/language; demo must show Fire OS/Vega execution.
- Priority uses: AI-enhanced viewing, sports, fitness, family entertainment, multi-modal interaction and computer vision.

### Ring

- Real working integration using a Ring API, SDK, documented simulator or device.
- Video must show the application working with simulator or device.
- Priority uses: accessibility, caretaking, delivery and package operations, home automation, and business systems.

### Bee wearable AI

- Real Bee-processed data recorded through a **Bee device or Apple Watch running Bee software** must be used.
- Show an actual data interaction in both runnable code and demo.
- Mock-only data or a README mention is not enough.
- Priority uses: productivity, education, developer experience.

**Track decision (planning, not a submitted choice):** Prioritize Alexa+ for no mandatory physical hardware and the ability to show reliable, auditable multi-step actions with a working client/server. Avoid presenting proposed capabilities as shipped.

## 3. Mini challenges

### AWS Builder

- Add a meaningful, clearly documented use of AWS services or qualifying AWS tools to the primary submission.
- Examples: Bedrock, AgentCore, Strands SDK, SageMaker; official rules also say **Kiro Crew on its own can qualify as a development tool**.
- Submission product feedback should identify exactly what was used and how.
- For competitiveness, prefer integrated reasoning plus real tools/records over a token one-off model call or unused infrastructure.

### Open Source

- Requires **an additional open-source project or meaningful public contribution** during the hackathon period alongside the main entry.
- A separate licensed repo, fork, branch or pull request (even unmerged) can qualify.
- Supply contribution URL, project repository URL, GitHub username, and explanation of what/how/why.
- **The MIT license on this main repository alone does NOT satisfy this mini challenge.**

A project can receive at most **one primary-track prize and one mini-challenge prize**.

## 4. Required submission package — checklist

- [ ] Register / join on [Devpost](https://amazonappdev2026.devpost.com/) and confirm eligibility.
- [ ] Select a primary track and make its required runtime integration genuinely work.
- [ ] Write clear product description: target user, problem, features and functionality.
- [ ] Supply **GitHub repository URL** with **all source code, assets, setup, run and test instructions**.
- [x] Repo is public with a **MIT LICENSE** file (checked October 16, 2026).
- [ ] Confirm GitHub visibly **detects license in repository header/About area** as required by rules.
- [ ] Demonstrate the required track technology **actually running**, not just referenced in documentation.
- [ ] Record a **public YouTube or Vimeo demo under three minutes** (judges need not watch after 3:00).
- [ ] Show the application on its intended device/platform or permitted simulator. For our Alexa+ route, show the independent MCP web client and actual tool calls, if choosing MCP.
- [ ] Ensure all video media/trademarks/music are original or used with permission.
- [ ] Complete product feedback for **each Amazon API/SDK/tool**: what used and for what; what worked; errors/limitations and workarounds; onboarding experience; would build again and why.
- [ ] Select primary and any mini-challenge categories in the Devpost submission form.
- [ ] For AWS Builder: document AWS tools/services and exact integration in product feedback.
- [ ] For Open Source (only if entered): include the separate contribution URL, repo, username, and explanation.
- [ ] Provide **free, unrestricted judging access** through at least the end of judging (Nov 20), including test credentials for private deployment if necessary. Judges may rely only on submitted text/video and might not run code.
- [ ] Confirm submission materials are in English (or include required English translation).
- [ ] Submit **before October 23 noon PDT**, then verify that Devpost shows submitted status.

**Public versus private GitHub:** Rules accept a public repository with an open-source license visible to GitHub, **or** a private repository shared with specified Amazon/Devpost reviewers. We already have public + MIT, so there is no need to invite private reviewers. Publishing under MIT permits broad reuse of the licensed code; do not commit secrets, credentials, private user data or proprietary assets not intended for redistribution.

## 5. How judges score

### Stage 1 eligibility gate

Pass/fail: reasonably fits theme and applies required APIs/SDKs/tools. Do not risk the entire submission by substituting a static mockup for the required running integration.

### Stage 2 — four equally weighted criteria

1. **Technical implementation (25%)** — actual working platform integration; reliability and appropriate use of technology.
2. **Design (25%)** — cohesive, accessible interaction tailored to target device.
3. **Potential impact (25%)** — specific customer problem, credible audience and real-world value.
4. **Quality of idea / creativity (25%)** — goes beyond a trivial assistant, API wrapper or existing feature.

**Optional developer friction logs can provide up to 10% bonus.** Log each genuine issue: attempted task, reproduction steps, expected result, actual result, severity, workaround and concrete suggestion. Do not invent tool failures.

### Demo narrative that matches scoring

1. Show the user's real problem (10–20 seconds).
2. Demonstrate a working request that spans multiple tools and persists records.
3. Show **independent verification** of actual state, including a deliberate failed action handled visibly.
4. Show later follow-up with reliable, correctable memory.
5. Explain the actual Amazon technology and its implementation (not just logos).

## 6. Proposed project direction (NOT an Amazon requirement)

**Working theme:** Verified AI Actions + Explainable Memory.

**Customer-research insight:** Repeated complaints about AI assistants claiming success without corresponding state changes, missing multi-step follow-through, or misremembering information. Separate genuine missing software capabilities from issues solved by device settings, subscription payment or basic existing features.

**Proposed MVP:**
- One conversational front end for entering an actionable task (e.g. organize a neighborhood event).
- A real MCP server (Streamable HTTP, MCP spec 2025-11-25) with create/list/update task operations and durable data storage.
- An action ledger recording requested actions, tool calls, success/failure and verifiable stored results.
- A follow-up session that retrieves accurate context and can correct a previously saved fact with provenance.
- Basic tests for tool calling, persistence, duplicate submissions, failures, and access control.
- Optional meaningful AWS Builder integration, documented and tested against real AWS service endpoints.
- **No false completion claims**; never claim a third-party task executed without a verifying response.

**Explicitly out of scope unless time permits:** Fire TV, Ring and Bee track integrations; generalized app marketplace; unverified Alexa+ consumer-device connectivity; unrelated extensions; purchasing/funds movement.

## 7. Repo structure / evidence we should produce

Suggested layout (not yet implemented unless files exist):

- `README.md` — elevator pitch, setup and demo commands, track/requirements proof.
- `docs/hackathon-requirements.md` — this document.
- `docs/architecture.md` — sequence of client → agent → MCP → tools → persistence.
- `docs/developer-feedback.md` — tools used, onboarding, what worked, limitations, feature requests.
- `docs/friction-log.md` — genuine problems with reproduction details.
- `docs/demo-script.md` — timed video script and demonstration checklist.
- `docs/submission-checklist.md` — final verification before Devpost submission.
- `src/` and/or `server/` — actual runnable implementation.
- `tests/` — runnable smoke/integration tests.
- `.env.example` — placeholder configuration names only, **never live credentials**.

## 8. Timeboxed implementation plan

- **Oct 16–17:** repository setup, validate chosen track, first runnable MCP endpoint/client.
- **Oct 18–19:** working persistence, core tools and actual verified task completion.
- **Oct 20–21:** memory/provenance, error handling, tests and AWS integration if feasible.
- **Oct 22:** demo recording, feedback/friction log, setup validation and submission draft.
- **Oct 23 before noon PDT:** final clean-room test and Devpost submission.

**Cost note:** Amazon says the earlier $150 AWS promotional credit codes were exhausted as of October 7, 2026. Avoid assuming any new credit allocation. Use AWS budgets/alerts and shut down billable services when not testing. The FAQ says an MCP server need not remain live continuously after submission, but ensure access if judges are invited to test it.

## 9. Source-of-truth reminders

- Source: [Rules, §4 (project/submission requirements)](https://amazonappdev2026.devpost.com/rules).
- Source: [Rules, §6 (judging)](https://amazonappdev2026.devpost.com/rules).
- Source: [FAQ (Alexa+ preview access, simulators, public GitHub, hosting)](https://amazonappdev2026.devpost.com/details/faqs).
- Source: [Resources (platform toolkits and samples)](https://amazonappdev2026.devpost.com/resources).

**Next action:** Implement one working Alexa+ MCP loop, verify it on a clean machine, and capture real evidence for the demo. The submission itself has not been made.
