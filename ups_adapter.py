"""Opt-in official UPS Tracking API client for localhost testing.

Requires UPS_CLIENT_ID, UPS_CLIENT_SECRET and a registered UPS developer application.
No password capture, scraping, persistent access tokens, or raw tracking logging.
The demo is never a multiuser production tracking service.
"""
from __future__ import annotations

import base64
from datetime import datetime
import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import quote


def configured() -> bool:
    return bool(os.getenv("UPS_CLIENT_ID") and os.getenv("UPS_CLIENT_SECRET"))


def tracking_lookup(number: str) -> dict:
    if not isinstance(number, str) or not re.fullmatch(r"[A-Za-z0-9]{7,34}", number):
        raise ValueError("UPS tracking number must contain 7–34 letters and digits")
    client_id = os.environ.get("UPS_CLIENT_ID", "")
    secret = os.environ.get("UPS_CLIENT_SECRET", "")
    if not client_id or not secret:
        raise ValueError("UPS developer credentials are not configured for this local installation")
    environment = os.getenv("UPS_ENVIRONMENT", "sandbox")
    if environment not in {"sandbox", "production"}:
        raise ValueError("Invalid UPS_ENVIRONMENT (use sandbox or production)")
    host = "https://onlinetools.ups.com" if environment == "production" else "https://wwwcie.ups.com"
    auth = base64.b64encode((client_id + ":" + secret).encode()).decode()
    token_req = Request(host + "/security/v1/oauth/token", data=b"grant_type=client_credentials",
                        headers={"Authorization": "Basic " + auth,
                                 "Content-Type": "application/x-www-form-urlencoded",
                                 "x-merchant-id": os.getenv("UPS_MERCHANT_ID", "")},
                        method="POST")
    try:
        with urlopen(token_req, timeout=12) as res:
            payload = json.load(res)
        if not isinstance(payload, dict):
            raise ValueError("UPS OAuth returned malformed data")
        token = payload.get("access_token")
        if not isinstance(token, str) or not token:
            raise ValueError("UPS OAuth did not return an access token")
        track_req = Request(host + "/api/track/v1/details/" + quote(number, safe=""),
                            headers={"Authorization": "Bearer " + token, "transId": "DG-tracking",
                                     "transactionSrc": "DeliveryGuardian", "Accept": "application/json"})
        with urlopen(track_req, timeout=15) as res:
            result = json.load(res)
    except HTTPError as exc:
        raise ValueError("UPS tracking request was rejected (HTTP " + str(exc.code) + ")") from None
    except (URLError, TimeoutError, OSError, json.JSONDecodeError):
        raise ValueError("UPS tracking is temporarily unavailable") from None
    if not isinstance(result, dict):
        raise ValueError("UPS returned malformed tracking data")
    response = result.get("trackResponse")
    if not isinstance(response, dict):
        raise ValueError("UPS returned malformed tracking data")
    shipments = response.get("shipment")
    if not isinstance(shipments, list) or not shipments or not isinstance(shipments[0], dict):
        raise ValueError("UPS returned no matching shipments")
    packages = shipments[0].get("package")
    if not isinstance(packages, list) or not packages or not isinstance(packages[0], dict):
        raise ValueError("UPS returned no package scan details")
    package = packages[0]
    activity = package.get("activity")
    latest = activity[0] if isinstance(activity, list) and activity and isinstance(activity[0], dict) else {}
    current_status = package.get("currentStatus")
    current_status = current_status if isinstance(current_status, dict) else {}
    status_info = latest.get("status")
    status_info = status_info if isinstance(status_info, dict) else {}
    description = current_status.get("description") or status_info.get("description") or "Status unavailable"
    description = str(description)[:130]
    code = str(status_info.get("type") or current_status.get("type") or "").upper()
    status_text = description.lower()
    if code == "D":
        state = "marked_delivered"
    elif code == "X" or any(x in status_text for x in ("exception", "failed", "return", "damage", "undeliver", "not delivered")):
        state = "exception"
    elif code == "O" or "out for delivery" in status_text:
        state = "out_for_delivery"
    elif code in {"I", "P"} or any(x in status_text for x in ("in transit", "on the way", "departed", "arrived", "origin scan")):
        state = "in_transit"
    elif code == "M":
        state = "expected"
    elif "delivered" in status_text:
        state = "marked_delivered"
    else:
        state = "expected"
    when = None
    date, hour, offset = latest.get("date"), latest.get("time"), latest.get("gmtOffset")
    if all(isinstance(v, str) for v in (date, hour, offset)):
        try:
            when = datetime.strptime(date + hour.zfill(6) + offset, "%Y%m%d%H%M%S%z").isoformat()
        except ValueError:
            pass
    return {"provider": "UPS", "environment": environment, "carrier_status": state,
            "status_description": description, "carrier_event_at": when,
            "observed_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "source": "official_ups_tracking_api_" + environment,
            "tracking_hint": number[-4:], "note": "A UPS API scan is a provider claim, not a physical receipt confirmation."}
