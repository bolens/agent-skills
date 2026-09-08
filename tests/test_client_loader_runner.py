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
