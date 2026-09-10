"""Exercise Hermes's native traversal, not its provider-backed skill tool."""
import importlib.util
import json
import sys
from pathlib import Path

native, repository, home = map(Path, sys.argv[1:])
sys.path.insert(0, str(native))
spec = importlib.util.spec_from_file_location('hermes_skill_utils', native / 'agent/skill_utils.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
manifest = json.loads((repository / 'PROVENANCE.json').read_text())['skills']
expected = {e['name'] for e in manifest if 'hermes' in e['optional_install_targets']}
catalog = home / '.hermes/skills'
paths = list(module.iter_skill_index_files(catalog, 'SKILL.md'))
assert {p.parent.name for p in paths} == expected
assert len(paths) == len(expected)
assert paths == sorted(paths)
for path in paths:
    assert path.resolve() == (repository / 'skills' / path.parent.name / 'SKILL.md').resolve()
owner = next(p for p in paths if p.parent.name == 'codebase-design')
assert (owner.parent / 'references/experience-and-interfaces.md').read_text()
assert (owner.parent / '../ci-maintenance/references/setup-contracts.md').read_text()
print(f'Hermes native traversal: {len(paths)} skills; filtered catalog and filesystem resource reads passed')
