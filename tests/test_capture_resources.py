"""Prove capture command and server-log resource limits without a real browser."""
import importlib.util
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/responsive-web-capture/scripts/capture-responsive.py'
spec = importlib.util.spec_from_file_location('capture_resources', SCRIPT)
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


@unittest.skipUnless(os.name == 'posix', 'capture requires POSIX process groups')
class CaptureResources(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def test_exact_log_limit_completes_without_truncation(self):
        log = self.root / 'command.log'
        capture.run([sys.executable, '-c', f"import os; os.write(1,b'x'*{capture.LOG_LIMIT})"], 5, log)
        self.assertEqual(capture.LOG_LIMIT, log.stat().st_size)

    def test_closed_output_does_not_bypass_process_deadline(self):
        start = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            capture.run([sys.executable, '-c', 'import os,time; os.close(1); os.close(2); time.sleep(60)'], 1, self.root / 'command.log')
        self.assertLess(time.monotonic() - start, 3)

    def test_signal_during_spawn_still_reaps_owned_process(self):
        original = subprocess.Popen
        children = []

        def interrupted_spawn(*args, **kwargs):
            process = original(*args, **kwargs)
            children.append(process)
            os.kill(os.getpid(), signal.SIGTERM)
            return process

        with patch.object(capture.subprocess, 'Popen', side_effect=interrupted_spawn):
            with self.assertRaises(KeyboardInterrupt):
                capture.run([sys.executable, '-c', 'import time; time.sleep(60)'], 5, self.root / 'command.log')
        self.assertIsNotNone(children[0].poll())
        self.assertTrue(children[0].stdout.closed)

    def test_parent_exit_does_not_leave_descendant_holding_log_pipe(self):
        log = self.root / 'command.log'
        code = "import subprocess,sys\np=subprocess.Popen([sys.executable,'-c','import time; time.sleep(60)'])\nprint(p.pid,flush=True)"
        with self.assertRaises(subprocess.TimeoutExpired):
            capture.run([sys.executable, '-c', code], 2, log)
        pid = int(log.read_text())
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            result = subprocess.run(['ps', '-o', 'stat=', '-p', str(pid)], capture_output=True, text=True, timeout=2, check=False)
            if result.returncode == 1 and not result.stdout.strip():
                return
            self.assertEqual(0, result.returncode, result.stderr)
            if result.stdout.strip().startswith('Z'):
                return
            time.sleep(0.01)
        self.fail('capture descendant is still running')

    def test_concurrent_server_logs_stop_at_cap_and_preserve_truncation(self):
        path = self.root / 'server.log'
        log = capture.BoundedServerLog(path)
        try:
            threads = [threading.Thread(target=log.write, args=('x' * capture.LOG_LIMIT,)) for _ in range(4)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=3)
                self.assertFalse(thread.is_alive())
            log.flush()
            self.assertTrue(log.truncated)
            self.assertEqual(capture.LOG_LIMIT, path.stat().st_size)
        finally:
            log.close()
        log.write('late request')
        self.assertEqual(capture.LOG_LIMIT, path.stat().st_size)


if __name__ == '__main__':
    unittest.main()
