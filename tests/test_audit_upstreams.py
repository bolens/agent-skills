import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit-upstreams.py"
SPEC = importlib.util.spec_from_file_location("audit_upstreams", SCRIPT)
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class AuditUpstreams(unittest.TestCase):
    def test_missing_git_still_emits_a_structured_result(self):
        with tempfile.TemporaryDirectory() as empty_path:
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--json", "--check"],
                env={**os.environ, "PATH": empty_path},
                capture_output=True,
                text=True,
                timeout=10,
            )

        self.assertEqual(2, result.returncode, result.stderr)
        rows = json.loads(result.stdout)
        self.assertTrue(rows)
        self.assertTrue(all(row["status"] == "error" and "could not run Git" in row["error"] for row in rows))

    def test_lookup_has_a_deadline_and_disables_prompts(self):
        with patch.object(AUDIT.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 30)) as git:
            tip, error = AUDIT.branch_tip("https://example.invalid/project", "main")
        self.assertIsNone(tip)
        self.assertIn("timed out", error)
        self.assertEqual(30, git.call_args.kwargs["timeout"])
        self.assertEqual("0", git.call_args.kwargs["env"]["GIT_TERMINAL_PROMPT"])

    def test_lookup_uses_only_the_requested_ref(self):
        shallow = "a" * 40
        actual = "b" * 40
        other_ref = f"{shallow}\trefs/heads/ref/refs/heads/main\n"
        exact_ref = f"{actual}\trefs/heads/main\n"

        with patch.object(AUDIT.subprocess, "run") as git:
            git.return_value = subprocess.CompletedProcess("git", 0, other_ref + exact_ref, "")
            self.assertEqual((actual, None), AUDIT.branch_tip("https://example.invalid/project", "main"))
            git.return_value = subprocess.CompletedProcess("git", 0, other_ref, "")
            self.assertEqual((None, "Git did not return the exact branch ref"),
                             AUDIT.branch_tip("https://example.invalid/project", "main"))
            git.return_value = subprocess.CompletedProcess("git", 2, "", "")
            self.assertEqual((None, "branch not found"), AUDIT.branch_tip("https://example.invalid/project", "main"))
