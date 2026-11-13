import http.client
import importlib.util
import json
from pathlib import Path
import unittest
import urllib.error

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

    def test_workflow_context_is_allowlisted_and_cannot_reuse_another_workflow(self):
        self.assertEqual(handoff.workflow_context('pull_request', 'archify'), 'ci/woodpecker/pr/archify')
        self.assertEqual(handoff.workflow_context('workflow_dispatch', 'portable'), CONTEXT)
        for event, workflow in [('schedule', 'archify'), ('push', 'publish')]:
            with self.assertRaises(ValueError):
                handoff.workflow_context(event, workflow)
        self.assertEqual(handoff.select_state(*pair(), SHA, 'ci/woodpecker/push/archify'), 'missing')

    def test_dynamic_positive_workflow_index_remains_bound_to_context_and_source(self):
        data, history = pair()
        context = 'ci/woodpecker/push/archify'
        for item in [data['statuses'][0], history[0]]:
            item['context'] = context
            item['target_url'] = 'https://woodpecker.bolens.dev/repos/28/pipeline/7/2'
        self.assertEqual(handoff.select_state(data, history, SHA, context), 'success')
        self.assertEqual(handoff.select_state(data, history, SHA, CONTEXT), 'missing')
        for suffix in ['0', '02', '2?other=1', '2/other']:
            for item in [data['statuses'][0], history[0]]:
                item['target_url'] = 'https://woodpecker.bolens.dev/repos/28/pipeline/7/' + suffix
            with self.assertRaises(ValueError):
                handoff.select_state(data, history, SHA, context)

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

    def test_transient_read_uses_a_fresh_pair_before_accepting_success(self):
        responses = iter([http.client.RemoteDisconnected('connection closed'),
                          pair('pending'), pair('success')])
        clock = [0]
        reads = []

        def read():
            reads.append(clock[0])
            response = next(responses)
            if isinstance(response, Exception):
                raise response
            return response

        handoff.wait(read, SHA, CONTEXT, clock=lambda: clock[0],
                     sleep=lambda seconds: clock.__setitem__(0, clock[0] + seconds), timeout=45)
        self.assertEqual(reads, [0, 15, 30])

    def test_narrow_socket_failures_and_wrappers_use_the_same_deadline(self):
        for error in [http.client.RemoteDisconnected('closed'), ConnectionResetError('reset'),
                      TimeoutError('timed out'),
                      urllib.error.URLError(http.client.RemoteDisconnected('closed')),
                      urllib.error.URLError(ConnectionResetError('reset')),
                      urllib.error.URLError(TimeoutError('timed out'))]:
            with self.subTest(error=repr(error)):
                clock = [0]
                reads = []

                def read():
                    reads.append(clock[0])
                    raise error

                with self.assertRaises(TimeoutError):
                    handoff.wait(read, SHA, CONTEXT, clock=lambda: clock[0],
                                 sleep=lambda seconds: clock.__setitem__(0, clock[0] + seconds),
                                 timeout=31)
                self.assertEqual(reads, [0, 15, 30])
                self.assertEqual(clock[0], 31)

    def test_fatal_lookup_errors_do_not_retry(self):
        for error in [urllib.error.HTTPError('https://api.github.com/', 401, 'Unauthorized', {}, None),
                      urllib.error.HTTPError('https://api.github.com/', 503, 'Unavailable', {}, None),
                      urllib.error.URLError('certificate verification failed'),
                      RuntimeError('unexpected GitHub API redirect'),
                      json.JSONDecodeError('invalid JSON', '', 0)]:
            with self.subTest(error=repr(error)), self.assertRaises(type(error)):
                def read():
                    raise error

                handoff.wait(read, SHA, CONTEXT,
                             sleep=lambda seconds: self.fail('fatal lookup must not retry'))
            if isinstance(error, urllib.error.HTTPError):
                error.close()

    def test_malformed_or_wrong_identity_pair_does_not_retry(self):
        for data, history in [(None, []), pair()]:
            if data is not None:
                history[0]['creator']['id'] = 42
            with self.subTest(data=data), self.assertRaises((AttributeError, ValueError)):
                handoff.wait(lambda: (data, history), SHA, CONTEXT,
                             sleep=lambda seconds: self.fail('invalid pair must not retry'))

    def test_transport_retry_does_not_hide_native_failure(self):
        clock = [0]
        reads = []

        def read():
            reads.append(clock[0])
            if len(reads) == 1:
                raise http.client.RemoteDisconnected('closed')
            return pair('failure')

        with self.assertRaisesRegex(RuntimeError, 'native validation failed'):
            handoff.wait(read, SHA, CONTEXT, clock=lambda: clock[0],
                         sleep=lambda seconds: clock.__setitem__(0, clock[0] + seconds), timeout=45)
        self.assertEqual(reads, [0, 15])
        self.assertEqual(clock[0], 15)

    def test_success_finishing_after_deadline_is_rejected(self):
        clock = [0]

        def read():
            clock[0] = 31
            return pair('success')

        with self.assertRaises(TimeoutError):
            handoff.wait(read, SHA, CONTEXT, clock=lambda: clock[0], timeout=30,
                         sleep=lambda seconds: self.fail('expired read must not sleep'))


if __name__ == '__main__':
    unittest.main()
