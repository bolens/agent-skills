#!/usr/bin/env python3
"""Generate hard-fork provenance records and per-skill pointers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"

EXTERNAL = {
    "archify": ("https://github.com/tt-a1i/archify", ".", None),
    "caveman": ("https://github.com/JuliusBrussee/caveman", "caveman", None),
    "caveman-commit": ("https://github.com/JuliusBrussee/caveman", "skills/caveman-commit", None),
    "caveman-compress": ("https://github.com/JuliusBrussee/caveman", "caveman-compress", None),
    "caveman-help": ("https://github.com/JuliusBrussee/caveman", "skills/caveman-help", None),
    "caveman-review": ("https://github.com/JuliusBrussee/caveman", "skills/caveman-review", None),
    "find-skills": ("https://github.com/vercel-labs/skills", "skills/find-skills", None),
    "diagnose-crash": ("https://github.com/basecamp/omarchy", "default/agents/skills/diagnose-crash", "6dae136d113054f8e8613f172a89c507634ef230"),
    "omarchy": ("https://github.com/basecamp/omarchy", "default/agents/skills/omarchy", "6dae136d113054f8e8613f172a89c507634ef230"),
}

AGENT_ONLY = {"caveman", "caveman-commit", "caveman-compress", "caveman-help", "caveman-review", "find-skills"}
DUAL_TARGET = {"diagnose-crash", "omarchy"}


def records() -> list[dict[str, object]]:
    result = []
    for directory in sorted(path for path in SKILLS.iterdir() if path.is_dir()):
        name = directory.name
        targets = [f"${{CODEX_HOME:-$HOME/.codex}}/skills/{name}"]
        if name in AGENT_ONLY:
            targets = [f"${{AGENTS_HOME:-$HOME/.agents}}/skills/{name}"]
        elif name in DUAL_TARGET:
            targets.append(f"${{AGENTS_HOME:-$HOME/.agents}}/skills/{name}")
        if name in EXTERNAL:
            url, source_path, source_ref = EXTERNAL[name]
            origin = {"type": "git", "url": url, "path": source_path}
            if source_ref:
                origin["ref"] = source_ref
        else:
            origin = {
                "type": "local-original",
                "ref": f"local://codex/skills/{name}",
                "imported_from": f"${{CODEX_HOME:-$HOME/.codex}}/skills/{name}",
            }
        result.append({"name": name, "hard_fork": True, "origin": origin, "install_targets": targets})
    return result


def upstream_text(record: dict[str, object]) -> str:
    origin = record["origin"]
    assert isinstance(origin, dict)
    lines = ["# Upstream", "", "This skill is maintained here as a **hard fork**.", ""]
    if origin["type"] == "git":
        lines += [f"Original project: [{origin['url']}]({origin['url']})", "", f"Original path: `{origin['path']}`"]
        if "ref" in origin:
            lines += ["", f"Imported reference: `{origin['ref']}`"]
    else:
        lines += ["Original: locally authored personal skill", "", f"Original reference: `{origin['ref']}`", "", f"Initial import path: `{origin['imported_from']}`"]
    lines += ["", "Updates are reviewed and merged manually. This fork does not track or represent upstream releases.", "", "See [`../../PROVENANCE.json`](../../PROVENANCE.json) for the machine-readable record.", ""]
    return "\n".join(lines)


def render() -> tuple[str, dict[Path, str]]:
    entries = records()
    manifest = json.dumps({"schema_version": 1, "fork_policy": "hard", "skills": entries}, indent=2) + "\n"
    pointers = {SKILLS / str(entry["name"]) / "UPSTREAM.md": upstream_text(entry) for entry in entries}
    return manifest, pointers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest, pointers = render()
    expected = {ROOT / "PROVENANCE.json": manifest, **pointers}
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, text in expected.items() if not path.is_file() or path.read_text() != text]
        if stale:
            print("stale generated provenance:")
            print("\n".join(f"- {path}" for path in stale))
            return 1
        print(f"provenance is current ({len(pointers)} skills)")
        return 0
    for path, text in expected.items():
        path.write_text(text)
    print(f"updated provenance for {len(pointers)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
