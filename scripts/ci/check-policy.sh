#!/usr/bin/env bash
# cspell:ignore ASKPASS NOSYSTEM
# Run the same pinned correctness and workflow policy as the retained hosted gates.
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)
# The tooling clone must never inherit caller indexes, worktrees, tracing or auth.
while IFS= read -r git_variable; do unset "$git_variable"; done < <(compgen -v GIT_)
unset SSH_ASKPASS SSH_ASKPASS_REQUIRE
export GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null
export GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/false
cd -- "$root"
test "$(git rev-parse --show-toplevel)" = "$root"
scratch=$(mktemp -d "${TMPDIR:-/tmp}/repository-ci-policy.XXXXXX")
trap 'rm -rf -- "$scratch"' EXIT
export PIP_NO_CACHE_DIR=1 npm_config_cache="$scratch/npm-cache"
python3 -m venv "$scratch/venv"
"$scratch/venv/bin/pip" install --disable-pip-version-check ruff==0.15.20 zizmor==1.29.0
export PATH="$scratch/venv/bin:$scratch:$PATH"
tooling=96705dc8d8147b92eee283dec1f43e91bd30c4e9
git init --quiet --template= "$scratch/tooling"
git -C "$scratch/tooling" fetch --quiet --depth=1 https://github.com/bolens/.github.git "$tooling"
git -C "$scratch/tooling" checkout --quiet --detach FETCH_HEAD
test "$(git -C "$scratch/tooling" rev-parse HEAD)" = "$tooling"
npm ci --ignore-scripts --no-audit --no-fund --prefix "$scratch/tooling/tools/source-lint"
python3 "$scratch/tooling/scripts/lint-source.py" "$root"
curl --fail --silent --show-error --location --retry 3 \
  --output "$scratch/actionlint.tar.gz" \
  https://github.com/rhysd/actionlint/releases/download/v1.7.12/actionlint_1.7.12_linux_amd64.tar.gz
printf '%s  %s\n' 8aca8db96f1b94770f1b0d72b6dddcb1ebb8123cb3712530b08cc387b349a3d8 "$scratch/actionlint.tar.gz" | sha256sum --check --strict
tar -xzf "$scratch/actionlint.tar.gz" -C "$scratch" actionlint
actionlint
zizmor --offline --min-severity medium --min-confidence medium .github
