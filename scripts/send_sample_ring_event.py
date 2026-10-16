"""Send ONE explicitly synthetic, HMAC-signed Ring-format event to LOCAL demo.

Never represents a real Ring event or a Ring developer Playground call.
Set DG_RING_HMAC_KEY on this process and on the running local server.
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from urllib.request import Request, urlopen

secret = os.environ.get("DG_RING_HMAC_KEY", "")
if not secret:
    sys.exit("DG_RING_HMAC_KEY must be set for this local demo. Never commit real secrets.")
now = datetime.now(timezone.utc).isoformat()
payload = {"meta": {"version": "1.1", "time": now,
                    "request_id": "synthetic-demo-" + str(uuid.uuid4())},
           "data": {"id": "sample-event", "type": "motion_detected",
                    "attributes": {"sub_type": "motion", "source": "synthetic-not-a-device"}}}
raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
signature = "sha256=" + hmac.new(secret.encode(), raw, hashlib.sha256).hexdigest()
req = Request("http://127.0.0.1:8000/webhooks/ring", data=raw,
              headers={"Content-Type": "application/json", "X-Signature": signature}, method="POST")
with urlopen(req, timeout=5) as response:
    print("Local signed synthetic Ring-format event response:", response.status)
    print(response.read().decode())
print("This is NOT real Ring hardware, Ring Playground, or Ring account data.")