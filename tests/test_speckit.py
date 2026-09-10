import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

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
        override = self.root / ".specify/templates/overrides/spec-template.md"
        override.parent.mkdir()
        override.write_text("Project-owned template override.\n")
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
        for relative, digest, expected in (
            ("../escape", "a" * 64, "invalid managed path"),
            ("/escape", "a" * 64, "invalid managed path"),
            ("", "a" * 64, "invalid managed path"),
            ("./file", "a" * 64, "invalid managed path"),
            ("dir//file", "a" * 64, "invalid managed path"),
            ("dir\\file", "a" * 64, "invalid managed path"),
            ("file", None, "invalid SHA-256 digest"),
            ("file", "bad", "invalid SHA-256 digest"),
            ("file", "A" * 64, "invalid SHA-256 digest"),
            ("file", "a" * 63, "invalid SHA-256 digest"),
        ):
            with self.subTest(relative=relative, digest=digest):
                self.write_manifest(
                    "codex", {"integration": "codex", "files": {relative: digest}}
                )
                self.assertIn(expected, "\n".join(speckit.check(self.root)))

    def test_manifest_identity_encoding_and_field_types_are_rejected(self):
        manifest = self.manifest_path("codex")
        for content in (
            b"\xff",
            b'{"integration":"speckit","files":{"file":"digest"}}',
            b'{"integration":"codex","files":null}',
            b'{"integration":"codex","files":42}',
            b'{"integration":"codex","files":"file"}',
        ):
            with self.subTest(content=content):
                manifest.write_bytes(content)
                result = self.run_cli()
                self.assertEqual(1, result.returncode)
                self.assertIn("invalid or missing manifest", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_unrelated_skills_and_unrecorded_core_additions(self):
        unrelated = self.root / ".agents/skills/local-helper/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("Local helper")
        self.assertEqual([], speckit.check(self.root))
        for relative in (
            ".specify/templates/new-template.md",
            ".specify/scripts/bash/new-helper.sh",
            ".agents/skills/speckit-new/SKILL.md",
        ):
            with self.subTest(relative=relative):
                target = self.root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("Unrecorded content")
                self.assertIn(
                    f"{relative}: missing from", "\n".join(speckit.check(self.root))
                )
                target.unlink()

    def test_multiple_failures_are_aggregated_without_repair(self):
        for paths in self.paths.values():
            (self.root / paths[0]).write_bytes(b"changed")
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        problems = speckit.check(self.root)
        self.assertEqual(2, len(problems), problems)
        self.assertTrue(all("hash mismatch" in p for p in problems))
        self.assertEqual(
            before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        )

    def test_directories_and_dangling_symlinks_fail(self):
        for target in (self.manifest_path("codex"), self.root / self.paths["codex"][0]):
            original = target.read_bytes()
            target.unlink()
            target.mkdir()
            self.assertIn("regular file", "\n".join(speckit.check(self.root)))
            target.rmdir()
            target.symlink_to(self.root / "absent")
            self.assertIn("symlink", "\n".join(speckit.check(self.root)))
            target.unlink()
            target.write_bytes(original)

    def test_read_errors_are_diagnostics_and_other_integrations_are_checked(self):
        original_read = Path.read_bytes
        (self.root / self.paths["codex"][0]).write_bytes(b"changed")
        for target in (
            self.manifest_path("speckit"),
            self.root / self.paths["speckit"][0],
        ):
            with self.subTest(path=target):

                def read(path, denied=target):
                    if path == denied:
                        raise PermissionError("fixture read denied")
                    return original_read(path)

                with mock.patch.object(Path, "read_bytes", read):
                    problems = speckit.check(self.root)
                self.assertEqual(2, len(problems), problems)
                self.assertIn("fixture read denied", problems[0])
                self.assertIn("hash mismatch", problems[1])

    def test_removed_manifest_entries_leave_no_existing_surface_unchecked(self):
        for integration, paths in self.paths.items():
            manifest = self.manifest_path(integration)
            original = manifest.read_bytes()
            for relative in paths:
                with self.subTest(path=relative):
                    content = json.loads(original)
                    del content["files"][relative]
                    # Keep a valid nonempty manifest even for the one-entry fixture.
                    content["files"]["retained.txt"] = hashlib.sha256(
                        b"retained"
                    ).hexdigest()
                    (self.root / "retained.txt").write_bytes(b"retained")
                    self.write_manifest(integration, content)
                    self.assertIn(
                        f"{relative}: missing from", "\n".join(speckit.check(self.root))
                    )
                    manifest.write_bytes(original)

    def run_cli(self):
        script = self.root / "scripts/check-speckit.py"
        script.parent.mkdir(exist_ok=True)
        shutil.copyfile(SCRIPT, script)
        return subprocess.run(
            [sys.executable, str(script)],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    def test_cli_reports_success_and_drift_with_exit_status(self):
        self.assertEqual(0, self.run_cli().returncode)
        (self.root / self.paths["codex"][0]).write_text("changed")
        result = self.run_cli()
        self.assertEqual(1, result.returncode)
        self.assertIn("hash mismatch", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    @unittest.skipUnless(hasattr(os, "mkfifo"), "named pipes require POSIX")
    def test_named_pipe_manifests_and_managed_files_fail_without_blocking(self):
        for target in (self.manifest_path("codex"), self.root / self.paths["codex"][0]):
            with self.subTest(path=target):
                original = target.read_bytes()
                target.unlink()
                os.mkfifo(target)
                try:
                    result = self.run_cli()
                    self.assertEqual(1, result.returncode)
                    self.assertIn("regular file", result.stdout)
                finally:
                    target.unlink()
                    target.write_bytes(original)

    def test_symlink_manifest_is_rejected(self):
        manifest = self.manifest_path("codex")
        destination = self.root / "saved-manifest.json"
        manifest.rename(destination)
        manifest.symlink_to(destination)
        self.assertIn("symlink", "\n".join(speckit.check(self.root)))

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
