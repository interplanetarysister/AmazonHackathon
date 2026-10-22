# Ring Guardian Alexa+ MCP deployment (2026-10-21)

## Working endpoint
- Demo-only MCP endpoint: https://ring-guardian-alexa-mcp.interplanetary-fund.workers.dev/mcp
- Health: https://ring-guardian-alexa-mcp.interplanetary-fund.workers.dev/health
- Deployment: Cloudflare Worker `ring-guardian-alexa-mcp`, separate from `ring-guardian-alexa-feed`.
- Protocol requested: MCP JSON-RPC over Streamable HTTP, 2025-11-25.
- Tools: `list_demo_packages`, `get_package_timeline`, `get_simulated_evidence`, `get_investigation_status`.
- Five examples (RG-DEMO-001 through RG-DEMO-005) are **fictional scripted scenarios**, not Ring footage, carrier data, or proof of official Ring API access.
- Worker /health returned `ok:true` from user Termux on October 21 (Pacific). Automated full MCP calls still need execution in an internet-connected environment.

## Smoke test (no AWS cost)
```sh
node scripts/verify-ring-guardian-cloudflare-mcp.mjs
```
Checks initialize, discovery, and all 5 scenario responses.

## Amazon hackathon eligibility
Per official 2026 rules, the **Alexa+ track permits a self-hosted MCP server** implementing spec 2025-11-25 or a simulated Alexa+ experience in a web app. Official Alexa+ add-on portal registration is not itself proof of Ring qualification. Alexa+ preview tools may not be available to all hackathon participants. Do not claim official Alexa+ registration or certification without an Add-on ID and Amazon-side test result.

If developer account is eligible for Alexa AI CLI MCP Toolkit:
```sh
alexa-ai configure --no-browser
alexa-ai new mcp --name "Ring Guardian" --locale en-US --mcp-server-url "https://ring-guardian-alexa-mcp.interplanetary-fund.workers.dev/mcp"
```
Then complete add-on descriptions, terms/privacy links, required media, security/account-linking requirements, stage deployment and simulator testing using the current Amazon official documentation. This is NOT yet done.

## Security / release gate
The endpoint currently returns publicly readable demo data with no bearer-token authentication. **Do not attach private package information, Ring credentials, real customer evidence or production data.** Official Alexa+ account linking expects OAuth2.1/PKCE S256, resource metadata, and an authenticated MCP resource server where applicable. Ring integrations need actual Ring Playground/API/device execution proof; fictional wearable cameras do not count. Keep the existing Flash Briefing URL unchanged.

## Remaining manual proof
1. Run and record the smoke-test output.
2. Capture video of the live application invoking this endpoint (not only a console GET to /health).
3. Demonstrate authentic Ring API/Playground flow if entering Ring as a primary track; otherwise clearly declare it future work.
4. If CLI preview access exists, authenticate the Amazon Developer account and finish registration; requires account owner sign-in/consent.
5. Complete Devpost entry, demonstration under 3 minutes, source/test instructions and tool feedback before **2026-10-23 noon PDT**.

This deployment did not create AWS resources and did not use Codex, Kiro or Base44 build credits. Cloudflare costs/quotas are separate and not guaranteed at zero.
