# Kiro communication and credit-efficiency playbook

**Updated:** 2026-10-16. **Owner-approved constraints:** $0 budget, preserve the final Kiro credit (with margin), win/qualify for Amazon Build, Ship, Shape, Oct 23 at noon PDT. **Source of truth for product scope:** `AGENTS.md`, `docs/product-scope.md`, `docs/hackathon-requirements.md`.

## Verified Kiro documentation and practices

1. **Do not send the entire project charter repeatedly.** Kiro recognizes root `AGENTS.md` and project `.kiro/steering/` directives automatically. Keep the always-loaded steering concise; separate detailed research and task descriptions. Official: https://kiro.dev/docs/steering/ .
2. **Use focused context.** CLI automatically knows working directory and operating system. Context/resources load on every request and consume context; skills/on-demand files are more efficient for large material. Use `/context show` to inspect context. Avoid loading the entire repository into context with broad `@` references. Official: https://kiro.dev/docs/cli/chat/context/ .
3. **Write an execution contract:** (a) repository/current state; (b) user outcome; (c) in-scope changes; (d) existing code to preserve; (e) constraints; (f) acceptance tests; (g) stop/report criteria; (h) explicit exclusions. Refer to already committed product documents instead of paraphrasing every requirement. This is our synthesis of Kiro's steering/spec guidance.
4. **Choose specs selectively.** A clear existing Python/FastAPI application is a brownfield project, not a greenfield blank slate. For changes, describe reproduction/current/expected/unchanged behavior; document testable `WHEN ... THEN the system SHALL ...` requirements. A formal Requirements/Design/Tasks spec is useful for complex features; do not run lengthy spec-generation loops for a straightforward known fix. Official: https://kiro.dev/docs/specs/feature-specs/requirements-first/ and https://kiro.dev/docs/specs/best-practices/ .
5. **Keep initial assignment bounded.** Ask for one independent MCP client/server interoperability and delivery verification milestone, with tests + customer-facing sample and stop after reporting. An instruction to complete the whole hackathon unconditionally makes credit use and testing less predictable.
6. **No fixed "one prompt = one credit" assumption.** Kiro meters a unit of work; complicated agent activity, specifications and hook execution can consume multiple credits, including on Free. A strict credit ceiling cannot be guaranteed by text in a prompt. The owner must inspect `/usage` before starting and after Kiro finishes; account usage may lag by at least several minutes. When close to the protected reserve, do not invoke Kiro. Official: https://kiro.dev/pricing/ ; https://kiro.dev/docs/cli/terminal-ui/ .
7. **Model must be actually available on Free.** The current pricing page lists 50 Free monthly credits and restricted model access, while the models guide generally recommends Auto. Do not assume Auto or premium models are offered on Free; choose from `/model` options allowed on the account. Higher reasoning effort may consume additional credits. Official: https://kiro.dev/pricing/ ; https://kiro.dev/docs/cli/models/ .
8. **Stay supervised.** Only approve required file edits and safe testing commands. Do not grant blanket tool trust, autonomous sessions, crew, subagents, background loops, hooks that invoke AI, cloud sessions, deployments, paid APIs, purchases or actual emails/claims. These consume credit and/or introduce account/financial risk. Official: https://kiro.dev/docs/cli/chat/permissions/ .
9. **Use free shell checks outside Kiro AI.** Review local repo with `git status`, `git remote -v`, `git log -1 --oneline`, run tests directly in Termux and verify the appropriate Python interpreter. Shell work performed by the user outside the model can be free; AI-tool-driven actions can accrue usage. Run `kiro-cli --version` and `kiro-cli --help` to inspect installed CLI.
10. **Reusable prompt storage.** Put reviewed prompt text into `.kiro/prompts/delivery-guardian-first-run.md`. Kiro V3 supports workspace prompts via slash completion, and versions using legacy syntax may use `@name`; an ordinary paste also works. Check `/prompts list`, `/prompts details`, `/help` before invoking. V3 can be tried via `kiro-cli --v3`, but switching harness is optional; do not spend credits experimenting with it just for novelty. Official: https://kiro.dev/docs/cli/chat/manage-prompts/ ; https://kiro.dev/docs/cli/v3/ .
11. **Multi-line entry on Termux.** `/editor` opens the editor for long prompts; file prompt invocation or clipboard paste is easier than retyping the charter. Confirm text before sending. Official: https://kiro.dev/docs/cli/chat/ .
12. **Evidence-first progress.** At each 10% *verified completion* milestone, save `docs/progress.md` with what works, tests that actually ran, limitations, customer demo command and feedback requested. Do not overstate status. Request customer feedback before irreversible UX changes, and protect demo accessibility/contest eligibility ahead of optional integrations.

## Review of our earlier master prompt (not the prompt to send)

**Purpose retained:** build Delivery Guardian (#11, #1 DoneProof, #5 Ring Resolution) as a polished, functioning, eligible Alexa+ MCP hackathon submission, prioritizing a real customer experience.

**Strong material worth preserving:** customer promise; evidence-vs-claims separation; independent action verification; zero budget/credit reserve; Ring authenticity; cross-device responsive browser; accessibility; actual tests; acceptance criteria; 10% customer checkpoints; setup/demo/Devpost materials.

**Problems improved:**
- Repeated the existing long scope and guardrails verbatim, which costs context and risks inconsistent instructions. Now link project documents.
- Unbounded "complete everything" and multi-role autonomy made the first call expensive and unpredictable. Now define one bounded batch and a stop point.
- Assigned Ring API integration, grocery preference intelligence, every browser, AWS and Devpost finalization to the same first run. Now defer beyond the first MCP/user-flow quality gate.
- Called for all possible open-source projects without a change criterion. Now require limited reuse that solves a verified gap and review third-party licenses.
- Requested ongoing 10% milestones but not a precise first report/sample. Now include concrete deliverables for the first verified checkpoint.
- Asked agent to protect credit balance without guaranteeing it can know future token usage. Now owner checks before/after, with an explicit warning that a hard cap is impossible.
- Assumed Auto is universally available. Now choose permitted Free-plan model.
- Potentially treated simulated Ring-format events as live integrations. Now strict proof-source terminology.

## First-run acceptance: one bounded implementation batch

1. Inspect and reconcile local vs GitHub without destructive commands.
2. Read scope and exact current code, run existing tests; report facts, not earlier claims.
3. Verify interoperability of existing MCP Streamable HTTP methods against the official MCP Python SDK if installable free; fix blocking protocol incompatibilities with regression tests.
4. Verify one complete customer journey in the browser where practical: import sample delivery -> mark carrier claim -> user reports missing -> show resolution guidance and proof -> refresh and retrieve persisted state. Fix only blockers/obvious UX confusion revealed in this journey.
5. Save concise test results, changes, genuine failures, sources and a user test walkthrough; commit on a safe branch (no force push and no automatic public deployment). Request user review at the next measured 10% progress boundary.
6. Defer unrelated features and do not claim actual Ring/customer email/carrier access.

### Free pre-flight checks (run in Termux, not as a Kiro AI prompt)

```sh
cd /root/amazonhackathon
git status --short --branch
git remote -v
kiro-cli --version
# Open Kiro, choose permitted Free-tier model, then use /usage and /context show
```

If the repository has unstaged work or is not the expected Git checkout, investigate non-destructively first. **Do not send the first AI request until the user has confirmed the available credits and model.**
