# AWS Builder and simulated-variable integration (October 21, 2026)

**Primary track eligibility is separate from the AWS Builder mini-challenge.**

The official rules at https://amazonappdev2026.devpost.com/rules allow documented **Kiro Crew** use to qualify for AWS Builder without any AWS runtime service. Generic Kiro CLI use should **not** be described as Kiro Crew unless it is independently evidenced. Do not claim a live AWS integration merely because fixture data is structured for it.

## Integration boundaries

- `demo_logistics.py` is the existing SQLite-backed source of five fictional Package P.I. scenarios.
- `simulation_variables.py` converts the existing `list_demo_logistics` rows into stable camelCase fields that a demo UI, narration, test script or future approved AWS adapter can consume.
- Invoke `simulation_batch(list_demo_logistics(connection, demo_user))` after calling `seed_demo_logistics(connection, demo_user)` with a local test database.
- Tracking IDs, truck IDs, scan states, facilities, package names, timestamps and review flags are **simulation-only**. No Amazon Logistics or Ring endpoint was queried.
- Ring Guardian's separately maintained source fixture is at https://github.com/interplanetarysister/RingGuardian/blob/main/fixtures/synthetic-evidence.json . Use the matching `trackingId` to correlate presentation events without asserting genuine camera recordings.
- The adapter is deliberately not enabled on the public Internet: existing application lacks production user isolation.

## AWS Builder evidence gate

1. Identify actual Kiro **Crew** use attributable to **this submission**, including dated screenshots, transcript excerpts or committed artifacts; do not label unrelated Kiro CLI prompts as Crew.
2. Alternatively build and document an actual authorized AWS service integration with its code, invocation evidence and test; optional, not a prerequisite if Kiro Crew use is proven.
3. Record exact services/tools, concrete implementation, tests and failures in the Devpost product-feedback section.
4. Verify the primary Alexa+ track separately using a running MCP server/client or eligible simulation.
5. Do not spend credits, enable paid APIs, or publish secrets merely for eligibility.
