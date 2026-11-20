#!/usr/bin/env python3
"""Summarize observable skill reads and completion in one Codex JSONL trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shlex

FRONTMATTER = re.compile(
    r"(?=^---[ \t]*\n((?:(?!^---[ \t]*$)[^\n]*\n)*)^---[ \t]*\n(?:[ \t]*\n)*(?!^---[ \t]*$)\S)",
    re.MULTILINE,
)
NAME = re.compile(r"^name:[ \t]*([a-z0-9-]+)[ \t]*$", re.MULTILINE)
READERS = {"cat", "sed", "head", "tail", "bat"}
SKILL_DIRECTORY = re.compile(r"(?:[a-z0-9-]+|\{[a-z0-9-]+(?:,[a-z0-9-]+)+\})")


def skill_paths(command: str) -> set[str]:
    """Recognize direct reads so unrelated command output cannot count."""
    try:
        args = shlex.split(command)
        if len(args) == 3 and Path(args[0]).name in {"bash", "sh", "zsh"} and args[1] in {"-c", "-lc"}:
            args = shlex.split(args[2])
    except ValueError:
        return set()
    if not args or Path(args[0]).name not in READERS:
        return set()
    reader, *paths = args
    if Path(reader).name == "sed" and len(paths) >= 3 and paths[0] == "-n" and re.fullmatch(r"\d+(?:,\d+)?p", paths[1]):
        paths = paths[2:]
    if Path(reader).name in {"head", "tail"} and paths:
        if re.fullmatch(r"-\d+", paths[0]):
            paths = paths[1:]
        elif len(paths) >= 3 and paths[0] == "-n" and paths[1].isdigit():
            paths = paths[2:]
    if paths and paths[0] == "--":
        paths = paths[1:]
    names = set()
    for path in map(Path, paths):
        directory = path.parent.name
        if path.name != "SKILL.md" or not SKILL_DIRECTORY.fullmatch(directory):
            return set()
        names.update(directory.strip("{}").split(","))
    return names


def summarize(trace: Path) -> dict:
    """Use command output to corroborate entrypoint reads, including batched reads."""
    reads: dict[str, str] = {}
    usage = None
    turn_status = "incomplete"
    with trace.open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            event = json.loads(line)
            if event["type"] == "turn.completed":
                turn_status = "completed"
                usage = event.get("usage")
            elif event["type"] == "turn.failed":
                turn_status = "failed"
            elif event["type"] == "item.completed":
                item = event["item"]
                if item["type"] != "command_execution" or item.get("exit_code") != 0:
                    continue
                names = skill_paths(item["command"])
                if not names:
                    continue
                output = (item.get("aggregated_output") or "").replace("\r\n", "\n")
                for header in FRONTMATTER.findall(output):
                    match = NAME.search(header)
                    if match and match.group(1) in names:
                        reads.setdefault(match.group(1), item["id"])
    return {"turn_status": turn_status, "skill_reads": reads, "usage": usage}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path)
    args = parser.parse_args()
    try:
        result = summarize(args.trace)
    except (OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Could not read Codex trace: {error}\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
