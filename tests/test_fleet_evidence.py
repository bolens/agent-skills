from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/audit-repo-fleet/scripts/evidence.py'


class FleetEvidence(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        self.root.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'user.name', 'Fixture')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.hooksPath', str(Path(self.temp.name) / 'no-hooks'))
        (self.root / 'source.txt').write_text('source\n')
        (self.root / '.gitignore').write_text('output/\n')
        self.git('add', '--', 'source.txt', '.gitignore')
        self.git('commit', '-qm', 'fixture')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True).strip()

    def cli(self, *args, root=None):
        return subprocess.run([sys.executable, str(SCRIPT), '--repo', str(root or self.root), *args], capture_output=True, text=True, timeout=15)

    def check(self, code, *options):
        return self.cli('run', '--label', 'native', *options, '--', sys.executable, '-c', code)

    def receipt(self, result):
        return json.loads(Path(json.loads(result.stdout)['receipt']).read_text())

    def test_success_keeps_logs_local_and_does_not_dirty_repository(self):
        result = self.check('import sys; print("stdout proof"); print("stderr proof", file=sys.stderr)')
        self.assertEqual(0, result.returncode, result.stderr)
        record = self.receipt(result)
        self.assertEqual('passed', record['status'])
        self.assertEqual('stderr proof\n', Path(record['stderr']).read_text())
        self.assertEqual('', self.git('status', '--porcelain'))
        self.assertEqual(0, self.cli('report', '--label', 'native').returncode)
        if os.name == 'posix':
            self.assertEqual(0o600, Path(record['stdout']).stat().st_mode & 0o777)

    def test_source_changes_and_deletions_invalidate_evidence(self):
        self.assertEqual(0, self.check('pass').returncode)
        (self.root / 'source.txt').write_text('changed\n')
        self.assertIn('stale', self.cli('report', '--label', 'native').stdout)
        (self.root / 'source.txt').unlink()
        self.assertEqual(1, self.cli('report', '--label', 'native').returncode)

    def test_untracked_sources_invalidate_but_ignored_outputs_do_not(self):
        self.check('pass')
        (self.root / 'output').mkdir()
        (self.root / 'output/cache').write_text('generated')
        self.assertEqual(0, self.cli('report', '--label', 'native').returncode)
        (self.root / 'new-source.txt').write_text('new')
        self.assertEqual(1, self.cli('report', '--label', 'native').returncode)

    def test_command_mutation_does_not_certify_new_candidate(self):
        result = self.check('from pathlib import Path; Path("source.txt").write_text("changed")')
        self.assertEqual(125, result.returncode)
        self.assertEqual('changed', self.receipt(result)['status'])
        self.assertEqual(1, self.cli('report', '--label', 'native').returncode)

    def test_failure_requires_reason_and_respects_attempt_bound(self):
        code = 'raise SystemExit(7)'
        first = self.check(code, '--max-attempts', '2')
        self.assertEqual(7, first.returncode)
        self.assertEqual('failed', self.receipt(first)['status'])
        self.assertEqual(2, self.check(code).returncode)
        second = self.check(code, '--max-attempts', '2', '--retry-reason', 'Check diagnosed transient fixture failure')
        self.assertEqual(7, second.returncode)
        self.assertEqual(2, self.receipt(second)['attempt'])
        self.assertEqual(2, self.check(code, '--max-attempts', '2', '--retry-reason', 'Still failing').returncode)

    def test_missing_tool_and_missing_gate_are_not_success(self):
        result = self.cli('run', '--label', 'missing', '--', str(self.root / 'missing-tool'))
        self.assertEqual(127, result.returncode)
        self.assertEqual('unavailable', self.receipt(result)['status'])
        self.assertEqual(1, self.cli('report', '--label', 'never-run').returncode)

    def test_timeout_is_recorded(self):
        result = self.check('import time; time.sleep(10)', '--timeout', '0.1')
        self.assertEqual(124, result.returncode)
        self.assertEqual('timed_out', self.receipt(result)['status'])

    @unittest.skipUnless(os.name == 'posix', 'POSIX process-group behavior')
    def test_timeout_stops_descendants(self):
        marker = Path(self.temp.name) / 'escaped-child'
        child = 'import time; from pathlib import Path; time.sleep(0.8); Path(' + repr(str(marker)) + ').touch()'
        code = 'import subprocess,sys,time; subprocess.Popen([sys.executable,"-c",' + repr(child) + ']); time.sleep(10)'
        self.assertEqual(124, self.check(code, '--timeout', '0.2').returncode)
        time.sleep(1)
        self.assertFalse(marker.exists())

    @unittest.skipUnless(os.name == 'posix', 'Symlink fixture')
    def test_symlink_targets_are_not_read(self):
        link = self.root / 'external'
        external = Path(self.temp.name) / 'private.txt'
        external.write_text('private source')
        link.symlink_to(external)
        self.assertEqual(0, self.check('pass').returncode)
        external.write_text('different private source')
        self.assertEqual(0, self.cli('report', '--label', 'native').returncode)
        link.unlink()
        link.symlink_to(Path(self.temp.name) / 'another')
        self.assertEqual(1, self.cli('report', '--label', 'native').returncode)

    def test_linked_worktree_has_independent_records(self):
        other = Path(self.temp.name) / 'other'
        self.git('worktree', 'add', '--detach', str(other), 'HEAD')
        self.assertEqual(0, self.check('pass').returncode)
        self.assertEqual(1, self.cli('report', '--label', 'native', root=other).returncode)

    def test_corrupt_receipt_cannot_reveal_an_older_pass(self):
        self.check('pass')
        latest = self.check('raise SystemExit(1)')
        receipt = Path(json.loads(latest.stdout)['receipt'])
        receipt.write_text('{broken')
        report = self.cli('report', '--label', 'native')
        self.assertEqual(2, report.returncode)
        self.assertIn('Unreadable evidence receipt', report.stderr)

    def test_branch_change_at_same_commit_invalidates_evidence(self):
        self.check('pass')
        self.git('switch', '-c', 'different-context')
        self.assertEqual(1, self.cli('report', '--label', 'native').returncode)

    def test_identical_concurrent_run_is_rejected(self):
        code = 'import time; time.sleep(2)'
        command = [sys.executable, str(SCRIPT), '--repo', str(self.root), 'run', '--label', 'native', '--', sys.executable, '-c', code]
        first = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            directory = self.root / '.git/fleet-evidence'
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if list(directory.glob('*/result.json')):
                    break
                time.sleep(0.02)
            second = self.check(code)
            self.assertEqual(2, second.returncode)
            self.assertIn('run lock', second.stderr)
            out, err = first.communicate(timeout=5)
            self.assertEqual(0, first.returncode, out + err)
        finally:
            if first.poll() is None:
                first.kill()
                first.communicate()

    def test_invalid_limits_do_not_execute_commands(self):
        for value in ['0', '-1', 'nan', 'inf', '86401']:
            with self.subTest(timeout=value):
                self.assertEqual(2, self.check('pass', '--timeout', value).returncode)


if __name__ == '__main__':
    unittest.main()
