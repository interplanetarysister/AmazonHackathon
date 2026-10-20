"""Judge-facing MCP/SQLite integration checks for the five-package demo.

Run alongside existing tests: python -m unittest discover -s tests -v
No network, Amazon account, Ring camera, or paid service required.
"""
import importlib
import os
import tempfile
import unittest

from fastapi.testclient import TestClient


class DemoMCPIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.old_path = os.environ.get("DG_DB_PATH")
        os.environ["DG_DB_PATH"] = os.path.join(self.tmp.name, "judge.sqlite3")
        import app
        self.mod = importlib.reload(app)
        self.client = TestClient(self.mod.app)
        self.sequence = 0

    def tearDown(self):
        self.client.close()
        if self.old_path is None:
            os.environ.pop("DG_DB_PATH", None)
        else:
            os.environ["DG_DB_PATH"] = self.old_path
        self.tmp.cleanup()

    def tool(self, name, **kwargs):
        self.sequence += 1
        result = self.client.post(
            "/mcp",
            headers={
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": "2025-11-25",
            },
            json={
                "jsonrpc": "2.0",
                "id": self.sequence,
                "method": "tools/call",
                "params": {"name": name, "arguments": kwargs},
            },
        )
        self.assertEqual(result.status_code, 200, result.text)
        response = result.json()["result"]
        return response

    def success(self, name, **kwargs):
        result = self.tool(name, **kwargs)
        self.assertFalse(result["isError"], result)
        return result["structuredContent"]

    def test_five_cases_readback_and_demo_namespaces(self):
        first = self.success("seed_demo_logistics", demo_user="judge-alpha")
        self.assertEqual(first["created"], 5)
        self.assertEqual(self.success("seed_demo_logistics", demo_user="judge-alpha")["created"], 0)
        self.assertEqual(self.success("seed_demo_logistics", demo_user="judge-beta")["created"], 5)
        rows = self.success("list_demo_logistics", demo_user="judge-alpha")["cases"]
        self.assertEqual(len(rows), 5)
        self.assertEqual({r["tracking_id"] for r in rows},
                         {"SIM-1001", "SIM-1002", "SIM-1003", "SIM-1004", "SIM-1005"})
        self.assertEqual(len({r["case_type"] for r in rows}), 5)
        self.assertTrue(all(r["evidence_source"] == "synthetic_not_amazon" for r in rows))
        before = self.success("get_demo_logistics", demo_user="judge-beta",
                              tracking_id="SIM-1003")["case"]
        self.assertEqual(before["scan_status"], "exception")
        changed = self.success("update_demo_logistics", demo_user="judge-alpha",
                               tracking_id="SIM-1003", scan_status="located",
                               details="Demo dock located fictional parcel")
        self.assertEqual(changed["status"], "verified")
        self.assertEqual(changed["source"], "synthetic_not_amazon")
        after = self.success("get_demo_logistics", demo_user="judge-alpha",
                             tracking_id="SIM-1003")["case"]
        self.assertEqual(after["scan_status"], "located")
        self.assertEqual(self.success("get_demo_logistics", demo_user="judge-beta",
                                     tracking_id="SIM-1003")["case"]["scan_status"], "exception")
        with TestClient(self.mod.app) as fresh_client:
            # Reopen a new app client and independently read the same SQLite file.
            self.sequence += 1
            reopened = fresh_client.post("/mcp", headers={
                "Accept": "application/json, text/event-stream",
                "MCP-Protocol-Version": "2025-11-25"
            }, json={"jsonrpc": "2.0", "id": self.sequence, "method": "tools/call",
                     "params": {"name": "get_demo_logistics", "arguments": {
                         "demo_user": "judge-alpha", "tracking_id": "SIM-1003"}}})
            self.assertEqual(reopened.json()["result"]["structuredContent"]["case"]["scan_status"], "located")

    def test_invalid_updates_cannot_fake_success(self):
        self.success("seed_demo_logistics", demo_user="judge-alpha")
        invalid = self.tool("update_demo_logistics", demo_user="judge-alpha",
                            tracking_id="SIM-1003", scan_status="stolen",
                            details="Unsupported claim")
        self.assertTrue(invalid["isError"])
        self.assertEqual(invalid["structuredContent"]["status"], "failed")
        missing = self.tool("get_demo_logistics", demo_user="judge-beta",
                            tracking_id="SIM-1003")
        self.assertTrue(missing["isError"])
        current = self.success("get_demo_logistics", demo_user="judge-alpha",
                               tracking_id="SIM-1003")["case"]
        self.assertEqual(current["scan_status"], "exception")


if __name__ == "__main__":
    unittest.main()
