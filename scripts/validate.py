#!/usr/bin/env python3
"""Validate skill metadata, hard-fork provenance, and script syntax."""

from __future__ import annotations

import ast
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
NAME = re.compile(r"^[a-z0-9-]{1,63}$")


def fail(message: str) -> None:
    raise SystemExit(message)


manifest = json.loads((ROOT / "PROVENANCE.json").read_text())
records = {entry["name"]: entry for entry in manifest["skills"]}
directories = {path.name: path for path in SKILLS.iterdir() if path.is_dir()}
if set(records) != set(directories):
    fail("PROVENANCE.json skill names do not match skills/")

for name, directory in sorted(directories.items()):
    if not NAME.fullmatch(name):
        fail(f"invalid skill directory name: {name}")
    skill = directory / "SKILL.md"
    if not skill.is_file():
        fail(f"missing {skill.relative_to(ROOT)}")
    text = skill.read_text()
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        fail(f"invalid frontmatter: {skill.relative_to(ROOT)}")
    frontmatter = text.split("\n---\n", 1)[0]
    if not re.search(rf"(?m)^name:\s*{re.escape(name)}\s*$", frontmatter):
        fail(f"frontmatter name mismatch: {skill.relative_to(ROOT)}")
    if not re.search(r"(?m)^description:\s*\S", frontmatter):
        fail(f"missing description: {skill.relative_to(ROOT)}")
    if "[TODO" in text:
        fail(f"unfinished placeholder: {skill.relative_to(ROOT)}")
    if records[name].get("hard_fork") is not True:
        fail(f"skill is not marked as a hard fork: {name}")
    upstream = directory / "UPSTREAM.md"
    if not upstream.is_file() or "hard fork" not in upstream.read_text().lower():
        fail(f"missing hard-fork pointer: {name}")

for path in ROOT.rglob("*.py"):
    if ".git" not in path.parts:
        ast.parse(path.read_text(), filename=str(path))
for path in ROOT.rglob("*.sh"):
    subprocess.run(["bash", "-n", str(path)], check=True)
for path in list(ROOT.rglob("*.mjs")) + list(ROOT.rglob("*.js")):
    if "node_modules" not in path.parts:
        subprocess.run(["node", "--check", str(path)], check=True, stdout=subprocess.DEVNULL)

print(f"validated {len(directories)} hard-forked skills")
