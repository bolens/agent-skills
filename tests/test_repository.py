from __future__ import annotations

import json
import subprocess
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
