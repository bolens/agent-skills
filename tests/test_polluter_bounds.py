"""Bounded polluter discovery and test ownership in disposable repositories."""
import json
import os
import signal
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/systematic-debugging/find-polluter.sh'
NPM = '''#!/usr/bin/env python3
import json,os,signal,subprocess,sys,time
from pathlib import Path
with Path('calls').open('a') as stream: stream.write(json.dumps(sys.argv[1:])+'\\n')
if os.environ.get('POLLUTER_FIXTURE') == 'hang':
    p=subprocess.Popen([sys.executable,'-c','import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(60)'])
    Path('child.pid').write_text(str(p.pid))
    time.sleep(60)
'''


@unittest.skipUnless(os.name == 'posix', 'polluter requires POSIX process groups')
class PolluterBounds(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        binary = self.root / 'bin'
        binary.mkdir()
        npm = binary / 'npm'
        npm.write_text(NPM)
        npm.chmod(0o755)
        self.env = {**os.environ, 'PATH': str(binary) + os.pathsep + os.environ['PATH']}

    def run_helper(self, *options, pattern='*.test.ts', target='pollution'):
        return subprocess.run(['bash', str(SCRIPT), target, pattern, *options], cwd=self.root,
                              env=self.env, capture_output=True, text=True, timeout=8, check=False)

    def test_order_and_dependency_pruning_are_repeatable(self):
        for path in ['z.test.ts', 'a.test.ts', 'node_modules/vendor.test.ts', '.git/hidden.test.ts', '.venv/hidden.test.ts']:
            candidate = self.root / path
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.touch()
        for _ in range(2):
            result = self.run_helper()
            self.assertEqual(0, result.returncode, result.stderr)
        calls = [json.loads(line) for line in (self.root / 'calls').read_text().splitlines()]
        self.assertEqual([['test','--','./a.test.ts'], ['test','--','./z.test.ts']] * 2, calls)

    def test_recursive_pattern_includes_direct_and_nested_tests(self):
        for path in ['src/direct.test.ts', 'src/nested/deep.test.ts']:
            candidate = self.root / path
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.touch()
        result = self.run_helper(pattern='src/**/*.test.ts')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(2, len((self.root / 'calls').read_text().splitlines()))

    def test_discovery_limit_never_runs_a_partial_selection(self):
        for name in ['a.test.ts', 'b.test.ts']:
            (self.root / name).touch()
        for options in [('--max-tests','1'), ('--max-entries','1')]:
            result = self.run_helper(*options)
            self.assertEqual(2, result.returncode)
            self.assertIn('limit reached', result.stderr)
            self.assertFalse((self.root / 'calls').exists())

    def test_uninspectable_target_does_not_run_tests(self):
        (self.root / 'a.test.ts').touch()
        (self.root / 'regular').write_text('preserve')
        result = self.run_helper(target='regular/child')
        self.assertEqual(2, result.returncode)
        self.assertFalse((self.root / 'calls').exists())
        self.assertEqual('preserve', (self.root / 'regular').read_text())

    def assert_child_stopped(self):
        pid = int((self.root / 'child.pid').read_text())
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            result = subprocess.run(['ps','-o','stat=','-p',str(pid)], capture_output=True, text=True, timeout=2, check=False)
            if result.returncode == 1 and not result.stdout.strip():
                return
            self.assertEqual(0, result.returncode, result.stderr)
            if result.stdout.strip().startswith('Z'):
                return
            time.sleep(0.01)
        self.fail('test descendant is still running')

    def test_deadlines_stop_descendants_and_skip_later_tests(self):
        (self.root / 'a.test.ts').touch()
        (self.root / 'b.test.ts').touch()
        self.env['POLLUTER_FIXTURE'] = 'hang'
        for options in [('--timeout','1'), ('--total-timeout','1')]:
            with self.subTest(options=options):
                result = self.run_helper(*options)
                self.assertEqual(2, result.returncode, result.stderr)
                self.assertIn('Inconclusive', result.stderr)
                self.assertEqual(1, len((self.root / 'calls').read_text().splitlines()))
                self.assert_child_stopped()
                (self.root / 'calls').unlink()
                (self.root / 'child.pid').unlink()

    def test_cancellation_cleans_test_group_and_preserves_artifacts(self):
        (self.root / 'a.test.ts').touch()
        self.env['POLLUTER_FIXTURE'] = 'hang'
        process = subprocess.Popen(['bash',str(SCRIPT),'pollution','*.test.ts'],cwd=self.root,env=self.env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            deadline = time.monotonic() + 5
            while not (self.root / 'child.pid').exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            self.assertTrue((self.root / 'child.pid').exists())
            process.send_signal(signal.SIGTERM)
            self.assertEqual(143, process.wait(timeout=3))
            self.assert_child_stopped()
            self.assertTrue((self.root / 'calls').exists())
        finally:
            if process.poll() is None:
                process.kill()
            process.wait()


if __name__ == '__main__':
    unittest.main()
