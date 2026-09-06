#!/usr/bin/env python3
"""Test the local Archify fork using its exact audited upstream test workspace."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def shard(value: str) -> str:
    """Accept a one-based, nonempty Node test partition."""
    if not re.fullmatch(r"[1-9][0-9]?/[1-9][0-9]?", value):
        raise argparse.ArgumentTypeError("shard must be INDEX/COUNT")
    index, count = map(int, value.split("/"))
    if index > count:
        raise argparse.ArgumentTypeError("shard index exceeds count")
    return value


def stage_skill(source: Path, workspace: Path) -> None:
    """Replace upstream runtime files; retain only its external test fixtures."""
    destination = workspace / "archify"
    upstream = json.loads((destination / "package.json").read_text())
    local = json.loads((source / "package.json").read_text())
    old_version = upstream["devDependencies"]["simple-icons"]
    new_version = local["devDependencies"]["simple-icons"]
    if not all(re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", value) for value in (old_version, new_version)):
        raise ValueError("Simple Icons notice checks require exact dependency versions")
    # The upstream harness hardcodes its dependency version in four disclosure
    # checks. Require the fork's pinned version while retaining every check.
    contract = workspace / "scripts/third-party-notices-contract.mjs"
    content = contract.read_text()
    if old_version != new_version:
        if content.count(old_version) != 4:
            raise ValueError("Upstream notice contract changed; review the adapter")
        contract.write_text(content.replace(old_version, new_version))
    # Upstream packaging requires the root and packaged notices to byte-match.
    # Mirror the fork notice into the disposable harness, never into the fork.
    shutil.copyfile(source / "THIRD_PARTY_NOTICES.md", workspace / "THIRD_PARTY_NOTICES.md")
    shutil.rmtree(destination)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("node_modules", "__pycache__", ".git"))


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shard", type=shard, default="1/1")
    parser.add_argument("--browser", action="store_true", help="run serialized WebM and site browser checks")
    args = parser.parse_args()
    node_major = subprocess.check_output(["node", "-p", "process.versions.node.split('.')[0]"], text=True).strip()
    if node_major != "22":
        parser.error("the upstream archive test harness requires Node 22")
    upstream = json.loads((ROOT / "UPSTREAMS.json").read_text())["skills"]["archify"]
    if upstream["url"] != "https://github.com/tt-a1i/archify" or upstream["path"] != "archify":
        raise ValueError("Review the test adapter when changing Archify's source")
    if not re.fullmatch(r"[0-9a-f]{40}", upstream["audited_ref"]):
        raise ValueError("The test harness requires an immutable audited revision")
    with tempfile.TemporaryDirectory(prefix="archify-ci-") as temporary:
        workspace = Path(temporary)
        run(["git", "init", "--quiet"], workspace)
        run(["git", "fetch", "--depth=1", upstream["url"], upstream["audited_ref"]], workspace)
        run(["git", "checkout", "--quiet", "--detach", "FETCH_HEAD"], workspace)
        stage_skill(ROOT / "skills/archify", workspace)
        # Packaging tests use the Git index to select files. Include this fork's
        # additions and removals in the disposable index, without publishing it.
        run(["git", "add", "--", "archify", "THIRD_PARTY_NOTICES.md", "scripts/third-party-notices-contract.mjs"], workspace)
        skill = workspace / "archify"
        run(["npm", "ci", "--ignore-scripts", "--no-audit"], skill)
        if args.browser:
            run(["npm", "run", "test:webm"], skill)
        else:
            # The upstream ZIP represents upstream bytes, not this fork. Build
            # its fixture once so timezone/reproducibility tests compare the fork.
            run(["bash", "scripts/build-zip.sh", "archify.zip"], workspace)
            if args.shard.startswith("1/"):
                for target in ("check:brand-marks", "check:validators", "check:release-identity"):
                    run(["npm", "run", target], skill)
                run(["node", "test/golden.mjs"], skill)
            files = sorted(path.relative_to(skill).as_posix() for path in (skill / "test").glob("*.test.mjs"))
            if len(files) < int(args.shard.split("/")[1]):
                raise ValueError("Shard count exceeds discovered test files")
            run(["node", "--test", "--test-concurrency=2", "--test-shard=" + args.shard, *files], skill)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
