#!/usr/bin/env python3
"""Check portable paths, shebangs, line endings, and shell syntax."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".venv", "__pycache__", "node_modules", "venv"}
PLATFORM_SPECIFIC_SKILLS = {"diagnose-crash", "omarchy"}
HOME_PATH = re.compile(r"(?:/home|/Users)/[A-Za-z0-9._-]+")
ABSOLUTE_RUNTIME_SHEBANG = re.compile(rb"^#!(?:/usr)?/bin/(?:bash|node|python3?)$")


def files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not IGNORED_PARTS.intersection(path.relative_to(ROOT).parts)
    ]


def is_platform_specific(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    return len(relative.parts) > 1 and relative.parts[0] == "skills" and relative.parts[1] in PLATFORM_SPECIFIC_SKILLS


def shell_scripts(paths: list[Path]) -> list[Path]:
    result = []
    for path in paths:
        try:
            first_line = path.read_bytes().splitlines()[0]
        except (IndexError, OSError):
            continue
        if path.suffix in {".bash", ".sh"} or first_line.endswith((b"/bash", b"/sh")):
            result.append(path)
    return result


def main() -> int:
    problems = []
    paths = files()
    for path in paths:
        try:
            data = path.read_bytes()
        except OSError:
            continue
        relative = path.relative_to(ROOT)
        first_line = data.splitlines()[0] if data else b""
        if ABSOLUTE_RUNTIME_SHEBANG.fullmatch(first_line):
            problems.append(f"{relative}: use /usr/bin/env in the shebang")
        if b"\r\n" in data and path.suffix in {".py", ".sh", ".bash"}:
            problems.append(f"{relative}: CRLF line endings in executable source")
        if is_platform_specific(path):
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if HOME_PATH.search(line):
                problems.append(f"{relative}:{line_number}: machine-specific home path")

    checker = shutil.which("shellcheck")
    if checker:
        for path in shell_scripts(paths):
            result = subprocess.run([checker, str(path)], check=False)
            if result.returncode:
                problems.append(f"{path.relative_to(ROOT)}: ShellCheck failed")
    else:
        print("SKIP shellcheck is not installed")

    if problems:
        print("\n".join(problems))
        return 1
    print("portability checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
