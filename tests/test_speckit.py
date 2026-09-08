import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check-speckit.py"
spec = importlib.util.spec_from_file_location("speckit_check", SCRIPT)
speckit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(speckit)


class ManagedIntegrationIntegrity(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.paths = {
            "speckit": [
                ".specify/templates/spec-template.md",
                ".specify/scripts/bash/common.sh",
            ],
            "codex": [".agents/skills/speckit-implement/SKILL.md"],
        }
        for integration, paths in self.paths.items():
            files = {}
            for relative in paths:
                target = self.root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(b"managed content\n")
                files[relative] = hashlib.sha256(target.read_bytes()).hexdigest()
            self.write_manifest(
                integration, {"integration": integration, "files": files}
            )

    def manifest_path(self, integration):
        return self.root / f".specify/integrations/{integration}.manifest.json"

    def write_manifest(self, integration, content):
        path = self.manifest_path(integration)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content))

    def test_intact_files_and_project_owned_memory_pass_without_writes(self):
        memory = self.root / ".specify/memory/project-guide.md"
        memory.parent.mkdir()
        memory.write_text("Local guidance can change independently.\n")
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual([], speckit.check(self.root))
        self.assertEqual(
            before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        )

    def test_changed_and_deleted_files_fail_for_every_managed_surface(self):
        for paths in self.paths.values():
            for relative in paths:
                target = self.root / relative
                original = target.read_bytes()
                for change in ("edit", "delete"):
                    with self.subTest(path=relative, change=change):
                        if change == "edit":
                            target.write_bytes(b"local edit\n")
                        else:
                            target.unlink()
                        problems = speckit.check(self.root)
                        self.assertEqual(1, len(problems), problems)
                        self.assertIn(relative, problems[0])
                        target.write_bytes(original)

    def test_missing_and_invalid_manifests_fail_cleanly(self):
        for integration in self.paths:
            manifest = self.manifest_path(integration)
            original = manifest.read_bytes()
            for content in (
                None,
                "{",
                "null",
                "[]",
                "{}",
                json.dumps({"integration": integration, "files": {}}),
                json.dumps({"integration": integration, "files": []}),
            ):
                with self.subTest(integration=integration, content=content):
                    if content is None:
                        manifest.unlink()
                    else:
                        manifest.write_text(content)
                    problems = speckit.check(self.root)
                    self.assertEqual(1, len(problems), problems)
                    self.assertIn("invalid or missing manifest", problems[0])
                    manifest.write_bytes(original)

    def test_invalid_paths_and_digests_fail(self):
        for relative, digest in (
            ("../escape", "a" * 64),
            ("/escape", "a" * 64),
            ("", "a" * 64),
            ("./file", "a" * 64),
            ("file", None),
            ("file", "bad"),
        ):
            with self.subTest(relative=relative, digest=digest):
                self.write_manifest(
                    "codex", {"integration": "codex", "files": {relative: digest}}
                )
                self.assertTrue(speckit.check(self.root))

    def test_symlink_file_and_parent_fail_even_with_matching_bytes(self):
        target = self.root / self.paths["codex"][0]
        destination = self.root / "saved"
        target.rename(destination)
        target.symlink_to(destination)
        self.assertIn("symlink", "\n".join(speckit.check(self.root)))
        target.unlink()
        destination.rename(target)
        directory = target.parent
        directory.rename(destination)
        directory.symlink_to(destination, target_is_directory=True)
        self.assertIn("symlink", "\n".join(speckit.check(self.root)))


if __name__ == "__main__":
    unittest.main()
