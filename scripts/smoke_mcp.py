"""Real HTTP smoke test of a temporary localhost Delivery Guardian MCP process.

Run: python scripts/smoke_mcp.py
Requires dependencies from requirements.txt. Uses a temporary database and no
accounts, paid services, or real tracking data.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def available_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def request_json(url: str, value: dict | None = None, protocol: bool = False) -> dict:
    headers = {"Accept": "application/json, text/event-stream"}
    if protocol:
        headers["MCP-Protocol-Version"] = "2025-11-25"
    data = None if value is None else json.dumps(value).encode("utf-8")
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method="POST" if value else "GET")
    with urlopen(req, timeout=5) as response:
        return json.load(response)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory() as folder:
        port = available_port()
        env = os.environ.copy()
        env["DG_DB_PATH"] = str(Path(folder) / "judge-smoke.sqlite3")
        env.pop("UPS_CLIENT_ID", None)
        env.pop("UPS_CLIENT_SECRET", None)
        env.pop("DG_RING_HMAC_KEY", None)
        process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app:app", "--host", "127.0.0.1",
             "--port", str(port), "--no-access-log"],
            cwd=root, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            text=True,
        )
        try:
            base = f"http://127.0.0.1:{port}"
            for _ in range(70):
                if process.poll() is not None:
                    raise RuntimeError("Temporary MCP server exited before starting")
                try:
                    response = request_json(base + "/health")
                    if response.get("status") == "ok":
                        break
                except (URLError, TimeoutError):
                    time.sleep(0.15)
            else:
                raise TimeoutError("Temporary MCP server did not become healthy")

            seq = 0
            def rpc(method: str, params: dict | None = None, version: bool = True) -> dict:
                nonlocal seq
                seq += 1
                return request_json(base + "/mcp", {
                    "jsonrpc": "2.0", "id": seq, "method": method,
                    "params": params or {}
                }, protocol=version)["result"]

            def tool(name: str, args: dict | None = None) -> dict:
                result = rpc("tools/call", {"name": name, "arguments": args or {}})
                if result.get("isError"):
                    raise AssertionError(name + " failed: " + result["content"][0]["text"])
                return result["structuredContent"]

            init = rpc("initialize", {
                "protocolVersion": "2025-11-25", "capabilities": {},
                "clientInfo": {"name": "standalone-smoke", "version": "2"}
            }, version=False)
            assert init["protocolVersion"] == "2025-11-25"
            names = {t["name"] for t in rpc("tools/list")["tools"]}
            for expected in ("plan_delivery_question", "import_delivery_notice",
                             "get_delivery_timeline", "prepare_resolution_steps",
                             "get_notification_preferences"):
                assert expected in names, expected

            add_args = {"label": "Synthetic sample notebook", "carrier": "UPS",
                        "eta": "Friday 2-5 PM", "direction": "incoming",
                        "idempotency_key": "smoke-create"}
            first = tool("import_delivery_notice", add_args)
            assert first["status"] == "verified", first
            replay = tool("import_delivery_notice", add_args)
            assert replay["replayed"] and replay["action_id"] == first["action_id"]
            did = first["delivery_id"]
            assert tool("get_delivery", {"delivery_id": did})["delivery"]["label"] == add_args["label"]
            tool("update_carrier_status", {"delivery_id": did,
                    "status": "marked_delivered", "idempotency_key": "smoke-status"})
            tool("confirm_delivery_receipt", {"delivery_id": did,
                    "status": "user_reported_missing", "idempotency_key": "smoke-missing"})
            help_info = tool("prepare_resolution_steps", {"delivery_id": did})
            assert not help_info["first_action"]["done"]
            assert help_info["carrier_contact"]["phone"] == "18007425877"
            assert "ups.com" in help_info["resolution_links"][0]["url"]
            assert help_info["support_message_draft"]
            entries = tool("get_delivery_timeline", {"delivery_id": did})["events"]
            assert len(entries) >= 3
            assert any(e["event_type"] == "user_reported_missing" for e in entries)
            plan = tool("plan_delivery_question", {"question": "My package is missing"})
            assert plan["intent"] == "resolve_missing"
            tool("set_notification_preference", {"delivery_id": did, "enabled": True,
                                                  "idempotency_key": "smoke-alert"})
            prefs = tool("get_notification_preferences")["preferences"]
            assert any(x["delivery_id"] == did and x["enabled"] for x in prefs)
            proof = tool("get_action_proof", {"action_id": first["action_id"]})
            assert proof["action"]["status"] == "verified"
            print("PASS: external HTTP MCP initialize/list/call, SQLite persistence, "
                  "idempotency, missing-package resolution, evidence and alert preference.")
            print("PASS: " + str(len(names)) + " MCP tools exposed; all data were synthetic.")
            return 0
        finally:
            process.terminate()
            try:
                process.communicate(timeout=4)
            except subprocess.TimeoutExpired:
                process.kill()
                process.communicate()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        sys.exit(1)
