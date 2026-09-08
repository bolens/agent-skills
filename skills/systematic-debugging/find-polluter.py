#!/usr/bin/env python3
"""Bounded sequential search for an npm test that creates a specified path."""
from __future__ import annotations

import argparse
import contextlib
import fnmatch
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

EXCLUDED = {'.git', 'node_modules', '.venv', '.devenv', '.direnv', '__pycache__'}


class Interrupted(BaseException):
    def __init__(self, signum):
        self.signum = signum


def interrupt(signum, _frame):
    raise Interrupted(signum)


@contextlib.contextmanager
def defer_interrupts():
    pending = []
    previous = {sig: signal.signal(sig, lambda signum, _frame: pending.append(signum))
                for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        yield
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)
        if pending:
            raise Interrupted(pending[0])


def discover(pattern, deadline, max_tests, max_entries):
    """Do not follow links or enumerate dependency/cache trees."""
    pattern = pattern.removeprefix('./')
    collapsed = pattern.replace('**/', '')
    pending = [Path('.')]
    matches = []
    visited = 0
    while pending:
        directory = pending.pop()
        with os.scandir(directory) as entries:
            for entry in entries:
                if time.monotonic() >= deadline:
                    raise TimeoutError('total deadline reached during discovery')
                visited += 1
                if visited > max_entries:
                    raise ValueError('discovery entry limit reached')
                if entry.is_symlink():
                    continue
                path = Path(entry.path)
                if entry.is_dir(follow_symlinks=False):
                    if entry.name not in EXCLUDED:
                        pending.append(path)
                elif entry.is_file(follow_symlinks=False):
                    relative = path.as_posix()
                    if fnmatch.fnmatchcase(relative, pattern) or fnmatch.fnmatchcase(relative, collapsed):
                        matches.append('./' + relative)
                        if len(matches) > max_tests:
                            raise ValueError('matching test limit reached')
    if time.monotonic() >= deadline:
        raise TimeoutError('total deadline reached during discovery')
    return sorted(matches)


def run_test(command, deadline):
    process = None
    try:
        with defer_interrupts():
            process = subprocess.Popen(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL, start_new_session=True)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError('test deadline reached')
        return process.wait(timeout=remaining)
    finally:
        if process is not None:
            with defer_interrupts():
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                else:
                    time.sleep(0.1)
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                process.wait(timeout=1)


def bounded_integer(low, high):
    def parse(value):
        number = int(value)
        if not low <= number <= high:
            raise argparse.ArgumentTypeError(f'must be between {low} and {high}')
        return number
    return parse


def target_exists(path):
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('target', type=Path)
    parser.add_argument('pattern')
    parser.add_argument('--timeout', type=bounded_integer(1, 3600), default=60, help='seconds per test (default: 60)')
    parser.add_argument('--total-timeout', type=bounded_integer(1, 86400), default=600, help='total discovery/test seconds (default: 600)')
    parser.add_argument('--max-tests', type=bounded_integer(1, 10000), default=1000)
    parser.add_argument('--max-entries', type=bounded_integer(1, 1000000), default=100000)
    args = parser.parse_args()
    if os.name != 'posix':
        parser.error('requires POSIX process groups')
    if not args.pattern or args.pattern.startswith('/') or '..' in Path(args.pattern).parts:
        parser.error('test pattern must stay under the current directory')
    previous = {sig: signal.signal(sig, interrupt) for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        if target_exists(args.target):
            raise ValueError('target already exists; preserve it and use an isolated fixture')
        deadline = time.monotonic() + args.total_timeout
        tests = discover(args.pattern, deadline, args.max_tests, args.max_entries)
        if not tests:
            raise ValueError('no matching tests outside excluded directories')
        npm = shutil.which('npm')
        if npm is None:
            raise ValueError('npm is not installed')
        print(f'Found {len(tests)} test files', flush=True)
        failed = False
        for index, path in enumerate(tests, 1):
            if target_exists(args.target):
                raise ValueError('target appeared between tests; attribution is inconclusive')
            if time.monotonic() >= deadline:
                raise TimeoutError('total deadline reached; remaining tests skipped')
            print(f'[{index}/{len(tests)}] Testing: {path!r}', flush=True)
            code = run_test([npm, 'test', '--', path], min(deadline, time.monotonic() + args.timeout))
            if target_exists(args.target):
                print(f'FOUND POLLUTER: {path!r}\nCreated: {str(args.target)!r}')
                return 1
            failed |= code != 0
        if failed:
            raise ValueError('a test failed; no creator of the target was observed')
        print('No creator of the requested target was observed in the selected tests.')
        return 0
    except Interrupted as exc:
        print('Inconclusive: interrupted; observed artifacts preserved.', file=sys.stderr)
        return 128 + exc.signum
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f'Inconclusive: {exc}', file=sys.stderr)
        return 2
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


if __name__ == '__main__':
    sys.exit(main())
