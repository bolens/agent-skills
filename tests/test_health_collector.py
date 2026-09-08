"""Exercise bounded diagnostics against hostile and interrupted child processes."""
import argparse
import importlib.util
import io
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/workstation-health-triage/scripts/collect-health.py'
WRAPPER = SCRIPT.with_suffix('.sh')
spec = importlib.util.spec_from_file_location('health_collector', SCRIPT)
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


class HealthCollectorTests(unittest.TestCase):
    def probe(self, code, limit=4096, seconds=1):
        output = io.BytesIO()
        start = time.monotonic()
        status = health.run_probe([sys.executable, '-c', code], output, start + seconds, limit)
        self.assertLess(time.monotonic() - start, seconds + 2)
        return status, output.getvalue()

    def test_success_failure_and_missing_tool(self):
        self.assertEqual(self.probe("print('hello')"), ('OK', b'hello\n'))
        self.assertEqual(self.probe('raise SystemExit(7)')[0], 'CHECK_FAILED: exit=7')
        self.assertTrue(health.run_probe(['/nonexistent/health-probe'], io.BytesIO(), time.monotonic() + 1, 100).startswith('UNAVAILABLE:'))

    def test_flood_is_capped_and_stopped(self):
        status, output = self.probe("import os\nwhile True: os.write(1,b'x'*8192)")
        self.assertEqual(status, 'OUTPUT_LIMIT')
        self.assertEqual(len(output), 4096)

    def test_closed_stdout_does_not_bypass_timeout(self):
        status, _ = self.probe('import os,time; os.close(1); os.close(2); time.sleep(60)')
        self.assertEqual(status, 'TIMEOUT')

    def assert_stopped(self, pid):
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            try:
                state = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[0]
            except FileNotFoundError:
                return
            if state == 'Z':
                return  # Already dead; only the host's reaper owns this zombie.
            time.sleep(0.01)
        self.fail(f'owned process {pid} is still running')

    def test_exited_parent_does_not_leave_child_running(self):
        status, output = self.probe("import subprocess,sys\np=subprocess.Popen([sys.executable,'-c','import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(60)'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\nprint(p.pid,flush=True)")
        self.assertEqual(status, 'OK')
        self.assert_stopped(int(output))

    def test_inherited_pipe_is_bounded_and_stubborn_child_is_killed(self):
        status, output = self.probe("import subprocess,sys\np=subprocess.Popen([sys.executable,'-c','import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(60)'])\nprint(p.pid,flush=True)", seconds=0.5)
        self.assertEqual(status, 'TIMEOUT')
        self.assert_stopped(int(output))

    def test_timeout_allows_cooperative_cleanup(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'cleanup'
            code = f"import signal,time,sys\ndef finish(*args):\n open({str(marker)!r},'w').write('cleaned')\n sys.exit(0)\nsignal.signal(signal.SIGTERM,finish)\nprint('ready',flush=True)\ntime.sleep(60)"
            status, output = self.probe(code, seconds=0.5)
            self.assertEqual(status, 'TIMEOUT')
            self.assertEqual(output, b'ready\n')
            self.assertEqual(marker.read_text(), 'cleaned')

    def test_signal_cleans_probe_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / 'pid'
            child = f"import os,time; open({str(marker)!r},'w').write(str(os.getpid())); time.sleep(60)"
            code = f"import runpy,signal,time,io,sys\nm=runpy.run_path({str(SCRIPT)!r})\nsignal.signal(signal.SIGTERM,m['interrupt'])\ntry: m['run_probe']([sys.executable,'-c',{child!r}],io.BytesIO(),time.monotonic()+60,1024)\nexcept m['Interrupted']: sys.exit(143)"
            process = subprocess.Popen([sys.executable, '-c', code])
            try:
                deadline = time.monotonic() + 5
                while not marker.exists() and time.monotonic() < deadline:
                    time.sleep(0.01)
                self.assertTrue(marker.exists())
                process.send_signal(signal.SIGTERM)
                self.assertEqual(process.wait(timeout=3), 143)
                self.assert_stopped(int(marker.read_text()))
            finally:
                if process.poll() is None:
                    process.kill()
                process.wait()

    def test_total_budget_skips_remaining_probes(self):
        args = argparse.Namespace(mode='quick', total_timeout=0.2, probe_timeout=1, max_bytes=1024)
        output = io.BytesIO()
        with patch.object(health, 'QUICK', [('slow', [sys.executable, '-c', 'import time; time.sleep(60)']), ('must not run', ['echo', 'bad'])]):
            self.assertEqual(health.collect(args, output), 1)
        self.assertIn(b'COLLECTION_TIMEOUT', output.getvalue())
        self.assertNotIn(b'must not run', output.getvalue())

    def test_slow_output_consumer_is_bounded(self):
        read_fd, write_fd = os.pipe()
        writer = health.DeadlineWriter(write_fd, time.monotonic() + 0.1)
        try:
            with self.assertRaises(TimeoutError):
                writer.write(b'x' * 1048576)
        finally:
            writer.close()
            os.close(write_fd)
            os.close(read_fd)

    def test_output_failure_is_not_a_probe_failure(self):
        class BrokenOutput:
            def write(self, _):
                raise OSError('disk full')
        with self.assertRaisesRegex(OSError, 'disk full'):
            health.run_probe([sys.executable, '-c', "print('hello')"], BrokenOutput(), time.monotonic() + 1, 1024)

    def test_existing_outputs_and_invalid_limits_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'report'
            target.write_text('keep')
            link = Path(tmp) / 'link'
            link.symlink_to(target)
            fifo = Path(tmp) / 'fifo'
            os.mkfifo(fifo)
            for path in (target, link, fifo):
                result = subprocess.run(['bash', str(WRAPPER), '--output', str(path)], capture_output=True, timeout=3, check=False)
                self.assertEqual(result.returncode, 1)
            result = subprocess.run(['bash', str(WRAPPER), '--probe-timeout', '0', '--output', str(Path(tmp) / 'new')], capture_output=True, timeout=3, check=False)
            self.assertEqual(result.returncode, 2)
            self.assertFalse((Path(tmp) / 'new').exists())
            self.assertEqual(target.read_text(), 'keep')

    def test_private_report_and_entrypoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp) / 'report'
            with patch.object(health, 'QUICK', []), patch.object(sys, 'argv', [str(SCRIPT), '--output', str(report)]):
                self.assertEqual(health.main(), 0)
            self.assertEqual(report.stat().st_mode & 0o777, 0o600)
            self.assertIn('Workstation health snapshot', report.read_text())
        result = subprocess.run(['bash', str(WRAPPER), '--help'], capture_output=True, timeout=3, check=False)
        self.assertEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
