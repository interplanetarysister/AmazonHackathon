#!/usr/bin/env python3
"""Read-only transport smoke test for the Alexa+ MCP demo.

Start the app locally with:
  uvicorn app:app --host 127.0.0.1 --port 8000
Then:
  python scripts/smoke-alexa-mcp.py
Does not contact Amazon or claim Alexa device integration.
"""
from __future__ import annotations
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = os.environ.get("DG_MCP_BASE", "http://127.0.0.1:8000").rstrip("/")
VERSION = "2025-11-25"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": VERSION,
}

def exchange(method, params=None, number=1):
    message = {"jsonrpc": "2.0", "id": number, "method": method}
    if params is not None:
        message["params"] = params
    request = Request(
        BASE + "/mcp", data=json.dumps(message).encode("utf-8"),
        headers=HEADERS, method="POST"
    )
    with urlopen(request, timeout=10) as response:
        if response.status != 200:
            raise AssertionError(f"{method} unexpected HTTP {response.status}")
        data = json.loads(response.read().decode("utf-8"))
    assert data.get("jsonrpc") == "2.0", data
    assert data.get("id") == number, data
    assert "error" not in data, data
    return data["result"]

def tool(name, arguments=None, number=10):
    answer = exchange("tools/call", {"name": name, "arguments": arguments or {}}, number)
    assert answer.get("isError") is False, answer
    assert isinstance(answer.get("structuredContent"), dict), answer
    return answer["structuredContent"]

def main():
    with urlopen(BASE + "/health", timeout=10) as resp:
        health = json.load(resp)
    assert health.get("mcp_protocol") == VERSION, health
    initialization = exchange("initialize", {
        "protocolVersion": VERSION,
        "capabilities": {},
        "clientInfo": {"name": "guardian-smoke", "version": "1.0"}
    }, 1)
    assert initialization["protocolVersion"] == VERSION, initialization
    assert "tools" in initialization["capabilities"], initialization
    catalog = exchange("tools/list", number=2)["tools"]
    names = {entry["name"] for entry in catalog}
    required = {"seed_demo_logistics", "list_demo_logistics", "get_demo_logistics",
                "update_demo_logistics", "find_delivery_issues", "prepare_resolution_steps",
                "list_ring_events"}
    assert required <= names, sorted(required - names)
    namespace = "alexa-smoke-" + str(os.getpid())
    first = tool("seed_demo_logistics", {"demo_user": namespace}, 3)
    snapshot = tool("list_demo_logistics", {"demo_user": namespace}, 4)
    assert len(snapshot.get("cases", snapshot.get("packages", []))) == 5 or len(
        snapshot.get("rows", [])
    ) == 5, {"first": first, "snapshot": snapshot}
    issues = tool("find_delivery_issues", number=5)
    assert isinstance(issues.get("issues"), list), issues
    ring = tool("list_ring_events", number=6)
    assert isinstance(ring, dict), ring
    print(json.dumps({
        "status": "passed", "scope": "local HTTP MCP app, not Amazon Alexa+ or Ring",
        "protocol": VERSION, "tool_count": len(catalog),
        "five_sample_namespace": namespace, "issue_count": len(issues["issues"])
    }, indent=2))

if __name__ == "__main__":
    try:
        main()
    except (AssertionError, HTTPError, URLError, KeyError, ValueError) as exc:
        print(f"MCP smoke verification failed: {exc}", file=sys.stderr)
        sys.exit(1)
