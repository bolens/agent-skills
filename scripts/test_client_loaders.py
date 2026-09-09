#!/usr/bin/env python3
"""Opt-in pinned client-loader checks. Network access required; no model calls."""
from __future__ import annotations

import base64
import contextlib
import hashlib
import io
import json
import os
import shutil
import signal
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/client-loaders'
MAX_DOWNLOAD = 32 * 1024 * 1024


@contextlib.contextmanager
def defer_interrupts():
    pending = []
    previous = {sig: signal.getsignal(sig) for sig in (signal.SIGINT, signal.SIGTERM)}
    try:
        for sig in previous:
            signal.signal(sig, lambda number, frame: pending.append(number))
        yield
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)
        if pending:
            raise KeyboardInterrupt


def download(url: str, algorithm: str, digest: str) -> bytes:
    with urllib.request.urlopen(url, timeout=30) as response:
        data = response.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise ValueError('client source download exceeds 32 MiB')
    actual = hashlib.new(algorithm, data).digest()
    expected = bytes.fromhex(digest) if algorithm == 'sha256' else base64.b64decode(digest, validate=True)
    if actual != expected:
        raise ValueError(f'client source integrity mismatch: {url}')
    return data


def extract_modules(archive: bytes, destination: Path, names: list[str]) -> None:
    # Never extract an archive wholesale or honor its symlinks or permissions.
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as bundle:
        for name in names:
            if Path(name).is_absolute() or '..' in Path(name).parts:
                raise ValueError('invalid module path')
            member = bundle.getmember('package/' + name)
            if not member.isfile() or member.size > 2 * 1024 * 1024:
                raise ValueError(f'invalid client module: {name}')
            output = destination / name
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(bundle.extractfile(member).read())


def run(command: list[str], cwd: Path, env: dict[str, str], timeout: int = 60) -> None:
    process = None
    try:
        with defer_interrupts():
            process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                       start_new_session=True)
        code = process.wait(timeout=timeout)
        if code:
            raise subprocess.CalledProcessError(code, command)
    finally:
        if process is not None:
            # Include surviving descendants even after their parent exits.
            with defer_interrupts():
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                except PermissionError:
                    process.poll()
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                finally:
                    process.wait(timeout=5)


def main() -> None:
    if os.name != 'posix':
        raise SystemExit('client-loader harness requires POSIX process groups')
    for tool in ('node', 'npm'):
        if not shutil.which(tool):
            raise SystemExit(f'{tool} is required; run through the repository development environment')
    sources = json.loads((FIXTURES / 'sources.json').read_text())
    with tempfile.TemporaryDirectory(prefix='agent-skills-loaders-') as directory:
        workspace = Path(directory)
        home = workspace / 'home'
        home.mkdir()
        env = {'PATH': os.environ.get('PATH', ''), 'HOME': str(home), 'LANG': 'C.UTF-8',
               'HERMES_HOME': str(home / '.hermes'), 'PI_CODING_AGENT_DIR': str(home / '.pi/agent'),
               'npm_config_userconfig': os.devnull, 'npm_config_cache': str(workspace / 'npm-cache'),
               'npm_config_update_notifier': 'false',
               'PYTHONDONTWRITEBYTECODE': '1'}
        run([sys.executable, str(ROOT / 'scripts/link-installed.py'), '--apply', '--client', 'pi', '--client', 'hermes'], workspace, env)
        for name in ('package.json', 'package-lock.json'):
            shutil.copyfile(FIXTURES / name, workspace / name)
        run(['npm', 'ci', '--ignore-scripts', '--no-audit', '--no-fund'], workspace, env, 180)
        pi = sources['pi']
        native = workspace / 'native-pi'
        algorithm, digest = pi['integrity'].split('-', 1)
        extract_modules(download(pi['url'], algorithm, digest), native, pi['files'])
        run(['node', str(FIXTURES / 'pi.mjs'), str(native), str(ROOT), str(home)], workspace, env)
        hermes = sources['hermes']
        native = workspace / 'native-hermes'
        for name, digest in hermes['files'].items():
            url = f"https://raw.githubusercontent.com/NousResearch/hermes-agent/{hermes['revision']}/{name}"
            data = download(url, 'sha256', digest)
            path = native / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        run([sys.executable, str(FIXTURES / 'hermes.py'), str(native), str(ROOT), str(home)], workspace, env)
    print('Client-loader checks passed; temporary profiles and dependencies removed')


if __name__ == '__main__':
    def interrupt(number, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, interrupt)
    main()
