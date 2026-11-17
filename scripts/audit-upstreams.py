#!/usr/bin/env python3
"""Report whether audited hard-fork upstream refs have advanced."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GIT_TIMEOUT_SECONDS = 30


def branch_tip(url: str, branch: str) -> tuple[str | None, str | None]:
    ref = f"refs/heads/{branch}"
    try:
        probe = subprocess.run(
            ["git", "ls-remote", "--exit-code", "--refs", "--", url, ref],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            errors="replace",
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return None, f"Git lookup timed out after {GIT_TIMEOUT_SECONDS}s"
    except OSError as error:
        return None, f"could not run Git: {error}"

    if probe.returncode == 2 and not probe.stdout.strip():
        return None, "branch not found"
    if probe.returncode:
        return None, probe.stderr.strip() or f"Git exited with status {probe.returncode}"

    for line in probe.stdout.splitlines():
        oid, separator, returned_ref = line.partition("\t")
        if separator and returned_ref == ref and re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", oid):
            return oid, None
    return None, "Git did not return the exact branch ref"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when an upstream advanced")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    sources = json.loads((ROOT / "UPSTREAMS.json").read_text())["skills"]
    resolved: dict[tuple[str, str], tuple[str | None, str | None]] = {}
    results = []

    for name, source in sorted(sources.items()):
        key = source["url"], source["branch"]
        if key not in resolved:
            resolved[key] = branch_tip(*key)
        current, error = resolved[key]
        status = "error" if error else "current" if current == source["audited_ref"] else "update-available"
        results.append({
            "name": name,
            "status": status,
            "audited_ref": source["audited_ref"],
            "current_ref": current,
            "error": error,
        })

    if args.as_json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            detail = " ".join(result["error"].splitlines()) if result["error"] else result["current_ref"]
            print(f"{result['status']}\t{result['name']}\t{result['audited_ref']}\t{detail}")

    if any(result["status"] == "error" for result in results):
        return 2
    if args.check and any(result["status"] == "update-available" for result in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
