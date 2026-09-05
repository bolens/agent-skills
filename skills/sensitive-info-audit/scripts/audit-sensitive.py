#!/usr/bin/env python3
"""Conservative, value-redacting secret and privacy scanner."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import stat
import subprocess
from typing import Optional

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


def git_files(root: Path, include_untracked: bool) -> Optional[list[Path]]:
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
if args.max_bytes < 1:
    parser.error("--max-bytes must be positive")
root = Path(args.path).expanduser().absolute()
try:
    mode = root.lstat().st_mode
except OSError:
    parser.error("input path is missing or inaccessible")
if stat.S_ISREG(mode) or stat.S_ISLNK(mode):
    files = [root]
    root = root.parent
elif stat.S_ISDIR(mode):
    files = git_files(root, args.include_untracked)
    if files is None:
        files = []

        def traversal_error(error: OSError) -> None:
            parser.error("directory traversal incomplete: " + str(error.filename))

        for directory, names, filenames in os.walk(root, onerror=traversal_error):
            names[:] = [name for name in names if name != ".git"]
            parent = Path(directory)
            files.extend(parent / name for name in filenames)
            files.extend(parent / name for name in names if (parent / name).is_symlink())
else:
    parser.error("input must be a regular file, symlink, or directory")

secrets = warnings = skipped = scanned = 0
for path in files:
    relative = path.relative_to(root)
    try:
        metadata = path.lstat()
        if not (stat.S_ISREG(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode)):
            print(f"SKIP\t{relative}\tnot a regular file or symlink")
            skipped += 1
            continue
        if metadata.st_size > args.max_bytes:
            print(f"SKIP\t{relative}\texceeds --max-bytes")
            skipped += 1
            continue
        data = os.fsencode(os.readlink(path)) if stat.S_ISLNK(metadata.st_mode) else path.read_bytes()
    except OSError:
        print(f"SKIP\t{relative}\tmissing or unreadable")
        skipped += 1
        continue
    scanned += 1
    for line_number, line in enumerate(data.splitlines(), start=1):
        for detector, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                print(f"SECRET\t{relative}:{line_number}\t{detector}\t[value redacted]")
                secrets += 1
        for detector, pattern in PRIVACY_PATTERNS.items():
            if pattern.search(line):
                print(f"REVIEW\t{relative}:{line_number}\t{detector}\t[value redacted]")
                warnings += 1

print(f"summary secrets={secrets} privacy_review={warnings} skipped={skipped} scanned={scanned}")
raise SystemExit(1 if secrets else 2 if skipped else 0)
