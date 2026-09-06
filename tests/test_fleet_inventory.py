"""Fleet discovery must distinguish missing evidence from clean worktrees."""

import csv
import io
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "skills/audit-repo-fleet/scripts/inventory.sh"


class FleetInventoryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def git(self, path, *args):
        return subprocess.run(
            ["git", "-C", str(path), *args], check=True,
            capture_output=True, text=True,
        )

    def repository(self, name):
        path = self.root / name
        path.mkdir()
        self.git(path, "init", "-q")
        return path

    def inventory(self):
        result = subprocess.run(
            ["bash", str(SCRIPT), str(self.root)],
            capture_output=True, text=True, check=False, timeout=20,
        )
        rows = {row["repository"]: row for row in csv.DictReader(io.StringIO(result.stdout), delimiter="\t")}
        return result, rows

    def test_invalid_marker_does_not_report_a_clean_repository(self):
        (self.root / "invalid" / ".git").mkdir(parents=True)
        self.repository("valid")
        result, rows = self.inventory()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("invalid", rows)
        self.assertEqual(rows["valid"]["tracked_changes"], "0")
        self.assertIn("unavailable repository: invalid", result.stderr)

    def test_bare_storage_is_excluded_but_linked_worktree_is_observed(self):
        repository = self.repository("storage")
        self.git(repository, "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "commit", "--allow-empty", "-qm", "initial")
        self.git(repository, "worktree", "add", "--detach", str(self.root / "linked"))
        self.git(repository, "config", "core.bare", "true")
        (self.root / "linked" / "new.txt").write_text("untracked\n")
        result, rows = self.inventory()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("storage", rows)
        self.assertEqual(rows["linked"]["untracked"], "1")
        self.assertIn("excluded bare repository: storage", result.stderr)

    def test_unreadable_index_is_unknown_and_other_repositories_continue(self):
        broken = self.repository("broken")
        (broken / ".git" / "index").write_bytes(b"broken index")
        self.repository("healthy")
        result, rows = self.inventory()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(rows["broken"]["tracked_changes"], "unknown")
        self.assertEqual(rows["broken"]["untracked"], "unknown")
        self.assertEqual(rows["healthy"]["tracked_changes"], "0")
        self.assertIn("unavailable worktree status: broken", result.stderr)

    @unittest.skipUnless(os.name == "posix" and os.geteuid() != 0, "requires POSIX directory permissions")
    def test_partial_discovery_does_not_return_success(self):
        self.repository("healthy")
        hidden = self.root / "unreadable"
        hidden.mkdir()
        hidden.chmod(0)
        try:
            result, rows = self.inventory()
        finally:
            hidden.chmod(0o700)
        self.assertEqual(result.returncode, 1)
        self.assertIn("healthy", rows)
        self.assertIn("unreadable", result.stderr)


if __name__ == "__main__":
    unittest.main()
