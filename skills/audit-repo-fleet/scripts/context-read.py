#!/usr/bin/env python3
"""Read bounded, numbered UTF-8 source without emitting partial overflow output."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

MAX_LINES = 350
MAX_BYTES = 24 * 1024


def read_source(path: Path, start: int | None, limit: int | None) -> str:
    """Return one bounded JSON response, or raise before returning any source."""
    if not path.is_file():
        raise ValueError("expected a regular file")
    first = start if start is not None else 1
    count = limit if limit is not None else MAX_LINES
    rows = []
    selected_bytes = 0
    more = False
    with path.open("rb") as source:
        number = 0
        while True:
            chunk = source.readline(MAX_BYTES + 1)
            if not chunk:
                break
            number += 1
            if number >= first + count:
                more = True
                break
            if number < first:
                # Discard skipped lines in bounded chunks, including minified data.
                while chunk and not chunk.endswith(b"\n"):
                    chunk = source.readline(MAX_BYTES + 1)
                continue
            selected_bytes += len(chunk)
            if selected_bytes > MAX_BYTES:
                raise ValueError("selected source exceeds 24 KiB; request a smaller range")
            text = chunk.decode("utf-8")
            if text.endswith("\n"):
                text = text[:-1].removesuffix("\r")
            rows.append({"line": number, "text": text})
    if start is None and more:
        raise ValueError("whole file exceeds 350 lines; search first, then use --start and --limit")
    if start is not None and not rows:
        raise ValueError("start is past the end of the file")
    result = json.dumps(
        {"path": str(path), "lines": rows, "next_start": first + count if more else None},
        ensure_ascii=False,
    ) + "\n"
    if len(result.encode("utf-8")) > MAX_BYTES:
        raise ValueError("encoded response exceeds 24 KiB; request a smaller range")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--start", type=int, help="first source line, one-based; requires --limit")
    parser.add_argument("--limit", type=int, help="number of source lines, 1..350; requires --start")
    args = parser.parse_args()
    if (args.start is None) != (args.limit is None):
        parser.error("--start and --limit must be supplied together")
    if args.start is not None and (args.start < 1 or not 1 <= args.limit <= MAX_LINES):
        parser.error("start must be positive and limit must be between 1 and 350")
    try:
        result = read_source(args.path, args.start, args.limit)
    except (OSError, ValueError) as exc:
        print(f"context-read: {exc}", file=sys.stderr)
        return 2
    sys.stdout.buffer.write(result.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
