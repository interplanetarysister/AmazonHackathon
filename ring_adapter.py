"""Verified-shape Ring webhook inbox for local demo and future authorized integration.

The test harness signs synthetic events using a locally selected key. Only the
actual production/partner Ring webhook signing key can authenticate a Ring sender.
No event proves a package was delivered; event association always needs a user.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from typing import Any


def ensure_ring_schema(con: sqlite3.Connection) -> None:
    con.execute("""CREATE TABLE IF NOT EXISTS ring_events (
        id TEXT PRIMARY KEY, request_id TEXT NOT NULL UNIQUE,
        event_type TEXT NOT NULL, subtype TEXT NOT NULL,
        observed_at TEXT NOT NULL, received_at TEXT NOT NULL,
        linked_delivery_id TEXT, source TEXT NOT NULL
    )""")


def verify_signature(secret: str, body: bytes, signature: str) -> bool:
    if not secret or len(body) > 32768 or not signature.startswith("sha256="):
        return False
    expected = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    received = signature[len("sha256="):]
    return len(received) == 64 and hmac.compare_digest(expected, received)


def _field(x: Any, limit: int = 120) -> str:
    if not isinstance(x, str) or not x or len(x) > limit:
        raise ValueError("Invalid or missing Ring event field")
    return x


def store_ring_event(con: sqlite3.Connection, payload: dict[str, Any], now: str) -> dict[str, Any]:
    if not isinstance(payload, dict) or not isinstance(payload.get("meta"), dict) or not isinstance(payload.get("data"), dict):
        raise ValueError("Invalid Ring event envelope")
    meta, data = payload["meta"], payload["data"]
    if meta.get("version") != "1.1":
        raise ValueError("Unsupported Ring event envelope version")
    request_id = _field(meta.get("request_id"), 160)
    event_type = _field(data.get("type"), 60)
    if event_type not in {"motion_detected", "button_press"}:
        return {"status": "ignored", "reason": "Not a doorstep event"}
    attributes = data.get("attributes", {})
    if not isinstance(attributes, dict):
        raise ValueError("Invalid Ring attributes")
    subtype = attributes.get("sub_type", "unspecified")
    if not isinstance(subtype, str) or len(subtype) > 60:
        raise ValueError("Invalid Ring event subtype")
    # Do not persist Ring account IDs, device IDs, images, full webhook content,
    # shipping addresses or other potentially identifying information.
    ensure_ring_schema(con)
    row = con.execute("SELECT id FROM ring_events WHERE request_id=?", (request_id,)).fetchone()
    if row:
        return {"status": "duplicate", "event_id": row[0]}
    event_id = str(uuid.uuid4())
    observed_at = _field(meta.get("time"), 100)
    try:
        parsed = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("Event time must specify a time zone")
    except ValueError as exc:
        raise ValueError("Invalid Ring event time") from exc
    # Ring's device event time is attributes.timestamp (milliseconds since epoch).
    # meta.time marks the event envelope; fall back to it for older synthetic fixtures.
    device_timestamp = attributes.get("timestamp")
    if device_timestamp is not None:
        if isinstance(device_timestamp, bool) or not isinstance(device_timestamp, (int, float)) or \
                not 1262304000000 <= device_timestamp <= 4102444800000:
            raise ValueError("Invalid Ring device event timestamp")
        observed_at = datetime.fromtimestamp(device_timestamp / 1000, tz=timezone.utc).isoformat(timespec="milliseconds")
    else:
        observed_at = parsed.astimezone(timezone.utc).isoformat(timespec="microseconds")
    # This is deliberately not labeled confirmed_Ring: tests also generate
    # signed synthetic messages; a signature proves only possession of the key.
    con.execute("""INSERT INTO ring_events VALUES (?,?,?,?,?,?,?,?)""",
                (event_id, request_id, event_type, subtype, observed_at, now,
                 None, "valid_hmac_ring_format_sender_unverified"))
    return {"status": "stored", "event_id": event_id,
            "note": "Signed Ring-format event. Sender is not independently identified by this local demo."}


def list_ring_events(con: sqlite3.Connection) -> dict[str, Any]:
    ensure_ring_schema(con)
    rows = [dict(row) for row in con.execute(
        "SELECT id, event_type, subtype, observed_at, received_at, linked_delivery_id, source "
        "FROM ring_events ORDER BY received_at DESC LIMIT 100")]
    return {"events": rows, "warning": "This includes locally signed sample payloads; a verified signature alone does not prove actual Ring hardware."}