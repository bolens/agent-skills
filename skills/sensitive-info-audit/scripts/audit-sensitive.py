#!/usr/bin/env python3
"""Conservative, value-redacting secret and privacy scanner."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess

SECRET_PATTERNS = {
    "private-key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "github-token": re.compile(rb"(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "aws-access-key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "google-api-key": re.compile(rb"AIza[0-9A-Za-z_-]{30,}"),
    "slack-token": re.compile(rb"xox[baprs]-[A-Za-z0-9-]{10,}"),
}
PRIVACY_PATTERNS = {
    "home-path": re.compile(rb"(?:/home|/Users)/[A-Za-z0-9._-]+"),
    "private-ip": re.compile(rb"(?<![0-9])(?:10\.(?:[0-9]{1,3}\.){2}[0-9]{1,3}|192\.168\.(?:[0-9]{1,3}\.)[0-9]{1,3}|172\.(?:1[6-9]|2[0-9]|3[01])\.(?:[0-9]{1,3}\.)[0-9]{1,3})(?![0-9])"),
    "email": re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
}


def git_files(root: Path, include_untracked: bool) -> list[Path] | None:
    probe = subprocess.run(["git", "-C", str(root), "rev-parse", "--is-inside-work-tree"], capture_output=True)
    if probe.returncode:
        return None
    command = ["git", "-C", str(root), "ls-files", "-z"]
    if include_untracked:
        command += ["--cached", "--others", "--exclude-standard"]
    result = subprocess.run(command, check=True, capture_output=True).stdout
    return [root / os.fsdecode(item) for item in result.split(b"\0") if item]


parser = argparse.ArgumentParser()
parser.add_argument("path", nargs="?", default=".")
parser.add_argument("--include-untracked", action="store_true")
parser.add_argument("--max-bytes", type=int, default=5 * 1024 * 1024)
args = parser.parse_args()
root = Path(args.path).resolve()
files = git_files(root, args.include_untracked)
if files is None:
    files = [path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts]

secrets = warnings = skipped = 0
for path in files:
    try:
        if path.stat().st_size > args.max_bytes:
            skipped += 1
            continue
        data = path.read_bytes()
    except (OSError, PermissionError):
        skipped += 1
        continue
    relative = path.relative_to(root)
    for line_number, line in enumerate(data.splitlines(), start=1):
        for detector, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                print(f"SECRET\t{relative}:{line_number}\t{detector}\t[value redacted]")
                secrets += 1
        for detector, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(line):
                print(f"REVIEW\t{relative}:{line_number}\t{detector}\t[value redacted]")
                warnings += 1

print(f"summary secrets={secrets} privacy_review={warnings} skipped={skipped}")
raise SystemExit(1 if secrets else 0)
