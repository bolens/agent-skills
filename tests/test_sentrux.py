import importlib.util
import json
import io
from contextlib import redirect_stdout, redirect_stderr
import shutil
import subprocess
from types import SimpleNamespace
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/audit-repo-fleet/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = load('sentrux')
setup = load('prepare-sentrux')


class SentruxTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name).resolve() / 'repo'
        self.repo.mkdir()
        runner.git(self.repo, 'init', '-q')
        self.scope = {'include': ['src/*'], 'extensions': {'.py': 'python'}}
        (self.repo / 'src').mkdir()

    def test_snapshot_includes_changes_and_new_files_without_staging(self):
        tracked = self.repo / 'src/old.py'
        tracked.write_text('old = 1\n')
        runner.git(self.repo, 'add', '--', 'src/old.py')
        tracked.write_text('old = 2\n')
        (self.repo / 'src/new.py').write_text('new = 1\n')
        (self.repo / '.gitignore').write_text('src/ignored.py\n')
        (self.repo / 'src/ignored.py').write_text('secret = 1\n')
        before = runner.git(self.repo, 'ls-files', '--stage')
        selected = runner.selected_files(self.repo, self.scope)
        self.assertEqual({'src/old.py', 'src/new.py'}, set(selected))
        self.assertEqual(b'old = 2\n', selected['src/old.py'])
        self.assertEqual(before, runner.git(self.repo, 'ls-files', '--stage'))

    def test_context_is_kept_and_exclusions_apply(self):
        (self.repo / 'src/main.py').write_text('pass\n')
        (self.repo / 'src/generated.py').write_text('pass\n')
        (self.repo / 'package.json').write_text('{}\n')
        self.scope.update(context=['package.json'], exclude=['src/generated.py'])
        self.assertEqual({'src/main.py', 'package.json'}, set(runner.selected_files(self.repo, self.scope)))

    def test_symlink_is_rejected(self):
        outside = self.repo.parent / 'outside.py'
        outside.write_text('secret = 1\n')
        (self.repo / 'src/link.py').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'Non-regular'):
            runner.selected_files(self.repo, self.scope)

    def test_empty_and_oversized_sources_fail(self):
        with self.assertRaisesRegex(ValueError, 'Empty scope'):
            runner.selected_files(self.repo, self.scope)
        (self.repo / 'src/large.py').write_bytes(b'x' * (512 * 1024 + 1))
        with self.assertRaisesRegex(ValueError, 'parse limit'):
            runner.selected_files(self.repo, self.scope)

    def test_comparison_rejects_changed_identity(self):
        runner.compatible({'identity': {'scope': 'a'}}, {'scope': 'a'})
        with self.assertRaisesRegex(ValueError, 'Incompatible'):
            runner.compatible({'identity': {'scope': 'a'}}, {'scope': 'b'})

    def test_bad_archive_does_not_create_runtime(self):
        archive = self.repo.parent / 'bad.tar.gz'
        archive.write_bytes(b'not the published archive')
        runtime = self.repo.parent / 'runtime'
        with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
            setup.prepare(archive, runtime)
        self.assertFalse(runtime.exists())

    def test_runtime_rejects_modified_grammars_and_missing_notices(self):
        runtime = self.repo.parent / 'runtime'
        grammar = runtime / '.sentrux/plugins/python/grammars/linux-x86_64.so'
        grammar.parent.mkdir(parents=True)
        grammar.write_bytes(b'fixture grammar')
        (runtime / 'grammars.json').write_text(json.dumps({
            'python/grammars/linux-x86_64.so': runner.digest(grammar.read_bytes())}))
        (runtime / '.sentrux/telemetry_opt_out').touch()
        shutil.copytree(setup.NOTICES, runtime / 'notices')
        binary = self.repo.parent / 'sentrux'
        binary.write_bytes(b'fixture binary')
        with patch.object(runner, 'BINARY_SHA256', runner.digest(binary.read_bytes())), \
                patch.object(runner.platform, 'system', return_value='Linux'), \
                patch.object(runner.platform, 'machine', return_value='x86_64'):
            runner.runtime_identity(runtime, binary, self.scope)
            grammar.write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Grammar manifest mismatch'):
                runner.runtime_identity(runtime, binary, self.scope)
            grammar.write_bytes(b'fixture grammar')
            (runtime / 'notices/python-LICENSE').unlink()
            with self.assertRaises(OSError):
                runner.runtime_identity(runtime, binary, self.scope)

    def test_unsupported_and_mismatched_extension_mappings_fail(self):
        for extensions in ({'.qml': 'python'}, {'.py': 'javascript'}, {}):
            with self.subTest(extensions=extensions), self.assertRaises(ValueError):
                runner.validate_scope(dict(self.scope, extensions=extensions))
        runner.validate_scope(self.scope)

    def test_context_without_source_is_not_a_scan(self):
        (self.repo / 'package.json').write_text('{}')
        with self.assertRaisesRegex(ValueError, 'Empty scope'):
            runner.selected_files(self.repo, dict(self.scope, context=['package.json']))

    def run_fixture(self, action, analysis, baseline=None):
        source = self.repo / 'src/main.py'
        source.write_text('def main():\n    return 1\n')
        runner.git(self.repo, 'add', '--', 'src/main.py')
        runner.git(self.repo, '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                   '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null',
                   'commit', '--allow-empty', '-qm', 'fixture')
        scope = self.repo.parent / 'scope.json'
        scope.write_text(json.dumps(self.scope))
        output = self.repo.parent / ('output-' + action)
        args = SimpleNamespace(action=action, repo=self.repo, runtime=self.repo.parent / 'runtime',
                               binary='sentrux', scope=scope, output=output, baseline=baseline)
        with patch.object(runner, 'runtime_identity', return_value={'fixture': 1}), \
                patch.object(runner, 'sandbox', side_effect=lambda runtime, snapshot, binary, *args: [str(snapshot)]), \
                patch.object(runner, 'analyze', side_effect=analysis), \
                redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            code = runner.run(args)
        return code, output, json.loads((output / 'evidence.json').read_text())

    def test_startup_failure_retains_diagnostics_and_is_unavailable(self):
        code, output, receipt = self.run_fixture('check', lambda command: (1, 'bwrap: namespace setup failed', None))
        self.assertEqual(2, code)
        self.assertEqual(1, receipt['raw_exit_code'])
        self.assertIn('namespace setup failed', (output / 'sentrux.log').read_text())

    def test_timeout_keeps_partial_logs_and_failure_receipt(self):
        with patch.object(runner.subprocess, 'run', side_effect=subprocess.TimeoutExpired(
                'fixture', 120, output=b'partial stdout', stderr=b'partial stderr')):
            analysis = runner.analyze(['fixture'])
        code, output, receipt = self.run_fixture('check', lambda command: analysis)
        self.assertEqual(2, code)
        self.assertIsNone(receipt['raw_exit_code'])
        self.assertIn('timed out', receipt['error'])
        self.assertEqual('partial stdoutpartial stderr', (output / 'sentrux.log').read_text())

    def test_completed_rule_finding_is_distinct_from_startup_failure(self):
        log = 'sentrux check — 1 rules checked\n1 violation(s) found\n'
        code, _, receipt = self.run_fixture('check', lambda command: (1, log, None))
        self.assertEqual(1, code)
        self.assertEqual(1, receipt['raw_exit_code'])

    def test_saved_baseline_is_copied_and_comparable(self):
        def saved(command):
            (Path(command[0]) / '.sentrux/baseline.json').write_text('{"total_import_edges": 1}')
            return 0, 'Baseline saved to fixture', None
        code, before, receipt = self.run_fixture('baseline', saved)
        self.assertEqual(0, code)
        self.assertEqual(receipt['baseline_sha256'], runner.digest((before / 'baseline.json').read_bytes()))
        log = 'sentrux gate — structural regression check\nNo degradation detected'
        code, _, receipt = self.run_fixture('compare', lambda command: (0, log, None), before)
        self.assertEqual(0, code)
        self.assertEqual({'src/main.py'}, set(receipt['files']))

    def test_retained_notices_match_provenance(self):
        record = json.loads((setup.NOTICES / 'provenance.json').read_text())
        self.assertEqual(record['binary_sha256'], runner.BINARY_SHA256)
        self.assertEqual(record['source_license_sha256'], runner.digest((setup.NOTICES / 'SENTRUX-LICENSE').read_bytes()))
        for grammar in record['grammars']:
            path = setup.NOTICES / (grammar['language'] + '-LICENSE')
            self.assertEqual(grammar['notice_sha256'], runner.digest(path.read_bytes()))


if __name__ == '__main__':
    unittest.main()
