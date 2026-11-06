#!/usr/bin/env python3
"""Select the official HTTPS Ubuntu archive in a disposable hosted CI job."""
import os
import platform
import re
import sys
import tempfile
from pathlib import Path

SOURCE = Path('/etc/apt/sources.list.d/ubuntu.sources')
ARCHIVE = 'https://archive.ubuntu.com/ubuntu'
HOSTED_MIRROR = 'mirror+file:/etc/apt/apt-mirrors.txt'
AZURE = {'http://azure.archive.ubuntu.com/ubuntu', 'https://azure.archive.ubuntu.com/ubuntu'}


def configure_sources(content):
    recognized = False
    output = []
    for line in content.splitlines(keepends=True):
        if line.startswith('URIs:'):
            def replace(match):
                nonlocal recognized
                uri = match.group(0)
                canonical = uri.rstrip('/')
                if canonical in AZURE or canonical == ARCHIVE or uri == HOSTED_MIRROR:
                    recognized = True
                    return ARCHIVE + ('/' if uri.endswith('/') else '')
                return uri
            line = re.sub(r'(?:https?://|mirror\+file:)[^\s]+', replace, line)
        output.append(line)
    if not recognized:
        raise ValueError('Expected the hosted Ubuntu archive source; no files changed')
    return ''.join(output)


def main():
    if sys.argv[1:] != ['--apply-github-hosted'] or sys.platform != 'linux' or os.geteuid() != 0:
        raise SystemExit('Use --apply-github-hosted only in a disposable Ubuntu Actions job')
    if platform.freedesktop_os_release().get('ID') != 'ubuntu':
        raise SystemExit('Ubuntu package sources required')
    original = SOURCE.read_text()
    changed = configure_sources(original)
    if changed != original:
        mode = SOURCE.stat().st_mode & 0o777
        descriptor, name = tempfile.mkstemp(prefix='.ci-ubuntu-', dir=SOURCE.parent)
        temporary = Path(name)
        try:
            with os.fdopen(descriptor, 'w') as stream:
                stream.write(changed)
            temporary.chmod(mode)
            temporary.replace(SOURCE)
        finally:
            temporary.unlink(missing_ok=True)
    print('Official HTTPS Ubuntu archive selected; suites and signing policy preserved.')


if __name__ == '__main__':
    main()
