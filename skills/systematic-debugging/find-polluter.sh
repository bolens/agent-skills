#!/usr/bin/env bash
# Preserve the shell entry point and resolve installed symlinks with Python.
set -eu
exec python3 -c '
import runpy
import sys
from pathlib import Path
script = Path(sys.argv[1]).resolve().with_suffix(".py")
sys.argv = [str(script), *sys.argv[2:]]
runpy.run_path(str(script), run_name="__main__")
' "${BASH_SOURCE[0]}" "$@"
