from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / 'scripts/link-installed.py'


class ClientInstallation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.env = {**os.environ, 'HOME': str(self.home)}
        for key in ('HERMES_HOME', 'PI_CODING_AGENT_DIR', 'CODEX_HOME', 'AGENTS_HOME', 'CLAUDE_HOME'):
            self.env.pop(key, None)
        self.entries = json.loads((ROOT / 'PROVENANCE.json').read_text())['skills']

    def run_installer(self, *args):
        return subprocess.run([sys.executable, str(INSTALLER), *args], env=self.env,
                              capture_output=True, text=True, timeout=15)

    def test_optional_clients_do_not_change_default_install(self):
        self.assertEqual(0, self.run_installer('--apply').returncode)
        self.assertEqual(0, self.run_installer('--check').returncode)
        self.assertFalse((self.home / '.hermes').exists())
        self.assertFalse((self.home / '.pi').exists())

    def test_native_homes_repeated_apply_and_relative_resources(self):
        args = ('--client', 'hermes', '--client', 'pi', '--client', 'pi')
        self.assertNotEqual(0, self.run_installer('--check', *args).returncode)
        self.assertEqual([], list(self.home.iterdir()))
        for _ in range(2):
            result = self.run_installer('--apply', *args)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(0, self.run_installer('--check', *args).returncode)
        self.assertFalse((self.home / '.codex').exists())
        self.assertFalse((self.home / '.agents').exists())
        pi = self.home / '.pi/agent/skills'
        hermes = self.home / '.hermes/skills'
        self.assertEqual(len(self.entries), len(list(pi.iterdir())))
        for entry in self.entries:
            name = entry['name']
            self.assertEqual((ROOT / 'skills' / name).resolve(), (pi / name).resolve())
            allowed = 'hermes' in entry['optional_install_targets']
            self.assertEqual(allowed, (hermes / name).exists())
        for directory in (pi, hermes):
            reference = directory / 'ci-maintenance/../codebase-design/references/experience-and-interfaces.md'
            self.assertTrue(reference.is_file())
            self.assertTrue((directory / 'systematic-debugging/find-polluter.py').is_file())

    def test_profile_overrides_and_conflict_preservation(self):
        for client, variable in (('hermes', 'HERMES_HOME'), ('pi', 'PI_CODING_AGENT_DIR')):
            with self.subTest(client=client):
                profile = self.home / (client + ' profile')
                self.env[variable] = str(profile)
                occupied = profile / 'skills/codebase-design'
                occupied.mkdir(parents=True)
                marker = occupied / 'user.txt'
                marker.write_text('independent work')
                result = self.run_installer('--apply', '--client', client)
                self.assertEqual(1, result.returncode)
                self.assertIn('refusing existing target', result.stdout)
                self.assertEqual('independent work', marker.read_text())
                self.assertEqual(1, self.run_installer('--check', '--client', client).returncode)

    def test_explicit_invocation_policy_matches_client_catalogs(self):
        for entry in self.entries:
            directory = ROOT / 'skills' / entry['name']
            metadata = directory / 'agents/openai.yaml'
            explicit = metadata.exists() and 'allow_implicit_invocation: false' in metadata.read_text()
            header = (directory / 'SKILL.md').read_text().split('\n---\n', 1)[0]
            self.assertEqual(explicit, '\ndisable-model-invocation: true\n' in header + '\n', entry['name'])
            self.assertEqual(not explicit, 'hermes' in entry['optional_install_targets'], entry['name'])

    def test_unknown_client_is_rejected_without_writes(self):
        self.assertEqual(2, self.run_installer('--apply', '--client', 'unknown').returncode)
        self.assertEqual([], list(self.home.iterdir()))
