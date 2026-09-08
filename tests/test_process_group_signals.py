"""Darwin can deny signals to an owned group containing only unreaped zombies."""
import importlib.util
import os
import signal
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    'skills/workstation-health-triage/scripts/collect-health.py',
    'skills/systematic-debugging/find-polluter.py',
    'skills/responsive-web-capture/scripts/capture-responsive.py',
]


@unittest.skipUnless(os.name == 'posix', 'helpers require POSIX process groups')
class ProcessGroupSignals(unittest.TestCase):
    def modules(self):
        for index, path in enumerate(PATHS):
            spec = importlib.util.spec_from_file_location(f'group_fixture_{index}', ROOT / path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            yield path, module

    def test_zombie_only_denial_reaps_and_retries_same_group(self):
        for path, module in self.modules():
            for signum in (signal.SIGTERM, signal.SIGKILL):
                with self.subTest(path=path, signum=signum):
                    child = Mock(pid=12345)
                    with patch.object(module.os, 'killpg', side_effect=[PermissionError(), ProcessLookupError()]) as kill:
                        self.assertFalse(module.signal_group(child, signum))
                    child.poll.assert_called_once_with()
                    self.assertEqual(kill.call_args_list, [call(child.pid, signum)] * 2)

    def test_persistent_permission_error_remains_an_error(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                child = Mock(pid=12345)
                with patch.object(module.os, 'killpg', side_effect=PermissionError()):
                    with self.assertRaises(PermissionError):
                        module.signal_group(child, signal.SIGKILL)
                child.poll.assert_called_once_with()

    def test_reaped_leader_does_not_skip_surviving_group(self):
        for path, module in self.modules():
            with self.subTest(path=path):
                child = Mock(pid=12345)
                child.poll.return_value = 0
                with patch.object(module.os, 'killpg', side_effect=[PermissionError(), None]) as kill:
                    self.assertTrue(module.signal_group(child, signal.SIGKILL))
                self.assertEqual(kill.call_count, 2)


if __name__ == '__main__':
    unittest.main()
