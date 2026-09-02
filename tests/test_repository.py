from __future__ import annotations

import json
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

    def test_generated_upstream_pointers_exist(self) -> None:
        for entry in self.manifest["skills"]:
            pointer = ROOT / "skills" / entry["name"] / "UPSTREAM.md"
            self.assertIn("hard fork", pointer.read_text().lower())


if __name__ == "__main__":
    unittest.main()
