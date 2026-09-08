#!/usr/bin/env python3
"""Check or install symlinks from configured skill homes to this repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_CATALOG_ENTRIES = 10000
IGNORED_DIRS = {".git", ".hub", ".archive", "node_modules", "__pycache__", ".venv"}


def snapshot(path: Path):
    try:
        state = path.lstat()
        return state.st_dev, state.st_ino, state.st_mode, state.st_mtime_ns
    except FileNotFoundError:
        return None


def audit_catalog(home: Path, expected: dict[Path, str], excluded: set[str]) -> list[str]:
    """Inspect a bounded catalog without deleting stale links or independent skills."""
    problems = []
    pending = [home]
    seen = set()
    count = 0
    names = set(expected.values())
    while pending:
        directory = pending.pop()
        try:
            identity = directory.stat()
            key = (identity.st_dev, identity.st_ino)
            if key in seen:
                problems.append(f"catalog directory alias or cycle: {directory}")
                continue
            seen.add(key)
            with os.scandir(directory) as entries:
                children = []
                for entry in entries:
                    count += 1
                    if count > MAX_CATALOG_ENTRIES:
                        return problems + [f"catalog scan incomplete: {home} exceeds {MAX_CATALOG_ENTRIES} entries"]
                    children.append(entry)
            for entry in sorted(children, key=lambda item: item.name):
                path = Path(entry.path)
                if entry.name in IGNORED_DIRS:
                    continue
                if entry.is_symlink() and path not in expected:
                    if path.resolve().is_relative_to(ROOT / "skills"):
                        problems.append(f"unexpected repository-owned link: {path}")
                if not entry.is_dir(follow_symlinks=True):
                    continue
                skill = path / "SKILL.md"
                if skill.is_file():
                    with skill.open() as stream:
                        header = stream.read(16384).split("\n---\n", 1)[0]
                    match = re.search(r'''(?m)^name:\s*["']?([a-z0-9-]+)["']?\s*$''', header)
                    name = match.group(1) if match else path.name
                    if name in excluded:
                        problems.append(f"excluded skill exposed in catalog: {path} ({name})")
                    elif name in names and path not in expected:
                        problems.append(f"conflicting skill name in catalog: {path} ({name})")
                    continue
                pending.append(path)
        except FileNotFoundError:
            if directory != home:
                problems.append(f"catalog entry disappeared: {directory}")
        except (OSError, RuntimeError, UnicodeError) as error:
            problems.append(f"cannot inspect catalog {directory}: {error}")
    return problems


def expand(value: str) -> Path:
    codex = os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))
    agents = os.environ.get("AGENTS_HOME", str(Path.home() / ".agents"))
    claude = os.environ.get("CLAUDE_HOME", str(Path.home() / ".claude"))
    hermes = os.environ.get("HERMES_HOME") or str(Path.home() / ".hermes")
    pi = os.environ.get("PI_CODING_AGENT_DIR") or str(Path.home() / ".pi" / "agent")
    return Path(
        value.replace("${CODEX_HOME:-$HOME/.codex}", codex)
        .replace("${AGENTS_HOME:-$HOME/.agents}", agents)
        .replace("${CLAUDE_HOME:-$HOME/.claude}", claude)
        .replace("${HERMES_HOME:-$HOME/.hermes}", hermes)
        .replace("${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}", pi)
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--plan", action="store_true", help="preview changes and conflicts without writing")
    parser.add_argument("--replace", action="store_true", help="replace existing non-symlink targets")
    parser.add_argument("--client", action="append", choices=("registered", "hermes", "pi"),
                        help="select client targets; repeat to combine (default: registered homes)")
    args = parser.parse_args()
    clients = set(args.client or ["registered"])
    manifest = json.loads((ROOT / "PROVENANCE.json").read_text())
    problems = []
    expected = {}
    homes = {}
    changes = []
    for entry in manifest["skills"]:
        source = (ROOT / "skills" / entry["name"]).resolve()
        targets = list(entry["install_targets"]) if "registered" in clients else []
        for client in ("hermes", "pi"):
            target = entry.get("optional_install_targets", {}).get(client)
            if client in clients and target:
                targets.append(target)
        for raw_target in targets:
            target = expand(raw_target)
            expected[target] = entry["name"]
            homes[target.parent] = "hermes" if raw_target.startswith("${HERMES_HOME") else "other"
            correct = target.is_symlink() and target.resolve() == source
            if correct:
                continue
            if args.check:
                problems.append(f"{target} -> expected {source}")
                continue
            if target.exists() and not target.is_symlink() and not args.replace:
                problems.append(f"refusing existing target without --replace: {target}")
                continue
            changes.append((target, source, snapshot(target)))
    excluded = {entry["name"] for entry in manifest["skills"]
                if "hermes" not in entry.get("optional_install_targets", {})}
    for home, client in sorted(homes.items()):
        problems.extend(audit_catalog(home, {p: n for p, n in expected.items() if p.parent == home},
                                      excluded if client == "hermes" else set()))
    if args.plan:
        for target, source, _ in changes:
            action = "replace" if target.exists() or target.is_symlink() else "link"
            print(f"{action} {target} -> {source}")
    if problems:
        print("\n".join(problems))
        return 1
    if args.apply:
        for target, source, previous in changes:
            if snapshot(target) != previous:
                print(f"target changed after preflight; stopping: {target}")
                return 1
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.is_symlink():
                target.unlink()
            elif target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            target.symlink_to(source, target_is_directory=True)
            print(f"linked {target} -> {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
