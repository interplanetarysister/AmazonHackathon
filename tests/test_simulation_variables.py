"""Offline tests of the demonstration-only field mapping."""
import unittest
from simulation_variables import simulation_variables, simulation_batch

class SimulationVariablesTests(unittest.TestCase):
    def test_review_flag_and_truthful_sources(self):
        row = {
            "tracking_id": "SIM-1001", "label": "Headphones",
            "facility": "SIM-HUB-A", "truck": "SIM-TRUCK-12",
            "scan_status": "scanned", "scanned_at": "2026-10-20T10:00:00Z",
            "carrier_status": "marked_delivered",
            "receipt_status": "user_reported_missing",
            "evidence_source": "synthetic_not_amazon"
        }
        result = simulation_variables(row)
        self.assertTrue(result["needsReview"])
        self.assertTrue(result["simulationMode"])
        self.assertFalse(result["ringEventVerified"])
        self.assertFalse(result["awsRuntimeIntegrationVerified"])
        self.assertEqual(result["trackingId"], "SIM-1001")

    def test_confirmed_delivery_is_not_missing(self):
        row = {
            "tracking_id": "SIM-1005", "carrier_status": "marked_delivered",
            "receipt_status": "user_confirmed_received",
            "evidence_source": "synthetic_not_amazon"
        }
        self.assertFalse(simulation_variables(row)["needsReview"])

    def test_reject_unverified_or_real_event_claim(self):
        with self.assertRaises(ValueError):
            simulation_variables({"tracking_id": "REAL-123",
                                  "evidence_source": "synthetic_not_amazon"})
        with self.assertRaises(ValueError):
            simulation_batch({"source": "real_aws", "cases": []})

if __name__ == "__main__":
    unittest.main()
