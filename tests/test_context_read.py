"""Behavioral coverage for bounded source output, including adversarial line sizes."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/audit-repo-fleet/scripts/context-read.py"


class ContextReadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "source with spaces.py"

    def run_reader(self, data, *args):
        self.path.write_bytes(data)
        return self.invoke(self.path, *args)

    def invoke(self, path, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(path), *map(str, args)],
            capture_output=True, check=False, timeout=10,
        )

    def assert_rejected(self, result):
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(result.stdout, b"")
        self.assertTrue(result.stderr)

    def test_exact_line_boundary_and_overflow(self):
        result = self.run_reader(b"x\n" * 350)
        self.assertEqual(result.returncode, 0, result.stderr)
        doc = json.loads(result.stdout)
        self.assertEqual(len(doc["lines"]), 350)
        self.assertEqual(doc["lines"][-1], {"line": 350, "text": "x"})
        self.assertIsNone(doc["next_start"])
        self.assert_rejected(self.run_reader(b"x\n" * 351))

    def test_targeted_read_preserves_numbers_and_continuation(self):
        data = b"".join(f"line {i}\n".encode() for i in range(1, 1001))
        result = self.run_reader(data, "--start", 600, "--limit", 2)
        self.assertEqual(result.returncode, 0, result.stderr)
        doc = json.loads(result.stdout)
        self.assertEqual(doc["lines"], [
            {"line": 600, "text": "line 600"}, {"line": 601, "text": "line 601"},
        ])
        self.assertEqual(doc["next_start"], 602)
        doc = json.loads(self.run_reader(data, "--start", 999, "--limit", 3).stdout)
        self.assertEqual(len(doc["lines"]), 2)
        self.assertIsNone(doc["next_start"])

    def test_long_selected_line_fails_but_can_be_skipped(self):
        data = b"x" * 1000000 + b"\nselected\n"
        self.assert_rejected(self.run_reader(data))
        result = self.run_reader(data, "--start", 2, "--limit", 1)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["lines"], [{"line": 2, "text": "selected"}])

    def test_json_escaping_also_obeys_byte_ceiling(self):
        self.assert_rejected(self.run_reader(b'"' * 14000))
        result = self.run_reader(b"x" * 22000)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertLessEqual(len(result.stdout), 24 * 1024)

    def test_exact_encoded_byte_boundary(self):
        sample = self.run_reader(b"x")
        self.assertEqual(sample.returncode, 0, sample.stderr)
        overhead = len(sample.stdout) - 1
        payload = b"x" * (24 * 1024 - overhead)
        result = self.run_reader(payload)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(result.stdout), 24 * 1024)
        self.assert_rejected(self.run_reader(payload + b"x"))

    def test_utf8_crlf_and_missing_final_newline(self):
        result = self.run_reader("caf\u00e9\r\nlast".encode())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["lines"], [
            {"line": 1, "text": "caf\u00e9"}, {"line": 2, "text": "last"},
        ])
        self.assert_rejected(self.run_reader(b"valid\n\xff"))

    def test_empty_file_and_past_eof(self):
        result = self.run_reader(b"")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["lines"], [])
        self.assert_rejected(self.run_reader(b"", "--start", 1, "--limit", 1))
        self.assert_rejected(self.run_reader(b"x\n", "--start", 2, "--limit", 1))

    def test_non_newline_carriage_returns_are_preserved(self):
        result = self.run_reader(b"first\r\r\nlast\r")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["lines"], [
            {"line": 1, "text": "first\r"}, {"line": 2, "text": "last\r"},
        ])

    def test_invalid_range_and_unavailable_paths(self):
        for args in (("--start", 1), ("--limit", 1), ("--start", 0, "--limit", 1),
                     ("--start", 1, "--limit", 351), ("--start", 1, "--limit", -1)):
            with self.subTest(args=args):
                self.assert_rejected(self.run_reader(b"source\n", *args))
        self.assert_rejected(self.invoke(self.path.parent / "missing"))
        self.assert_rejected(self.invoke(self.path.parent))


if __name__ == "__main__":
    unittest.main()
