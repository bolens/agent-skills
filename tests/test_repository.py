from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RepositoryContract(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads((ROOT / "PROVENANCE.json").read_text())

    def test_all_skills_are_hard_forks(self) -> None:
        self.assertTrue(self.manifest["skills"])
        self.assertTrue(all(entry["hard_fork"] is True for entry in self.manifest["skills"]))

    def test_sources_have_stable_identity(self) -> None:
        for entry in self.manifest["skills"]:
            origin = entry["origin"]
            self.assertIn(origin["type"], {"git", "local-original"})
            self.assertTrue(origin.get("url") or origin.get("ref"))

    def test_git_sources_have_audited_refs(self) -> None:
        for entry in self.manifest["skills"]:
            origin = entry["origin"]
            if origin["type"] == "git":
                self.assertRegex(origin["ref"], r"^[0-9a-f]{40}$")
                self.assertTrue(origin["branch"])

    def test_generated_upstream_pointers_exist(self) -> None:
        for entry in self.manifest["skills"]:
            pointer = ROOT / "skills" / entry["name"] / "UPSTREAM.md"
            self.assertIn("hard fork", pointer.read_text().lower())

    def test_skills_target_shared_and_claude_homes(self) -> None:
        for entry in self.manifest["skills"]:
            targets = entry["install_targets"]
            name = entry["name"]
            self.assertIn(f"${{AGENTS_HOME:-$HOME/.agents}}/skills/{name}", targets)
            self.assertIn(f"${{CLAUDE_HOME:-$HOME/.claude}}/skills/{name}", targets)

    def test_link_installer_supports_all_global_homes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            env = {
                **os.environ,
                "CODEX_HOME": str(root / "codex"),
                "AGENTS_HOME": str(root / "agents"),
                "CLAUDE_HOME": str(root / "claude"),
            }
            installer = ROOT / "scripts" / "link-installed.py"
            subprocess.run([sys.executable, str(installer), "--apply"], check=True, env=env, stdout=subprocess.DEVNULL)
            subprocess.run([sys.executable, str(installer), "--check"], check=True, env=env)
            for home in ("agents", "claude"):
                for entry in self.manifest["skills"]:
                    self.assertTrue((root / home / "skills" / entry["name"]).is_symlink())

    def test_hook_installer_supports_linked_worktrees(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            repository = root / "repository"
            worktree = root / "worktree"
            subprocess.run(["git", "init", "-q", str(repository)], check=True)
            subprocess.run(
                ["git", "-C", str(repository), "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "--allow-empty", "-qm", "initial"],
                check=True,
            )
            subprocess.run(["git", "-C", str(repository), "worktree", "add", "--detach", "-q", str(worktree)], check=True)
            installer = ROOT / "scripts" / "install-git-hooks.py"
            subprocess.run([sys.executable, str(installer), "--repository", str(worktree)], check=True, stdout=subprocess.DEVNULL)
            hook_path = subprocess.run(
                ["git", "rev-parse", "--git-path", "hooks/pre-commit"],
                cwd=worktree,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            hook = Path(hook_path)
            if not hook.is_absolute():
                hook = worktree / hook
            self.assertEqual("#!/bin/sh", hook.read_text(encoding="utf-8").splitlines()[0])
            self.assertTrue(os.access(hook, os.X_OK))

    def test_fleet_inventory_handles_repositories_without_workflows(self) -> None:
        inventory = ROOT / "skills" / "audit-repo-fleet" / "scripts" / "inventory.sh"
        with tempfile.TemporaryDirectory() as directory:
            fleet = Path(directory)
            subprocess.run(["git", "init", "-q", str(fleet / "alpha")], check=True)
            subprocess.run(["git", "init", "-q", str(fleet / "group" / "beta")], check=True)
            output = subprocess.run(
                [str(inventory), str(fleet)],
                check=True,
                capture_output=True,
                text=True,
            ).stdout
        self.assertIn("alpha\t", output)
        self.assertIn("group/beta\t", output)
        self.assertEqual(3, len(output.splitlines()))


if __name__ == "__main__":
    unittest.main()
