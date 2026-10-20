"""Synthetic multi-user logistics fixtures for the Package P.I. hackathon demo.

All IDs, scans and statuses are fictional. No Amazon internal systems are queried.
Demo users are explicit namespaces, NOT authentication identities.
"""
import sqlite3
from datetime import datetime, timezone

SCENARIOS = [
 ("SIM-1001","Headphones — delivered but missing","Example Carrier","marked_delivered","user_reported_missing","doorstep_conflict","Marked delivered; recipient reports missing"),
 ("SIM-1002","Medicine — delayed in hub","Example Carrier","exception","unknown","hub_delay","Expected arrival delayed at hub"),
 ("SIM-1003","Laptop — misrouted truck","Example Carrier","in_transit","unknown","wrong_truck","Scanned to incorrect demo truck"),
 ("SIM-1004","Books — video review request","Example Carrier","out_for_delivery","unknown","evidence_request","Recipient requests last known handling evidence"),
 ("SIM-1005","Groceries — confirmed arrival","Example Carrier","marked_delivered","user_confirmed_received","resolved","Delivery confirmed received"),
]

def validate_user(user):
    if not isinstance(user,str) or not (1 <= len(user) <= 40) or not all(c.isalnum() or c in "-_" for c in user):
        raise ValueError("demo_user must be 1-40 letters, numbers, hyphens or underscores")
    return user

def ensure_schema(con):
    con.execute("""CREATE TABLE IF NOT EXISTS demo_logistics (
       demo_user TEXT NOT NULL, tracking_id TEXT NOT NULL, case_type TEXT NOT NULL,
       facility TEXT NOT NULL, truck TEXT NOT NULL, scan_status TEXT NOT NULL,
       scanned_at TEXT NOT NULL, last_updated TEXT NOT NULL,
       evidence_source TEXT NOT NULL, details TEXT NOT NULL,
       PRIMARY KEY(demo_user, tracking_id))""")
    con.execute("""CREATE TABLE IF NOT EXISTS demo_packages (
       demo_user TEXT NOT NULL, tracking_id TEXT NOT NULL, delivery_id TEXT NOT NULL,
       PRIMARY KEY(demo_user, tracking_id))""")

def seed(con, demo_user):
    user=validate_user(demo_user)
    ensure_schema(con)
    existing=con.execute("SELECT COUNT(*) FROM demo_packages WHERE demo_user=?",(user,)).fetchone()[0]
    if existing:
        return {"demo_user":user,"created":0,"existing":existing,"note":"Existing scenario records preserved; no duplicate seed"}
    from uuid import uuid4
    now=datetime.now(timezone.utc).isoformat()
    for i,(tracking,label,carrier,status,receipt,case,details) in enumerate(SCENARIOS):
        did=str(uuid4())
        con.execute("""INSERT INTO deliveries VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
          (did,label,carrier,"Demo day "+str(i+1),tracking,status,receipt,
           "demo_event_observed" if i==0 else "unknown","synthetic_demo_fixture",now,now))
        con.execute("INSERT INTO demo_packages VALUES (?,?,?)",(user,tracking,did))
        con.execute("""INSERT INTO demo_logistics VALUES (?,?,?,?,?,?,?,?,?,?)""",
          (user,tracking,case,"SIM-HUB-A","SIM-TRUCK-15" if i==2 else "SIM-TRUCK-12",
           "exception" if i in (1,2) else "scanned",now,now,"synthetic_not_amazon",details))
        con.execute("INSERT INTO evidence VALUES (?,?,?,?,?,?)",
          (str(uuid4()),did,"synthetic_logistics_case","synthetic_not_amazon",details,now))
    return {"demo_user":user,"created":5,"existing":0,"note":"Five fictional tracking scenarios created; not Amazon data"}

def list_cases(con, demo_user):
    user=validate_user(demo_user)
    ensure_schema(con)
    rows=con.execute("""SELECT l.*,p.delivery_id,d.label,d.carrier_status,d.receipt_status
      FROM demo_logistics l JOIN demo_packages p ON p.demo_user=l.demo_user AND p.tracking_id=l.tracking_id
      JOIN deliveries d ON d.id=p.delivery_id WHERE l.demo_user=? ORDER BY l.tracking_id""",(user,)).fetchall()
    return {"demo_user":user,"cases":[dict(r) for r in rows],"source":"synthetic_not_amazon"}

def update_case(con,demo_user,tracking_id,scan_status,details):
    user=validate_user(demo_user)
    if scan_status not in {"scanned","exception","located","reconciled"}:
        raise ValueError("Unsupported mock logistics scan status")
    if not isinstance(details,str) or not 1<=len(details)<=240:
        raise ValueError("details must be 1-240 characters")
    ensure_schema(con)
    now=datetime.now(timezone.utc).isoformat()
    cur=con.execute("""UPDATE demo_logistics SET scan_status=?,details=?,last_updated=?
     WHERE demo_user=? AND tracking_id=?""",(scan_status,details,now,user,tracking_id))
    if cur.rowcount!=1:
        raise ValueError("Demo package not found for this user")
    row=con.execute("SELECT scan_status,details FROM demo_logistics WHERE demo_user=? AND tracking_id=?",(user,tracking_id)).fetchone()
    return {"status":"verified" if row["scan_status"]==scan_status and row["details"]==details else "needs_review",
            "demo_user":user,"tracking_id":tracking_id,"scan_status":scan_status,
            "source":"synthetic_not_amazon","note":"Read-after-write verified only in simulated logistics SQLite database"}
