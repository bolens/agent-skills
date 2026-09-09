import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class MetadataTests(unittest.TestCase):
    def parse(self, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'SKILL.md'
            path.write_text(text)
            return subprocess.run(
                [sys.executable, '-c',
                 'from skill_metadata import read_metadata; import sys; print(read_metadata(__import__("pathlib").Path(sys.argv[1])))',
                 str(path)], cwd=ROOT / 'scripts', text=True, capture_output=True, timeout=5)

    def test_comments_quotes_crlf_and_block_description(self):
        result = self.parse('---\r\nname: "test-skill"\r\ndescription: >\r\n  useful description\r\ndisable-model-invocation: true # explicit\r\n---\r\n')
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("'disable-model-invocation': True", result.stdout)

    def test_ambiguous_or_unbounded_metadata_fails_closed(self):
        for addition in ('disable-model-invocation: "false"', 'disable-model-invocation: yes',
                         'name: duplicate', 'metadata: &a [*a]', 'compatibility: 123',
                         'description: ' + 'x' * 17000):
            with self.subTest(addition=addition[:80]):
                result = self.parse('---\nname: test-skill\ndescription: useful\n' + addition + '\n---\n')
                self.assertNotEqual(0, result.returncode)
                self.assertIn('invalid metadata', result.stderr)
