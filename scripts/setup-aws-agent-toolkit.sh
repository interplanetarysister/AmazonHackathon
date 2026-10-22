#!/usr/bin/env bash
# AWS Agent Toolkit setup for Ring Guardian. No chargeable AWS resources are created here.
set -euo pipefail
PROFILE="ring-guardian"
REGION="us-east-2"
log() { printf '\n==> %s\n' "$*"; }
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
[[ "$(uname -s)" == "Linux" || "$(uname -s)" == "Darwin" ]] || fail "Run this script from macOS/Linux (AWS CloudShell supported)."
command -v curl >/dev/null || fail "curl is required."
curl -fsSI --max-time 15 https://awscli.amazonaws.com >/dev/null || fail "Cannot reach the official AWS CLI endpoint."
if ! command -v uv >/dev/null; then
  log "Installing uv using the official installer."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi
command -v uv >/dev/null || fail "uv installation needs attention."
if ! command -v aws >/dev/null; then
  log "Installing AWS CLI v2 via the official installer."
  curl -fsSL https://awscli.amazonaws.com/v2/install.sh | bash
  export PATH="$HOME/.local/bin:$PATH"
fi
command -v aws >/dev/null || fail "AWS CLI is unavailable after installation."
log "Using $(aws --version 2>&1)"
aws configure set region "$REGION" --profile "$PROFILE"
log "AWS browser authentication (you must complete the AWS sign-in)."
aws login --region "$REGION" --profile "$PROFILE"
log "Verifying the AWS identity before installing."
aws sts get-caller-identity --profile "$PROFILE" >/dev/null || fail "AWS login not verified."
log "Running the official interactive Agent Toolkit installer."
aws configure agent-toolkit --yes --region us-east-1 --profile "$PROFILE"
log "Checking remote AWS skills catalog."
aws agent-toolkit list-available-skills --region us-east-1 --profile "$PROFILE"
log "Repairing AWS MCP named-profile configuration (existing JSON files only)."
if command -v python3 >/dev/null; then
  python3 scripts/patch-aws-mcp-profile.py --profile "$PROFILE" || log "MCP auto-repair not verified; inspect generated configuration manually."
else
  log "python3 absent: use an available Python runtime or edit the MCP configuration manually."
fi
log "AWS login and Agent Toolkit CLI verified; MCP client connection still needs an interactive test."
printf '\nNEXT: In every generated AI-tool MCP configuration, set aws-mcp.env.AWS_MCP_PROXY_PROFILES to %s, retaining all other generated fields. Restart the AI tool.\n' "$PROFILE"
printf 'Do not commit AWS credential files or MCP configurations containing secrets.\n'
