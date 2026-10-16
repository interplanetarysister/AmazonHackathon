"""Run: python -m unittest discover -s tests -v"""
import importlib
import os
import tempfile
import unittest

from fastapi.testclient import TestClient


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["DG_DB_PATH"] = os.path.join(self.tmp.name, "data.sqlite3")
        import app
        importlib.reload(app)
        self.api = app
        self.client = TestClient(app.app)
        self.ident = 0

    def tearDown(self):
        self.client.close()
        self.tmp.cleanup()

    def rpc(self, method, params=None, version=True):
        self.ident += 1
        headers = {"Accept": "application/json, text/event-stream"}
        if version:
            headers["MCP-Protocol-Version"] = "2025-11-25"
        return self.client.post("/mcp", json={"jsonrpc": "2.0", "id": self.ident,
                                "method": method, "params": params or {}}, headers=headers)

    def tool(self, name, **args):
        res = self.rpc("tools/call", {"name": name, "arguments": args})
        self.assertEqual(res.status_code, 200)
        self.assertNotIn("error", res.json())
        result = res.json()["result"]
        self.assertFalse(result.get("isError"), result)
        return result["structuredContent"]

    def create(self):
        return self.tool("import_delivery_notice", label="Books", carrier="Test Carrier",
                         eta="Saturday", idempotency_key="create-1")

    def test_mcp_transport_and_tools(self):
        v = self.rpc("initialize", {"protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}}, version=False)
        self.assertEqual(v.json()["result"]["protocolVersion"], "2025-11-25")
        r = self.rpc("tools/list")
        self.assertGreaterEqual(len(r.json()["result"]["tools"]), 9)
        self.assertEqual(self.client.get("/mcp").status_code, 405)
        self.assertEqual(self.rpc("tools/list", version=False).status_code, 400)
        self.assertEqual(self.client.post("/mcp", headers={"Origin": "https://evil.example", "Accept": "application/json, text/event-stream"}, json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).status_code, 403)
        self.assertEqual(self.client.get("/health").json()["status"], "ok")

    def test_create_persistence_and_idempotence(self):
        item = self.create()
        self.assertEqual(item["status"], "verified")
        self.assertTrue(item["evidence"]["read_after_write"])
        again = self.create()
        self.assertTrue(again["replayed"])
        self.assertEqual(again["action_id"], item["action_id"])
        self.assertEqual(len(self.tool("list_deliveries")["deliveries"]), 1)
        got = self.tool("get_delivery", delivery_id=item["delivery_id"])
        self.assertEqual(got["delivery"]["label"], "Books")
        self.assertTrue(got["evidence"])
        proof = self.tool("get_action_proof", action_id=item["action_id"])
        self.assertEqual(proof["action"]["status"], "verified")

    def test_missing_package_trail(self):
        did = self.create()["delivery_id"]
        self.tool("update_carrier_status", delivery_id=did, status="marked_delivered", idempotency_key="status-1")
        self.tool("record_doorstep_event", delivery_id=did, event="motion", idempotency_key="door-1")
        self.assertEqual(self.tool("find_delivery_issues")["issues"], [])
        self.tool("confirm_delivery_receipt", delivery_id=did, status="user_reported_missing", idempotency_key="receipt-1")
        issue = self.tool("find_delivery_issues")["issues"]
        self.assertEqual(len(issue), 1)
        self.assertIn("not evidence of theft", issue[0]["certainty"])
        data = self.tool("get_delivery", delivery_id=did)
        self.assertEqual(data["delivery"]["doorstep_status"], "demo_event_observed")
        self.assertIn("local_fixture_not_ring", [e["source"] for e in data["evidence"]])
        self.assertIn("no complaint", self.tool("prepare_resolution_steps", delivery_id=did)["warning"])

    def test_failures_do_not_fake_success(self):
        x = self.rpc("tools/call", {"name": "get_delivery", "arguments": {"delivery_id": "missing"}}).json()["result"]
        self.assertTrue(x["isError"])
        self.assertEqual(self.tool("list_deliveries")["deliveries"], [])
        self.create()
        result = self.rpc("tools/call", {"name": "import_delivery_notice", "arguments": {"label": "Not same", "carrier": "Test", "eta": "Now", "idempotency_key": "create-1"}}).json()["result"]
        self.assertTrue(result["isError"])  # key reuse with different data is rejected
        self.assertEqual(len(self.tool("list_deliveries")["deliveries"]), 1)
        bad = self.rpc("tools/call", {"name": "update_carrier_status", "arguments": {"delivery_id": "missing", "status": "stolen", "idempotency_key": "x"}}).json()["result"]
        self.assertTrue(bad["isError"])


if __name__ == "__main__":
    unittest.main()