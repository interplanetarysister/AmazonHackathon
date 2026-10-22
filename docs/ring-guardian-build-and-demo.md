# Ring Guardian — build and demonstration guide

This repository contains the self-contained, local Delivery Guardian demonstration. The public Ring Guardian interactive experience is a separate web application. The published web UI is **not reproducible from this repository alone**; build commands below cover the source included here.

## Install and test

Requires Python 3.11–3.13 and a web browser.

```bash
git clone https://github.com/interplanetarysister/AmazonHackathon.git
cd AmazonHackathon
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m unittest discover -s tests -v
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

For Windows PowerShell, activate with `.venv\\Scripts\\Activate.ps1` instead.

Open http://127.0.0.1:8000 on the same device. The test application stores records locally and has no production authentication or user separation. **Do not expose it to the internet or enter private delivery records.**

## Demonstration flow

1. Load an example shipment.
2. Record a carrier-delivered claim, labeled as manually entered.
3. Add fictional doorstep evidence and inspect its timestamps.
4. Mark the shipment missing and review the discrepancy.
5. Review support steps and the action status.
6. Refresh to verify that local records persist.

### MCP integration

The local server supports JSON-RPC `initialize`, `tools/list` and `tools/call` over Streamable HTTP at `POST /mcp` using MCP version `2025-11-25`. Demonstrate actual request and response exchange; do not confuse a functioning MCP endpoint with a registered Alexa device.

## Public interactive demonstration

- Home: https://ring-guardian.base44.app/
- User: https://ring-guardian.base44.app/view/customer
- Management: https://ring-guardian.base44.app/view/management
- Guided demo: https://ring-guardian.base44.app/guided-demo
- Voice demonstration: https://ring-guardian.base44.app/alexa

The public UI and this local repository are distinct deployments. Confirm the published version before recording. When showing Ring or Alexa capabilities, distinguish simulated events and browser-generated speech from authorized live device integrations.

## Submission preflight

- [ ] The public demonstration opens in a fresh browser.
- [ ] User and Management paths are clear and role-specific.
- [ ] Demonstrated controls visibly respond, and recorded evidence matches the selected package.
- [ ] Spoken narration and screen instructions are synchronized.
- [ ] MCP requests run successfully and response data is shown.
- [ ] Repository instructions can be followed with a clean installation.
- [ ] The submitted source accurately represents the demonstrated functionality.
- [ ] A public demonstration video shorter than three minutes and all required submission fields are complete.

Official rules: https://amazonappdev2026.devpost.com/rules
