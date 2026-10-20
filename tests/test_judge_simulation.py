"""Judges' mock account, camera-footage references and local claim workflow."""
import importlib, os, tempfile, unittest
from fastapi.testclient import TestClient

class JudgeSimulationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.old=os.environ.get("DG_DB_PATH")
        os.environ["DG_DB_PATH"]=self.temp.name+"/judge.sqlite3"
        import app
        self.app=importlib.reload(app)
        self.client=TestClient(self.app.app)
        self.ident=0
    def tearDown(self):
        self.client.close()
        if self.old is None:os.environ.pop("DG_DB_PATH",None)
        else:os.environ["DG_DB_PATH"]=self.old
        self.temp.cleanup()
    def call(self,name,**arguments):
        self.ident+=1
        r=self.client.post("/mcp",headers={"Accept":"application/json, text/event-stream","MCP-Protocol-Version":"2025-11-25"},json={"jsonrpc":"2.0","id":self.ident,"method":"tools/call","params":{"name":name,"arguments":arguments}})
        self.assertEqual(r.status_code,200,r.text)
        return r.json()["result"]
    def test_five_cases_mock_inbox_footage_and_claim_persistence(self):
        x=self.call("judge_demo_dashboard")
        self.assertFalse(x["isError"])
        data=x["structuredContent"]
        self.assertEqual(len(data["packages"]),5)
        self.assertEqual(len(data["gmail_inbox"]),5)
        self.assertTrue(all("last_scan" in p for p in data["packages"]))
        self.assertTrue(all(-90 <= p["last_scan"]["latitude"] <= 90 and -180 <= p["last_scan"]["longitude"] <= 180 for p in data["packages"]))
        self.assertTrue(all(p["last_scan"]["meaning"].startswith("fictional") for p in data["packages"]))
        self.assertEqual(data["connections"]["Gmail"],"SIMULATED")
        self.assertEqual(data["connections"]["Blink"],"SIMULATED")
        self.assertEqual({p["carrier"] for p in data["packages"] if p["issue"]=="received"},{"Amazon"})
        self.assertIn("delivery_grabbed",[e["type"] for e in data["packages"][0]["events"]])
        self.assertIn("recorded_missed_delivery_timeslot",[e["type"] for e in data["packages"][1]["events"]])
        self.assertEqual(data["camera_clips"]["theft"]["license"],"CC BY 3.0; attribution required")
        self.assertEqual(self.client.get("/judge.js").status_code,200)
        filed=self.call("judge_demo_claim",case_id="SIM-1001",notes="Demo claim: package missing after carrier scan")
        self.assertEqual(filed["structuredContent"]["status"],"demo_claim_submitted")
        after=self.call("judge_demo_dashboard")["structuredContent"]
        self.assertEqual(after["packages"][0]["claim_status"],"demo_claim_submitted")
        self.assertEqual(after["packages"][0]["claim_notes"],"Demo claim: package missing after carrier scan")
    def test_fictional_claim_does_not_accept_real_submission_or_safe_delivery(self):
        self.assertTrue(self.call("judge_demo_claim",case_id="SIM-1005",notes="unneeded")["isError"])
        self.assertTrue(self.call("judge_demo_claim",case_id="DOES-NOT-EXIST",notes="bad")["isError"])
        self.assertIn('id="judge-load"',self.client.get("/").text)
        self.assertIn('src="/judge.js"',self.client.get("/").text)
        self.assertIn("www.google.com/maps/search/?api=1",self.client.get("/judge.js").text)
if __name__=="__main__":unittest.main()
