"""Presentation variable adapter for synthetic Package P.I. records.

Consumes the existing list_demo_logistics response. Never identifies a fixture as
an authenticated AWS, Ring, carrier, or Amazon Logistics event.
"""
from typing import Any

def simulation_variables(record: dict[str, Any]) -> dict[str, Any]:
    """Build UI/voice-script variables from one SQLite demo logistics row."""
    if not isinstance(record, dict):
        raise TypeError("Expected a demo logistics record")
    tracking = record.get("tracking_id")
    if not isinstance(tracking, str) or not tracking.startswith("SIM-"):
        raise ValueError("Only clearly labeled synthetic demo tracking IDs are accepted")
    if record.get("evidence_source") != "synthetic_not_amazon":
        raise ValueError("Only the explicitly synthetic logistics source is supported")
    carrier_status = record.get("carrier_status", "unknown")
    receipt_status = record.get("receipt_status", "unknown")
    return {
        "trackingId": tracking,
        "packageName": record.get("label", "Demo package"),
        "facilityId": record.get("facility", "unknown"),
        "truckId": record.get("truck", "unknown"),
        "scanStatus": record.get("scan_status", "unknown"),
        "lastScanAt": record.get("scanned_at"),
        "lastUpdatedAt": record.get("last_updated"),
        "carrierReportedStatus": carrier_status,
        "recipientConfirmedStatus": receipt_status,
        "investigationType": record.get("case_type", "unknown"),
        "investigationDetails": record.get("details", ""),
        "needsReview": (
            carrier_status == "marked_delivered"
            and receipt_status != "user_confirmed_received"
        ),
        "source": "synthetic_not_amazon",
        "simulationMode": True,
        "ringEventVerified": False,
        "awsRuntimeIntegrationVerified": False,
        "disclaimer": "Simulated event. Not a real Amazon, Ring, or carrier scan.",
    }

def simulation_batch(api_result: dict[str, Any]) -> list[dict[str, Any]]:
    """Map list_demo_logistics({demo_user}) result into UI variables."""
    if api_result.get("source") != "synthetic_not_amazon":
        raise ValueError("Synthetic dataset source required")
    return [simulation_variables(r) for r in api_result["cases"]]
