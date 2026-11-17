#!/usr/bin/env python3
"""Summarize observable skill reads and completion in one Codex JSONL trace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

FRONTMATTER = re.compile(
    r"(?=^---[ \t]*\n((?:(?!^---[ \t]*$)[^\n]*\n)*)^---[ \t]*\n(?:[ \t]*\n)*(?!^---[ \t]*$)\S)",
    re.MULTILINE,
)
NAME = re.compile(r"^name:[ \t]*([a-z0-9-]+)[ \t]*$", re.MULTILINE)
READER = re.compile(r"\b(cat|sed|head|tail|bat)\b")


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
                command = item["command"]
                if "SKILL.md" not in command or not READER.search(command):
                    continue
                output = item.get("aggregated_output") or ""
                for header in FRONTMATTER.findall(output):
                    match = NAME.search(header)
                    if match:
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
