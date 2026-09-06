"""Incomplete inspection must not be reported as successful evidence."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
COMPARE = ROOT / 'skills/managed-config-drift/scripts/compare-trees.py'
HEALTH = ROOT / 'skills/workstation-health-triage/scripts/collect-health.sh'


class HelperFailureTests(unittest.TestCase):
    def test_comparison_reports_failed_traversal_and_continues(self):
        # Inject an actual traversal error at the filesystem API boundary, without
        # relying on whether the test runner has permission to bypass mode bits.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('live', 'managed', 'other-live', 'other-managed'):
                (root / name).mkdir()
            (root / 'other-managed/sentinel').write_text('retain me')
            code = '''import os, runpy, sys
from unittest.mock import patch
original_scandir = os.scandir
def denied(path):
    if str(path) == sys.argv[1].split('=', 1)[0]:
        raise PermissionError(13, 'fixture traversal denied', str(path))
    return original_scandir(path)
script = sys.argv.pop(1)
with patch('os.scandir', side_effect=denied):
    runpy.run_path(script, run_name='__main__')
'''
            args = [f'{root / "live"}={root / "managed"}',
                    f'{root / "other-live"}={root / "other-managed"}']
            result = subprocess.run([sys.executable, '-c', code, str(COMPARE), *args],
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
            self.assertIn('UNAVAILABLE:', result.stdout)
            self.assertIn('managed-only\tsentinel', result.stdout)
            self.assertEqual((root / 'other-managed/sentinel').read_text(), 'retain me')

    def test_health_does_not_claim_unwritable_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'missing/report.txt'
            result = subprocess.run(['bash', str(HEALTH), '--output', str(output)],
                                    text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('wrote ', result.stdout)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
