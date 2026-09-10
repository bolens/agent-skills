#!/usr/bin/env bash
# Fail setup when the tools or mounted checkout are unavailable.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
test -w . || { echo "Checkout must be writable" >&2; exit 1; }
for tool in git bash python3 node make shellcheck ruff actionlint hadolint zizmor; do
  command -v "${tool}" >/dev/null || { echo "Missing development tool: ${tool}" >&2; exit 1; }
done
checkout_root=$(git rev-parse --show-toplevel) || { echo "Git checkout is unavailable" >&2; exit 1; }
test "${checkout_root}" = "$(pwd -P)" || { echo "Workspace must be the Git repository root" >&2; exit 1; }
node -e 'if (Number(process.versions.node.split(".")[0]) !== 26) process.exit(1)' || {
  echo "Node 26 is required; rebuild the development container" >&2
  exit 1
}
printf "%s\n" "Development tools ready. See .devcontainer/README.md for repository checks."
