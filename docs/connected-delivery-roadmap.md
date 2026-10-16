# Connected Delivery — phased integration architecture (not implemented)

## Why this comes after the hackathon demo

The October 23 Alexa+ entry must remain runnable offline with zero-dollar dependencies and the MCP client/server verified end to end. This document preserves the owner's wider vision without claiming an external platform is already connected.

## Unified end-user experience

The eventual **Connections** screen has sections for Shopping, Carriers, Email, Seller Stores, and Cameras. Each provider card displays **Connect**, **Connected and working**, **Needs reauthorization**, or **Unavailable** based on a real provider check (never an artificial toggle). The user consents once per provider/scoped integration and can disconnect/revoke permissions from the same screen.

- **Shopping:** Amazon (Login with Amazon can authorize identity, not ordinary shopping-order history), Temu (verify whether a supported customer-order API is available), and future approved marketplaces.
- **Carrier:** UPS, FedEx, USPS, and regional services. Check developer and consumer-account API eligibility separately; account login does not automatically grant shipment history. Use official report forms as an immediately available fallback.
- **Email notices:** Gmail via Google OAuth + Gmail `gmail.readonly`; restrict search to delivery-related messages, parse only explicit fields, ask users to confirm ambiguous results, minimize stored message data. Use authorized push or opt-in refresh, with no silent mailbox scanning.
- **Selling:** Shopify store authorization can expose fulfillment objects with `trackingInfo`, `updatedAt`, and shipping events within granted read scopes. TikTok Shop APIs require documented seller permissions/eligibility; no generic login scraping.
- **Ring:** Ring Appstore approved partner app, developer authorization, scoped event/device data, official webhooks and separate source verification. An Amazon identity login cannot silently grant camera access.
- **Other compatible cameras:** Home Assistant or Frigate adapters may normalize camera motion/package-like observations on user-selected devices; never assume recording is enabled or clear enough.

### Open-source shortlist

1. **Activepieces community/core**: MIT licensed workflow connector host; proprietary commercial/enterprise folders and hosted services are excluded from the free build. Verify that any chosen piece or integration is available under the community license and permits embedding/distribution before release: https://www.activepieces.com/docs/about/license
2. **Home Assistant**: optional integration broker for supported devices/home automation, with explicit user permission: https://www.home-assistant.io/
3. **Frigate**: optional local NVR and object-detection engine for supported camera streams; setup is hardware/resource dependent: https://docs.frigate.video/
4. **Existing Python MCP + SQLite**: authoritative package/case ledger, provenance, idempotency, user-visible history; no required new database.

These products do not themselves make private Amazon consumer orders, TikTok Shop seller transactions, or Ring footage freely available.

### Provider-specific technical references

- Gmail API: https://developers.google.com/workspace/gmail/api/reference/rest/v1/users.messages/list
- Shopify fulfillment: https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment
- Ring partner integration: https://developer.amazon.com/docs/ring/develop.html
- Login with Amazon: https://developer.amazon.com/docs/login-with-amazon/customer-profile.html
- Ring API release notes: https://developer.amazon.com/docs/ring/release-notes.html

## Incoming vs outgoing shipments

Every `Delivery` eventually has `direction = incoming | outgoing`, `record_origin`, `source_account_id` (opaque), a verified origin timestamp, and sanitized event references. Outgoing merchant records may refer to recipient details, which must be protected per account and omitted from demo data, logs and evidence exports by default.

A person running a home-based business can:
1. Connect an approved store/courier account; select orders and whether to import existing shipments.
2. Record a handoff or request an at-home courier pickup, using carrier confirmation as distinct from camera observations.
3. Review a mismatch between a scheduled pickup, camera event and carrier acceptance scan.
4. Opt into recipient notifications with an explicit sender/recipient communications policy; provide a preview and test channel before enabling future automatic updates.
5. Open the official carrier case path with assembled timestamps if a claimed pickup/drop-off is disputed.

## Camera observation pipeline

The selected camera/source reports event time, receiving time, retention limits, covered zones, event type, and source authorization. A dedicated adapter normalizes observations, then matches *candidate* pickups or deliveries against shipment windows and known courier schedules. The system can say **possible pickup activity** or **no relevant event recorded in the selected view during the inspected interval**, but not that a courier definitely picked up a particular package from generic motion alone. Allow the owner to approve or correct associations, or turn monitoring off. Avoid face recognition and covert monitoring of couriers, neighbors, or passersby.

A visible **camera coverage/availability** row matters: recording turned off, video overwritten, motion excluded from a configured zone, network outages or incomplete retention must produce **insufficient footage** rather than “nothing happened.” Analyze only authorized camera zones, retain the minimum derived metadata and let users delete it. Recorded clips are optional, explicitly consented, and encrypted.

## Consent and connection security gates

- OAuth with provider-approved redirects, PKCE where appropriate, correct scopes and documented token lifecycle; no embedded passwords, developer-side scraping or unsupported API calls.
- Server-side encrypted secrets, owner-specific isolated storage, refresh/revocation, disclosure and deletion controls, plus explicit pre-production security tests. The current localhost sample has none of this; do not connect real consumer accounts to it.
- For outbound messaging: opt-in, reasonable limits, clear contact provenance and unsubscribing, error/retry handling, proof of provider acceptance separate from recipient receipt; no automatic complaint or refund submission without user review and suitable authorization.
- Free/open source choices must not create mandatory billing dependencies or compromise the hackathon deadline.

## Suggested post-submission implementation order

**First:** authorized Gmail shipment imports, provider normalization and per-source provenance. **Second:** Shopify outgoing orders and manual pickups. **Third:** official Ring events and one selected Home Assistant/Frigate camera path. **Fourth:** other marketplaces and carrier APIs only where authorized access is actually available. **Fifth:** opt-in recipient updates, scheduling, and well-tested camera activity comparisons.

All milestones must have a real authorization demo, failed/expired-connection tests, and integration-specific help pages before labeling them working.
