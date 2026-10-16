"""Version 2 regressions. Run: python -m unittest discover -s tests -v"""
from __future__ import annotations
import io
import importlib
import json
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient


class Version2Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {"DG_DB_PATH": os.path.join(self.temp.name, "case.sqlite3")})
        self.env.start()
        import app
        self.api = importlib.reload(app)
        self.http = TestClient(self.api.app)
        self.id = 1000

    def tearDown(self):
        self.http.close()
        self.env.stop()
        self.temp.cleanup()

    def call(self, tool, **kwargs):
        self.id += 1
        res = self.http.post("/mcp", json={"jsonrpc": "2.0", "id": self.id,
                 "method": "tools/call", "params": {"name": tool, "arguments": kwargs}},
                 headers={"Accept": "application/json, text/event-stream",
                          "MCP-Protocol-Version": "2025-11-25"})
        self.assertEqual(res.status_code, 200, res.text)
        payload = res.json()["result"]
        self.assertFalse(payload.get("isError"), payload)
        return payload["structuredContent"]

    def new(self, direction="incoming", carrier="UPS"):
        return self.call("import_delivery_notice", label="Sample book", carrier=carrier,
                         eta="Friday 2pm", direction=direction,
                         idempotency_key="v2-create-"+direction+"-"+carrier)["delivery_id"]

    def test_shipment_directions_are_persistent(self):
        did = self.new(direction="outgoing")
        item = self.call("get_delivery", delivery_id=did)["delivery"]
        self.assertEqual(item["direction"], "outgoing")
        self.assertEqual(self.call("list_deliveries")["deliveries"][0]["direction"], "outgoing")
        self.assertEqual(self.http.get("/health").status_code, 200)

    def test_per_package_notification_preference(self):
        first = self.new()
        other = self.new(carrier="FedEx")
        self.call("set_notification_preference", delivery_id=first, enabled=True,
                  idempotency_key="alert-on")
        result = self.call("get_notification_preferences")["preferences"]
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["delivery_id"], first)
        self.assertEqual(result[0]["enabled"], 1)
        self.assertNotIn(other, [row["delivery_id"] for row in result])
        self.call("set_notification_preference", delivery_id=first, enabled=False,
                  idempotency_key="alert-off")
        result = self.call("get_notification_preferences")["preferences"]
        self.assertEqual(result[0]["enabled"], 0)

    def test_local_email_preview_not_gmail_access(self):
        raw = ("From: example@example.org\nSubject: Shipping notice\n"
               "Content-Type: text/plain\n\n"
               "Item: Sample book\nCarrier: UPS\nETA: Saturday")
        data = self.call("parse_email_notice", text=raw)
        self.assertEqual(data["fields"]["label"], "Sample book")
        self.assertEqual(data["fields"]["carrier"], "UPS")
        self.assertEqual(data["fields"]["eta"], "Saturday")
        self.assertIn("not_gmail_connected", data["source"])
        self.assertEqual(self.call("list_deliveries")["deliveries"], [])

    def test_csv_preview_omits_recipient_and_address(self):
        raw = ("product_title,shipping_company,estimated_delivery,recipient_email,street_address,tracking_number\n"
               "Cookbook,UPS,Monday,private@example.org,123 Private Ave,1Z123456789\n")
        data = self.call("preview_shipping_export", text=raw)
        self.assertEqual(data["rows"][0]["label"], "Cookbook")
        self.assertEqual(data["rows"][0]["carrier"], "UPS")
        self.assertNotIn("private@example.org", json.dumps(data))
        self.assertNotIn("123 Private Ave", json.dumps(data))
        self.assertNotIn("1Z123456789", json.dumps(data))
        self.assertEqual(self.call("list_deliveries")["deliveries"], [])

    def test_missing_package_has_phone_and_first_action(self):
        did = self.new()
        steps = self.call("prepare_resolution_steps", delivery_id=did)
        self.assertEqual(steps["carrier_contact"]["phone"], "18007425877")
        self.assertFalse(steps["first_action"]["done"])
        self.assertIn("newer carrier scan", steps["first_action"]["name"])
        self.assertIn("include", steps["evidence_prompt"].lower())
        self.assertIn("corrected drop-off timestamp", steps["support_message_draft"])
        self.assertIn("ups.com", steps["first_action"]["tracking_url"])

    def test_production_ups_api_requires_real_credentials(self):
        with patch.dict(os.environ, {"UPS_CLIENT_ID": "", "UPS_CLIENT_SECRET": ""}):
            providers = self.call("get_connection_capabilities")["providers"]
            ups = next(p for p in providers if p["name"] == "UPS tracking")
            self.assertEqual(ups["state"], "requires_developer_credentials")
            self.assertFalse(ups["can_link_consumer_account"])
            error = self.http.post("/mcp", json={
                "jsonrpc":"2.0","id":999,"method":"tools/call",
                "params":{"name":"check_ups_tracking","arguments":{"tracking_number":"1Z1234567891012345"}}},
                headers={"Accept":"application/json, text/event-stream",
                         "MCP-Protocol-Version":"2025-11-25"}).json()["result"]
            self.assertTrue(error["isError"])

    def test_ups_api_response_can_sync_without_real_network(self):
        did = self.new()
        sample = {"carrier_status": "marked_delivered", "status_description": "Delivered at front door",
                  "environment": "sandbox", "carrier_event_at": "2026-10-16T15:30:00+00:00",
                  "source": "official_ups_tracking_api_sandbox"}
        with patch("app.tracking_lookup", return_value=sample) as tracked:
            result = self.call("sync_ups_tracking", delivery_id=did,
                tracking_number="1Z1234567891012345", idempotency_key="ups-sync")
            self.assertEqual(result["status"], "verified")
            tracked.assert_called_once_with("1Z1234567891012345")
        timeline = self.call("get_delivery_timeline", delivery_id=did)["events"]
        api_events = [e for e in timeline if e["event_type"] == "ups_tracking_scan"]
        self.assertEqual(len(api_events), 1)
        self.assertEqual(api_events[0]["claimed_at"], sample["carrier_event_at"])
        self.assertIn("official_ups_tracking_api_sandbox", api_events[0]["source_type"])
        summary = self.call("prepare_resolution_steps", delivery_id=did)
        self.assertTrue(summary["first_action"]["done"])
        self.assertIsNotNone(summary["first_action"]["checked_at"])

    def test_original_record_migrates_for_direction(self):
        database = os.environ["DG_DB_PATH"]
        with sqlite3.connect(database) as con:
            con.execute("""CREATE TABLE deliveries (
                id TEXT PRIMARY KEY, label TEXT NOT NULL, carrier TEXT NOT NULL,
                eta TEXT NOT NULL, tracking_hint TEXT NOT NULL, carrier_status TEXT NOT NULL,
                receipt_status TEXT NOT NULL, doorstep_status TEXT NOT NULL,
                source TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL)""")
            con.execute("INSERT INTO deliveries VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                        ("old", "Legacy", "UPS", "Tomorrow", "", "expected",
                         "unknown", "unknown", "user_entered", "2026-10-16", "2026-10-16"))
        item = self.call("get_delivery", delivery_id="old")["delivery"]
        self.assertEqual(item["direction"], "incoming")

    def test_v2_routes_and_assets(self):
        for route in ["/", "/v2.js", "/notify-sw.js"]:
            response=self.http.get(route)
            self.assertEqual(response.status_code,200,route)
        html=self.http.get("/").text
        for item in ('id="csv-file"','id="eml-file"','id="ups-number"',
                     'id="v2-camera-file"','id="v2-zip"','id="v2-alert-enabled"'):
            self.assertIn(item,html)
        self.assertIn("selectedClip.arrayBuffer()",self.http.get("/v2.js").text)
        self.assertIn("showNotification",self.http.get("/v2.js").text)

    def test_ups_adapter_safely_parses_mock_api_response(self):
        from ups_adapter import tracking_lookup
        class FakeResponse:
            def __init__(self,content):
                self.stream = io.BytesIO(json.dumps(content).encode())
            def read(self,n=-1):
                return self.stream.read(n)
            def __enter__(self):
                return self
            def __exit__(self,*args):
                return None
        token = {"access_token":"not-a-real-token"}
        scan = {"trackResponse":{"shipment":[{"package":[{
            "currentStatus":{"description":"Delivered"},
            "activity":[{"date":"20261016","time":"152430","gmtOffset":"+00:00",
                         "status":{"description":"Delivered","type":"D"}}]}]}]}}
        with patch.dict(os.environ, {"UPS_CLIENT_ID":"test-id","UPS_CLIENT_SECRET":"test-secret",
                                    "UPS_ENVIRONMENT":"sandbox"}), \
             patch("ups_adapter.urlopen",side_effect=[FakeResponse(token),FakeResponse(scan)]) as opened:
            result=tracking_lookup("1Z1234567891012345")
        self.assertEqual(result["carrier_status"],"marked_delivered")
        self.assertEqual(result["carrier_event_at"],"2026-10-16T15:24:30+00:00")
        self.assertEqual(result["environment"],"sandbox")
        self.assertEqual(opened.call_count,2)


if __name__ == "__main__":
    unittest.main()
