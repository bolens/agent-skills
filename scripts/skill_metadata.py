"""Bounded, fail-closed skill frontmatter parsing shared by repository tools."""

import re
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    raise SystemExit("PyYAML is required: install requirements-dev.txt in your Python environment") from None


class SkillLoader(yaml.SafeLoader):
    """Reject aliases and duplicate keys instead of guessing client precedence."""

    def compose_node(self, parent, index):
        if self.check_event(yaml.AliasEvent):
            raise ValueError("frontmatter aliases are unsupported")
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise ValueError("frontmatter keys must be unique strings")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


# YAML 1.1's yes/no/on/off booleans differ from current client parsers.
SkillLoader.yaml_implicit_resolvers = {
    key: [(tag, pattern) for tag, pattern in values if tag != 'tag:yaml.org,2002:bool']
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
SkillLoader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(true|false)$'), list('tf'))


def read_metadata(path: Path) -> dict:
    try:
        with path.open(encoding='utf-8') as stream:
            text = stream.read(16385)
        lines = text.splitlines(keepends=True)
        if not lines or lines[0].strip() != '---':
            raise ValueError('missing frontmatter')
        end = next((i for i, line in enumerate(lines[1:], 1) if line.strip() == '---'), None)
        if end is None or sum(map(len, lines[:end + 1])) > 16384:
            raise ValueError('missing terminator or frontmatter exceeds 16384 characters')
        data = yaml.load(''.join(lines[1:end]), Loader=SkillLoader)
        if not isinstance(data, dict):
            raise ValueError('frontmatter must be a mapping')
        name = data.get('name')
        if not isinstance(name, str) or len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
            raise ValueError('invalid skill name')
        for key, limit in (('description', 1024), ('compatibility', 500)):
            if key == 'description' or key in data:
                value = data.get(key)
                if not isinstance(value, str) or not value.strip() or len(value) > limit:
                    raise ValueError(f'{key} must be a nonempty string of at most {limit} characters')
        if 'disable-model-invocation' in data and type(data['disable-model-invocation']) is not bool:
            raise ValueError('disable-model-invocation must be true or false')
        return data
    except (yaml.YAMLError, ValueError, RecursionError) as error:
        raise ValueError(f'{path}: invalid metadata: {error}') from error
