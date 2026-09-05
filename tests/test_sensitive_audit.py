from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCANNER = Path(__file__).resolve().parents[1] / "skills/sensitive-info-audit/scripts/audit-sensitive.py"
# Synthetic detector fixture, assembled to avoid looking like a stored credential.
SECRET = "ghp_" + "a" * 36


class SensitiveAudit(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def scan(self, path: Path, *options: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCANNER), str(path), *options],
            capture_output=True, text=True, timeout=10,
        )

    def test_missing_input_is_unavailable(self) -> None:
        result = self.scan(self.root / "missing")
        self.assertEqual(2, result.returncode)
        self.assertNotIn("summary secrets=0", result.stdout)

    def test_single_file_is_scanned_and_secrets_are_redacted(self) -> None:
        candidate = self.root / "candidate.txt"
        candidate.write_text(SECRET)
        result = self.scan(candidate)
        self.assertEqual(1, result.returncode)
        self.assertIn("github-token", result.stdout)
        self.assertNotIn(SECRET, result.stdout + result.stderr)

    def test_empty_directory_reports_zero_scanned(self) -> None:
        result = self.scan(self.root)
        self.assertEqual(0, result.returncode)
        self.assertIn("scanned=0", result.stdout)

    def test_oversized_file_makes_scan_incomplete(self) -> None:
        (self.root / "large.txt").write_text("ordinary text")
        result = self.scan(self.root, "--max-bytes", "3")
        self.assertEqual(2, result.returncode)
        self.assertIn("large.txt", result.stdout)
        self.assertIn("skipped=1", result.stdout)

    def test_secret_status_wins_over_incomplete_scan(self) -> None:
        (self.root / "secret.txt").write_text(SECRET)
        (self.root / "large.txt").write_text("x" * 200)
        result = self.scan(self.root, "--max-bytes", "100")
        self.assertEqual(1, result.returncode)
        self.assertIn("skipped=1", result.stdout)

    @unittest.skipUnless(hasattr(os, "symlink"), "requires symlinks")
    def test_symlink_scans_link_text_without_reading_external_file(self) -> None:
        candidate = self.root / "candidate"
        candidate.mkdir()
        external = self.root / "external.txt"
        external.write_text(SECRET)
        (candidate / "link").symlink_to(external)
        result = self.scan(candidate)
        self.assertEqual(0, result.returncode)
        self.assertNotIn("github-token", result.stdout)
        self.assertIn("scanned=1", result.stdout)

    def test_git_scope_preserves_untracked_opt_in_and_reports_missing_files(self) -> None:
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        tracked = self.root / "tracked.txt"
        tracked.write_text("ordinary text")
        subprocess.run(["git", "-C", str(self.root), "add", "tracked.txt"], check=True)
        (self.root / "untracked.txt").write_text(SECRET)
        self.assertEqual(0, self.scan(self.root).returncode)
        self.assertEqual(1, self.scan(self.root, "--include-untracked").returncode)
        tracked.unlink()
        result = self.scan(self.root)
        self.assertEqual(2, result.returncode)
        self.assertIn("tracked.txt", result.stdout)


if __name__ == "__main__":
    unittest.main()
