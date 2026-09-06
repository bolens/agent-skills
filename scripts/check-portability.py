#!/usr/bin/env python3
"""Check portable paths, shebangs, line endings, and shell syntax."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".venv", "__pycache__", "node_modules", "venv", ".devenv", ".direnv"}
PLATFORM_SPECIFIC_SKILLS = {"diagnose-crash", "omarchy"}
HOME_PATH = re.compile(r"(?:/home|/Users)/[A-Za-z0-9._-]+")
ABSOLUTE_RUNTIME_SHEBANG = re.compile(rb"^#!(?:/usr)?/bin/(?:bash|node|python3?)$")


def files() -> list[Path]:
    return [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and path.name != ".devenv.flake.nix"
        and not IGNORED_PARTS.intersection(path.relative_to(ROOT).parts)
        and not any(part.startswith(".devenv.") for part in path.relative_to(ROOT).parts)
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

    # Spec Kit owns these helpers. Preserve its hashes instead of forking them
    # to satisfy local style rules, but still reject tampering and invalid Bash.
    manifest_path = ROOT / ".specify/integrations/speckit.manifest.json"
    managed = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            managed = manifest["files"]
            if not isinstance(managed, dict):
                raise ValueError("files must be an object")
        except (OSError, ValueError, KeyError, TypeError) as exc:
            problems.append(f"{manifest_path.relative_to(ROOT)}: invalid manifest: {exc}")
            managed = {}

    checker = shutil.which("shellcheck")
    owned_scripts = []
    for path in shell_scripts(paths):
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith(".specify/scripts/bash/") and relative in managed:
            if hashlib.sha256(path.read_bytes()).hexdigest() != managed[relative]:
                problems.append(f"{relative}: managed-file hash mismatch")
            result = subprocess.run(["bash", "-n", str(path)], check=False)
            if result.returncode:
                problems.append(f"{relative}: Bash syntax failed")
        else:
            owned_scripts.append(path)
    if checker:
        for path in owned_scripts:
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
