#!/usr/bin/env bash
# Verify checkout readiness without installing dependencies or starting services.
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
bash .devcontainer/smoke.sh
