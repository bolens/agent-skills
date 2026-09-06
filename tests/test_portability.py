import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check-portability.py"
spec = importlib.util.spec_from_file_location("portability", SCRIPT)
portability = importlib.util.module_from_spec(spec)
spec.loader.exec_module(portability)


class GeneratedEnvironmentBoundary(unittest.TestCase):
    def test_local_environment_state_is_excluded_but_source_is_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (".devenv/generated.sh", ".devenv.test123/generated.sh", ".direnv/generated.sh", ".devenv.flake.nix", "devenv.nix", "script.sh"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("source\n")
            with mock.patch.object(portability, "ROOT", root):
                files = {p.relative_to(root).as_posix() for p in portability.files()}
            self.assertEqual(files, {"devenv.nix", "script.sh"})


class ManagedShellBoundary(unittest.TestCase):
    def run_check(self, source, *, managed=True, changed=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = ".specify/scripts/bash/example.sh"
            script = root / relative
            script.parent.mkdir(parents=True)
            script.write_text(source)
            if managed:
                manifest = root / ".specify/integrations/speckit.manifest.json"
                manifest.parent.mkdir(parents=True)
                manifest.write_text(json.dumps({"files": {
                    relative: hashlib.sha256(script.read_bytes()).hexdigest(),
                }}))
            if changed:
                script.write_text(source + "# altered after generation\n")
            checked = []

            def run(argv, **kwargs):
                checked.append(argv[0])
                # Model upstream ShellCheck warnings while checking real syntax.
                if argv[0] == "test-shellcheck":
                    return mock.Mock(returncode=1)
                return original_run(argv, **kwargs)

            original_run = portability.subprocess.run
            output = io.StringIO()
            with mock.patch.object(portability, "ROOT", root), \
                 mock.patch.object(portability.shutil, "which", return_value="test-shellcheck"), \
                 mock.patch.object(portability.subprocess, "run", side_effect=run), \
                 contextlib.redirect_stdout(output):
                result = portability.main()
            return result, checked, output.getvalue()

    def test_generated_helpers_keep_hash_and_syntax_validation(self):
        result, checked, _ = self.run_check("#!/usr/bin/env bash\ntrue\n")
        self.assertEqual(0, result)
        self.assertIn("bash", checked)
        self.assertNotIn("test-shellcheck", checked)

    def test_modified_generated_helper_is_rejected(self):
        result, _, output = self.run_check("#!/usr/bin/env bash\ntrue\n", changed=True)
        self.assertEqual(1, result)
        self.assertIn("managed-file hash mismatch", output)

    def test_generated_helper_still_requires_valid_bash(self):
        result, _, output = self.run_check("#!/usr/bin/env bash\nif then\n")
        self.assertEqual(1, result)
        self.assertIn("Bash syntax failed", output)

    def test_unmanaged_helper_still_requires_shellcheck(self):
        result, checked, output = self.run_check("#!/usr/bin/env bash\ntrue\n", managed=False)
        self.assertEqual(1, result)
        self.assertIn("test-shellcheck", checked)
        self.assertIn("ShellCheck failed", output)


if __name__ == "__main__":
    unittest.main()
