from __future__ import annotations

import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import tarfile
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('client_loader_runner', ROOT / 'scripts/test_client_loaders.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class ClientLoaderRunner(unittest.TestCase):
    def test_download_checks_integrity_and_size_before_use(self):
        with patch.object(runner.urllib.request, 'urlopen', return_value=io.BytesIO(b'valid')):
            self.assertEqual(b'valid', runner.download('https://example.invalid/module', 'sha256', hashlib.sha256(b'valid').hexdigest()))
        with patch.object(runner.urllib.request, 'urlopen', return_value=io.BytesIO(b'changed')):
            with self.assertRaisesRegex(ValueError, 'integrity mismatch'):
                runner.download('https://example.invalid/module', 'sha256', '00' * 32)
        with patch.object(runner, 'MAX_DOWNLOAD', 4), patch.object(runner.urllib.request, 'urlopen', return_value=io.BytesIO(b'12345')):
            with self.assertRaisesRegex(ValueError, 'exceeds'):
                runner.download('https://example.invalid/module', 'sha256', '00' * 32)

    def test_transient_download_retries_then_checks_integrity(self):
        error = urllib.error.HTTPError('https://example.invalid', 429, 'limited', {'Retry-After': '2'}, io.BytesIO())
        with patch.object(runner.urllib.request, 'urlopen', side_effect=[error, io.BytesIO(b'valid')]) as fetch, patch.object(runner.time, 'sleep') as sleep:
            self.assertEqual(b'valid', runner.download('https://example.invalid', 'sha256', hashlib.sha256(b'valid').hexdigest()))
        sleep.assert_called_once_with(2)
        self.assertEqual(2, fetch.call_count)
        self.assertTrue(error.closed)

    def test_download_retry_budget_and_nonretryable_errors(self):
        for status, retry_after, attempts in [(429, None, 3), (503, None, 3), (404, None, 1), (429, '61', 1)]:
            with self.subTest(status=status, retry_after=retry_after):
                errors = [urllib.error.HTTPError('https://example.invalid', status, 'failure',
                          {} if retry_after is None else {'Retry-After': retry_after}, io.BytesIO()) for _ in range(attempts)]
                with patch.object(runner.urllib.request, 'urlopen', side_effect=errors) as fetch, patch.object(runner.time, 'sleep') as sleep:
                    with self.assertRaises(urllib.error.HTTPError):
                        runner.download('https://example.invalid', 'sha256', '00' * 32)
                self.assertEqual(attempts, fetch.call_count)
                self.assertEqual(attempts - 1, sleep.call_count)
                self.assertTrue(all(error.closed for error in errors))
                if attempts == 3:
                    self.assertEqual([30, 60], [call.args[0] for call in sleep.call_args_list])

    def test_retry_after_dates_and_malformed_values(self):
        with patch.object(runner.time, 'time', return_value=0):
            self.assertEqual(30, runner.retry_delay('Thu, 01 Jan 1970 00:00:30 GMT', 60))
            self.assertEqual(60, runner.retry_delay('invalid', 60))
            self.assertEqual(0, runner.retry_delay('-1', 60))

    def test_archive_only_copies_allowlisted_regular_modules(self):
        archive = io.BytesIO()
        with tarfile.open(fileobj=archive, mode='w:gz') as bundle:
            for name, content in [('package/dist/skills.js', b'export {};'), ('package/unrelated.js', b'ignore')]:
                member = tarfile.TarInfo(name)
                member.size = len(content)
                bundle.addfile(member, io.BytesIO(content))
            link = tarfile.TarInfo('package/link.js')
            link.type = tarfile.SYMTYPE
            link.linkname = '/outside'
            bundle.addfile(link)
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            runner.extract_modules(archive.getvalue(), target, ['dist/skills.js'])
            self.assertEqual(b'export {};', (target / 'dist/skills.js').read_bytes())
            self.assertFalse((target / 'unrelated.js').exists())
            for name in ['../escape', '/absolute', 'link.js']:
                with self.subTest(name=name), self.assertRaises(ValueError):
                    runner.extract_modules(archive.getvalue(), target, [name])

    @unittest.skipUnless(os.name == 'posix', 'POSIX process supervision')
    def test_timeout_reaps_owned_process(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            marker = home / 'pid'
            code = "import os,time,pathlib; pathlib.Path('pid').write_text(str(os.getpid())); time.sleep(30)"
            with self.assertRaises(subprocess.TimeoutExpired):
                runner.run([sys.executable, '-c', code], home, dict(os.environ), timeout=1)
            pid = int(marker.read_text())
            with self.assertRaises(ProcessLookupError):
                os.kill(pid, 0)

    @unittest.skipUnless(os.name == 'posix', 'POSIX process supervision')
    def test_nonzero_producer_is_not_reported_as_success(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(subprocess.CalledProcessError):
                runner.run([sys.executable, '-c', 'raise SystemExit(3)'], Path(directory), dict(os.environ))

    @unittest.skipUnless(os.name == 'posix', 'POSIX process supervision')
    def test_sigterm_cleans_worker_and_descendant(self):
        import time
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            descendant = "import time,pathlib; time.sleep(2); pathlib.Path('survived').touch()"
            worker = (
                f"import os,subprocess,sys,time,pathlib; subprocess.Popen([sys.executable,'-c',{descendant!r}]); "
                "pathlib.Path('ready').write_text(str(os.getpid())); time.sleep(30)"
            )
            supervisor = '''
import importlib.util, os, signal, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location('runner', sys.argv[1])
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
def interrupt(*args):
    raise KeyboardInterrupt
signal.signal(signal.SIGTERM, interrupt)
runner.run([sys.executable, '-c', sys.argv[2]], Path.cwd(), dict(os.environ))
'''
            process = subprocess.Popen([sys.executable, '-c', supervisor, str(ROOT / 'scripts/test_client_loaders.py'), worker],
                                       cwd=home, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                deadline = time.monotonic() + 5
                while not (home / 'ready').exists() and process.poll() is None and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue((home / 'ready').exists(), 'worker did not start')
                process.terminate()
                process.communicate(timeout=5)
                self.assertNotEqual(0, process.returncode)
                time.sleep(2)
                self.assertFalse((home / 'survived').exists(), 'descendant survived cancellation')
            finally:
                if process.poll() is None:
                    process.terminate()
                process.communicate(timeout=5)
