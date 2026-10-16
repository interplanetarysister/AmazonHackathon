# Version 2: Test separately in Termux without overwriting your working demo

This is the feature branch for [draft PR #1](https://github.com/interplanetarysister/AmazonHackathon/pull/1). **Do not merge or switch the old Termux working tree until the newer UI and uncommitted changes are reconciled.** The PR must remain a draft until the checks below pass. Nothing in this document requires Kiro credits, AWS, paid hosting, or subscriptions.

## Safe checkout

In the Termux shell where the existing repository is available, first read the state:

```sh
pwd
git status --short
git branch --show-current
git remote -v
```

If there are uncommitted changes, **do not stash, reset, checkout, or overwrite them automatically**. From inside that Git repository, create a separate working directory:

```sh
git fetch origin
git worktree add ../amazonhackathon-v2 origin/feat/missing-package-resolution-paths
cd ../amazonhackathon-v2
```

The new directory will be a separate checkout, possibly at detached HEAD, which is fine for testing. SQLite data and scripts remain separate; do not copy your old database until you have made a separate backup and compared migrations. To keep both apps running, use port **8001** for this checkout, not the original 8000.

## Install, test and run

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/verify_client.py
python scripts/smoke_mcp.py
uvicorn app:app --host 127.0.0.1 --port 8001
```

Open `http://127.0.0.1:8001` in a browser on the same Android phone. The browser's own localhost is the Termux process on that phone. The `verify_client.py` check requires Node.js (Node 20+); it exits nonzero if Node is missing rather than claiming a pass. The `smoke_mcp.py` check starts an **independent real HTTP server** with a throwaway database and exercises the MCP protocol without relying on the browser or personal accounts.

If any test fails, preserve and report the full failing test name and traceback without private account data or real tracking numbers. **A Python syntax check or browser render alone is not proof the app works.**

## Manual delivery-case validation

1. Tap **Load example**; confirm sample UPS delivery is selected.
2. Tap **Carrier says delivered**; supply a clearly identified sample carrier-reported time. See the claimed time and automatic recorded time in the evidence timeline.
3. Tap **I can't find it**; verify missing help remains visible, an official UPS claim link appears, and a call option plus an editable support draft is offered. Confirm no claim was automatically filed.
4. Ask **My package says delivered but I can't find it** in the assistant section; check the live MCP activity and readable persistent answer. This is deterministic routing, not real Alexa+ account access.
5. Load an exported .eml and a small CSV with `product_title,shipping_company,estimated_delivery` columns. Data must only populate editable preview fields until the person presses Save. Do not put recipient data in Git.
6. Select a saved Blink clip (.mp4, .mov, .webm or supported image) under **Camera evidence**. Opt in to include the file and save the evidence ZIP. Open the ZIP locally and verify `delivery-case.txt` and the chosen clip are readable. **The clip does not upload to the backend.**
7. Enable alerts for one package only. Tap **Test phone notification**, grant permission if requested, and verify a notification appears. Disable that package and verify you cannot test an alert from it. This is a user-initiated notification test, **not background push**.
8. Run **Test a failing action** and check DoneProof persists a failure rather than reporting success. Refresh the browser; check delivery records and notification preference remain saved.
9. Verify a second delivery with the *same* label and carrier can still be selected correctly.
10. Test both narrow Android portrait and landscape/window resized; controls must not disappear after tapping.

## Optional real UPS scan (owner-only local verification)

A regular UPS sign-in does **not** install the developer API automatically. Create an authorized developer application in the [UPS Developer Portal](https://developer.ups.com/get-started), select the supported Tracking API and obtain its Client ID and Secret. Check its application terms, developer usage limits and any charges before enabling production access. Keep credentials **in the Termux process environment**, not in source, Git, chat or recordings.

```sh
export UPS_ENVIRONMENT=sandbox
export UPS_CLIENT_ID='YOUR_OWN_LOCAL_ID'
export UPS_CLIENT_SECRET='YOUR_OWN_LOCAL_SECRET'
# Optional when required by your UPS application: six-digit UPS account number
# export UPS_MERCHANT_ID='000000'
uvicorn app:app --host 127.0.0.1 --port 8001
```

Those strings are examples, not working credentials. A sandbox response must never be presented as live package tracking. To test a real tracking number, use a developer app authorized for **production** and explicitly set `UPS_ENVIRONMENT=production` only after the provider's eligibility, terms, quotas and cost are confirmed. The UI does not save your tracking number; it uses it for the requested lookup. An official UPS response is a carrier report, not physical receipt proof.

With a real permitted integration, test **Check official UPS status** then **Save verified UPS response to selected package**. If a tracking number is provided, pressing **I can't find it** attempts an initial status recheck when UPS API credentials are configured. Missing-package instructions are still available if lookup fails.

## Account and production limitations

- There is **no** production-ready consumer Amazon shopping-order OAuth, Gmail mailbox connector, UPS consumer-account linker, or Blink camera account authorization.
- Judges **can** use their own manually entered delivery information and own selected files when testing locally. Do not invite a public judge to connect a personal account to this unauthenticated localhost sample.
- A protected multi-user hosted deployment requires authentication, per-account isolation, encrypted secrets, explicit scopes/revocation, HTTPS, abuse/rate controls, privacy terms, and secure storage/data deletion.
- Notification preference storage and test notifications are implemented; background UPS/Gmail update processing and delivery to the Android status bar when the app is closed are **not** implemented.
- Brand and partner claims must remain accurate: independent Amazon Build, Ship, Shape entry; not certified or sponsored by Amazon, Ring, Blink or UPS.

## Version 3 is separate

Package P.I. and Grocery Freshness Guardian are **specifications only**, at `docs/version-3-package-pi-and-freshness.md`. Do not use remaining Kiro credits on Version 3 until Version 2 is tested and submitted.
