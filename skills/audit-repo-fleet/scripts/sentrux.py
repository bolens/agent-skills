#!/usr/bin/env python3
"""Optional, offline Sentrux snapshots. Linux x86_64, Python 3.10+, Git, bwrap."""
import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

BINARY_SHA256 = '3237f80fe20d54aad4deefa8a143f0d60543bb5d2d6ad891eb42432f155725a6'
VERSION = 1


# Extensions exported by the reviewed 0.5.7 embedded plugin configurations.
EXTENSIONS = {
    'bash': ['sh', 'bash'], 'python': ['py'],
    'javascript': ['js', 'mjs', 'cjs', 'jsx'],
    'typescript': ['ts', 'mts', 'cts', 'tsx'],
    'go': ['go'], 'rust': ['rs'], 'powershell': ['ps1', 'psm1', 'psd1'],
}


def validate_scope(scope):
    if not isinstance(scope, dict):
        raise ValueError('Scope must be an object')
    for key in ('include', 'exclude', 'context'):
        patterns = scope.get(key, [])
        if not isinstance(patterns, list) or any(not isinstance(p, str) or not p for p in patterns):
            raise ValueError(f'{key} must contain nonempty string patterns')
    if not scope.get('include'):
        raise ValueError('Scope requires include patterns')
    extensions = scope.get('extensions')
    if not isinstance(extensions, dict) or not extensions:
        raise ValueError('Scope requires extension/plugin mappings')
    for extension, language in extensions.items():
        if not isinstance(language, str) or extension not in ['.' + e for e in EXTENSIONS.get(language, [])]:
            raise ValueError(f'Unsupported extension/plugin mapping: {extension}: {language}')
    if 'rules' in scope and not isinstance(scope['rules'], str):
        raise ValueError('Rules must be TOML text')


def analyze(command):
    """Keep partial diagnostics even when the launcher fails or times out."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        return result.returncode, result.stdout + result.stderr, None
    except subprocess.TimeoutExpired as error:
        def decode(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
        return None, decode(error.stdout) + decode(error.stderr), 'Analyzer timed out after 120 seconds'
    except OSError as error:
        return None, '', str(error)


def analyzer_status(action, raw_status, log):
    """Exit 1 requires positive evidence of a completed architectural finding."""
    if action == 'baseline':
        return 0 if raw_status == 0 and 'Baseline saved to ' in log else 2
    if action == 'check':
        header = re.search(r'sentrux check .+? (\d+) rules checked', log)
        if not header or int(header[1]) == 0:
            return 2
        passed, failed = 'All rules pass', 'violation(s) found'
    else:
        if 'sentrux gate' not in log:
            return 2
        passed, failed = 'No degradation detected', 'DEGRADED'
    if raw_status == 0 and passed in log:
        return 0
    if raw_status == 1 and failed in log:
        return 1
    return 2


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def selected_files(repo, scope):
    """Include working changes and new files without writing the caller's index."""
    names = git(repo, 'ls-files', '-z', '--cached', '--others', '--exclude-standard')
    selected = {}
    source_count = 0
    for name in sorted(set(os.fsdecode(n) for n in names.split(b'\0') if n)):
        path = Path(name)
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('Unsafe Git path')
        context = any(fnmatch.fnmatchcase(name, p) for p in scope.get('context', []))
        if not context and not any(fnmatch.fnmatchcase(name, p) for p in scope['include']):
            continue
        if any(fnmatch.fnmatchcase(name, p) for p in scope.get('exclude', [])):
            continue
        if not context and path.suffix not in scope['extensions']:
            continue
        source = repo / path
        if source.is_symlink():
            raise ValueError(f'Non-regular input: {name}')
        if not source.exists():  # tracked deletion
            continue
        if not source.is_file() or not source.resolve().is_relative_to(repo):
            raise ValueError(f'Non-regular or escaping input: {name}')
        data = source.read_bytes()
        if len(data) > 512 * 1024:
            raise ValueError(f'Exceeds Sentrux parse limit: {name}')
        selected[name] = data
        source_count += path.suffix in scope['extensions']
    if not source_count or len(selected) >= 100_000:
        raise ValueError('Empty scope or Sentrux file limit reached')
    return selected


def runtime_identity(runtime, binary, scope):
    validate_scope(scope)
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise ValueError('This isolated runner supports Linux x86_64 only')
    if digest(binary.read_bytes()) != BINARY_SHA256:
        raise ValueError('Unreviewed Sentrux binary; expected verified 0.5.7')
    manifest = json.loads((runtime / 'grammars.json').read_text())
    plugins = runtime / '.sentrux/plugins'
    actual = {str(p.relative_to(plugins)): digest(p.read_bytes())
              for p in plugins.rglob('*.so')}
    if actual != manifest:
        raise ValueError('Grammar manifest mismatch')
    for language in set(scope['extensions'].values()):
        if f'{language}/grammars/linux-x86_64.so' not in manifest:
            raise ValueError(f'Missing grammar: {language}')
        if language in {'markdown', 'vlang'}:
            raise ValueError(f'Known broken 0.5.7 grammar: {language}')
    if not (runtime / '.sentrux/telemetry_opt_out').is_file():
        raise ValueError('Runtime must disable telemetry before startup')
    notices = Path(__file__).resolve().parents[1] / 'references/sentrux-notices'
    provenance = json.loads((notices / 'provenance.json').read_text())
    expected = {'SENTRUX-LICENSE': provenance['source_license_sha256']}
    expected.update({p['language'] + '-LICENSE': p['notice_sha256'] for p in provenance['grammars']})
    for name, sha in expected.items():
        if digest((runtime / 'notices' / name).read_bytes()) != sha:
            raise ValueError(f'Runtime license notice mismatch: {name}')
    return {'runner': VERSION, 'runner_sha256': digest(Path(__file__).read_bytes()),
            'binary': BINARY_SHA256, 'grammars': manifest}


def compatible(previous, identity):
    if previous['identity'] != identity:
        raise ValueError('Incompatible repository, scope, runner, binary, or grammars')


def sandbox(runtime, snapshot, binary, *args):
    home = str(Path.home())
    return ['bwrap', '--ro-bind', '/', '/', '--tmpfs', '/home',
            '--dir', home, '--bind', str(runtime), home,
            '--tmpfs', '/tmp', '--bind', str(snapshot), '/tmp/scan',
            '--ro-bind', str(binary), '/tmp/sentrux',
            '--chdir', '/tmp/scan', '--unshare-net', '--die-with-parent',
            '--setenv', 'SENTRUX_SKIP_GRAMMAR_DOWNLOAD', '1', '/tmp/sentrux', *args,
            '/tmp/scan']


def run(args):
    repo = args.repo.resolve()
    runtime = args.runtime.resolve()
    binary = Path(shutil.which(args.binary) or args.binary).resolve()
    scope = json.loads(args.scope.read_text())
    if args.output.resolve().is_relative_to(repo):
        raise ValueError('Evidence output must be outside the scanned repository')
    identity = runtime_identity(runtime, binary, scope)
    identity.update(repo=str(repo), scope=scope)
    files = selected_files(repo, scope)
    if args.output.exists():
        raise ValueError('Output already exists; choose a new evidence directory')
    previous = None
    if args.action == 'compare':
        if args.baseline is None:
            raise ValueError('compare requires --baseline')
        previous = json.loads((args.baseline / 'evidence.json').read_text())
        compatible(previous, identity)
        if previous['action'] != 'baseline' or previous['exit_code'] != 0:
            raise ValueError('Baseline is not a successful baseline run')
    evidence = {'identity': identity, 'revision': git(repo, 'rev-parse', 'HEAD').decode().strip(),
                'status': git(repo, 'status', '--porcelain').decode(errors='replace'),
                'files': {n: digest(d) for n, d in files.items()},
                'action': args.action,
                'coverage': 'Selected source only; parser availability does not prove import completeness.'}
    args.output.mkdir(parents=True, mode=0o700)
    with tempfile.TemporaryDirectory(prefix='sentrux-snapshot-') as temp:
        snapshot = Path(temp)
        for name, data in files.items():
            target = snapshot / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        (snapshot / '.sentrux').mkdir(exist_ok=True)
        (snapshot / '.sentrux/rules.toml').write_text(scope.get('rules', '[constraints]\nmax_cycles = 0\n'))
        if previous:
            baseline = args.baseline / 'baseline.json'
            if digest(baseline.read_bytes()) != previous['baseline_sha256']:
                raise ValueError('Baseline metrics were modified')
            shutil.copyfile(baseline, snapshot / '.sentrux/baseline.json')
        git(snapshot, 'init', '-q')
        git(snapshot, 'add', '-f', '--all')
        command = {'baseline': ['gate', '--save'], 'compare': ['gate'], 'check': ['check']}[args.action]
        raw_status, log, error = analyze(sandbox(runtime, snapshot, binary, *command))
        (args.output / 'sentrux.log').write_text(log)
        evidence['raw_exit_code'] = raw_status
        evidence['exit_code'] = analyzer_status(args.action, raw_status, log)
        if evidence['exit_code'] == 2:
            evidence['error'] = error or 'Analyzer did not complete the requested operation'
            print(evidence['error'], file=sys.stderr)
        counts = re.search(r'\[build_graphs\] (\d+) files .*?\| (\d+) import, (\d+) call, (\d+) inherit edges', log)
        if counts:
            evidence['graph_counts'] = dict(zip(('files', 'imports', 'calls', 'inheritance'), map(int, counts.groups())))
        metrics = snapshot / '.sentrux/baseline.json'
        if evidence['exit_code'] == 0 and args.action == 'baseline' and not metrics.is_file():
            evidence['exit_code'] = 2
            evidence['coverage'] = 'Inconclusive: analyzer did not save baseline metrics.'
        if evidence['exit_code'] == 0 and args.action == 'baseline' and metrics.is_file():
            if json.loads(metrics.read_text()).get('total_import_edges', 0) == 0:
                evidence['exit_code'] = 2
                evidence['coverage'] = 'Inconclusive: empty import graph; baseline not accepted.'
                print(evidence['coverage'], file=sys.stderr)
            else:
                shutil.copyfile(metrics, args.output / 'baseline.json')
                evidence['baseline_sha256'] = digest(metrics.read_bytes())
        (args.output / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
        print(log, end='')
        print(f'Evidence: {args.output}')
        return evidence['exit_code']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['baseline', 'compare', 'check'])
    parser.add_argument('repo', type=Path)
    parser.add_argument('--scope', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline', type=Path)
    parser.add_argument('--binary', default='sentrux')
    args = parser.parse_args()
    try:
        return run(args)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(f'Sentrux evidence unavailable: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
