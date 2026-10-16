"""Delivery Guardian: local-only, stateless MCP Streamable HTTP demo.

Uses only self-contained sample records. Do not expose on a public interface:
there is no authentication or multi-user separation.
"""
from __future__ import annotations

import json
import hashlib
import hmac
import os
import re
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, FileResponse
from ring_adapter import ensure_ring_schema, verify_signature, store_ring_event, list_ring_events

VERSION = "2025-11-25"
DATABASE = os.environ.get("DG_DB_PATH", str(Path(__file__).parent / "delivery-guardian.sqlite3"))
app = FastAPI(title="Delivery Guardian — MCP demo", docs_url=None, redoc_url=None)


def utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def db():
    con = sqlite3.connect(DATABASE, timeout=10)
    con.row_factory = sqlite3.Row
    try:
        con.execute("PRAGMA busy_timeout=10000")
        con.execute("""CREATE TABLE IF NOT EXISTS deliveries (
            id TEXT PRIMARY KEY, label TEXT NOT NULL, carrier TEXT NOT NULL,
            eta TEXT NOT NULL, tracking_hint TEXT NOT NULL, carrier_status TEXT NOT NULL,
            receipt_status TEXT NOT NULL, doorstep_status TEXT NOT NULL,
            source TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS actions (
            id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE, tool TEXT NOT NULL,
            status TEXT NOT NULL, delivery_id TEXT, evidence TEXT NOT NULL,
            created_at TEXT NOT NULL, verified_at TEXT)""")
        con.execute("""CREATE TABLE IF NOT EXISTS evidence (
            id TEXT PRIMARY KEY, delivery_id TEXT NOT NULL, event_type TEXT NOT NULL,
            source TEXT NOT NULL, details TEXT NOT NULL, observed_at TEXT NOT NULL)""")
        con.execute("""CREATE TABLE IF NOT EXISTS delivery_timeline (
            id TEXT PRIMARY KEY, delivery_id TEXT NOT NULL, event_type TEXT NOT NULL,
            source_type TEXT NOT NULL, claimed_at TEXT, recorded_at TEXT NOT NULL,
            details TEXT NOT NULL)""")
        con.commit()
        yield con
        con.commit()
    finally:
        con.close()


def delivery(con, delivery_id: str) -> dict[str, Any]:
    row = con.execute("SELECT * FROM deliveries WHERE id=?", (delivery_id,)).fetchone()
    if not row:
        raise ValueError("Delivery not found")
    return dict(row)


def required_str(a: dict, key: str, max_len: int = 120) -> str:
    val = a.get(key)
    if not isinstance(val, str) or not val.strip() or len(val) > max_len:
        raise ValueError(f"{key} must be text between 1 and {max_len} characters")
    return val.strip()


def optional_str(a: dict, key: str, max_len: int = 120) -> str:
    val = a.get(key, "")
    if not isinstance(val, str) or len(val) > max_len:
        raise ValueError(f"{key} must contain at most {max_len} characters")
    return val.strip()


def add_evidence(con, did: str, event: str, source: str, details: str):
    con.execute("INSERT INTO evidence VALUES (?,?,?,?,?,?)", (str(uuid.uuid4()), did, event, source, details[:300], utc()))


def claimed_timestamp(a: dict, key: str = "claimed_at") -> str | None:
    """Separate a claimed time from when the app actually recorded the claim."""
    value = optional_str(a, key, 50)
    if not value:
        return None
    try:
        date = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if date.tzinfo is None:
            raise ValueError("Time zone required")
        return date.astimezone(timezone.utc).isoformat(timespec="seconds")
    except ValueError as exc:
        raise ValueError(f"{key} must be ISO 8601 with time zone") from exc


def timeline_record(con, did: str, kind: str, source: str, details: str,
                    claimed_at: str | None = None) -> str:
    event_id = str(uuid.uuid4())
    con.execute("INSERT INTO delivery_timeline VALUES (?,?,?,?,?,?,?)",
                (event_id, did, kind, source, claimed_at,
                 datetime.now(timezone.utc).isoformat(timespec="microseconds"), details[:300]))
    return event_id


def resolution_links(carrier: str) -> list[dict[str, str]]:
    """Official provider entry points, never a pretend automatic claim submission."""
    name = carrier.casefold().strip()
    if "ups" in name or "united parcel" in name:
        return [{"label": "Open UPS missing-package claim",
                 "url": "https://www.ups.com/guestclaims/create?loc=en_us",
                 "instructions": "Review the claim form and submit it yourself. A tracking number may be required."}]
    if "fedex" in name or "fed ex" in name:
        return [{"label": "Open FedEx tracking and missing-package report",
                 "url": "https://www.fedex.com/en-us/tracking.html",
                 "instructions": "Enter the tracking number, then Manage Delivery → Report Missing Package."}]
    if "usps" in name or "postal service" in name:
        return [{"label": "Open USPS Missing Mail search",
                 "url": "https://missingmail.usps.com/",
                 "instructions": "USPS generally accepts search requests from seven days after mailing."}]
    if "amazon" in name:
        return [{"label": "Open Amazon Your Orders",
                 "url": "https://www.amazon.com/gp/css/order-history",
                 "instructions": "Select the order, review the delivery details, and contact Amazon support for a missing package."}]
    return []


def mutation(con, name: str, a: dict, work):
    key = required_str(a, "idempotency_key", 100)
    digest = hashlib.sha256(json.dumps({k: v for k, v in a.items() if k != "idempotency_key"},
                                    sort_keys=True).encode()).hexdigest()
    prior = con.execute("SELECT * FROM actions WHERE idempotency_key=?", (key,)).fetchone()
    if prior:
        if prior["tool"] != name or json.loads(prior["evidence"]).get("request_digest") != digest:
            raise ValueError("Idempotency key already used for a different request")
        return {"action_id": prior["id"], "status": prior["status"], "replayed": True,
                "evidence": json.loads(prior["evidence"])}
    aid = str(uuid.uuid4())
    did, details, check = work()
    con.commit()  # The record must be durably saved before DoneProof checks it.
    confirmed = bool(check())
    status = "verified" if confirmed else "needs_review"
    proof = {"scope": "local database state", "read_after_write": confirmed,
             "source": details, "request_digest": digest,
             "note": "This verifies stored app data, not physical delivery."}
    con.execute("INSERT INTO actions VALUES (?,?,?,?,?,?,?,?)",
                (aid, key, name, status, did, json.dumps(proof), utc(), utc() if confirmed else None))
    return {"action_id": aid, "delivery_id": did, "status": status, "evidence": proof, "replayed": False}


def failed_action(tool: str, error: str) -> str:
    """Persist a sanitized failed mutation, without private arguments."""
    aid = str(uuid.uuid4())
    with db() as con:
        con.execute("INSERT INTO actions VALUES (?,?,?,?,?,?,?,?)",
            (aid, None, tool, "failed", None,
             json.dumps({"scope": "local execution", "error": error[:180],
                         "note": "No completed action was verified."}), utc(), None))
    return aid


def parse_notice(raw: str) -> dict[str, Any]:
    """Extract only explicit sample notice fields. No AI or carrier verification."""
    found: dict[str, str] = {}
    patterns = {
        "label": r"(?:item|package|product|order item)\s*:\s*(.+)",
        "carrier": r"(?:carrier|courier|shipped via)\s*:\s*(.+)",
        "eta": r"(?:estimated delivery|expected arrival|delivery date|eta)\s*:\s*(.+)",
    }
    for key, pattern in patterns.items():
        match = re.search(r"^\s*" + pattern + r"\s*$", raw, flags=re.IGNORECASE | re.MULTILINE)
        if match:
            found[key] = match.group(1).strip()[:120]
    return {"fields": found, "missing": [k for k in patterns if k not in found],
            "source": "user_pasted_text_not_verified", "needs_review": True,
            "notice": "Review and correct every extracted field before saving; no carrier API was consulted."}


def plan_delivery_question(question: str) -> dict[str, Any]:
    """Rule-based, read-only intent routing. Never present as a generative AI model."""
    q = question.casefold()
    if re.search(r"\b(missing|lost|not received|not arrived|never arrived|didn.t arrive|can.t find|wasn.t delivered|not here|didn.t show up|report.*package)\b", q):
        intent = "resolve_missing"
        calls = ["get_delivery", "get_delivery_timeline", "find_delivery_issues", "prepare_resolution_steps"]
    elif re.search(r"\b(proof|verify|verified|action|audit|failure|failed|what changed)\b", q):
        intent = "check_proof"
        calls = ["list_actions"]
    elif re.search(r"\b(doorstep|camera|ring|timeline|timestamp|evidence|when|footage|motion)\b", q):
        intent = "review_timeline"
        calls = ["get_delivery", "get_delivery_timeline"]
    elif re.search(r"\b(today|arriving|due|expected|upcoming|all packages|all deliveries)\b", q):
        intent = "check_upcoming"
        calls = ["list_deliveries"]
    elif re.search(r"\b(where|status|track|delivered|received|package|shipment|delivery)\b", q):
        intent = "check_status"
        calls = ["get_delivery", "get_delivery_timeline"]
    else:
        intent = "clarify"
        calls = []
    return {"intent": intent, "planned_tools": calls,
            "method": "deterministic_keyword_routing_not_generative_ai",
            "requires_user_confirmation_for_changes": True,
            "description": "Read-only plan. No changes, claims or provider messages have been sent.",
            "suggestions": ["Where is my package?", "It says delivered but I can't find it",
                            "Show my delivery evidence", "Show verified actions"]}


def execute(name: str, a: dict) -> dict[str, Any]:
    if name == "plan_delivery_question":
        return plan_delivery_question(required_str(a, "question", 500))
    if name == "parse_delivery_notice":
        raw = required_str(a, "text", 3000)
        return parse_notice(raw)
    with db() as con:
        if name == "import_delivery_notice":
            label = required_str(a, "label")
            carrier = required_str(a, "carrier", 40)
            eta = required_str(a, "eta", 60)
            hint = optional_str(a, "tracking_hint", 30)
            if hint and not re.fullmatch(r"[A-Za-z0-9*#-]+", hint):
                raise ValueError("Use a redacted tracking hint, not a full private tracking number")
            did = str(uuid.uuid4())
            def work():
                now = utc()
                con.execute("INSERT INTO deliveries VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                            (did, label, carrier, eta, hint, "expected", "unknown", "unknown", "user_entered", now, now))
                add_evidence(con, did, "import", "user_entered", "Fields confirmed by user; not carrier verified")
                timeline_record(con, did, "arrival_estimate_recorded", "user_entered", eta)
                return did, "User-entered delivery record", lambda: con.execute("SELECT label FROM deliveries WHERE id=?", (did,)).fetchone()[0] == label
            return mutation(con, name, a, work)

        if name == "list_deliveries":
            return {"deliveries": [dict(r) for r in con.execute("SELECT * FROM deliveries ORDER BY created_at DESC LIMIT 100")]}

        if name == "get_delivery":
            did = required_str(a, "delivery_id", 80)
            return {"delivery": delivery(con, did), "evidence": [dict(r) for r in con.execute(
                "SELECT * FROM evidence WHERE delivery_id=? ORDER BY observed_at", (did,))]}

        if name == "get_action_proof":
            aid = required_str(a, "action_id", 80)
            record = con.execute("SELECT * FROM actions WHERE id=?", (aid,)).fetchone()
            if not record:
                raise ValueError("Action not found")
            data = dict(record)
            data["evidence"] = json.loads(data["evidence"])
            return {"action": data}

        if name == "update_carrier_status":
            did = required_str(a, "delivery_id", 80)
            status = required_str(a, "status", 40)
            if status not in {"expected", "in_transit", "out_for_delivery", "marked_delivered", "exception"}:
                raise ValueError("Unsupported carrier status")
            # Operator-entered provider claim: the software does not have live carrier access.
            carrier_claim_time = claimed_timestamp(a)
            def work():
                delivery(con, did)
                con.execute("UPDATE deliveries SET carrier_status=?, updated_at=? WHERE id=?", (status, utc(), did))
                add_evidence(con, did, "carrier_status", "demo_manual_status", status)
                timeline_record(con, did, "carrier_" + status, "demo_manual_status",
                                "Manually transcribed claim; no carrier API verification", carrier_claim_time)
                return did, "Manually entered carrier claim (not live carrier API)", lambda: delivery(con, did)["carrier_status"] == status
            return mutation(con, name, a, work)

        if name == "correct_delivery_eta":
            did = required_str(a, "delivery_id", 80)
            new_eta = required_str(a, "eta", 60)
            def work():
                previous = delivery(con, did)["eta"]
                con.execute("UPDATE deliveries SET eta=?, updated_at=? WHERE id=?", (new_eta, utc(), did))
                add_evidence(con, did, "eta_correction", "user_correction", "ETA corrected by user; earlier value was: " + previous)
                timeline_record(con, did, "arrival_estimate_corrected", "user_correction",
                                "Previous: " + previous + " | New: " + new_eta)
                return did, "User corrected expected arrival, not carrier confirmed", lambda: delivery(con, did)["eta"] == new_eta
            return mutation(con, name, a, work)

        if name == "confirm_delivery_receipt":
            did = required_str(a, "delivery_id", 80)
            status = required_str(a, "status", 40)
            if status not in {"user_confirmed_received", "user_reported_missing"}:
                raise ValueError("Status requires user confirmation")
            def work():
                delivery(con, did)
                con.execute("UPDATE deliveries SET receipt_status=?, updated_at=? WHERE id=?", (status, utc(), did))
                add_evidence(con, did, "receipt", "user_statement", status)
                timeline_record(con, did, status, "user_statement", "Recorded when the person pressed the button")
                return did, "User statement", lambda: delivery(con, did)["receipt_status"] == status
            return mutation(con, name, a, work)

        if name == "record_doorstep_event":
            did = required_str(a, "delivery_id", 80)
            event = required_str(a, "event", 40)
            if event not in {"motion", "package_like_activity", "doorbell"}:
                raise ValueError("Unsupported event type")
            # No real Ring API credentials or live-device source accepted in P0.
            def work():
                delivery(con, did)
                con.execute("UPDATE deliveries SET doorstep_status=?, updated_at=? WHERE id=?", ("demo_event_observed", utc(), did))
                add_evidence(con, did, event, "local_fixture_not_ring", "Demonstration event; no camera consulted")
                timeline_record(con, did, "sample_doorstep_event", "local_fixture_not_ring", event)
                return did, "Local fixture only, NOT Ring evidence", lambda: delivery(con, did)["doorstep_status"] == "demo_event_observed"
            return mutation(con, name, a, work)

        if name == "record_package_sighting":
            did = required_str(a, "delivery_id", 80)
            observed = claimed_timestamp(a, "observed_at") or utc()
            def work():
                delivery(con, did)
                eid = timeline_record(con, did, "package_seen", "user_statement",
                                      "Person reports seeing a package; not camera confirmed", observed)
                return did, "User-reported package sighting, not verified by Ring", \
                    lambda: con.execute("SELECT id FROM delivery_timeline WHERE id=?", (eid,)).fetchone() is not None
            return mutation(con, name, a, work)

        if name == "get_delivery_timeline":
            did = required_str(a, "delivery_id", 80)
            delivery(con, did)
            events = [dict(r) for r in con.execute(
                "SELECT id, event_type, source_type, claimed_at, recorded_at, details "
                "FROM delivery_timeline WHERE delivery_id=? ORDER BY recorded_at, rowid", (did,))]
            ensure_ring_schema(con)
            for row in con.execute(
                "SELECT id, event_type, subtype, observed_at, received_at, source "
                "FROM ring_events WHERE linked_delivery_id=?", (did,)):
                events.append({"id": row["id"], "event_type": "ring_" + row["event_type"],
                               "source_type": row["source"], "claimed_at": row["observed_at"],
                               "recorded_at": row["received_at"],
                               "details": "Signed Ring-format event (" + row["subtype"] + "); sender unverified"})
            events.sort(key=lambda e: (e["recorded_at"], e["id"]))
            return {"delivery_id": did, "events": events,
                    "explanation": "Claimed time is not verification. Recorded time is when the app received the entry. "
                    "Ring-format source is not guaranteed genuine until an approved integration authenticates it."}

        if name == "list_actions":
            rows = [dict(r) for r in con.execute("SELECT * FROM actions ORDER BY created_at DESC, rowid DESC LIMIT 30")]
            for entry in rows:
                entry["evidence"] = json.loads(entry["evidence"])
            return {"actions": rows}

        if name == "list_ring_events":
            return list_ring_events(con)

        if name == "attach_ring_event":
            did = required_str(a, "delivery_id", 80)
            event_id = required_str(a, "event_id", 80)
            def work():
                delivery(con, did)
                ensure_ring_schema(con)
                row = con.execute("SELECT * FROM ring_events WHERE id=?", (event_id,)).fetchone()
                if row is None:
                    raise ValueError("Ring-format event not found")
                if row["linked_delivery_id"] not in (None, did):
                    raise ValueError("Event has already been linked to a different delivery")
                con.execute("UPDATE ring_events SET linked_delivery_id=? WHERE id=?", (did, event_id))
                con.execute("UPDATE deliveries SET doorstep_status=?, updated_at=? WHERE id=?",
                            ("signed_event_linked", utc(), did))
                add_evidence(con, did, row["event_type"], "signed_ring_format_unconfirmed_source",
                             "User associated a signed Ring-format event. Not evidence of a package or receipt.")
                return did, "User-linked signed event; Ring origin not independently established", \
                    lambda: con.execute("SELECT linked_delivery_id FROM ring_events WHERE id=?", (event_id,)).fetchone()[0] == did
            return mutation(con, name, a, work)

        if name == "find_delivery_issues":
            records = [dict(r) for r in con.execute("SELECT * FROM deliveries ORDER BY created_at DESC")]
            issues = [{"delivery_id": d["id"], "label": d["label"], "reason": "Carrier status entered as delivered; user reports not received",
                       "certainty": "unresolved; not evidence of theft"} for d in records
                      if d["carrier_status"] == "marked_delivered" and d["receipt_status"] == "user_reported_missing"]
            return {"issues": issues}

        if name == "prepare_resolution_steps":
            did = required_str(a, "delivery_id", 80)
            d = delivery(con, did)
            return {"delivery_id": did, "steps": ["Check the delivery location and ask others at the address.",
                "Review the retailer's actual order details and delivery notice.",
                "Contact the seller or carrier through their official support channel.",
                "Keep the order confirmation and report your missing-package concern if needed."],
                "warning": "Guidance only; no complaint or refund request has been submitted.",
                "current_claim": d["carrier_status"], "user_receipt": d["receipt_status"],
                "resolution_links": resolution_links(d["carrier"]),
                "support_message_draft": (
                    "Hello, I need assistance locating my shipment. "
                    "The package is listed as: " + d["label"][:120] + ". "
                    "The carrier is " + d["carrier"][:40] + ". "
                    "The carrier status entered into my record is " + d["carrier_status"].replace("_", " ") + ". "
                    "My receipt status is " + d["receipt_status"].replace("_", " ") + ". "
                    "Please check the delivery scan and help me confirm the actual delivery or next steps. "
                    "I can supply order details privately through your official support channel."
                )}

        raise ValueError("Unknown tool")


TOOL_INPUTS = {
    "plan_delivery_question": ({"question": "string"}, ["question"]),
    "parse_delivery_notice": ({"text": "string"}, ["text"]),
    "correct_delivery_eta": ({"delivery_id": "string", "eta": "string", "idempotency_key": "string"}, ["delivery_id", "eta", "idempotency_key"]),
    "import_delivery_notice": ({"label": "string", "carrier": "string", "eta": "string", "tracking_hint": "string", "idempotency_key": "string"}, ["label", "carrier", "eta", "idempotency_key"]),
    "list_deliveries": ({}, []),
    "get_delivery": ({"delivery_id": "string"}, ["delivery_id"]),
    "get_action_proof": ({"action_id": "string"}, ["action_id"]),
    "update_carrier_status": ({"delivery_id": "string", "status": "string", "claimed_at": "string", "idempotency_key": "string"}, ["delivery_id", "status", "idempotency_key"]),
    "confirm_delivery_receipt": ({"delivery_id": "string", "status": "string", "idempotency_key": "string"}, ["delivery_id", "status", "idempotency_key"]),
    "record_doorstep_event": ({"delivery_id": "string", "event": "string", "idempotency_key": "string"}, ["delivery_id", "event", "idempotency_key"]),
    "find_delivery_issues": ({}, []),
    "record_package_sighting": ({"delivery_id": "string", "observed_at": "string", "idempotency_key": "string"}, ["delivery_id", "idempotency_key"]),
    "get_delivery_timeline": ({"delivery_id": "string"}, ["delivery_id"]),
    "list_actions": ({}, []),
    "list_ring_events": ({}, []),
    "attach_ring_event": ({"delivery_id": "string", "event_id": "string", "idempotency_key": "string"}, ["delivery_id", "event_id", "idempotency_key"]),
    "prepare_resolution_steps": ({"delivery_id": "string"}, ["delivery_id"]),
}


def jsonrpc_result(id_: Any, result: dict):
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def jsonrpc_error(id_: Any, code: int, message: str):
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "web" / "index.html", media_type="text/html")


@app.get("/health")
def health():
    return {"status": "ok", "mode": "local_demo", "mcp_protocol": VERSION}


@app.get("/mcp")
def no_stream():
    return Response(status_code=405, headers={"Allow": "POST"})


@app.post("/mcp")
async def mcp(request: Request):
    origin = request.headers.get("origin")
    if origin:
        url = urlsplit(origin)
        if url.scheme != "http" or url.hostname not in {"localhost", "127.0.0.1", "[::1]"}:
            return JSONResponse({"error": "Invalid origin"}, status_code=403)
    if not "application/json" in request.headers.get("content-type", ""):
        return JSONResponse({"error": "JSON required"}, status_code=415)
    accept = request.headers.get("accept", "")
    if "application/json" not in accept or "text/event-stream" not in accept:
        return JSONResponse({"error": "MCP requires JSON and event-stream Accept types"}, status_code=406)
    if len(await request.body()) > 32768:
        return JSONResponse({"error": "Request too large"}, status_code=413)
    try:
        msg = await request.json()
    except (ValueError, UnicodeError):
        return JSONResponse(jsonrpc_error(None, -32700, "Invalid JSON"), status_code=400)
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        return JSONResponse(jsonrpc_error(None, -32600, "Invalid JSON-RPC request"), status_code=400)
    method = msg["method"]
    if method != "initialize" and request.headers.get("mcp-protocol-version") != VERSION:
        return JSONResponse(jsonrpc_error(msg.get("id"), -32600, "Unsupported or missing MCP protocol version"), status_code=400)
    if "id" not in msg:
        return Response(status_code=202)  # initialization and client notifications are stateless
    ident = msg["id"]
    params = msg.get("params", {})
    if not isinstance(params, dict):
        return JSONResponse(jsonrpc_error(ident, -32602, "Invalid parameters"))
    if method == "initialize":
        if params.get("protocolVersion") != VERSION:
            return JSONResponse(jsonrpc_error(ident, -32602, "Expected protocol version 2025-11-25"))
        result = {"protocolVersion": VERSION, "capabilities": {"tools": {"listChanged": False}},
                  "serverInfo": {"name": "delivery-guardian", "version": "0.1.0"},
                  "instructions": "Local independent demo only; no live carriers or Ring connection."}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": [{"name": name, "description": name.replace("_", " ").capitalize(),
                 "inputSchema": {"type": "object", "properties": {k: {"type": t} for k, t in props.items()},
                                 "required": req, "additionalProperties": False}}
                 for name, (props, req) in TOOL_INPUTS.items()]}
    elif method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        if name not in TOOL_INPUTS or not isinstance(arguments, dict):
            return JSONResponse(jsonrpc_error(ident, -32602, "Unknown tool or invalid arguments"))
        allowed = set(TOOL_INPUTS[name][0])
        if set(arguments) - allowed:
            return JSONResponse(jsonrpc_error(ident, -32602, "Unexpected argument(s)"))
        try:
            output = execute(name, arguments)
            result = {"content": [{"type": "text", "text": json.dumps(output)}], "structuredContent": output, "isError": False}
        except (ValueError, sqlite3.IntegrityError) as exc:
            error = str(exc)
            # Record real failures separately from successful changes. Never store
            # untrusted raw tool arguments (may contain personal information).
            aid = failed_action(name, error) if name in {
                "import_delivery_notice", "update_carrier_status", "correct_delivery_eta",
                "record_doorstep_event", "record_package_sighting", "confirm_delivery_receipt", "attach_ring_event"
            } else None
            result = {"content": [{"type": "text", "text": error}],
                      "structuredContent": {"status": "failed", "action_id": aid, "error": error},
                      "isError": True}
    else:
        return JSONResponse(jsonrpc_error(ident, -32601, "Method not found"))
    return JSONResponse(jsonrpc_result(ident, result))


@app.post("/webhooks/ring")
async def ring_webhook(request: Request):
    """Ring-compatible authenticated webhook inbox; intentionally no account linking."""
    key = os.environ.get("DG_RING_HMAC_KEY", "")
    if not key:
        return JSONResponse({"error": "Ring webhook adapter disabled"}, status_code=503)
    body = await request.body()
    if len(body) > 32768:
        return JSONResponse({"error": "Body too large"}, status_code=413)
    if not verify_signature(key, body, request.headers.get("X-Signature", "")):
        return JSONResponse({"error": "Invalid signature"}, status_code=401)
    try:
        payload = json.loads(body)
        with db() as con:
            result = store_ring_event(con, payload, utc())
        return result
    except (ValueError, TypeError, sqlite3.IntegrityError):
        return JSONResponse({"error": "Invalid Ring-format event payload"}, status_code=422)