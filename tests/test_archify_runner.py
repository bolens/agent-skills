"""Verify the fork test adapter preserves coverage and fails on contract drift."""

import argparse
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("test_archify", Path(__file__).resolve().parents[1] / "scripts/test_archify.py")
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


class ArchifyRunnerTests(unittest.TestCase):
    def test_shard_boundaries(self):
        for valid in ("1/1", "1/2", "2/2"):
            self.assertEqual(RUNNER.shard(valid), valid)
        for invalid in ("0/2", "3/2", "1/0", "1", "-1/2", "1/100", "01/2"):
            with self.subTest(invalid=invalid), self.assertRaises(argparse.ArgumentTypeError):
                RUNNER.shard(invalid)

    def test_stage_replaces_runtime_and_adapts_exact_notice_version(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, workspace = root / "local", root / "upstream"
            source.mkdir()
            (workspace / "archify").mkdir(parents=True)
            (workspace / "scripts").mkdir()
            for path, version in ((source, "16.29.0"), (workspace / "archify", "16.28.0")):
                (path / "package.json").write_text(json.dumps({"devDependencies": {"simple-icons": version}}))
            (source / "runtime.mjs").write_text("local fork")
            (source / "THIRD_PARTY_NOTICES.md").write_text("complete local notices")
            (source / "node_modules").mkdir()
            (source / "node_modules/generated").touch()
            (workspace / "archify/stale.mjs").touch()
            contract = workspace / "scripts/third-party-notices-contract.mjs"
            contract.write_text("16.28.0\n" * 4 + "keep every disclosure check")
            RUNNER.stage_skill(source, workspace)
            self.assertEqual((workspace / "archify/runtime.mjs").read_text(), "local fork")
            self.assertFalse((workspace / "archify/stale.mjs").exists())
            self.assertEqual((workspace / "THIRD_PARTY_NOTICES.md").read_text(), "complete local notices")
            self.assertFalse((workspace / "archify/node_modules").exists())
            self.assertEqual(contract.read_text(), "16.29.0\n" * 4 + "keep every disclosure check")


if __name__ == "__main__":
    unittest.main()
