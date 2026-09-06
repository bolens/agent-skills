#!/usr/bin/env python3
"""Compare live and managed directory trees without changing either one."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path


def fingerprint(path: Path) -> tuple[str, str]:
    if path.is_symlink():
        return "symlink", os.readlink(path)
    if path.is_dir():
        return "directory", ""
    if path.is_file():
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return "file", digest.hexdigest()
    return "other", ""


def inventory(root: Path, excludes: set[str]) -> dict[Path, tuple[str, str]]:
    result: dict[Path, tuple[str, str]] = {}
    def traversal_error(error: OSError) -> None:
        raise error

    for directory, names, files in os.walk(root, onerror=traversal_error):
        names[:] = [name for name in names if name not in excludes]
        for name in names + files:
            if name in excludes:
                continue
            path = Path(directory) / name
            result[path.relative_to(root)] = fingerprint(path)
    return result


parser = argparse.ArgumentParser()
parser.add_argument("mapping", nargs="+", metavar="LIVE=MANAGED")
parser.add_argument("--exclude", action="append", default=[])
args = parser.parse_args()
status = 0

for mapping in args.mapping:
    if "=" not in mapping:
        parser.error(f"mapping must be LIVE=MANAGED: {mapping}")
    live_text, managed_text = mapping.split("=", 1)
    live, managed = Path(live_text).expanduser(), Path(managed_text).expanduser()
    print(f"## {live} <= {managed}")
    if not live.is_dir() or not managed.is_dir():
        print("UNAVAILABLE: both paths must be directories")
        status = 2
        continue
    try:
        left, right = inventory(live, set(args.exclude)), inventory(managed, set(args.exclude))
    except OSError as error:
        print(f"UNAVAILABLE: comparison incomplete: {error}")
        status = 2
        continue
    differences = 0
    for relative in sorted(left.keys() | right.keys()):
        if relative not in left:
            print(f"managed-only\t{relative}")
        elif relative not in right:
            print(f"live-only\t{relative}")
        elif left[relative] != right[relative]:
            print(f"changed\t{relative}\t{left[relative][0]}->{right[relative][0]}")
        else:
            continue
        differences += 1
    print(f"differences={differences}")
    status = max(status, int(differences > 0))

raise SystemExit(status)
