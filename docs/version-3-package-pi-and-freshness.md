# Version 3 (PARKED): Package P.I. + Grocery Freshness Guardian
**Planning status:** Future version only. Do NOT implement, enable billing, show paid service availability, or promote as live during Version 2 or the October 23, 2026 hackathon submission. Finish and verify Version 2 first.

## Package P.I. — authorized expedited recovery
**Customer problem:** A valuable or urgent shipment was missorted, scanned as delivered, left at the wrong address, placed on a wrong truck, delayed at a facility, or cannot be located. People need a fast, accountable escalation route rather than a generic support queue.

### Intended flow
1. Customer selects their shipment and requests *Emergency recovery*. Explain that availability depends on provider agreements, local law, authorized access, and operating hours.
2. Package P.I. AI reads only carrier-authorized scan events and customer's own order/recipient data; proposes a source-labeled last-known location and confidence, without claiming physical custody.
3. It compares permitted options: official delivery correction, carrier intercept, warehouse customer-service escalation, return-to-sender, licensed local recovery provider, or independently contracted last-mile delivery. It **never** dispatches Amazon Flex drivers or accesses hidden internal scans without a signed partner integration granting that specific capability.
4. Customer reviews a transparent quote, service terms, cancellation/refund policy, and the plan before any charge. A high price does **not** guarantee retrieval. No paid functionality in the zero-dollar hackathon demo.
5. Only assigned and verified workers may take custody from an authorized handler or location; log parcel handoff, barcode, time, custody verification and receipts. No trespass, third-party property retrieval without permission, courier interception, impersonation, or bypass of carrier systems.
6. Track follow-through through DoneProof: requested -> accepted by provider -> assigned -> verified custody -> delivered/closed, or declined/unavailable/failed. Preserve user communications and data deletion controls.

### Replaceable simulation adapter
Use a pluggable `LogisticsEventSource` interface; in a sandbox it reads synthetic:
- Parcel IDs and sanitized barcodes
- Order and shipment associations
- Provider scan facility IDs, UTC event timestamps, scan type
- Truck-route assignments and barcode transfer records
- Misroute or incorrect address event
- Authorized personnel roster and simulated dispatch capacity
- Recovery quotes, status, custody checkpoints, exception and rejection cases

Every screen and exported item says **SIMULATED** when fixtures are used. A production connector must meet contract, scope, audit, data minimization, and read-back requirements and never be substituted just by providing arbitrary credentials. Simulator must simulate realistic denial/failure, wrong-package matches, stale scans and dispatch unavailability.

### Version 3 acceptance gates
- Works end-to-end with synthetic data, including failed recovery and refused unauthorized requests.
- No shipment locational tracking beyond lawful scope and consent.
- Official carrier/partner access verified before claiming real-time internal scan availability.
- Approved dispatch service, commercial terms, insurance, contractor safety, address verification, payment compliance, and redress implemented before real charges or field recovery.
- No guarantee of immediate delivery absent a provider-confirmed SLA.

## Grocery Freshness Guardian — source-based packing alerts
**Customer problem:** Packed groceries may be expired, recalled, improperly stored, or too close to expiration for an expected delivery date.

### Intended flow
1. Scan GTIN/UPC or internal SKU, then retrieve **authorized** lot/batch identifier and item-level date where available. Ordinary UPC alone does not uniquely identify the lot or its expiration.
2. Cross-reference the lot with authorized supplier/retailer batch tables, recall databases, expiration/use-by/best-before labels, storage and inspection observations, and user substitution preferences.
3. Produce **Good**, **Replace**, or **Needs inspection** with a reason, timestamp and source evidence. Never claim a visual or barcode-only check proves that fresh produce is safe.
4. Alert the employee via accessible beep/vibration and clear on-screen action; record replacement and batch check result. Allow override only with reason, permissions and audit trail.
5. Keep scanned raw identifying data private; log product and lot sources, confidence, model version, and where the conclusion came from.

### Replaceable demonstration data
`FreshnessDataSource` exposes synthetic SKUs, product barcodes, lot/batch IDs, date labels, recalls, storage constraints and packing timestamps. Include examples for expired lots, recalled lots, near-expiry goods, unknown batches and safe substitutions. Label every result SIMULATED. Only connect actual retailer inventory/food-quality systems with authorization, technical validation and appropriate food-safety review.

### V3 exclusions until V2 is completed
- Actual Flex/contractor dispatch
- Private Amazon logistics scan data
- Emergency payment collection
- Camera-driven people identification or autonomous physical retrieval
- Official Amazon warehouse/inventory/lot databases
- Food freshness or safety certification

## Development priority lock
Complete Version 2: save/restore/package timeline, genuine available UPS API, local .eml/CSV import, Blink file attachment, evidence ZIP, direct reporting + phone, opt-in per-package alerts, test suite, clean-room judge walkthrough, truthfully labeled connection statuses and review-safe security. Do not consume Kiro credits (particularly the final reserved credit) or introduce billable services to work on Version 3.
