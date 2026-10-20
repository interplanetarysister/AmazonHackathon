# Package P.I. — judge-ready live demonstration and submission gate
_Updated October 20, 2026. This is an execution plan, not proof that untested items passed._

## Critical contest fact
Deadline: **October 23, 2026, 12:00 PM PDT**. Primary track remains **Alexa+**: independently built MCP protocol 2025-11-25 Streamable HTTP server. Ring is a *supplemental simulated evidence source*, not a qualifying Ring track integration yet. No Vega OS app has been verified. **Do not change the track based on cosmetics.**

Official rules: https://amazonappdev2026.devpost.com/rules
Research: [Amazon developer research](amazon-developer-research-2026.md)

## Judge setup — on the machine running the demo
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
uvicorn app:app --host 127.0.0.1 --port 8000
```
Open http://127.0.0.1:8000 on the same machine. For Termux, activate your Python environment as appropriate; the commands above are for ordinary POSIX Python. Never expose the unauthenticated demo to the internet.

## Under-three-minute recording script (actual screen capture)
- **0:00–0:18, problem:** A package can be marked delivered even when its owner cannot find it. Delivery Guardian keeps carrier statements and user confirmation separate. Show the running dashboard.
- **0:18–0:40, real track proof:** Point to the screen's MCP connected state. Show the app using real `initialize`, `tools/list`, and `tools/call` on `POST /mcp`. The web client is an MCP client; the demo is **not** running on an Alexa device. Do not imply Alexa account linking.
- **0:40–1:20, five packages:** Enter `judge-demo` and select **Load five samples**. Show all five named fictional cases, one each for delivered-but-missing, hub delay, wrong truck, evidence requested, and confirmed received. Read status and provenance labels.
- **1:20–1:52, resolution:** Pick `SIM-1003` and change its **simulated** logistics status to `located`. Refresh and confirm stored read-back; do not say an Amazon truck was actually contacted or a package retrieved.
- **1:52–2:24, DoneProof:** Demonstrate a carrier delivered claim and customer missing report, then review issue guidance and the persisted action record. Show one deliberately invalid operation is a failure, not a success.
- **2:24–2:45, finish:** Refresh to show persistence; explain that this runs locally with SQLite and synthetic records, while real carrier/Ring integration, authentication, and deployment remain future work.

Record one continuous or honestly edited capture of actual running functionality with legible text and narration/captions. Upload an accessible **YouTube or Vimeo video under 3:00** and provide the link in Devpost; do not use concept animations instead of runtime proof.

## Required objective evidence before declaring ready
| Gate | Evidence to produce | Status Oct 20 |
|---|---|---|
| Existing MCP + DB tests | Entire `python -m unittest discover -s tests -v` stdout, exit 0 | NOT RUN HERE |
| Five-package MCP test | `tests/test_demo_mcp_integration.py` pass | ADDED, NOT RUN |
| Independent MCP SDK interoperability | Separate client initializes/lists/calls successfully | NOT VERIFIED |
| Five demo cases visually usable | UI capture, update, refresh, failure path | NOT VERIFIED in this session |
| Official Ring SDK/Playground | Real authorized invocation and response logs | NOT VERIFIED; do not claim |
| Vega OS simulator/device | Official SDK build and runtime recording | NOT VERIFIED; do not claim |
| No secrets or personal data | Inspect tracked files and recording | NOT VERIFIED |
| Judge setup | Clean Python environment succeeds without credentials | NOT VERIFIED |
| Public video | Link to real app recording under 3 minutes | NOT PROVIDED |
| Devpost submitted | Confirmation on Devpost before deadline | NOT SUBMITTED |

## Judge-facing product feedback (only record observed experiences)
For each actually used tool (MCP protocol/implementation, Python/FastAPI; Kiro *only if personally used*), record:
1. Tool/version and the actual task.
2. What worked and what specifically did not.
3. Concrete steps and error text to reproduce any friction.
4. Workaround actually tried and result.
5. Improvement requested, and whether you would use it again.

The prior project history says Kiro was used, but **do not claim Kiro Crew was used** without proof of that distinct product. Only select the AWS Builder mini-challenge if documented qualifying usage exists. The Open Source mini-challenge requires a qualifying additional contribution and its links; this repo alone does not automatically meet that distinct requirement.

## Submission text
Use [Devpost entry draft](devpost-submission-draft.md), adapting its tense to what the recorded demo actually proves. Required: project title, English text description, qualifying primary track, code URL, actual running demo video, exact integrations claimed, and honest product feedback. Confirm form completion and receipt. Repository: https://github.com/interplanetarysister/AmazonHackathon

## Final protocol
1. Finish and run tests, then fix every failure before video recording.
2. Verify an independent MCP client or clearly disclose that limitation.
3. Capture actual app and core five workflows in under three minutes.
4. Verify links from a signed-out viewer; fill Devpost fields.
5. Submit **before** October 23 noon PDT. Freeze repo/video/entry after the official deadline.
6. **No Kiro credit spent, no paid hosting, no fabricated Ring/Alexa/Vega integration.**

## Android Termux judge option (confirmed by project owner on October 20)

For judges viewing and running the project on an Android phone with Termux, the project owner successfully used this alternative to the standard Linux virtual-environment setup:

```sh
pkg update -y
pkg install python git -y
cd ~/AmazonHackathon
python -m unittest discover -s tests -v
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

Open **http://127.0.0.1:8000** in the Android browser on the same phone. Change `cd ~/AmazonHackathon` if the repository is located elsewhere. This route presumes FastAPI, Uvicorn and their dependencies are already installed (as on the owner's device); if missing, use `python -m pip install -r requirements.txt` and troubleshoot Termux/Pydantic compatibility as needed. `pkg` commands belong in native Termux, not inside a proot Ubuntu shell. Keep the terminal/server open while browsing. The demo has no authentication, so do **not** bind it to a public interface. This is a user-reported successful Termux launch, not an independently verified clean-room install on every Android device.
