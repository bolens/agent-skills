"""Keep native selection equivalent to the hosted aggregate's requirements."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


class ArchifySelection(unittest.TestCase):
    def test_pull_request_paths_match_both_ci_systems(self):
        hosted = yaml.safe_load((ROOT / '.github/workflows/ci.yml').read_text())
        filters = hosted['jobs']['changes']['steps'][0]['with']['filters']
        paths = yaml.safe_load(filters)['archify']
        native = yaml.safe_load((ROOT / '.woodpecker/archify.yml').read_text())
        selected = [rule for rule in native['when'] if rule['event'] == 'pull_request']
        self.assertEqual(len(selected), 1)
        self.assertEqual(set(paths), set(selected[0]['path']['include']))
        self.assertIn('skills/archify/**', paths)
        self.assertIn('scripts/test_archify.py', paths)
        self.assertIn('.woodpecker/archify.yml', paths)

    def test_main_and_manual_native_runs_do_not_depend_on_path_changes(self):
        native = yaml.safe_load((ROOT / '.woodpecker/archify.yml').read_text())
        rules = {rule['event']: rule for rule in native['when']}
        self.assertEqual(rules['push'], {'event': 'push', 'branch': 'main'})
        self.assertEqual(rules['manual'], {'event': 'manual'})
        self.assertEqual(native['depends_on'], ['portable'])


if __name__ == '__main__':
    unittest.main()
