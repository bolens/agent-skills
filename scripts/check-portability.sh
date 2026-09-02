#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)

if command -v shellcheck >/dev/null 2>&1; then
  while IFS= read -r -d '' script; do shellcheck "$script"; done < <(find "$root" -type f -name '*.sh' -print0)
else
  printf '%s\n' 'SKIP shellcheck is not installed'
fi

python3 - "$root" <<'PY'
from pathlib import Path
import re
import sys

root = Path(sys.argv[1])
excluded = {"omarchy", "diagnose-crash"}
pattern = re.compile(r"(?:/home|/Users)/[A-Za-z0-9._-]+")
matches = []

for path in (root / "skills").rglob("*"):
    relative = path.relative_to(root / "skills")
    if not path.is_file() or relative.parts[0] in excluded:
        continue
    try:
        contents = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for line_number, line in enumerate(contents.splitlines(), start=1):
        if pattern.search(line):
            matches.append(f"{path.relative_to(root)}:{line_number}:{line}")

if matches:
    print("\n".join(matches))
    raise SystemExit("machine-specific home path found")
PY

printf '%s\n' 'portability checks passed'
