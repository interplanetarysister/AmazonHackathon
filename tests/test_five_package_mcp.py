"""End-to-end MCP demo acceptance tests for five independent fictional packages."""
import importlib
import os
import tempfile
import unittest
from fastapi.testclient import TestClient

class FivePackageMCPTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        os.environ["DG_DB_PATH"]=os.path.join(self.temp.name,"test.sqlite3")
        import app
        self.module=importlib.reload(app)
        self.client=TestClient(self.module.app)
        self.counter=0

    def tearDown(self):
        self.client.close()
        self.temp.cleanup()
        os.environ.pop("DG_DB_PATH",None)

    def call(self,name,**arguments):
        self.counter+=1
        response=self.client.post("/mcp",headers={
           "Accept":"application/json, text/event-stream",
           "MCP-Protocol-Version":"2025-11-25"},json={
           "jsonrpc":"2.0","id":self.counter,"method":"tools/call",
           "params":{"name":name,"arguments":arguments}})
        self.assertEqual(response.status_code,200,response.text)
        value=response.json()["result"]
        self.assertFalse(value["isError"],value)
        return value["structuredContent"]

    def test_five_demo_scenarios_over_real_mcp_transport(self):
        first=self.call("seed_demo_logistics",demo_user="judge1")
        self.assertEqual(first["created"],5)
        self.assertEqual(self.call("seed_demo_logistics",demo_user="judge1")["created"],0)
        cases=self.call("list_demo_logistics",demo_user="judge1")["cases"]
        self.assertEqual(len(cases),5)
        self.assertEqual({c["tracking_id"] for c in cases},
                         {"SIM-1001","SIM-1002","SIM-1003","SIM-1004","SIM-1005"})
        self.assertEqual(len({c["case_type"] for c in cases}),5)
        self.assertTrue(all(c["evidence_source"]=="synthetic_not_amazon" for c in cases))
        # Reconciliation represents only a demo database write, never actual carrier delivery.
        resolved=self.call("update_demo_logistics",demo_user="judge1",tracking_id="SIM-1003",
                           scan_status="located",details="Located on mock Truck 15")
        self.assertEqual(resolved["status"],"verified")
        detail=self.call("get_demo_logistics",demo_user="judge1",tracking_id="SIM-1003")
        self.assertEqual(detail["case"]["scan_status"],"located")
        self.assertEqual(detail["case"]["details"],"Located on mock Truck 15")
        # Another visitor gets five separate mock rows, unchanged by visitor one.
        self.assertEqual(self.call("seed_demo_logistics",demo_user="judge2")["created"],5)
        untouched=self.call("get_demo_logistics",demo_user="judge2",tracking_id="SIM-1003")
        self.assertEqual(untouched["case"]["scan_status"],"exception")

    def test_error_does_not_mutate_other_demo_namespace(self):
        self.call("seed_demo_logistics",demo_user="judge1")
        self.counter+=1
        response=self.client.post("/mcp",headers={
            "Accept":"application/json, text/event-stream",
            "MCP-Protocol-Version":"2025-11-25"},json={
            "jsonrpc":"2.0","id":self.counter,"method":"tools/call",
            "params":{"name":"update_demo_logistics","arguments":{
             "demo_user":"judge2","tracking_id":"SIM-1003",
             "scan_status":"located","details":"Unauthorized cross-namespace lookup"}}})
        self.assertTrue(response.json()["result"]["isError"])
        unchanged=self.call("get_demo_logistics",demo_user="judge1",tracking_id="SIM-1003")
        self.assertEqual(unchanged["case"]["scan_status"],"exception")

if __name__=="__main__":
    unittest.main()
