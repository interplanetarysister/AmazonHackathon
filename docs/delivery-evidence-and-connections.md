# Delivery Guardian: timestamped evidence, direct resolution, and authorized accounts

Updated 2026-10-16 after the owner's live Termux screenshots and feedback.

## What is working on this feature branch

- Timeline events are append-only for user-entered ETA, ETA changes, manually transcribed carrier states, user receipt/missing confirmation, explicit package sightings, and sample doorstep events.
- Each entry has a server-recorded UTC timestamp. Claimed carrier time is stored separately, with its original offset normalized to UTC. Neither is backdated on an edit. The UI displays both in local time, with source labels.
- The Ring-format webhook inbox retains the device event timestamp from `data.attributes.timestamp` when present, and the server receipt time separately. Events are automatically logged as they arrive, but only after a webhook key is configured. They remain unlinked to packages until a person associates the event; an arbitrary signed sample is **not** proof of genuine Ring hardware.
- `get_delivery_timeline` is a real MCP read tool. `record_package_sighting` is a real persisted mutation with DoneProof read-back. A sighting can be marked “just now” with automatic time capture or entered with an explicit time-zone-aware ISO timestamp.
- “What should I do?” provides verified official reporting destinations where the carrier is recognized, without claiming that a case or refund was submitted. Links point to authorized company forms or tracking pages rather than made-up deep links.
- The guidance panel is persistent within the page. Timeline and buttons are mobile-friendly.
- Backend regression tests have been added, but not yet executed on Termux on this branch. Do not claim release-ready until the tests and local smoke test pass.

## What counts as evidence

1. **Carrier-reported time:** exact time visible in an official update, when available. Capture source, timestamp, and the time our app *received* that update. Imported/manual transcriptions are labeled honestly.
2. **Doorstep-event time:** a motion, package classification, or doorbell event sent from a Ring device, only when the developer integration is legitimately authorized and the source is authenticated. Ring events are clues; a “package detected” classification must not be inferred from generic motion.
3. **Human observation time:** recorded when the user taps “I saw a package just now,” or an explicitly entered historic sighting time. Source is a user statement.
4. **No event observed:** do not equate a gap in motion history with proof of non-delivery. If device availability, privacy zones, recording coverage, subscription, or video retention cannot be confirmed, display that limitation as an evidence gap.
5. **Resolution submission:** only mark submitted after an authorized carrier/retailer response or the person's own confirmation; opening a link is not submission.

## Resolution URLs (retrieved from official documentation)

| Provider | Destination | Notes |
|---|---|---|
| UPS | https://www.ups.com/guestclaims/create?loc=en_us | Direct guest claim form; tracking information generally required. |
| FedEx | https://www.fedex.com/en-us/tracking.html | Enter tracking, choose **Manage Delivery → Report Missing Package** where eligible. |
| USPS | https://missingmail.usps.com/ | Missing Mail search requires authentication and is generally available starting seven days after mailing. |
| Amazon Logistics | https://www.amazon.com/gp/css/order-history | Your Orders → delivery issue and customer support; Amazon's published guidance sometimes recommends waiting 48 hours after a premature delivered scan. |
| Other | No guessed link | Ask user to confirm provider and only add researched official reporting destinations. |

Sources:
- https://www.ups.com/guestclaims/create?loc=en_us
- https://www.fedex.com/en-us/customer-support/faqs/receiving/tracking-questions/fedex-says-delivered-but-no-package.html
- https://www.usps.com/help/missing-mail.htm
- https://digprjsurvey.amazon.com/csad/help/node/GCU8BWGTQNJKQEBS?theme=light

## One-flow account linking: design and permission gates

The end-user goal is **“Connect Amazon, then enable Ring in one additional approval”**. Two providers may still require separate consent even for people with the same Amazon email. Do not re-prompt for permissions on each parcel.

1. Show **Connect Amazon** only when Login with Amazon is registered and the complete OAuth 2.0 state + PKCE/callback + token flow works. This returns scoped Amazon *identity/profile* info, NOT Amazon shopping order history. Never show “Orders synced” on the basis of profile login.
2. To actually import orders, use an explicitly permitted consumer order-data integration, if one becomes available to this app and region. Amazon Data Portability marketplace transaction coverage is region-dependent; standard LWA does not grant U.S. shopping history. A user-selected email/notice import remains the honest local option. No private shopping page scraping, password capture, or browser session hijacking.
3. Show **Connect Ring** after Amazon sign-in as a prominent next step, but redirect through the official Ring Appstore developer authorization flow and obtain permission separately. If same email, prefill it where Ring's documented customer-experience pattern permits. Cache legitimate authorization securely so repeated confirmations are unnecessary, and support disconnect/revoke.
4. Ring partner onboarding and actual developer configuration must be completed before presenting that button as functional. Official Ring requires client credentials, OAuth account linking, authorized device selection, securely hosted callback and signed HTTPS webhook. Playground calls are valid for testing but not production account-linking proof.
5. Ring device event history may return activity only *after user consent*. Don't claim access to prior footage. Record `attributes.timestamp` (event occurrence), `meta.time` (envelope timestamp) and local receipt time distinctly when available. Respect device configuration, motion zones, retention, privacy zones, and subscription limitations.
6. The production cloud connection requires HTTPS and per-user authenticated, encrypted token storage, rotation and deletion. The current `127.0.0.1` unauthenticated sample app must **never** accept real consumer OAuth tokens.
7. Link candidate camera events to packages by time window and approved device/household only after device authentication; don't identify an event as the delivery without enough context. Offer a correction button. Do not auto-submit claims without review.

Official docs:
- https://developer.amazon.com/docs/login-with-amazon/customer-profile.html
- https://developer.amazon.com/docs/amazon-data-portability/overview.html
- https://developer.amazon.com/docs/ring/develop.html
- https://developer.amazon.com/docs/ring/api-documentation.html
- https://developer.amazon.com/docs/ring/ux-design-guide.html

## Expected next iteration before public demo

- Confirm the newer Termux local frontend is committed; it differs from `main`. Carefully reconcile this branch's timeline and persistent guidance changes with that local interface so no styling or functionality is lost.
- Test persistent guidance on all three flagged buttons after repeated clicks, page refresh, and back/forward navigation.
- Add a sanitized, exportable case summary that lists both UTC and local times with source labels and a reviewable carrier claim. Never falsely certify provider data.
- If Ring Playground developer credentials are available at no cost, test one true Playground event without labeling it customer hardware. Do not enable unregistered public OAuth.
- Run `python -m unittest discover -s tests -v` and a fresh Termux browser walkthrough before merge.
