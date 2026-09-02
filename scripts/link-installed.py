#!/usr/bin/env python3
"""Check or install symlinks from configured skill homes to this repository."""

from __future__ import annotations

import argparse
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def expand(value: str) -> Path:
    codex = os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))
    agents = os.environ.get("AGENTS_HOME", str(Path.home() / ".agents"))
    return Path(value.replace("${CODEX_HOME:-$HOME/.codex}", codex).replace("${AGENTS_HOME:-$HOME/.agents}", agents))


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--replace", action="store_true", help="replace existing non-symlink targets")
    args = parser.parse_args()
    manifest = json.loads((ROOT / "PROVENANCE.json").read_text())
    problems = []
    for entry in manifest["skills"]:
        source = (ROOT / "skills" / entry["name"]).resolve()
        for raw_target in entry["install_targets"]:
            target = expand(raw_target)
            correct = target.is_symlink() and target.resolve() == source
            if correct:
                continue
            if args.check:
                problems.append(f"{target} -> expected {source}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.is_symlink():
                target.unlink()
            elif target.exists():
                if not args.replace:
                    problems.append(f"refusing existing target without --replace: {target}")
                    continue
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            target.symlink_to(source, target_is_directory=True)
            print(f"linked {target} -> {source}")
    if problems:
        print("\n".join(problems))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
