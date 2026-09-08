#!/usr/bin/env python3
"""Verify Spec Kit's managed files without rewriting integration state."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(root: Path) -> list[str]:
    problems = []
    for integration in ("speckit", "codex"):
        relative_manifest = f".specify/integrations/{integration}.manifest.json"
        try:
            manifest = json.loads(
                (root / relative_manifest).read_text(encoding="utf-8")
            )
            if (
                not isinstance(manifest, dict)
                or manifest.get("integration") != integration
            ):
                raise ValueError("integration name does not match manifest")
            files = manifest.get("files")
            if not isinstance(files, dict) or not files:
                raise ValueError("files must be a nonempty object")
        except (OSError, ValueError) as exc:
            problems.append(f"{relative_manifest}: invalid or missing manifest: {exc}")
            continue

        for relative, digest in files.items():
            path = Path(relative)
            if (
                path.is_absolute()
                or ".." in path.parts
                or path.as_posix() != relative
                or not path.parts
                or "\\" in relative
            ):
                problems.append(
                    f"{relative_manifest}: invalid managed path: {relative!r}"
                )
                continue
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                problems.append(f"{relative}: invalid SHA-256 digest")
                continue
            target = root / path
            try:
                if any(
                    (root / parent).is_symlink() for parent in (path, *path.parents)
                ):
                    raise ValueError("managed path must not be a symlink")
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
            except (OSError, ValueError) as exc:
                problems.append(
                    f"{relative}: missing or unreadable managed file: {exc}"
                )
                continue
            if actual != digest:
                problems.append(f"{relative}: managed-file hash mismatch")
    return problems


def main() -> int:
    problems = check(ROOT)
    if problems:
        print("\n".join(problems))
        print(
            "Review drift and restore or regenerate through Spec Kit; do not rehash local edits."
        )
        return 1
    print("Spec Kit managed-file integrity checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
