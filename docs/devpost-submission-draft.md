# Package P.I. — Devpost entry draft (October 20, 2026)

**Status:** Draft only; not submitted on Devpost. Public demo video intentionally pending at owner's direction; verify Devpost permits submission and subsequent editing before relying on that workflow.

## Project name
Package P.I. — Delivery Guardian

## Primary track / Amazon product
Alexa+; custom MCP Streamable HTTP server and browser MCP client implementing protocol 2025-11-25. The Alexa+ device SDK and genuine Alexa device integration are NOT used or claimed.

## Inspiration
A carrier can mark an order delivered when its recipient cannot find it. Tracking information, doorstep activity, receipts and internal handling clues frequently describe different things. Customers need help understanding discrepancies without unsupported theft accusations or false assurances.

## What it does
Package P.I. accepts shipment information, separates reported carrier status from user-confirmed receipt, identifies unresolved conflicts, prepares next steps, and preserves a DoneProof log of changes it actually saved. A new synthetic logistics fixture demonstrates five distinct package situations with fake scan records and editable status data.

## Demonstrated capabilities
1. SIM-1001 Headphones: delivered claim conflicts with recipient missing report; safe investigation steps.
2. SIM-1002 Medicine: sorting-hub delay and exception.
3. SIM-1003 Laptop: misrouted truck; demo database update to located.
4. SIM-1004 Books: last-known-evidence request scenario; **actual Ring video retrieval not implemented**.
5. SIM-1005 Groceries: receipt confirmation and resolved outcome.

Use the UI's **Load five samples** action to seed five packages into a local SQLite-backed simulated logistics dataset per demonstration name. Updates are verified by reading the synthetic database back. Namespaces are NOT authenticated accounts. Original application delivery listing is shared within this local prototype; do not expose this app publicly or claim production tenant isolation.

## How built
Python, FastAPI, SQLite, MCP JSON-RPC over Streamable HTTP, vanilla JavaScript web client and local synthetic logistics fixtures. Package status and external operations are explicitly labeled as manually entered or simulated. No authentic Amazon logistics database, Ring hardware, or carrier integration is used.

## Challenges / lessons
Distinguishing carrier assertions, customer statements, Ring-format synthetic events, and verified local software writes. Showing failed operations as failures rather than success.

## What next
Independent official MCP SDK interoperability check; run entire test suite; clean-room installation; customer authentication and tenant isolation; verified external API integrations; secure footage request approval; public video of the actual running application; Devpost submission confirmation.

## Product feedback TODO — actual experience only
Document Amazon developer tool names, onboarding, actual protocol tests, errors and their reproduction, workarounds, suggestions, and whether tools would be used again. Do not invent friction logs.

## Submission requirements remaining
- [ ] Verify official Devpost form permits an initial submission without video and later editing; don't assume.
- [ ] Confirm actual developer integration at runtime and reproducible independent SDK tests.
- [ ] Execute all tests and verify demo UI functionality.
- [ ] Verify README, LICENSE and judge-facing setup.
- [ ] Create public unlisted-or-public YouTube/Vimeo actual running-app video under 3 minutes, following the organizer's precise visibility rules.
- [ ] Provide product feedback and any separately eligible mini-challenge evidence.
- [ ] Enter Devpost form data, submit, and confirm submission receipt before Oct 23, 2026 12:00 PM PDT.
