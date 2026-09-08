#!/usr/bin/env bash
# Resolve installed links without depending on GNU realpath or dirname.
set -eu
exec python3 -c '
import runpy
import sys
from pathlib import Path
script = Path(sys.argv[1]).resolve().with_suffix(".py")
sys.argv = [str(script), *sys.argv[2:]]
runpy.run_path(str(script), run_name="__main__")
' "${BASH_SOURCE[0]}" "$@"
