# Delivery Guardian — judge-ready local walkthrough (feature-branch draft)

**Scope:** `feat/missing-package-resolution-paths`; this is an independent hackathon demo, not a live Amazon/Alexa+/Ring or carrier-connected application. Before recording, reconcile the owner's newer Termux local UI with this branch, run the test suite, and verify behavior in a real browser.

## Free setup

```sh
git checkout feat/missing-package-resolution-paths
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/verify_client.py
uvicorn app:app --host 127.0.0.1 --port 8000
```

Visit `http://127.0.0.1:8000` on the same machine. A `127.0.0.1` server should not be exposed publicly: there is no user authentication, account isolation or secure credential storage. Don't enter real addresses, private tracking numbers or camera footage.

If preparing a clean demonstration, optionally set `DG_DB_PATH` to a fresh temporary file **before** running the server; do not delete the user's existing local data.

### Three-minute evidence-first video outline

- **0:00–0:15 — Problem:** "A delivery says delivered, but nobody can find it. Carrier timestamps and camera events don't automatically tell a consistent story."
- **0:15–0:35 — Import:** Click **Load example** (creates a synthetic package labeled UPS); show that the record was persisted and the action has a DoneProof ID.
- **0:35–0:55 — Carrier claim:** Enter a clearly sample carrier-claimed time and click **Carrier says delivered**. Show the automatically recorded intake timestamp and separately retained reported time.
- **0:55–1:15 — Missing:** Click **I can't find it**. Show the durable resolution guidance, UPS direct claim form link, and editable support message. No complaint or email is sent by this app.
- **1:15–1:40 — Ask question:** Enter "My package says delivered but I can't find it." Watch the browser call the real MCP `plan_delivery_question`, `get_delivery`, `find_delivery_issues`, and `prepare_resolution_steps`. This is a deterministic keyword planner, not an LLM or connected Alexa+ device.
- **1:40–2:05 — Ring distinction:** Click **Add sample doorstep event**. Show the sample-only provenance and recorded event. If a genuine Ring Playground API call has been separately accomplished, demonstrate it truthfully rather than displaying fake device footage.
- **2:05–2:25 — Evidence:** Read the timeline's actual recorded/claimed timestamps. Click **Save evidence summary** and show the redacted text export.
- **2:25–2:40 — DoneProof:** Click **Test a failing action**; show the failure recorded rather than claimed as done.
- **2:40–2:55 — Persistence:** Refresh the browser and show the package and action ledger still exist; explain that only local database state has been verified.

Actual outcomes and timing must be captured in a real recording, not edited in as fake actions. If anything fails, shorten the script and repair it before submission.

### Browser checks for the owner

1. Open in Termux browser on Android; verify that the correct newest UI is present. Select two deliveries with the *same name and carrier* and confirm the correct row stays highlighted.
2. Tap **I can't find it** and ensure the advice, direct link, and draft remain visible, not merely flashing.
3. Ask all four example questions; each should use real `tools/call` methods and stay readable.
4. Tap the resolution link; it must point at an official carrier page. Check that it **does not** pre-submit a claim.
5. Save evidence; confirm line breaks and local timestamps read properly.
6. Refresh; verify records and proof persist. Test both success and intentionally failed mutations.
7. Run `python scripts/verify_client.py` to validate inline and external JavaScript syntax. This requires Node.js; without it, the script exits with code 2 (`NOT VERIFIED`), not a passing skip.
8. Test both mobile and wide-screen layout, text resizing, button focus, and readable contrast.

### Important submission truth boundaries

- **Amazon branding:** independent 2026 hackathon entry; no partnership or certified "Works with Alexa" claims.
- **Alexa+ route:** local self-hosted MCP + web MCP client only. The actual Alexa+ SDK is gated. The tools are invoked, not merely depicted.
- **Ring:** signed Ring-format fixture/hook is not proof a customer camera was connected or that an event came from real Ring hardware.
- **Carrier:** statuses and times are entered manually. Opening a carrier page is not a filed complaint.
- **DoneProof:** a verified local database write is not a verified real-world delivery.
- **Credentials:** do not expose personal login sessions in the public video.

Official FAQ: https://amazonappdev2026.devpost.com/details/faqs
