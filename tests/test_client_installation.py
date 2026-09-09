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

    def test_plan_reports_conflicts_before_any_apply_writes(self):
        home = self.home / '.pi/agent/skills'
        occupied = home / 'codebase-design'
        occupied.mkdir(parents=True)
        for mode in ('--plan', '--apply'):
            result = self.run_installer(mode, '--client', 'pi')
            self.assertEqual(1, result.returncode)
            self.assertIn('refusing existing target', result.stdout)
            self.assertEqual([occupied], list(home.iterdir()))

    def test_stale_owned_links_and_excluded_aliases_are_reported_not_removed(self):
        self.assertEqual(0, self.run_installer('--apply', '--client', 'hermes').returncode)
        home = self.home / '.hermes/skills'
        stale = home / 'old-skill'
        stale.symlink_to(ROOT / 'skills/no-longer-present')
        group = home / 'custom'
        group.mkdir()
        alias = group / 'renamed'
        alias.mkdir()
        (alias / 'SKILL.md').write_text('---\nname: caveman\ndescription: local copy\n---\n')
        unrelated = home / 'independent'
        unrelated.mkdir()
        (unrelated / 'SKILL.md').write_text('---\nname: independent\ndescription: own skill\n---\n')
        result = self.run_installer('--check', '--client', 'hermes')
        self.assertEqual(1, result.returncode)
        self.assertIn('unexpected repository-owned link', result.stdout)
        self.assertIn('excluded skill exposed', result.stdout)
        self.assertNotIn('independent', result.stdout)
        self.assertTrue(stale.is_symlink())
        self.assertTrue((alias / 'SKILL.md').is_file())

    def test_duplicate_names_and_cycles_fail_bounded_check(self):
        self.assertEqual(0, self.run_installer('--apply', '--client', 'pi').returncode)
        home = self.home / '.pi/agent/skills'
        group = home / 'group'
        group.mkdir()
        duplicate = group / 'different-directory'
        duplicate.mkdir()
        (duplicate / 'SKILL.md').write_text('---\nname: code-review\ndescription: duplicate\n---\n')
        (group / 'cycle').symlink_to(home)
        result = self.run_installer('--check', '--client', 'pi')
        self.assertEqual(1, result.returncode)
        self.assertIn('conflicting skill name', result.stdout)
        self.assertIn('alias or cycle', result.stdout)

    def test_empty_relative_and_overlapping_profiles(self):
        self.env['CODEX_HOME'] = ''
        self.assertEqual(0, self.run_installer('--apply').returncode)
        self.assertTrue((self.home / '.codex/skills/code-review').is_symlink())
        self.env['HERMES_HOME'] = 'relative'
        result = self.run_installer('--plan', '--client', 'hermes', '--json')
        self.assertEqual('operation_failed', json.loads(result.stdout)['issues'][0]['code'])
        self.env['HERMES_HOME'] = str(self.home / '.pi/agent')
        result = self.run_installer('--apply', '--client', 'hermes', '--client', 'pi', '--json')
        self.assertEqual(1, result.returncode)
        self.assertFalse((self.home / '.pi').exists())

    def test_json_receipts_and_busy_catalog(self):
        import fcntl
        args = ('--client', 'pi', '--json')
        report = json.loads(self.run_installer('--check', *args).stdout)
        self.assertEqual(1, report['schema_version'])
        self.assertEqual('missing_link', report['issues'][0]['code'])
        report = json.loads(self.run_installer('--apply', *args).stdout)
        self.assertTrue(all(row['applied'] for row in report['changes']))
        home = self.home / '.pi/agent/skills'
        descriptor = os.open(home, os.O_RDONLY)
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            for mode in ('--apply', '--check', '--plan'):
                report = json.loads(self.run_installer(mode, *args).stdout)
                self.assertEqual('busy', report['issues'][0]['code'])
                self.assertEqual('failed', report['status'])
        finally:
            os.close(descriptor)
        self.assertEqual(0, self.run_installer('--apply', *args).returncode)
        self.assertEqual(len(self.entries), len(list(home.iterdir())))

    def test_json_reports_partial_apply_for_recoverable_io_failure(self):
        code = '''
import importlib.util, sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(sys.argv[1]).parent))
spec = importlib.util.spec_from_file_location('installer', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original = Path.symlink_to
calls = 0
def fail_second(self, *args, **kwargs):
    global calls
    calls += 1
    if calls == 2:
        raise OSError('synthetic disk failure')
    return original(self, *args, **kwargs)
sys.argv = ['installer', '--apply', '--client', 'pi', '--json']
with patch.object(Path, 'symlink_to', fail_second):
    sys.exit(module.main())
'''
        result = subprocess.run([sys.executable, '-c', code, str(INSTALLER)], env=self.env,
                                capture_output=True, text=True, timeout=15)
        report = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertEqual('partial', report['status'])
        self.assertEqual(1, sum(row['applied'] for row in report['changes']))
        self.assertEqual(0, self.run_installer('--apply', '--client', 'pi').returncode)

    def test_symlinked_home_tilde_and_unicode_source_paths(self):
        import shutil
        root = self.home / 'source space café'
        (root / 'scripts').mkdir(parents=True)
        for name in ('link-installed.py', 'skill_metadata.py'):
            shutil.copyfile(ROOT / 'scripts' / name, root / 'scripts' / name)
        entry = next(entry for entry in self.entries if entry['name'] == 'code-review')
        (root / 'PROVENANCE.json').write_text(json.dumps({'skills': [entry]}))
        skill = root / 'skills/code-review'
        skill.mkdir(parents=True)
        (skill / 'SKILL.md').write_text('---\nname: code-review\ndescription: fixture\n---\n')
        (skill / 'resource.txt').write_text('resource through installed link')
        real_home = self.home / 'real profile'
        real_home.mkdir()
        (self.home / 'profile alias').symlink_to(real_home, target_is_directory=True)
        self.env['PI_CODING_AGENT_DIR'] = '~/profile alias'
        for mode in ('--apply', '--check', '--apply'):
            result = subprocess.run([sys.executable, str(root / 'scripts/link-installed.py'), mode,
                                     '--client', 'pi', '--json'], env=self.env,
                                    capture_output=True, text=True, timeout=15)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual('resource through installed link',
                         (real_home / 'skills/code-review/resource.txt').read_text())

    def test_case_alias_catalogs_are_rejected_on_case_insensitive_filesystems(self):
        home = self.home / 'MixedCase'
        (home / 'skills').mkdir(parents=True)
        alias = self.home / 'mixedcase'
        if not alias.exists():
            self.skipTest('filesystem is case sensitive; exercised by native macOS CI where applicable')
        self.env['HERMES_HOME'] = str(home)
        self.env['PI_CODING_AGENT_DIR'] = str(alias)
        result = self.run_installer('--apply', '--client', 'hermes', '--client', 'pi', '--json')
        self.assertEqual(1, result.returncode)
        self.assertIn('share a', result.stdout)
        self.assertEqual([], list((home / 'skills').iterdir()))
        self.env['PI_CODING_AGENT_DIR'] = str(alias / 'skills/nested')
        result = self.run_installer('--apply', '--client', 'hermes', '--client', 'pi', '--json')
        self.assertEqual(1, result.returncode)
        self.assertIn('overlap', result.stdout)
        self.assertEqual([], list((home / 'skills').iterdir()))

    def test_failed_link_replacement_preserves_old_link(self):
        home = self.home / '.pi/agent/skills'
        home.mkdir(parents=True)
        target = home / 'accessibility'
        old = self.home / 'previous-source'
        old.mkdir()
        target.symlink_to(old, target_is_directory=True)
        code = '''
import importlib.util, sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(sys.argv[1]).parent))
spec = importlib.util.spec_from_file_location('installer', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.argv = ['installer', '--apply', '--client', 'pi', '--json']
with patch.object(Path, 'symlink_to', side_effect=PermissionError('synthetic filesystem denial')):
    sys.exit(module.main())
'''
        result = subprocess.run([sys.executable, '-c', code, str(INSTALLER)], env=self.env,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(1, result.returncode)
        self.assertEqual(old.resolve(), target.resolve())
        self.assertEqual([target], list(home.iterdir()))
        result = self.run_installer('--apply', '--client', 'pi')
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertEqual(ROOT / 'skills/accessibility', target.resolve())

    def test_unsupported_filesystem_locking_fails_before_link_writes(self):
        code = '''
import errno, importlib.util, sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(sys.argv[1]).parent))
spec = importlib.util.spec_from_file_location('installer', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
sys.argv = ['installer', '--apply', '--client', 'pi', '--json']
with patch('fcntl.flock', side_effect=OSError(errno.ENOTSUP, 'synthetic unsupported filesystem')):
    sys.exit(module.main())
'''
        result = subprocess.run([sys.executable, '-c', code, str(INSTALLER)], env=self.env,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(1, result.returncode)
        self.assertIn('does not support directory locking', result.stdout)
        self.assertEqual([], list((self.home / '.pi/agent/skills').iterdir()))

    def test_replacement_ignores_obsolete_metadata_but_check_reports_it(self):
        home = self.home / '.pi/agent/skills'
        target = home / 'code-review'
        target.mkdir(parents=True)
        (target / 'SKILL.md').write_text('Obsolete independent metadata')
        self.assertEqual(1, self.run_installer('--check', '--client', 'pi').returncode)
        self.assertEqual(1, self.run_installer('--apply', '--client', 'pi').returncode)
        result = self.run_installer('--apply', '--replace', '--client', 'pi')
        self.assertEqual(0, result.returncode, result.stdout)
        target.unlink()
        old = self.home / 'obsolete-source'
        old.mkdir()
        (old / 'SKILL.md').write_text('Obsolete symlink source')
        target.symlink_to(old)
        result = self.run_installer('--apply', '--client', 'pi')
        self.assertEqual(0, result.returncode, result.stdout)
        self.assertEqual(ROOT / 'skills/code-review', target.resolve())
        self.assertTrue((old / 'SKILL.md').exists())

    def test_cleanup_failure_reports_completed_link_replacement(self):
        self.assertEqual(0, self.run_installer('--apply', '--client', 'pi').returncode)
        target = self.home / '.pi/agent/skills/code-review'
        target.unlink()
        old = self.home / 'old-source'
        old.mkdir()
        target.symlink_to(old)
        code = '''
import importlib.util, sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(sys.argv[1]).parent))
spec = importlib.util.spec_from_file_location('installer', sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original = tempfile.TemporaryDirectory.cleanup
def fail_after_cleanup(self):
    original(self)
    raise PermissionError('synthetic cleanup failure')
sys.argv = ['installer', '--apply', '--client', 'pi', '--json']
with patch.object(tempfile.TemporaryDirectory, 'cleanup', fail_after_cleanup):
    sys.exit(module.main())
'''
        result = subprocess.run([sys.executable, '-c', code, str(INSTALLER)], env=self.env,
                                capture_output=True, text=True, timeout=15)
        report = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertEqual('partial', report['status'])
        self.assertTrue(report['changes'][0]['applied'])
        self.assertEqual(ROOT / 'skills/code-review', target.resolve())
        self.assertEqual(0, self.run_installer('--check', '--client', 'pi').returncode)
