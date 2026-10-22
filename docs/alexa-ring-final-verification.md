# Alexa+ and Ring release verification — October 22, 2026

## Live findings
- AWS API connection verified in account 875476618073 through STS GetCallerIdentity; identity at verification was the **account root principal**, not a dedicated automation identity. Do not use long-lived root access keys.
- IAM Identity Center is ACTIVE in us-east-2, with **zero Identity Store users** and **zero permission sets** observed. No scoped delegate identity exists yet.
- No Lambda functions or API Gateway HTTP APIs were found in us-east-1/us-east-2, and no S3 buckets were found. The AWS backend should not be described as deployed.
- GitHub application implements a local HTTP MCP demo; signed Ring-format webhook **does not** constitute official Ring API/Playground integration.
- No AWS billable resources were created during this check.

## Judge-ready Alexa+ verification
1. Install repository requirements in an ordinary local Python 3.11-3.13 environment (no AWS resource required).
2. Run `python -m unittest discover -s tests -v`.
3. Run `uvicorn app:app --host 127.0.0.1 --port 8000`.
4. In a second terminal run `python scripts/smoke-alexa-mcp.py`.
5. Verify JSON-RPC initialize, tools/list, tools/call, five sample package records and issue lookup succeeded.
6. Manually exercise the web MCP client in a new browser session and check saved state persists.
7. Use a separate MCP SDK client to verify true independent interoperability (not yet done).
8. Record actual calls, client and server output, and a video under three minutes.

The smoke test is **not** a live Alexa skill, Alexa+ hosted integration, or a Ring source verification. Do not use its success alone for those claims.

## Ring integration acceptance gate
Ring eligibility requires actual supported Ring APIs, SDK, Playground, official simulator, or a device. Before claiming integration:
- Record the official Ring entitlement, API/SDK/Playground method and permitted workflow.
- Execute a real API/Playground/simulator call and capture a sanitized response with provenance.
- Match an actual observed event to the correct fictional package through explicit user confirmation.
- Show that event in the recorded demo. Distinguish generated sample footage from authentic Ring footage.
- If official access is missing, keep Ring supplementary and preserve the Alexa+ primary-track submission without a false claim.

## AWS access and permissions
CloudShell is an interactive temporary shell, not an unattended persistent agent endpoint. Reusable ChatGPT operations currently use AWS APIs. For future non-root access, assign an identifiable principal to a permission set through Identity Center, with least privilege and MFA. Never create persistent root keys or store credentials in GitHub. No IAM permission changes were made without a concrete delegated identity and verified trust path.

## Final submission blockers
- Judge-recorded, independently executed Alexa MCP trace and demo video.
- Official Ring runtime proof (only if entering the Ring track).
- Human review of submission details; required Devpost submission must be completed separately.
- Safe hosting/access strategy for judges. The local unauthenticated demo must **not** be deployed publicly as-is.
