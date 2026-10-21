# Final hackathon compliance gate — 2026-10-21

Official rules: https://amazonappdev2026.devpost.com/rules
Submission deadline: **2026-10-23 12:00 PDT**. This is an evidence checklist, not a certificate of eligibility. Never check an item without dated evidence.

## Track truth

- Package P.I. primary track: **Alexa+**. An MCP Streamable HTTP endpoint and browser client are implemented in this repository. End-to-end running validation on the intended demo host and independent MCP client remain to be confirmed. Official rules alternatively permit clearly labeled Alexa+ simulation with its source available.
- Ring Guardian primary track: **Ring**. Its current synthetic scanner/camera events **do not qualify**. Obtain and demonstrate an authenticated documented Ring API/SDK/simulator/device runtime interaction. See official Ring developer portal.
- Vega OS/Fire TV: **not yet qualified** for either project merely by having web UI or APK. Only claim Fire TV if it runs on actual Fire OS/Vega OS hardware or official simulator.
- AWS Builder mini-challenge: **not yet evidenced**. Official rules say **Kiro Crew** qualifies as a development tool without a runtime AWS service. Do not equate an unverified Kiro CLI session to verified Kiro Crew; identify actual usage and provide proof. Synthetic variables do not establish AWS integration.

## Required independently verified evidence

- [ ] Track technology executes in running app, shown in demo, with console/API/session proof.
- [ ] Source and dependencies, all assets, setup/run/test instructions and working judge access are reproducible.
- [ ] Public open-source repository with a detectable open-source LICENSE, or approved private reviewer access.
- [ ] Actual running product demo, **under 3 minutes**, publicly visible on YouTube/Vimeo, link in Devpost.
- [ ] If preexisting, explain and demonstrate significant changes during hackathon window.
- [ ] Product feedback for **each Amazon tool/API/SDK actually used**: usage, strengths, problems, onboarding, future choice.
- [ ] AWS Builder only: documented actual AWS service use or verified Kiro Crew use, described in product feedback.
- [ ] Optional Open Source: separate qualifying new project or contribution with URL, repo URL, GitHub username and meaningful explanation.
- [ ] Permission/privacy/IP check; no unauthorized real customer, Ring video or carrier data; no private credentials in repo.
- [ ] English materials or English translation.
- [ ] Submit complete Devpost fields before deadline and verify final submission receipt.
- [ ] Keep source and demo accessible without payment/restrictions through judging (Nov 9–20).
- [ ] Unique, substantially different entries when both projects are submitted.
- [ ] Optional evidence-based friction log for each actual issue: task, steps, expected, observed, severity, workaround and recommendation.

## Recorded code change October 21

The two projects now share fictional SIM tracking IDs for demonstrable offline correlation: Package P.I. `simulation_variables.py` maps its existing SQLite fixture; Ring Guardian `/simulated-camera-events` exposes a JSON fixture and local UI button. Neither is a real AWS or Ring cloud integration. New tests were committed but had not yet been executed in the authenticated development environment at the time of authoring.

## Immediate acceptance tests

Package P.I.: `python -m unittest discover -s tests -v`; then start FastAPI on localhost and use its five-package UI; verify MCP initialize/tools/list/tools/call using an independent client.
Ring Guardian: `python -m unittest discover -s tests -v`; run `python -m src.server`, click *View simulated camera events* and inspect `/simulated-camera-events`.
Actual Ring Playground/API integration remains a blocking Ring primary-track acceptance gate. Never represent the above local tests as a substitute.
