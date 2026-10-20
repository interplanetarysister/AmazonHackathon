"""Local-only fictional judge services. Stock videos are illustrative, not event evidence."""
from datetime import datetime, timezone
CASES=[
("SIM-1001","Headphones","UPS","marked_delivered","possible_theft","14:08","recorded_delivery","14:13","delivery_grabbed"),
("SIM-1002","Tablet cover","FedEx","marked_delivered","missing_at_dropoff","16:20","recorded_missed_delivery_timeslot","16:20","no_courier_seen"),
("SIM-1003","Laptop stand","USPS","exception","misrouted","09:20","sorting_exception","11:10","still_at_wrong_hub"),
("SIM-1004","Office supplies","UPS","out_for_delivery","late","17:00","recorded_missed_delivery_timeslot","18:00","no_delivery"),
("SIM-1005","Groceries","Amazon","marked_delivered","received","11:55","recorded_delivery","12:00","received"),
]
SUPPORT={"UPS":"https://www.ups.com/us/en/support/file-a-claim","FedEx":"https://www.fedex.com/en-us/customer-support/claims.html","USPS":"https://www.usps.com/help/claims.htm","Amazon":"https://www.amazon.com/gp/css/order-history"}
FOOTAGE={
"delivery":{"url":"https://www.pexels.com/video/a-person-leaving-a-parcel-at-the-door-6667230/","credit":"Kampus Production / Pexels","license":"Pexels free license"},
"received":{"url":"https://www.pexels.com/video/man-delivering-a-parcel-on-doorstep-6715794/","credit":"Kampus Production / Pexels","license":"Pexels free license"},
"pickup":{"url":"https://www.pexels.com/video/woman-picking-up-the-packages-at-door-entrance-6031871/","credit":"ArtHouse Studio / Pexels","license":"Pexels free license"},
"theft":{"url":"https://commons.wikimedia.org/wiki/File:Porch_Pirates.ogv","credit":"nayrproductions / Wikimedia Commons","license":"CC BY 3.0; attribution required"},
}
def initialize(con):
    con.execute("""CREATE TABLE IF NOT EXISTS judge_demo_claims
    (case_id TEXT PRIMARY KEY,status TEXT NOT NULL,notes TEXT NOT NULL,created_at TEXT NOT NULL)""")
def show(con):
    initialize(con)
    saved={x["case_id"]:dict(x) for x in con.execute("SELECT * FROM judge_demo_claims")}
    rows=[]
    inbox=[]
    for ident,item,carrier,status,issue,t1,e1,t2,e2 in CASES:
        rows.append({"id":ident,"label":item,"carrier":carrier,"status":status,"issue":issue,
                     "events":[{"time":t1,"type":e1},{"time":t2,"type":e2}],
                     "claim_status":saved[ident]["status"] if ident in saved else "not_filed",
                     "claim_notes":saved[ident]["notes"] if ident in saved else "",
                     "support_url":SUPPORT[carrier],"demo_only":True})
        inbox.append({"id":"MAIL-"+ident,"from":"simulation@"+carrier.lower()+".example.invalid",
                      "subject":carrier+" shipment notification: "+item,
                      "body":carrier+" reports status "+status.replace("_"," ")+".",
                      "case_id":ident,"synthetic":True})
    return {"packages":rows,"gmail_inbox":inbox,"camera_clips":FOOTAGE,
            "connections":{"Gmail":"SIMULATED","Blink":"SIMULATED","carrier_APIs":"SIMULATED"},
            "notice":"No real providers contacted; stock clips illustrate scenarios and are NOT evidence of these fictional packages."}
def claim(con,ident,notes):
    ids={x[0] for x in CASES}
    if ident not in ids: raise ValueError("Unknown demonstration case")
    if ident=="SIM-1005": raise ValueError("Safely received package does not require a claim")
    if not isinstance(notes,str) or len(notes)>800: raise ValueError("Claim notes too long")
    initialize(con)
    now=datetime.now(timezone.utc).isoformat()
    con.execute("""INSERT INTO judge_demo_claims VALUES (?,?,?,?)
      ON CONFLICT(case_id) DO UPDATE SET status=excluded.status,notes=excluded.notes,created_at=excluded.created_at""",
      (ident,"demo_claim_submitted",notes,now))
    return {"case_id":ident,"status":"demo_claim_submitted","submitted_at":now,
            "note":"Stored locally only. Nothing was filed with a real carrier.","demo_only":True}
