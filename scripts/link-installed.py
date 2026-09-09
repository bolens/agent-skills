#!/usr/bin/env python3
"""Check or install symlinks from configured skill homes to this repository."""

from __future__ import annotations

import argparse
import errno
import json
import os
import shutil
import tempfile
from contextlib import ExitStack
from pathlib import Path

from skill_metadata import read_metadata

ROOT = Path(__file__).resolve().parents[1]
MAX_CATALOG_ENTRIES = 10000
IGNORED_DIRS = {".git", ".hub", ".archive", "node_modules", "__pycache__", ".venv"}


def snapshot(path: Path):
    try:
        state = path.lstat()
        return state.st_dev, state.st_ino, state.st_mode, state.st_mtime_ns
    except FileNotFoundError:
        return None


def audit_catalog(home: Path, expected: dict[Path, str], excluded: set[str]) -> list[str]:
    """Inspect a bounded catalog without deleting stale links or independent skills."""
    problems = []
    pending = [home]
    seen = set()
    count = 0
    names = set(expected.values())
    while pending:
        directory = pending.pop()
        try:
            identity = directory.stat()
            key = (identity.st_dev, identity.st_ino)
            if key in seen:
                problems.append(f"catalog directory alias or cycle: {directory}")
                continue
            seen.add(key)
            with os.scandir(directory) as entries:
                children = []
                for entry in entries:
                    count += 1
                    if count > MAX_CATALOG_ENTRIES:
                        return problems + [f"catalog scan incomplete: {home} exceeds {MAX_CATALOG_ENTRIES} entries"]
                    children.append(entry)
            for entry in sorted(children, key=lambda item: item.name):
                path = Path(entry.path)
                if entry.name in IGNORED_DIRS:
                    continue
                if entry.is_symlink() and path not in expected:
                    if path.resolve().is_relative_to(ROOT / "skills"):
                        problems.append(f"unexpected repository-owned link: {path}")
                if not entry.is_dir(follow_symlinks=True):
                    continue
                skill = path / "SKILL.md"
                if skill.is_file():
                    name = read_metadata(skill)['name']
                    if name in excluded:
                        problems.append(f"excluded skill exposed in catalog: {path} ({name})")
                    elif name in names and path not in expected:
                        problems.append(f"conflicting skill name in catalog: {path} ({name})")
                    continue
                pending.append(path)
        except FileNotFoundError:
            if directory != home:
                problems.append(f"catalog entry disappeared: {directory}")
        except (OSError, RuntimeError, UnicodeError, ValueError) as error:
            problems.append(f"cannot inspect catalog {directory}: {error}")
    return problems


def expand(value: str) -> Path:
    defaults = {'CODEX_HOME': '.codex', 'AGENTS_HOME': '.agents',
                'CLAUDE_HOME': '.claude', 'HERMES_HOME': '.hermes',
                'PI_CODING_AGENT_DIR': '.pi/agent'}
    for variable, default in defaults.items():
        token = '${' + variable + ':-$HOME/' + default + '}'
        if value.startswith(token + '/'):
            base = Path(os.environ.get(variable) or str(Path.home() / default)).expanduser()
            if not base.is_absolute():
                raise ValueError(f'{variable} must be absolute: {base}')
            target = base / value[len(token) + 1:]
            # Resolve parent aliases, never dereference the skill link itself.
            return target.parent.resolve() / target.name
    raise ValueError(f'unsupported install target: {value}')


def issue(code, message):
    return {'code': code, 'message': message}


def check_catalog_identities(homes):
    identities = {}
    for home in homes:
        try:
            state = home.stat()
        except FileNotFoundError:
            continue
        identity = state.st_dev, state.st_ino
        if identity in identities and identities[identity] != home:
            raise ValueError(f'client catalogs share a filesystem directory: {identities[identity]} and {home}')
        identities[identity] = home


def prepare(args, manifest):
    clients = set(args.client or ['registered'])
    expected, homes, changes, problems = {}, {}, [], []
    for entry in manifest['skills']:
        source = (ROOT / 'skills' / entry['name']).resolve()
        if not (source / 'SKILL.md').is_file():
            raise ValueError(f'missing source skill: {source}')
        targets = list(entry['install_targets']) if 'registered' in clients else []
        for client in ('hermes', 'pi'):
            target = entry.get('optional_install_targets', {}).get(client)
            if client in clients and target:
                targets.append(target)
        for raw_target in targets:
            target = expand(raw_target)
            profile = raw_target.split('}', 1)[0]
            if target.parent in homes and homes[target.parent] != profile:
                raise ValueError(f'client catalogs share a destination: {target.parent}')
            homes[target.parent] = profile
            expected[target] = entry['name']
            if target.is_symlink() and target.resolve() == source:
                continue
            if args.check:
                code = 'conflict' if snapshot(target) is not None else 'missing_link'
                problems.append(issue(code, f'{target} -> expected {source}'))
            elif target.exists() and not target.is_symlink() and not args.replace:
                problems.append(issue('conflict', f'refusing existing target without --replace: {target}'))
            else:
                changes.append((target, source, snapshot(target)))
    ordered = sorted(homes)
    for index, home in enumerate(ordered):
        if any(other.is_relative_to(home) for other in ordered[index + 1:]):
            raise ValueError(f'client catalogs overlap: {home}')
    check_catalog_identities(homes)
    excluded = {entry['name'] for entry in manifest['skills']
                if 'hermes' not in entry.get('optional_install_targets', {})}
    for home, profile in sorted(homes.items()):
        for message in audit_catalog(home, {p: n for p, n in expected.items() if p.parent == home},
                                     excluded if profile.startswith('${HERMES_HOME') else set()):
            code = 'scan_incomplete'
            if message.startswith('excluded skill'):
                code = 'excluded_skill'
            elif message.startswith('unexpected repository-owned'):
                code = 'stale_link'
            elif message.startswith('conflicting skill'):
                code = 'conflict'
            problems.append(issue(code, message))
    return homes, changes, problems


def lock_catalogs(stack, homes, apply):
    # Directory descriptors coordinate aliases and independent source worktrees.
    # No lockfile can be orphaned or unlinked while another writer owns it.
    try:
        import fcntl
    except ImportError:
        if apply:
            raise ValueError('catalog apply requires POSIX directory locking') from None
        return
    if apply:
        for home in sorted(homes):
            home.mkdir(parents=True, exist_ok=True)
        check_catalog_identities(homes)
    for home in sorted(homes):
        if not home.exists():
            continue
        descriptor = os.open(home, os.O_RDONLY)
        stack.callback(os.close, descriptor)
        try:
            fcntl.flock(descriptor, (fcntl.LOCK_EX if apply else fcntl.LOCK_SH) | fcntl.LOCK_NB)
        except BlockingIOError:
            raise BlockingIOError(f'catalog busy: {home}') from None
        except OSError as error:
            if error.errno in {errno.ENOSYS, errno.ENOTSUP, errno.EOPNOTSUPP, errno.EINVAL, errno.EBADF}:
                raise ValueError(f'catalog filesystem does not support directory locking: {home}; '
                                 'use a local POSIX filesystem (the Linux filesystem inside WSL)') from error
            raise


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--apply', action='store_true')
    mode.add_argument('--plan', action='store_true', help='preview changes without writing')
    parser.add_argument('--replace', action='store_true', help='replace existing non-symlink targets')
    parser.add_argument('--json', action='store_true', help='emit a versioned result object')
    parser.add_argument('--client', action='append', choices=('registered', 'hermes', 'pi'))
    args = parser.parse_args()
    report = {'schema_version': 1, 'mode': 'apply' if args.apply else 'check' if args.check else 'plan',
              'source': str(ROOT), 'status': 'ok', 'changes': [], 'issues': []}
    try:
        manifest = json.loads((ROOT / 'PROVENANCE.json').read_text())
        homes, changes, problems = prepare(args, manifest)
        with ExitStack() as stack:
            if not problems:
                lock_catalogs(stack, homes, args.apply)
                locked_homes, changes, problems = prepare(args, manifest)
                if locked_homes != homes:
                    raise ValueError('catalog paths changed during preflight')
            report['issues'] = problems
            for target, source, previous in changes:
                row = {'target': str(target), 'source': str(source),
                       'action': 'replace' if previous is not None else 'link', 'applied': False}
                report['changes'].append(row)
            if args.apply and not problems:
                for (target, source, previous), row in zip(changes, report['changes']):
                    if snapshot(target) != previous:
                        raise ValueError(f'target changed after preflight; stopping: {target}')
                    if target.is_symlink():
                        # Build the replacement before touching the old link. The
                        # temporary directory is on the destination filesystem.
                        with tempfile.TemporaryDirectory(prefix='.agent-skills-link-', dir=target.parent) as directory:
                            candidate = Path(directory) / 'link'
                            candidate.symlink_to(source, target_is_directory=True)
                            if snapshot(target) != previous:
                                raise ValueError(f'target changed during replacement: {target}')
                            os.replace(candidate, target)
                        row['applied'] = True
                        continue
                    elif target.exists():
                        if target.is_dir():
                            shutil.rmtree(target)
                        else:
                            target.unlink()
                    target.symlink_to(source, target_is_directory=True)
                    row['applied'] = True
    except BlockingIOError as error:
        report['issues'].append(issue('busy', str(error)))
    except (OSError, ValueError, RuntimeError) as error:
        report['issues'].append(issue('operation_failed', str(error)))
    if report['issues']:
        report['status'] = 'partial' if any(row['applied'] for row in report['changes']) else 'failed'
    if args.json:
        print(json.dumps(report, sort_keys=True))
    else:
        for row in report['changes']:
            if args.plan or row['applied']:
                verb = 'linked' if row['applied'] else row['action']
                print(f"{verb} {row['target']} -> {row['source']}")
        for problem in report['issues']:
            print(problem['message'])
    return 0 if report['status'] == 'ok' else 1


if __name__ == '__main__':
    raise SystemExit(main())
