# Delivery Guardian — locally runnable milestone 1

**Independent demo; not an Amazon-supported service.** No Alexa device, carrier account, or Ring camera connects to this prototype. Ring events are explicitly **local fixtures**, never presented as real Ring evidence.

## Dependency installation

Use Python 3.11–3.13 where available. Run `python -m pip install -r requirements.txt` to install FastAPI, Uvicorn, HTTPX, Starlette, Pydantic and their automatically resolved dependencies, including pydantic-core. Run `python -m pip check` before tests. Native Termux Python 3.14 may fail to build pydantic-core; use a supported Linux Python environment rather than installing individual packages with `--no-deps`.

## Start (Python 3.11+)

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
uvicorn app:app --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000` on the *same* device running the server. On Termux Ubuntu, run inside Ubuntu; open the address in your Android browser. Keep it bound to localhost. An external phone cannot connect to a desktop's localhost.

## Live proof walkthrough

1. Load example → creates a database-backed delivery and *independently reads it back*.
2. Carrier says delivered → records a **manually entered claim**, not a live carrier API result.
3. Add sample doorstep event → creates **local fixture** evidence, not Ring evidence.
4. I can't find it → reports user testimony and flags a mismatch; it does not assert theft.
5. What should I do? → local guidance; no claims/contacts were sent.
6. Test a failing action → the real MCP tool returns `isError: true`, and the UI does not report success.
7. Refresh page → deliveries and proof records remain in SQLite.

The page executes actual MCP `initialize`, `tools/list` and `tools/call` over stateless Streamable HTTP `POST /mcp` using protocol version `2025-11-25`. Server supports JSON responses and responds `405` to unsupported GET streaming. Tools use JSON-RPC 2.0. This is a small self-contained implementation of the specified protocol (not the official SDK); compatibility must still be validated with a second independent MCP client before final submission.

`DG_DB_PATH=/tmp/demo.sqlite3` can override the storage location. Delete the database file to reset the demo. The server has **no authentication or multi-user separation**: it is NOT safe for internet deployment. Never enter real tracking numbers or personal details.

## Future work

Before submission: verify with independent MCP SDK client; ensure clean-room installation and demo under 3 minutes; implement actual Ring Playground adapter only after verifying access/terms. For production: OAuth/account controls, encryption and per-user access control, rate limiting, data deletion, privacy policy, authorized carriers and Ring services. Do not confuse this demo with a launched product.

## Optional Ring-format webhook adapter (actual signature verification, synthetic sender)

The backend now implements `/webhooks/ring` with **raw-body HMAC-SHA256** verification, Ring v1.1 payload validation, deduplication by `meta.request_id`, and a user-controlled inbox. No webhook is accepted without a configured `DG_RING_HMAC_KEY`. For a local demonstration, use **two separate terminals**:

```bash
# Terminal 1: local server with a disposable DEMO-ONLY key
DG_RING_HMAC_KEY=local-demo-secret-change-me uvicorn app:app --host 127.0.0.1 --port 8000

# Terminal 2: send one clearly synthetic signed sample using the same disposable key
DG_RING_HMAC_KEY=local-demo-secret-change-me python scripts/send_sample_ring_event.py
```

Open the browser page, select a saved delivery, choose **Check event inbox**, then **Link to selected delivery**. This changes a real database record and logs a DoneProof verification. The UI must continue to say that a signed Ring-*format* payload does **not** establish that a genuine Ring device or package was detected. No Ring customer account, Ring Playground, webhook subscription, or real camera has been linked. The Ring Playground simulates live view events, but does not necessarily send webhooks to our local server. A real deployment additionally requires partner onboarding, authorized OAuth/account linking, secure HTTPS hosting, a genuine signing key, and per-customer isolation. Never put real keys into source code.

Signed payloads must have `meta.version=1.1`, `meta.request_id`, `meta.time`, and `data.type` equal to `motion_detected` or `button_press`; only their sanitized event type, timestamp and subtype are retained. Webhooks are NOT automatically assigned to a package. User association is explicit. Verification only establishes the signature against the configured key, not the sender's identity in a test environment.

## Current verification record

- Seven `unittest` backend checks pass, including real MCP JSON-RPC POST requests, SQLite persistence/idempotency, incorrect delivery claims, failures saved in DoneProof, and signed Ring-format event/invalid signature/replay handling.
- Chromium browser UI was exercised through a local test bridge against the same FastAPI app: sample save, carrier status, missing report, guidance, failed action, and fresh-page persistence worked without browser JavaScript exceptions.
- **Not yet validated** with a second implementation of the official MCP SDK, a Ring Playground account, public URL, or actual carriers. Do not label the adapter as a live Ring integration or consumer-ready production service.

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
