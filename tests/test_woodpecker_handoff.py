import importlib.util
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('handoff', Path(__file__).resolve().parents[1] / 'scripts/wait-for-woodpecker.py')
handoff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(handoff)
SHA = 'a' * 40
CONTEXT = 'ci/woodpecker/push/portable'


def payload(state='success'):
    return {'sha': SHA, 'repository': {'id': handoff.REPOSITORY_ID, 'full_name': handoff.REPOSITORY},
            'statuses': [{'id': 123, 'context': CONTEXT, 'state': state,
                          'target_url': 'https://woodpecker.bolens.dev/repos/28/pipeline/7/1'}]}


def pair(state='success'):
    combined = payload(state)
    raw = dict(combined['statuses'][0], creator={'id': handoff.CREATOR_ID},
               url=f'https://api.github.com/repos/{handoff.REPOSITORY}/statuses/{SHA}')
    return combined, [raw]


class Handoff(unittest.TestCase):
    def test_actual_gitHub_schema_fixture(self):
        data = json.loads(Path(__file__).with_name('woodpecker-status.fixture.json').read_text())
        combined = data['combined']
        state = handoff.select_state(combined, data['history'], combined['sha'], CONTEXT)
        self.assertIn(state, {'pending', 'success', 'changed'})
        self.assertNotIn('creator', combined['statuses'][0])

    def test_success_is_for_exact_revision(self):
        self.assertEqual(handoff.select_state(*pair(), SHA, CONTEXT), 'success')
        with self.assertRaises(ValueError):
            handoff.select_state(*pair(), 'b' * 40, CONTEXT)

    def test_wrong_repository_and_publisher_fail(self):
        for field, value in [('repository', {'id': 1, 'full_name': handoff.REPOSITORY})]:
            data, history = pair()
            data[field] = value
            with self.assertRaises(ValueError):
                handoff.select_state(data, history, SHA, CONTEXT)
        data, history = pair()
        history[0]['creator']['id'] = 42
        with self.assertRaises(ValueError):
            handoff.select_state(data, history, SHA, CONTEXT)

    def test_wrong_pipeline_origin_or_repository_fails(self):
        for target in ['https://woodpecker.bolens.dev.attacker.test/repos/28/pipeline/7/1',
                       'https://woodpecker.bolens.dev/repos/17/pipeline/7/1']:
            data, history = pair()
            data['statuses'][0]['target_url'] = target
            history[0]['target_url'] = target
            with self.assertRaises(ValueError):
                handoff.select_state(data, history, SHA, CONTEXT)

    def test_other_event_context_cannot_satisfy_gate(self):
        self.assertEqual(handoff.select_state(*pair(), SHA, 'ci/woodpecker/pr/portable'), 'missing')

    def test_duplicate_context_is_not_arbitrarily_selected(self):
        data, history = pair()
        data['statuses'].append(dict(data['statuses'][0], state='failure'))
        with self.assertRaises(ValueError):
            handoff.select_state(data, history, SHA, CONTEXT)

    def test_newer_pending_cannot_reuse_old_success(self):
        data, history = pair()
        history.insert(0, dict(history[0], id=124, state='pending',
                               url=f'https://api.github.com/repos/{handoff.REPOSITORY}/statuses/{SHA}'))
        self.assertEqual(handoff.select_state(data, history, SHA, CONTEXT), 'changed')

    def test_combined_response_has_no_creator(self):
        data, history = pair()
        self.assertNotIn('creator', data['statuses'][0])
        self.assertEqual(handoff.select_state(data, history, SHA, CONTEXT), 'success')

    def test_actual_pending_to_success_transition(self):
        states = iter([pair('pending'), pair('success')])
        clock = [0]
        handoff.wait(lambda: next(states), SHA, CONTEXT, clock=lambda: clock[0],
                     sleep=lambda seconds: clock.__setitem__(0, clock[0] + seconds), timeout=30)
        self.assertEqual(clock[0], 15)

    def test_failure_is_immediate_and_never_sleeps(self):
        for state in ['failure', 'error']:
            with self.assertRaises(RuntimeError):
                handoff.wait(lambda: pair(state), SHA, CONTEXT,
                             sleep=lambda seconds: self.fail('failure must not retry'))

    def test_deadline_does_not_turn_missing_status_green(self):
        clock = [0]
        data, history = pair()
        data['statuses'] = []
        with self.assertRaises(TimeoutError):
            handoff.wait(lambda: (data, history), SHA, CONTEXT, clock=lambda: clock[0],
                         sleep=lambda seconds: clock.__setitem__(0, clock[0] + seconds), timeout=16)
        self.assertEqual(clock[0], 16)


if __name__ == '__main__':
    unittest.main()
