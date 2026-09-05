#!/usr/bin/env python3
"""Install repository hooks without assuming the shape of .git."""

from __future__ import annotations

import argparse
import stat
import subprocess
from pathlib import Path

HOOK = """#!/bin/sh
set -eu
root=$(git rev-parse --show-toplevel)
make -C "$root" check-fast
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=Path.cwd())
    args = parser.parse_args()
    repository = args.repository.resolve()
    result = subprocess.run(
        ["git", "rev-parse", "--git-path", "hooks"],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    )
    hooks = Path(result.stdout.strip())
    if not hooks.is_absolute():
        hooks = repository / hooks
    hooks.mkdir(parents=True, exist_ok=True)
    target = hooks / "pre-commit"
    target.write_text(HOOK, encoding="utf-8", newline="\n")
    target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"installed {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
