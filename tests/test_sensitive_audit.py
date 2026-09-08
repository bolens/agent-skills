from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCANNER = Path(__file__).resolve().parents[1] / "skills/sensitive-info-audit/scripts/audit-sensitive.py"
# Fabricated detector input only: fixed repeated characters, never a credential.
DETECTOR_FIXTURE = "ghp_" + "a" * 36


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
        candidate.write_text(DETECTOR_FIXTURE)
        result = self.scan(candidate)
        self.assertEqual(1, result.returncode)
        self.assertIn("github-token", result.stdout)
        self.assertNotIn(DETECTOR_FIXTURE, result.stdout + result.stderr)

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
        (self.root / "secret.txt").write_text(DETECTOR_FIXTURE)
        (self.root / "large.txt").write_text("x" * 200)
        result = self.scan(self.root, "--max-bytes", "100")
        self.assertEqual(1, result.returncode)
        self.assertIn("skipped=1", result.stdout)

    @unittest.skipUnless(hasattr(os, "symlink"), "requires symlinks")
    def test_symlink_scans_link_text_without_reading_external_file(self) -> None:
        candidate = self.root / "candidate"
        candidate.mkdir()
        external = self.root / "external.txt"
        external.write_text(DETECTOR_FIXTURE)
        (candidate / "link").symlink_to(external)
        result = self.scan(candidate)
        self.assertEqual(0, result.returncode)
        self.assertNotIn("github-token", result.stdout)
        self.assertIn("scanned=1", result.stdout)

    def test_long_nonmatching_tokens_finish_without_backtracking_stall(self) -> None:
        candidate = self.root / "long.txt"
        candidate.write_bytes(b"a" * 1000000 + b"\n" + b"a" * 1000000 + b"@invalid\n")
        result = self.scan(candidate)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("scanned=1", result.stdout)

    def test_email_detection_retains_punctuation_and_plus_addresses(self) -> None:
        candidate = self.root / "addresses.txt"
        candidate.write_text("<person+tag@example.org>\nfirst.last@example.net\n")
        result = self.scan(candidate)
        self.assertEqual(0, result.returncode)
        self.assertIn("privacy_review=2", result.stdout)
        self.assertNotIn("person+tag", result.stdout)

    @unittest.skipUnless(os.name == "posix", "race fixtures require POSIX file types")
    def test_changed_candidates_are_incomplete_and_never_followed(self) -> None:
        for mode in ("grow", "symlink", "fifo"):
            with self.subTest(mode=mode):
                candidate = self.root / mode
                candidate.write_text("small")
                external = self.root / "external"
                external.write_text(DETECTOR_FIXTURE)
                code = '''import os,runpy,sys
from pathlib import Path
from unittest.mock import patch
script, candidate, external, mode = sys.argv[1:]
original = os.open
def changed(path, flags, *args, **kwargs):
    if Path(path) == Path(candidate):
        if mode == 'grow':
            Path(path).write_text('x' * 100)
        else:
            Path(path).unlink()
            if mode == 'symlink': Path(path).symlink_to(external)
            else: os.mkfifo(path)
    return original(path, flags, *args, **kwargs)
sys.argv = [script, candidate, '--max-bytes', '50']
with patch('os.open', side_effect=changed):
    runpy.run_path(script, run_name='__main__')
'''
                result = subprocess.run([sys.executable, "-c", code, str(SCANNER), str(candidate), str(external), mode], capture_output=True, text=True, timeout=3, check=False)
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn("skipped=1 scanned=0", result.stdout)
                self.assertNotIn("github-token", result.stdout)
                self.assertEqual(DETECTOR_FIXTURE, external.read_text())

    def test_report_order_is_independent_of_file_creation_order(self) -> None:
        reports = []
        for name, order in [('first', ['z/file.txt', 'a/file.txt']), ('second', ['a/file.txt', 'z/file.txt'])]:
            root = self.root / name
            root.mkdir()
            for relative in order:
                candidate = root / relative
                candidate.parent.mkdir()
                candidate.write_text('person@example.org\n')
            result = self.scan(root)
            self.assertEqual(0, result.returncode, result.stderr)
            reports.append(result.stdout)
        self.assertEqual(reports[0], reports[1])
        self.assertLess(reports[0].index('a/file.txt'), reports[0].index('z/file.txt'))

    def test_git_scope_preserves_untracked_opt_in_and_reports_missing_files(self) -> None:
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        tracked = self.root / "tracked.txt"
        tracked.write_text("ordinary text")
        subprocess.run(["git", "-C", str(self.root), "add", "tracked.txt"], check=True)
        (self.root / "untracked.txt").write_text(DETECTOR_FIXTURE)
        self.assertEqual(0, self.scan(self.root).returncode)
        self.assertEqual(1, self.scan(self.root, "--include-untracked").returncode)
        tracked.unlink()
        result = self.scan(self.root)
        self.assertEqual(2, result.returncode)
        self.assertIn("tracked.txt", result.stdout)


if __name__ == "__main__":
    unittest.main()
