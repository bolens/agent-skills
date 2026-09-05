#!/usr/bin/env python3
"""Report whether audited hard-fork upstream refs have advanced."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--check", action="store_true", help="fail when an upstream advanced")
parser.add_argument("--json", action="store_true", dest="as_json")
args = parser.parse_args()
sources = json.loads((ROOT / "UPSTREAMS.json").read_text())["skills"]
resolved: dict[tuple[str, str], tuple[Optional[str], Optional[str]]] = {}
results = []

for name, source in sorted(sources.items()):
    key = source["url"], source["branch"]
    if key not in resolved:
        probe = subprocess.run(
            ["git", "ls-remote", source["url"], f"refs/heads/{source['branch']}"],
            text=True,
            capture_output=True,
        )
        if probe.returncode or not probe.stdout.strip():
            resolved[key] = None, (probe.stderr.strip() or "branch not found")
        else:
            resolved[key] = probe.stdout.split()[0], None
    current, error = resolved[key]
    status = "error" if error else "current" if current == source["audited_ref"] else "update-available"
    results.append({"name": name, "status": status, "audited_ref": source["audited_ref"], "current_ref": current, "error": error})

if args.as_json:
    print(json.dumps(results, indent=2))
else:
    for result in results:
        print(f"{result['status']}\t{result['name']}\t{result['audited_ref']}\t{result['error'] or result['current_ref']}")

errors = any(result["status"] == "error" for result in results)
updates = any(result["status"] == "update-available" for result in results)
raise SystemExit(2 if errors else 1 if args.check and updates else 0)
