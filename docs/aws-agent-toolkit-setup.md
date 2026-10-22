# Ring Guardian AWS Agent Toolkit setup

This procedure follows [AWS's official setup guide](https://github.com/aws/agent-toolkit-for-aws/blob/main/setup-instructions/setup.md). The AWS profile is `ring-guardian`; AWS Agent Toolkit is currently in `us-east-1`.

## Run in your own authenticated AWS environment

On AWS CloudShell or a trusted Linux/macOS computer with outbound internet, from the repository root run:

```bash
bash scripts/setup-aws-agent-toolkit.sh
```

The script checks Linux/macOS, curl, uv, AWS CLI, and connectivity to AWS. It installs missing CLI prerequisites using official installers. AWS `login` is interactive and needs the account owner to complete browser authentication. The Toolkit wizard may also request input. Credentials are valid for 12 hours and renewable for up to 90 days without repeating browser sign-in.

The script verifies identity with `aws sts get-caller-identity`, runs the official `aws configure agent-toolkit --yes --region us-east-1 --profile ring-guardian`, and lists available skills. Do not mistake the script being committed for successful execution in your own account.

## Required MCP follow-up

The wizard generates a configuration for supported AI clients. Open each generated configuration and update **only** the `aws-mcp` server's environment block, preserving `command`, `args`, `timeout`, `transport`, and all unrelated servers:

```json
"env": {
  "AWS_MCP_PROXY_PROFILES": "ring-guardian"
}
```

If `aws-mcp` or its `env` block already exists, reconcile it without replacing existing unrelated values. OpenCode uses a different schema; follow its documented equivalent. Restart your AI coding client and verify AWS MCP can list tools. Never add keys, cookies, AWS credentials, or token files to the repository.

For a second account, authenticate with `aws login --profile OTHER_PROFILE`, then add that profile to the space-separated `AWS_MCP_PROXY_PROFILES` list.


## MCP repair automation

The installer now invokes `scripts/patch-aws-mcp-profile.py` when Python 3 is available. It changes only an existing JSON `mcpServers.aws-mcp.env.AWS_MCP_PROXY_PROFILES` value and saves a `.aws-agent-toolkit.bak` backup. It refuses to overwrite an existing different profile, reports files that it did not recognize, and does not auto-edit OpenCode or TOML configurations. If the installer wrote a different JSON path, pass the exact path manually:

```bash
python3 scripts/patch-aws-mcp-profile.py --profile ring-guardian /absolute/path/to/mcp.json
```

The repair helper uses Python 3 *only if already available*; it is not required for the AWS installer itself. An environment without Python 3 can edit the MCP configuration manually. The helper cannot prove that the MCP server is connected; start the configured agent and run a real MCP tool-list call to verify.

## Verification and release gate

- `aws sts get-caller-identity --profile ring-guardian` succeeds.
- `aws agent-toolkit list-available-skills --region us-east-1 --profile ring-guardian` returns skills.
- The chosen AI coding client has an `aws-mcp` entry with the named profile and actually connects.
- The app's separate Ring and Alexa+ runtime integration tests pass before claiming hackathon compliance. Agent Toolkit alone does not establish those integrations.

## Cost and permissions

Do not provision metered AWS resources or spend credits as part of this setup. Any paid infrastructure requires separate authorization. The project rules in `AGENTS.md` override more general AWS agent guidance.
