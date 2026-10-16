# Delivery Guardian — locally runnable milestone 1

**Independent demo; not an Amazon-supported service.** No Alexa device, carrier account, or Ring camera connects to this prototype. Ring events are explicitly **local fixtures**, never presented as real Ring evidence.

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