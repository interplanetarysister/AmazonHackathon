# Ring Guardian / Package P.I. — build, demo, and verification guide

Updated October 22, 2026. This guide describes **two separate codebases** and does not claim that the published Base44 application is built from this GitHub repository.

## 1. Which version to run?

| Build | Location | What it contains |
| --- | --- | --- |
| GitHub runnable prototype (Delivery Guardian / Package P.I.) | This repository, Python `app.py` | Local FastAPI/SQLite demonstration and MCP Streamable HTTP endpoint |
| Ring Guardian Cam — Unrewound | Base44 app ID `6ad9406e7da53afe29334379` | Vite/React management and customer experiences, five fictional package scenarios, scanner/camera evidence, voice-guided tour, Ring/Amazon adapter demonstrations |
| Cloudflare Alexa+ demonstration MCP | `https://ring-guardian-alexa-mcp.interplanetary-fund.workers.dev/mcp` | Separate public demo endpoint; not proof of official Alexa+ registration |

The **Base44 frontend source is not currently bundled in this GitHub repository**. Do not try `npm install` or `npm run build` at this repository root. These instructions are for the actual files present.

## 2. Build and run the code in GitHub (free, local)

Requirements: Python 3.11–3.13, terminal and browser. Python 3.14 on Termux can require additional native builds; choose a supported environment. No AWS or Kiro credits are required.

```bash
git clone https://github.com/interplanetarysister/AmazonHackathon.git
cd AmazonHackathon
python -m venv .venv
# Linux, macOS or Termux Ubuntu:
. .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
python -m unittest discover -s tests -v
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` **on the same device**. The database is SQLite; set `DG_DB_PATH` if a different temporary filename is needed. This localhost application **has no authentication/multiuser protection; never expose port 8000 to the public internet or use real customer records.**

In the interface: load an example delivery, mark a *manually entered* carrier-delivered claim, add a *local fictional* doorstep event, report “I can't find it,” review support guidance and the recorded action status, then refresh to confirm saved SQLite state. See [QUICKSTART.md](../QUICKSTART.md) for details. A simulated Ring-format webhook is **not** a real Ring API event.

## 3. Inspect the separate published Ring Guardian demonstration

- Public landing page: https://ring-guardian.base44.app/
- User/customer route: https://ring-guardian.base44.app/view/customer
- Warehouse/management route: https://ring-guardian.base44.app/view/management
- Guided demo: https://ring-guardian.base44.app/guided-demo
- Ring adapter demonstration: https://ring-guardian.base44.app/ring
- Alexa/MCP demonstration: https://ring-guardian.base44.app/alexa

**Publish the newest Base44 source version before recording.** Base44 is the authority for this frontend; GitHub's Python prototype is different. The Base44 application currently implements a demo-mode selection screen, role-specific customer and management workspaces, and clearly labeled unconnected-service placeholders in its latest saved source. Publication of that exact version must be verified separately.

The Base44 project build commands (run inside an **exported Base44 React/Vite project**, not at this GitHub root) are:

```bash
npm install
npm run build
npm test
```

Its package scripts are Vite production build and `node --test scripts/live-workflows.test.mjs`. The last observed Base44 run passed eight tests. This does not replace tests of the published site or a local build from actual exported source. **No exported React files are present here yet.**

## 4. Alexa+ MCP test checklist

Primary-track demonstration target: MCP protocol `2025-11-25` or later, Streamable HTTP. For the GitHub prototype, run `app.py` locally and use its web client to demonstrate JSON-RPC `initialize`, `tools/list`, and `tools/call` at `POST /mcp`.

The separate Cloudflare endpoint can be inspected at `https://ring-guardian-alexa-mcp.interplanetary-fund.workers.dev/health`. At last check it returned `ok: true`, `mode: fictional-demo-only`, `ring_connected: false`, `alexa_plus_registered: false`. Its reported four tools were `list_demo_packages`, `get_package_timeline`, `get_simulated_evidence`, and `get_investigation_status`.

**Do not advertise an official Alexa+ voice device, registered skill, Ring device, or live customer camera connection without an authenticated real-world test.** Browser text-to-speech is the current demo narrator, not an Alexa voice service.

## 5. Recording path — fewer than 3 minutes

1. Open the newly published landing page; demonstrate the admin-controlled Demo On switch and choose User or Management.
2. In User: select a fictional package, identify a missing-delivery scenario, create a clearly labeled complaint draft and show the Amazon support guidance. Do not say it was submitted.
3. In Management: inspect wearable scanner/camera status and battery percentages (simulated), scan evidence, an exception, and an investigation/corrective recovery.
4. On Alexa/MCP: demonstrate a **working** MCP handshake, tool discovery, and package lookup or show the browser-generated narration as **simulated voice**. State which is actually running.
5. End with labels differentiating real application logic from fictional devices and data.

Ensure on-screen timestamps, spoken narration, and camera scenes refer to the **same selected package and event**. Do not describe a mocked scene as genuine Ring footage.

## 6. Submission preflight — check rather than assume

- [ ] Public Base44 site serves the newest landing page and both role workspaces, not an older build.
- [ ] Demo On and Demo Off behave as labeled; only authorized admin changes global mode.
- [ ] The five fictional scenarios load in a fresh judge browser session.
- [ ] Customer complaint draft and management recovery each work from end to end.
- [ ] Narration is audible, and an instruction visibly identifies the corresponding element.
- [ ] The real MCP server and web client exchange initialize/list/call messages; document request/results.
- [ ] Source in GitHub matches **the code represented as the submitted project**, or clearly link each separate project with build instructions and an export where required.
- [ ] Public YouTube/Vimeo video is shorter than three minutes and shows software actually running.
- [ ] Project description, screenshots/media, source URL, platform/tool feedback and any required form fields are complete in Devpost.
- [ ] All Ring, Alexa, Amazon and simulated-branding claims are truthful.

Official links: https://amazonappdev2026.devpost.com/rules and https://amazonappdev2026.devpost.com/resources. Deadline: **October 23, 2026 at 12:00 PM PDT**. Submission to Devpost is a separate user action; this document does not submit anything.
