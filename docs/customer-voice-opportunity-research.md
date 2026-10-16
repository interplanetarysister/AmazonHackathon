# Customer Voice: 5 Product Complaints + 5 Unmet Opportunities

**Amazon Build, Ship, Shape Hackathon — research decision memo**  
**Research cutoff:** October 16, 2026  
**Products investigated:** Alexa+, Bee (including October 15 updates), Ring, Fire TV  
**Companion:** [Hackathon requirements](hackathon-requirements.md)

## Scope and reliability

This is a qualitative, targeted public-source review of reported user problems and possible developer opportunities, **not** a representative survey of customers or every published article. Sources include Reddit posts/comments, direct App Store reviews, Amazon support/developer documents, and independent product reviews. Rankings reflect evidence triangulation, user harm/friction, whether an app can actually help, and feasibility by October 23; they are **not frequency estimates or market-share statistics**.

**Strict exclusion applied:** neither list includes something already resolved by one settings toggle, one paid upgrade, a built-in feature, or purchasing upgraded hardware. Also excluded: repairs only Amazon can make to its proprietary voice-recognition/OS internals, unless a third-party workflow can independently solve an aspect. Some complained-about issues can have multiple causes; direct evidence that a user's device failed does not alone prove the built-in feature is completely absent.

### Top five complaints (qualitative ranking)

| Rank | Frustration expressed by users | Affected ecosystems | Confidence / qualification |
| --- | --- | --- | --- |
| 1 | Commands or routines **appear to succeed but cannot be trusted as fully executed**; actions silently fail or do the wrong thing | Alexa+, connected services | **High** for recurring reports; not evidence every user has failures |
| 2 | Personal context, speaker attribution and facts are sometimes **inaccurate, misremembered or lost**, and fixing a memory doesn't establish what future tasks it affected | Alexa+, Bee | **High** as issue; stronger linked provenance/correction is a new proposal |
| 3 | Captured ideas, summaries, tasks, and commitments **do not automatically become accountable work across chosen third-party tools** without manual steps | Bee, Alexa+ | **Moderate-high**; API/CLI and certain integrations already exist, so generic export/sync isn't a valid new feature |
| 4 | Camera footage and alerts identify events, but **don't reliably establish or track whether the real-world situation was resolved**; imperfect classifications further muddy status | Ring | **Moderate**; Ring already has package alerts, video search/descriptions, single-event/unusual-event alerts |
| 5 | Cross-service **watch progress and deep resumption remain fragmented or incorrect**; users sometimes must choose providers again or locate the program manually | Fire TV | **Moderate**; built-in Continue Watching already exists for supported partners; several reported failures have settings/workarounds, and external streaming providers may limit integration |

#### Evidence detail

1. **Action reliability:** A September 9 Alexa user reports routine steps not running despite unchanged devices/network, and repeated identical commands yielding different outcomes: https://www.reddit.com/r/alexa/comments/1wbmeqx/alexa_has_somehow_gotten_worse_at_the_one_thing_i/. Another September report describes routines/smart-home commands not functioning: https://www.reddit.com/r/alexa/comments/1w838jv/alexa_is_the_worst/. Amazon's own support forum documents routines not found and factual answers improvised: https://www.amazonforum.com/s/question/0D5at00000kkZekCAE/alexa-plus-early-access-issues. Independent October review finds the assistant improved in smart-home use but still falls short on complex personal tasks: https://www.theverge.com/tech/1007565/amazon-alexa-plus-review-one-year-echo-show-dot-max. **Opportunity is independently confirming our own tools**, not modifying Alexa's internal smart-home routines.

2. **Memory and attribution:** A May Bee App Store review mentions serious long-term memory flaws; other users report incorrect context and editing/correction. See https://apps.apple.com/us/app/bee-your-personal-ai/id6480349491?see-all=reviews. TechCrunch's Bee hands-on testing reported inability to label all speakers easily and lack of source audio replay (Bee deletes audio): https://techcrunch.com/2026/01/12/hands-on-with-bee-amazons-latest-ai-wearable/ and https://techcrunch.com/2026/05/24/i-tried-amazons-bee-wearable-and-am-both-intrigued-and-slightly-creeped-out/. July Bee user feedback reported poor speaker attribution while praising its open API: https://www.reddit.com/r/Bee_computer/comments/1us4g6z/why_isnt_this_more_popular/. **Never propose a covert recording archive** as the fix; use retained transcripts, uncertainty tags, user corrections and consent.

3. **Workflow follow-through:** Aug 12 Bee thread asks about automatically turning captured ideas and todos into Notion actions and says starter workflows are lacking: https://www.reddit.com/r/Bee_computer/comments/1vmhfuj/your_favorite_flow/. App Store reviewer wanted CRM/desktop workflow without manual phone copying: https://apps.apple.com/us/app/bee-your-personal-ai/id6480349491. However Bee **already supports** public API, CLI markdown export, MCP and syncing: https://docs.bee.computer/docs and https://docs.bee.computer/docs/api. An October 15 Bee device/software launch and Bee Pro plan expanded compatibility and desktop/tool capabilities: https://www.theverge.com/tech/1011475/amazon-bee-frontier-eclipse-price-specs and https://www.reddit.com/r/Bee_computer/comments/1x6nq18/new_bee_announcement_will_we_be_charged/. Thus the gap is **stateful verified handoff with ownership and retries**, not merely a way to export or an app on PC.

4. **Event resolution:** Apr 2026 Ring App Store reviewer describes receiving dozens of alerts during one known visit: https://apps.apple.com/us/app/ring-always-home/id926252661?see-all=reviews. Earlier/later Ring customers report package/person events missed: https://www.reddit.com/r/Ring/comments/1q3xf1z/ring_isnt_catching_most_of_my_deliveries_or/ and https://www.reddit.com/r/Ring/comments/1pmq3bi/ring_doorbell_doesnt_detect_amazon_deliveries/. But missing footage can reflect device placement, power, motion settings or hardware limits. **Do not rank simple notification snoozing or package detection as missing**. Ring has all of these: video search, descriptions, familiar faces, single-event alerts, unusual-event alerts, active warnings: https://blog.ring.com/home-security/ring-intelligent-features-explained/ . A third-party project could take authorized observable events, open tasks and require human confirmation to close. It must label missing/corrupted footage as **unknown**, not evidence that an event did or did not occur. Ring developer API: https://developer.ring.com/ and https://developer.amazon.com/docs/ring/develop.html. Ring TAKE/E2EE may constrain access: https://community.amazondeveloper.com/t/aug-31-2026-hackathon-ring-updates/29048.

5. **Playback continuity:** Apr 20 user says Fire TV Continue Watching makes them reselect services and hunt for the show rather than resume: https://www.amazonforum.com/s/question/0D5at00000ivXpTCAU/fire-tv-continue-watching-feature-not-functioning-properly. Nov 2025 watchlist feedback seeks a genuinely convenient cross-app list: https://www.reddit.com/r/fireTV/comments/1p0mwfl/universal_watchlist_poor_implementation/. Amazon documents supported-app Continue Watching and how to manage its sharing settings: https://digprjsurvey.amazon.co.uk/csad/help/node/TEIq4vikEIpvh49FW1 and https://digprjsurvey.amazon.co.uk/csad/help/node/TpJxOEPHMPJbmKq5Bh. Fire TV developer docs describe the partner's required playback events and limitations: https://developer.amazon.com/docs/fire-tv/watch-activity.html . One Reddit stuck-list case **was solved by the remote's long OK press**, so it is excluded: https://www.reddit.com/r/firetvstick/comments/1thzhh9/need_help_with_my_continue_watching_list/.

### Top five recommended features *not provided as end-to-end workflows by basic existing capabilities*

Each is an app opportunity, **not** a claim that no third-party solution exists anywhere.

| Rank | Feature | Primary track | How to show it's real | Confidence |
| --- | --- | --- | --- | --- |
| 1 | **Verified Action Ledger** | Alexa+ | In one voice/text request create several entities through tools; read actual stored state; visibly show completed, failed, retried and awaiting approval | **High** |
| 2 | **Evidence-Linked, Correctable Context** | Alexa+; possible future Bee import | Show user what source supported each memory, mark uncertain claims; correct one fact, locate affected tasks, re-evaluate them | **High** |
| 3 | **Consent-Based Cross-App Commitment Handoffs** | Alexa+; possible Bee extension | Turn conversation into assigned tasks in authorized systems; handle OAuth, deduplication, retries and confirmation; track who owns each task | **High / implementation access dependent** |
| 4 | **From Ring Event to Confirmed Resolution** | Ring | Simulated authorized Ring event → task requiring pickup/check-in → explicit household confirmation; offline/camera gaps flagged unknown | **Medium / available simulator & API scope dependent** |
| 5 | **Household Viewing Continuity Workspace** | Fire TV | Family profiles, decision votes and manual state corrections; launch available titles in participating services, never promise third-party resume data without access | **Medium / streaming partner limits** |

#### Why feature 1 wins for this hackathon

- A narrow end-to-end MCP skill can show a non-trivial, **stateful multi-step agent**, exactly aligned with Alexa+ track.
- No Amazon hardware is required; a self-hosted MCP server and our own client demo are permitted.
- Testability is clear: tool calls, database records, idempotent operation keys, retrieval, error detection and honest completion statuses.
- We can distinguish ourselves from generic task-list AI through **independent post-write verification** and an explicit evidence trail, while being candid that we cannot intercept or fix Alexa's internal routines.
- A meaningful AWS Builder integration can be added if verified, but no claim of AWS use before it is running.

#### Proposed 2–3 minute demo

1. User: "Organize a Saturday neighborhood cleanup: create six assignments and a supply list."
2. Agent calls structured tools; server validates permissions, writes records and reads them back.
3. One tool is made to fail predictably; UI says **not complete**, stores error context and a safe retry action instead of falsely saying success.
4. Follow-up conversation references saved project; user corrects a fact; app shows memory provenance and affected tasks.
5. Final dashboard shows who owns what, which changes are verified and which need user attention.
6. Show the actual MCP initialize/tools/list/tools/call traces, persistence tests, and AWS integration only if actually implemented.

#### Non-negotiable design safeguards

- Verify read-after-write when supported; recognize that some external APIs are eventually consistent and never equate accepted request with final external completion.
- Explicit user consent for connected services; least-privileged scopes, revocation, no credential collection into logs.
- Human approval for public posts/messages, payments, locks/alarms or other consequential actions.
- Record **source and uncertainty**, do not invent facts from missing camera or audio evidence.
- No covert recording, no unauthorized use of third-party conversations or personal information.
- Keep the app useful without hardware or paid subscriptions; enhanced authorized integrations may be optional.

## Items intentionally removed from earlier candidate lists

- **"Ring smart notifications / AI video descriptions / familiar faces / video search"** — already available, including with existing eligible paid plans; configuration does not equal new software.
- **"Mute a burst of Ring notifications"** — platform alert and snooze controls and Single Event/Unusual Event exist; not a qualifying core innovation.
- **"Fire TV universal watchlist / Continue Watching exists"** — built-in support; focus only on additional collaborative accountability or gaps in unsupported apps, not reimplementing the existing row.
- **"Bee basic export/download"** — developer CLI/API and markdown sync exist as of Oct 16.
- **"Bee desktop app"** — October 15 launch brings desktop/Pro options; excluded under no-paywall-duplicates rule.
- **"Bee basic suggested tasks, conversations, memories, calendar/email connections"** — existing offerings; our feature must add verifiable cross-service state.
- **"Alexa shorter responses / change voice / disable Alexa+"** — device/app preference controls, not a hackathon feature.
- **"Improve Alexa's core speech recognizer or private routine engine"** — Amazon platform fix beyond third-party MCP scope; do not promise it.

## Other strong signals — not falsely treated as proven missing app features

- Some Alexa users report unsolicited interjections/AI privacy concern: https://www.reddit.com/r/alexa/comments/1wg1gg8/after_a_decade_of_alexa_in_my_home_im_done/. Independently reported and not necessarily reproducible on all devices; build consent and transparency into our own product rather than promise to change Amazon listening policy.
- Bee feedback is strongly mixed; many praise its accuracy and usefulness (same App Store page and https://www.reddit.com/r/Bee_computer/comments/1us4g6z/why_isnt_this_more_popular/). Avoid framing the product as universally broken.
- Some Ring camera detection faults are solvable via zone/sensitivity/device changes: https://pa.ring.com/support/articles/9qnpt/receiving-person-and-package-alerts-with-smart-alerts. Exclude those as product ideas.
- New Bee Frontier/Eclipse and subscription/software capabilities were announced **October 15, 2026**. Recheck the exact capability matrix before deciding to enter Bee.

## Decision and next technical test

**Recommendation:** Build **Verified AI Actions + Evidence-Linked Context**, starting with an Alexa+ eligible **MCP 2025-11-25+ Streamable HTTP server** and a web demo client. Build a real persistent read/write/verify flow first. Add optional cross-app handoff as a narrow second feature. Avoid Ring, Bee and Fire TV as simultaneous primary builds this week.

**Requirements reference:** https://amazonappdev2026.devpost.com/rules and https://amazonappdev2026.devpost.com/details/faqs . Deadline October 23 at noon PDT.

### Open research/validation questions

- Can our exact chosen read-after-write verification be implemented under realistic service permissions?
- Which partner data are actually accessible, versus inferred from a demo fixture?
- Can clean-room judges run the demo without paid/private accounts?
- Is the evidence feature usable on a small phone as well as desktop?
- Does the product sound differentiated to first-time users in a five-second pitch?

*Research is continuously revisable; do not convert suggested capabilities into README “completed” claims until running tests prove them.*
