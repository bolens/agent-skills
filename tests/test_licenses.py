from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LicenseRetention(unittest.TestCase):
    def test_integration_and_bundled_dependency_notices_are_retained(self) -> None:
        # Exact upstream copies audited in LICENSE.md and Archify's notices.
        copies = {
            ".specify/LICENSE": "2510b446bc1f0cf9702453075d20cd88631e20e5642658edb7325d9c1eb534f7",
            "skills/archify/licenses/Apache-2.0.txt": "0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594",
            "skills/archify/licenses/ajv-LICENSE": "a05350a88e318e4f5f2c2a1ff1e2e88daa4dd38e6e78b71cccae422bdc762cc3",
            "skills/archify/licenses/javascript-LICENSE": "0d3f7c086c6b6cf3ea4aac714e9aa3e1fb02e355ce35bd21c56acf8d04390885",
            "skills/archify/licenses/simple-icons-DISCLAIMER.md": "5757a1f28eff735a8b5e7425478f367812d71e974530f5bedd01219480965f4a",
            "skills/archify/licenses/simple-icons-LICENSE.md": "9046848b63a5c92bff14e4accca80bd987e0623b74adf9226ce5198d312b79d5",
        }
        for relative, expected in copies.items():
            with self.subTest(path=relative):
                path = ROOT / relative
                self.assertFalse(path.is_symlink())
                self.assertEqual(expected, hashlib.sha256(path.read_bytes()).hexdigest())

    def test_validation_requires_a_bundled_unchanged_license(self) -> None:
        for change, expected in (
            ("intact", None),
            ("deleted", "missing bundled upstream license"),
            ("edited", "upstream license copy changed without audit"),
            ("unrecorded", "missing upstream license metadata"),
            ("external", "invalid license path"),
            ("symlink", "missing bundled upstream license"),
        ):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                script = root / "scripts" / "validate.py"
                script.parent.mkdir()
                shutil.copyfile(ROOT / "scripts" / "validate.py", script)
                skill = root / "skills" / "example"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(
                    "---\nname: example\ndescription: Example fixture\n---\n"
                )
                (skill / "UPSTREAM.md").write_text("This is a hard fork.\n")
                content = b"Synthetic copyright and permission notice for testing.\n"
                notice = skill / "LICENSE"
                notice.write_bytes(content)
                license = {
                    "spdx": "MIT",
                    "path": "LICENSE",
                    "upstream_path": "LICENSE",
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
                if change == "deleted":
                    notice.unlink()
                elif change == "edited":
                    notice.write_text("Removed attribution.\n")
                elif change == "external":
                    license["path"] = "../../LICENSE"
                elif change == "symlink":
                    target = root / "LICENSE"
                    notice.rename(target)
                    notice.symlink_to(target)
                origin = {"type": "git", "ref": "a" * 40}
                source = {}
                if change != "unrecorded":
                    origin["license"] = license
                    source["license"] = license
                (root / "UPSTREAMS.json").write_text(json.dumps({"skills": {"example": source}}))
                (root / "PROVENANCE.json").write_text(json.dumps({"skills": [
                    {"name": "example", "hard_fork": True, "origin": origin}
                ]}))
                result = subprocess.run(
                    [sys.executable, str(script)], capture_output=True, text=True
                )
                if expected is None:
                    self.assertEqual(0, result.returncode, result.stderr)
                else:
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(expected, result.stderr)


if __name__ == "__main__":
    unittest.main()
