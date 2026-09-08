#!/usr/bin/env python3
"""Collect bounded, read-only Linux diagnostics with owned process-group cleanup."""

from __future__ import annotations

import argparse
import datetime
import os
import select
import selectors
import signal
import subprocess
import sys
import time


class Interrupted(BaseException):
    def __init__(self, signum):
        self.signum = signum


def interrupt(signum, _frame):
    raise Interrupted(signum)


def stop_group(process):
    """Clean descendants even when their original parent has already exited."""
    previous = {sig: signal.signal(sig, signal.SIG_IGN) for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        else:
            # Allow cooperative shutdown, then kill remaining group members.
            time.sleep(0.1)
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        try:
            process.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            # SIGKILL is pending for an uninterruptible kernel task. Do not hang.
            pass
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def run_probe(command, output, deadline, byte_limit):
    """Read small chunks without buffering the entire subprocess output."""
    process = None
    # Defer cancellation until spawn records ownership, without blocking signals
    # in the child (an inherited signal mask would prevent graceful shutdown).
    pending_signals = []
    previous = {sig: signal.signal(sig, lambda signum, _frame: pending_signals.append(signum))
                for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        try:
            process = subprocess.Popen(
                command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                stdin=subprocess.DEVNULL, start_new_session=True,
                env={**os.environ, 'PAGER': 'cat', 'SYSTEMD_PAGER': 'cat', 'LC_ALL': 'C'},
            )
        except FileNotFoundError:
            return f'UNAVAILABLE: {command[0]} is not installed'
        except OSError as exc:
            return f'CHECK_FAILED: {exc}'
        finally:
            for sig, handler in previous.items():
                signal.signal(sig, handler)
            if pending_signals:
                raise Interrupted(pending_signals[0])
        assert process.stdout is not None
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            remaining = byte_limit
            while True:
                wait = deadline - time.monotonic()
                if wait <= 0:
                    return 'TIMEOUT'
                events = selector.select(min(wait, 0.1))
                if not events:
                    continue
                chunk = os.read(process.stdout.fileno(), min(8192, remaining + 1))
                if not chunk:
                    try:
                        code = process.wait(timeout=max(0.001, deadline - time.monotonic()))
                    except subprocess.TimeoutExpired:
                        return 'TIMEOUT'
                    return 'OK' if code == 0 else f'CHECK_FAILED: exit={code}'
                output.write(chunk[:remaining])
                remaining -= min(len(chunk), remaining)
                if remaining == 0:
                    return 'OUTPUT_LIMIT'
    finally:
        if process is not None:
            stop_group(process)
            if process.stdout is not None:
                process.stdout.close()


QUICK = [
    ('Kernel and host', ['uname', '-a']),
    ('Uptime and load', ['uptime']),
    ('Memory', ['free', '-h']),
    ('Filesystem capacity', ['df', '-hT']),
    ('Failed system units', ['systemctl', '--failed', '--no-pager', '--no-legend']),
    ('Failed user units', ['systemctl', '--user', '--failed', '--no-pager', '--no-legend']),
    ('Recent coredumps', ['coredumpctl', '--no-pager', '--since', '-7 days']),
    ('Mount verification', ['findmnt', '--verify', '--verbose']),
    ('Block devices', ['lsblk', '-o', 'NAME,TYPE,FSTYPE,SIZE,FSUSE%,MOUNTPOINTS']),
    ('Package database lock', ['stat', '/var/lib/pacman/db.lck']),
]
FULL = [
    ('Journal errors this boot', ['journalctl', '-b', '-p', 'err', '--no-pager', '-n', '200']),
    ('Kernel warnings this boot', ['journalctl', '-k', '-b', '-p', 'warning', '--no-pager', '-n', '200']),
    ('Pressure', ['vmstat', '1', '5']),
    ('Top processes', ['ps', '-eo', 'pid,ppid,stat,%cpu,%mem,comm', '--sort=-%cpu']),
    ('Network links and addresses', ['ip', '-brief', 'address']),
    ('Routes', ['ip', 'route']),
    ('Sensors', ['sensors']),
    ('PCI graphics', ['lspci', '-k']),
    ('Hyprland version', ['hyprctl', 'version']),
    ('Hyprland config errors', ['hyprctl', 'configerrors']),
    ('Pending updates (cached databases; may be stale)', ['pacman', '-Qu']),
    ('Foreign packages', ['pacman', '-Qm']),
    ('Orphan packages', ['pacman', '-Qdt']),
]


def bounded_integer(low, high):
    def parse(value):
        number = int(value)
        if not low <= number <= high:
            raise argparse.ArgumentTypeError(f'must be between {low} and {high}')
        return number
    return parse


def collect(args, output):
    deadline = time.monotonic() + args.total_timeout
    output.write(f'# Workstation health snapshot\nmode={args.mode}\ncollected_at={datetime.datetime.now(datetime.timezone.utc).isoformat()}\n'.encode())
    output.write(b'\n## Session environment\n')
    for name in ('XDG_CURRENT_DESKTOP', 'XDG_SESSION_DESKTOP', 'XDG_SESSION_TYPE', 'WAYLAND_DISPLAY', 'DISPLAY', 'HYPRLAND_INSTANCE_SIGNATURE', 'DBUS_SESSION_BUS_ADDRESS'):
        value = os.environ.get(name, 'UNSET')
        # repr keeps multiline environment values out of report structure.
        output.write(f'{name}={value[:1024]!r}\n'.encode())
    limited = False
    for label, command in QUICK + (FULL if args.mode == 'full' else []):
        if time.monotonic() >= deadline:
            output.write(b'\nCOLLECTION_TIMEOUT: remaining probes skipped\n')
            return 1
        output.write(f'\n## {label}\n'.encode())
        status = run_probe(command, output, min(deadline, time.monotonic() + args.probe_timeout), args.max_bytes)
        output.write(f'\n{status}\n'.encode())
        limited |= status in ('TIMEOUT', 'OUTPUT_LIMIT')
    return int(limited)


class DeadlineWriter:
    """Bound pipe backpressure and handle partial nonblocking writes."""

    def __init__(self, fd, deadline):
        self.fd = fd
        self.deadline = deadline
        self.blocking = os.get_blocking(fd)
        os.set_blocking(fd, False)

    def write(self, data):
        pending = memoryview(data)
        while pending:
            remaining = self.deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError('collection deadline reached while writing report')
            try:
                written = os.write(self.fd, pending)
                if written == 0:
                    raise OSError('report output made no progress')
                pending = pending[written:]
            except BlockingIOError:
                select.select([], [self.fd], [], min(remaining, 0.1))

    def close(self):
        os.set_blocking(self.fd, self.blocking)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', nargs='?', choices=('quick', 'full'), default='quick')
    parser.add_argument('--output', help='create a private report; refuse existing paths')
    parser.add_argument('--probe-timeout', type=bounded_integer(1, 30), default=8, metavar='SECONDS')
    parser.add_argument('--total-timeout', type=bounded_integer(1, 300), default=60, metavar='SECONDS')
    parser.add_argument('--max-bytes', type=bounded_integer(1024, 1048576), default=65536, help='output bytes per probe (default: 65536)')
    args = parser.parse_args()
    output = None
    fd = None
    owned = False
    previous = {sig: signal.signal(sig, interrupt) for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        if args.output:
            fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
            owned = True
        else:
            fd = sys.stdout.fileno()
        output = DeadlineWriter(fd, time.monotonic() + args.total_timeout)
        result = collect(args, output)
        return result
    except Interrupted as exc:
        print('Collection interrupted; partial report retained.', file=sys.stderr)
        return 128 + exc.signum
    except (OSError, ValueError) as exc:
        print(f'Collection failed: {exc}', file=sys.stderr)
        return 1
    finally:
        if output is not None:
            output.close()
        if owned:
            os.close(fd)
        for sig, handler in previous.items():
            signal.signal(sig, handler)


if __name__ == '__main__':
    sys.exit(main())
