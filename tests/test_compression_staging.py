"""Exercise compressor writes with synthetic model output and isolated state."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/caveman-compress/scripts'
SPEC = importlib.util.spec_from_file_location('caveman_fixture', SCRIPTS / '__init__.py',
                                            submodule_search_locations=[str(SCRIPTS)])
PACKAGE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PACKAGE
SPEC.loader.exec_module(PACKAGE)
from caveman_fixture import compress


class CompressionStagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='compression-fixture-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'notes.md'
        self.original = b'# Notes\n\nYou should always preserve the source.\n'
        self.source.write_bytes(self.original)
        self.neighbor = self.root / 'notes.md.caveman-staged'
        self.neighbor.write_bytes(b'unrelated existing work')
        state = patch.object(compress, '_state_base_dir',
                             side_effect=lambda kind: self.root / 'state' / kind)
        state.start()
        self.addCleanup(state.stop)

    def assert_preserved_neighbor_and_no_scratch(self):
        self.assertEqual(self.neighbor.read_bytes(), b'unrelated existing work')
        self.assertEqual(sorted(p.name for p in self.root.iterdir()),
                         ['notes.md', 'notes.md.caveman-staged', 'state'])

    @patch.object(compress, 'call_claude', return_value='# Notes\n\nPreserve source.\n')
    def test_success_retains_neighbor_and_exact_backup(self, model):
        self.assertTrue(compress.compress_file(self.source))
        self.assertEqual(self.source.read_text(), '# Notes\n\nPreserve source.\n')
        backup = compress.backup_dir_for(self.source) / 'notes.original.md'
        self.assertEqual(backup.read_bytes(), self.original)
        self.assert_preserved_neighbor_and_no_scratch()
        model.assert_called_once()

    @patch.object(compress, 'call_claude', return_value='# Changed\n\nWrong heading.\n')
    def test_rejected_candidates_leave_source_and_neighbor_intact(self, _model):
        self.assertFalse(compress.compress_file(self.source))
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assert_preserved_neighbor_and_no_scratch()

    @patch.object(compress, 'validate', side_effect=RuntimeError('fixture validation error'))
    @patch.object(compress, 'call_claude', return_value='# Notes\n\nPreserve source.\n')
    def test_exception_cleans_candidate_and_preserves_source(self, _model, _validate):
        with self.assertRaisesRegex(RuntimeError, 'fixture validation error'):
            compress.compress_file(self.source)
        self.assertEqual(self.source.read_bytes(), self.original)
        self.assert_preserved_neighbor_and_no_scratch()
