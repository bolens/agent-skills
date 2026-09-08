import os
import shlex
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASH = shutil.which("bash")
GIT = shutil.which("git")
TOOLS = (
    "git",
    "bash",
    "python3",
    "node",
    "make",
    "shellcheck",
    "ruff",
    "actionlint",
    "hadolint",
    "zizmor",
)


class DevcontainerSetup(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="setup-contract-")
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / "checkout with spaces"
        self.config = self.root / ".devcontainer"
        self.config.mkdir(parents=True)
        for name in ("smoke.sh", "post-create.sh"):
            shutil.copyfile(ROOT / ".devcontainer" / name, self.config / name)
        self.env = {
            key: value
            for key, value in os.environ.items()
            if not key.startswith("GIT_")
        }
        self.env["GIT_CONFIG_NOSYSTEM"] = "1"
        self.env["GIT_CONFIG_GLOBAL"] = os.devnull
        self.bin = self.base / "bin"
        self.bin.mkdir()
        self.env["PATH"] = str(self.bin)
        for name in (*TOOLS, "dirname"):
            if name in ("git", "bash", "dirname"):
                (self.bin / name).symlink_to(shutil.which(name))
            else:
                self.tool(name, "exit 0\n")
        subprocess.run([GIT, "init", "-q", str(self.root)], env=self.env, check=True)
        (self.root / ".env").write_bytes(b"PRIVATE_FIXTURE=preserve-me\n")
        (self.root / "source.txt").write_bytes(b"unchanged source\n")

    def tool(self, name, body):
        target = self.bin / name
        if target.exists() or target.is_symlink():
            target.unlink()
        target.write_text(f"#!{BASH}\n" + body)
        target.chmod(0o755)

    def run_setup(self, entry="smoke.sh"):
        return subprocess.run(
            [BASH, str(self.config / entry)],
            cwd=self.base,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

    def assert_failure(self, result, diagnostic=None):
        self.assertNotEqual(0, result.returncode, result.stdout)
        self.assertNotIn("Development tools ready", result.stdout)
        self.assertTrue(result.stderr.strip(), "failure needs a diagnostic")
        if diagnostic:
            self.assertIn(diagnostic, result.stderr)

    def test_both_entrypoints_are_repeatable_and_preserve_checkout(self):
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        for entry in ("smoke.sh", "post-create.sh"):
            for _ in range(2):
                result = self.run_setup(entry)
                self.assertEqual(0, result.returncode, result.stderr)
                self.assertIn("Development tools ready", result.stdout)
        self.assertEqual(
            before, {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        )

    def test_each_missing_tool_fails_and_wrapper_propagates_failure(self):
        for name in TOOLS:
            with self.subTest(tool=name):
                target = self.bin / name
                saved = self.base / "saved-tool"
                target.rename(saved)
                try:
                    for entry in ("smoke.sh", "post-create.sh"):
                        self.assert_failure(self.run_setup(entry), name)
                finally:
                    saved.rename(target)

    def test_wrong_node_major_is_reported(self):
        self.tool("node", "exit 1\n")
        for entry in ("smoke.sh", "post-create.sh"):
            self.assert_failure(self.run_setup(entry), "Node 26")

    @unittest.skipUnless(
        shutil.which("node"), "requires Node to execute the version predicate"
    )
    def test_node_version_predicate_accepts_only_supported_major(self):
        self.tool(
            "node",
            f"exec {shlex.quote(shutil.which('node'))} -e "
            '\'Object.defineProperty(process.versions, "node", '
            '{value: process.env.SETUP_NODE_VERSION}); eval(process.argv[1]);\' "$2"\n',
        )
        for version in ("25.9.0", "26.0.0", "26.8.1", "27.0.0"):
            with self.subTest(version=version):
                self.env["SETUP_NODE_VERSION"] = version
                result = self.run_setup()
                if version.startswith("26."):
                    self.assertEqual(0, result.returncode, result.stderr)
                else:
                    self.assert_failure(result, "Node 26")

    def test_git_failure_is_reported(self):
        self.tool("git", "exit 7\n")
        self.assert_failure(self.run_setup(), "Git")

    def test_non_repository_and_parent_repository_are_rejected(self):
        shutil.rmtree(self.root / ".git")
        self.assert_failure(self.run_setup())
        subprocess.run([GIT, "init", "-q", str(self.base)], env=self.env, check=True)
        self.assert_failure(self.run_setup(), "root")

    @unittest.skipUnless(
        os.name == "posix" and os.geteuid() != 0, "requires non-root POSIX permissions"
    )
    def test_read_only_checkout_is_rejected(self):
        self.root.chmod(0o555)
        try:
            self.assert_failure(self.run_setup(), "writable")
        finally:
            self.root.chmod(0o755)


if __name__ == "__main__":
    unittest.main()
