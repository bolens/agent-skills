"""Keep native selection equivalent to the hosted aggregate's requirements."""
import copy
import json
from pathlib import Path
import subprocess
import sys
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


    def test_hosted_aggregate_is_cancellable_without_implicit_success_guard(self):
        hosted = yaml.safe_load((ROOT / '.github/workflows/ci.yml').read_text())
        validate = hosted['jobs']['validate']
        self.assertEqual(validate['if'], '${{ !cancelled() }}')
        self.assertEqual(
            validate['needs'], ['changes', 'archify', 'archify-browser', 'symlinks-macos']
        )

    def test_actual_hosted_dependency_validator_remains_fail_closed(self):
        hosted = yaml.safe_load((ROOT / '.github/workflows/ci.yml').read_text())
        steps = hosted['jobs']['validate']['steps']
        validator = next(step['run'] for step in steps if step.get('name') == 'Require selected validation jobs')
        lines = validator.splitlines()
        self.assertEqual(lines[0], "python3 - <<'PYTHON'")
        self.assertEqual(lines[-1], 'PYTHON')
        script = '\n'.join(lines[1:-1])
        successful = {
            'changes': {'result': 'success', 'outputs': {'archify': 'true'}},
            'archify': {'result': 'success'},
            'archify-browser': {'result': 'success'},
            'symlinks-macos': {'result': 'success'},
        }
        cases = [('selected-success', successful, 0)]
        unselected = copy.deepcopy(successful)
        unselected['changes']['outputs']['archify'] = 'false'
        for name in ['archify', 'archify-browser']:
            unselected[name]['result'] = 'skipped'
        cases.append(('unselected-success', unselected, 0))
        for name in successful:
            for result in ['failure', 'cancelled', 'skipped']:
                changed = copy.deepcopy(successful)
                changed[name]['result'] = result
                cases.append((name + '-' + result, changed, 1))
        wrong_selection = copy.deepcopy(successful)
        wrong_selection['changes']['outputs']['archify'] = 'false'
        cases.append(('unexpected-executed-job', wrong_selection, 1))
        missing_selection = copy.deepcopy(successful)
        missing_selection['changes']['outputs'] = {}
        cases.append(('missing-selection', missing_selection, 1))
        invalid_selection = copy.deepcopy(successful)
        invalid_selection['changes']['outputs']['archify'] = 'invalid'
        cases.append(('invalid-selection', invalid_selection, 1))
        for label, needs, expected in cases:
            with self.subTest(label=label):
                result = subprocess.run(
                    [sys.executable, '-I', '-c', script],
                    env={'NEEDS_JSON': json.dumps(needs)},
                    capture_output=True,
                    timeout=5,
                    check=False,
                )
                self.assertEqual(result.returncode, expected, result.stderr.decode())

if __name__ == '__main__':
    unittest.main()
