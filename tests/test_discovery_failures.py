"""Exercise scan failure boundaries with isolated command and repository fixtures."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class DiscoveryFailureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        self.env = dict(os.environ, PATH=str(self.bin) + os.pathsep + os.environ['PATH'])

    def command(self, name, source):
        target = self.bin / name
        target.write_text('#!/bin/sh\n' + source + '\n')
        target.chmod(0o755)

    def run_helper(self, skill, helper, *args):
        return subprocess.run(['bash', str(ROOT / 'skills' / skill / helper), *map(str, args)],
                              cwd=self.repo, env=self.env, text=True, capture_output=True)

    def test_html_discovery_failure_is_not_success(self):
        self.command('find', 'exit 42')
        result = self.run_helper('web-quality-audit', 'scripts/analyze.sh', self.repo)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)['success'])

    def test_html_read_failure_is_not_a_quality_result(self):
        source = self.repo / 'fixture.html'
        source.write_text('<!doctype html>')
        self.command('grep', 'exit 2')
        result = self.run_helper('web-quality-audit', 'scripts/analyze.sh', source)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(json.loads(result.stdout)['success'])

    def test_html_filename_newline_remains_one_finding(self):
        source = self.repo / 'two\nlines.html'
        source.write_text('<!doctype html><html lang="en"><head>'
                          '<meta charset="utf-8"><title>Fixture</title></head></html>')
        result = self.run_helper('web-quality-audit', 'scripts/analyze.sh', source)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['issueCount'], 1)
        self.assertEqual(len(report['issues']), 1)
        self.assertIn(str(source), report['issues'][0])

    def test_plugin_discovery_failure_is_not_success(self):
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True)
        subprocess.run(['git', '-C', str(self.repo), '-c', 'user.name=Fixture',
                        '-c', 'user.email=fixture@example.test', 'commit', '-qm', 'fixture',
                        '--allow-empty'], check=True)
        (self.repo / 'manifest.json').write_text(json.dumps({
            'id': 'fixture.test', 'version': '1.0.0', 'entryPoints': {'main': 'main.qml'}}))
        (self.repo / 'main.qml').write_text('Item {}')
        (self.repo / 'README.md').write_text('Install, removal, dependencies')
        (self.repo / 'LICENSE').write_text('fixture license')
        self.command('omarchy', 'exit 0')
        self.command('find', 'exit 42')
        result = self.run_helper('audit-omarchy-plugin', 'scripts/preflight.sh', self.repo)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('discovery', result.stdout.lower())

    def test_polluter_discovery_failure_is_inconclusive(self):
        self.command('find', 'exit 42')
        result = self.run_helper('systematic-debugging', 'find-polluter.sh', 'pollution', '*.test.ts')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertNotIn('all tests clean', result.stdout)

    def test_polluter_failed_test_is_inconclusive(self):
        (self.repo / 'fixture.test.ts').write_text('fixture')
        self.command('npm', 'exit 9')
        result = self.run_helper('systematic-debugging', 'find-polluter.sh', 'pollution', '*.test.ts')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_polluter_existing_target_is_inconclusive(self):
        (self.repo / 'fixture.test.ts').write_text('fixture')
        (self.repo / 'pollution').write_text('retain')
        self.command('npm', 'exit 97')
        result = self.run_helper('systematic-debugging', 'find-polluter.sh', 'pollution', '*.test.ts')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual((self.repo / 'pollution').read_text(), 'retain')

    def test_polluter_observed_creator_is_reported(self):
        (self.repo / 'fixture.test.ts').write_text('fixture')
        self.command('npm', 'touch pollution\nexit 9')
        result = self.run_helper('systematic-debugging', 'find-polluter.sh', 'pollution', '*.test.ts')
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('FOUND POLLUTER', result.stdout)


if __name__ == '__main__':
    unittest.main()
