#!/usr/bin/env python3
"""Prepare a private Linux x86_64 runtime from the verified Sentrux grammar archive."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tarfile

NOTICES = Path(__file__).resolve().parents[1] / 'references/sentrux-notices'


def prepare(archive, runtime):
    provenance = json.loads((NOTICES / 'provenance.json').read_text())
    if hashlib.sha256(archive.read_bytes()).hexdigest() != provenance['grammar_archive_sha256']:
        raise ValueError('Grammar archive SHA-256 mismatch')
    expected_notices = {'SENTRUX-LICENSE': provenance['source_license_sha256']}
    expected_notices.update({p['language'] + '-LICENSE': p['notice_sha256'] for p in provenance['grammars']})
    for name, sha in expected_notices.items():
        if hashlib.sha256((NOTICES / name).read_bytes()).hexdigest() != sha:
            raise ValueError(f'License notice mismatch: {name}')
    runtime.mkdir(parents=True, exist_ok=False, mode=0o700)
    plugins = runtime / '.sentrux/plugins'
    plugins.mkdir(parents=True)
    manifest = {}
    with tarfile.open(archive, 'r:gz') as bundle:
        for item in provenance['grammars']:
            name = item['language'] + '/grammars/linux-x86_64.so'
            member = bundle.getmember(name)
            if not member.isfile() or member.size > 100 * 1024 * 1024:
                raise ValueError(f'Unexpected grammar member: {name}')
            stream = bundle.extractfile(member)
            if stream is None:
                raise ValueError(f'Missing grammar content: {name}')
            with stream:
                data = stream.read()
            target = plugins / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            manifest[name] = hashlib.sha256(data).hexdigest()
    (runtime / 'grammars.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (runtime / '.sentrux/telemetry_opt_out').touch()
    shutil.copytree(NOTICES, runtime / 'notices')
    print(f'Prepared {len(manifest)} verified grammars with notices: {runtime}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    args = parser.parse_args()
    try:
        prepare(args.archive, args.runtime)
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        print(f'Runtime unavailable: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
