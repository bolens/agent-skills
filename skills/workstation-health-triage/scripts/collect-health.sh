#!/usr/bin/env bash
# Preserve the established entry point; one supervisor owns all probe lifetimes.
set -eu
exec python3 "$(dirname -- "$(realpath -- "${BASH_SOURCE[0]}")")/collect-health.py" "$@"
