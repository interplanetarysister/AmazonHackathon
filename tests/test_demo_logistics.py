"""Tests for isolated five-package synthetic logistics demo."""
import os
import sqlite3
import tempfile
import unittest
from unittest.mock import patch
from demo_logistics import ensure_schema, seed, list_cases, update_case, get_case

class LogisticsFixtureTests(unittest.TestCase):
    def setUp(self):
        self.con=sqlite3.connect(":memory:")
        self.con.row_factory=sqlite3.Row
        self.con.execute("""CREATE TABLE deliveries(id TEXT PRIMARY KEY,label TEXT,carrier TEXT,eta TEXT,tracking_hint TEXT,carrier_status TEXT,receipt_status TEXT,doorstep_status TEXT,source TEXT,created_at TEXT,updated_at TEXT,direction TEXT NOT NULL DEFAULT 'incoming')""")
        self.con.execute("""CREATE TABLE evidence(id TEXT PRIMARY KEY,delivery_id TEXT,event_type TEXT,source TEXT,details TEXT,observed_at TEXT)""")
    def tearDown(self):
        self.con.close()
    def test_five_independent_cases(self):
        self.assertEqual(seed(self.con,"alice")["created"],5)
        self.assertEqual(seed(self.con,"bob")["created"],5)
        self.assertEqual(seed(self.con,"alice")["created"],0)
        self.assertEqual(len(list_cases(self.con,"alice")["cases"]),5)
        self.assertEqual(len(list_cases(self.con,"bob")["cases"]),5)
        self.assertEqual(len({x["case_type"] for x in list_cases(self.con,"alice")["cases"]}),5)
    def test_mock_push_pull_isolated(self):
        seed(self.con,"alice");seed(self.con,"bob")
        self.assertEqual(update_case(self.con,"alice","SIM-1003","located","Found at dock")["status"],"verified")
        a={x["tracking_id"]:x for x in list_cases(self.con,"alice")["cases"]}
        b={x["tracking_id"]:x for x in list_cases(self.con,"bob")["cases"]}
        self.assertEqual(a["SIM-1003"]["scan_status"],"located")
        self.assertEqual(b["SIM-1003"]["scan_status"],"exception")
    def test_scoped_detail_and_missing_cross_user_record(self):
        seed(self.con,"alice")
        one=get_case(self.con,"alice","SIM-1003")["case"]
        self.assertEqual(one["case_type"],"wrong_truck")
        self.assertEqual(one["source"] if "source" in one else one["evidence_source"],"synthetic_not_amazon")
        with self.assertRaises(ValueError):
            get_case(self.con,"bob","SIM-1003")

    def test_invalid_namespace_and_status(self):
        with self.assertRaises(ValueError): seed(self.con,"../bad")
        seed(self.con,"alice")
        with self.assertRaises(ValueError): update_case(self.con,"alice","SIM-1003","stolen","unsupported")
        with self.assertRaises(ValueError): update_case(self.con,"alice","UNKNOWN","located","not found")

if __name__=="__main__":
    unittest.main()
