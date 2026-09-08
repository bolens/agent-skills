# Hermes and Pi

This collection uses Agent Skills directories with SKILL.md entrypoints and
relative resources. Client discovery support does not supply missing tools,
model credentials, browser integrations, or the operating system required by a
skill. Keep the repository at its stable installed path.

## Installation

The existing default installer still manages Codex, shared, and Claude homes.
Select optional native homes explicitly:

```sh
python3 scripts/link-installed.py --apply --client hermes --client pi
python3 scripts/link-installed.py --check --client hermes --client pi
```

| Client | Default target | Override | Catalog |
| --- | --- | --- | --- |
| Hermes Agent | ~/.hermes/skills | HERMES_HOME, the active profile directory | Automatically invocable skills only |
| Pi coding agent | ~/.pi/agent/skills | PI_CODING_AGENT_DIR | All registered skills |

Repeat `--client` to combine selections. Add `--client registered` to include the
original homes. Default `make check` verifies only the original homes, so run the
explicit check above for optional installations. Generated `optional_install_targets`
in PROVENANCE.json owns these paths. Existing independent directories are refused
unless `--replace` is explicitly supplied. Inspect collisions before replacing
anything. Apply may install other entries before reporting a conflict.

Pi also supports the shared ~/.agents/skills home. Its inspected loader follows
symlinks and deduplicates identical real files. Native links help when using a
separate Pi profile or a version without shared-home discovery. Do not add every
client home to settings. Inspect same-name collisions from independent copies.
For a session-scoped load, Pi supports `--skill /absolute/path/to/skills`.

Hermes supports `skills.external_dirs` in config.yaml as an alternative, with
local skills taking precedence. Do not point it at the entire shared collection
when preserving explicit-only invocation: its inspected loader does not honor
Pi's frontmatter flag. The optional installer supplies a filtered native catalog
without changing profile configuration or project trust.

## Invocation and ownership

Pi uses `/skill:name`. Hermes uses `/name` or its skill discovery tools. Slash
examples inside imported skills may use another client's spelling. Use the
current client's invocation syntax while retaining the skill's task and authority.

Seven existing explicit-only skills retain Codex's agents/openai.yaml policy and
now carry `disable-model-invocation: true` for Pi. Hermes optional targets omit
these skills. To use one there, explicitly ask the agent to read its absolute
SKILL.md path in the canonical checkout and follow it for the requested task.
Resolve its resources from that file's directory. This is explicit file loading,
not a claim of native slash-command support for excluded skills. If another
installation already exposes one, the installer does not remove it. Inspect that
catalog separately before relying on its invocation policy.

Read referenced files through the client's filesystem tool when a specialized
skill-view tool cannot follow a sibling reference. Resolve references from the
canonical skill location, never the current project by guesswork. Load only the
needed resource. Use the client's available read, shell, edit, or browser tools
for their equivalent capabilities. Do not invent Codex tool names or assume
subagent, image-generation, permission, or artifact-rendering features exist.
Report a required unavailable capability and complete independent work in scope.

Symlinks expose the source checkout. Hermes can modify writable skills, including
external directories. Keep edits under this repository's review workflow and
preserve independent client-created skills. Installation does not configure a
read-only boundary, grant action authority, or install the agent runtimes.

## Evidence and references

Reviewed 2026-09-08:

- [Pi skills documentation](https://pi.dev/docs/latest/skills) describes discovery,
  explicit invocation, schemas, and relative resources.
- [Pi loader at 6160683](https://github.com/badlogic/pi-mono/blob/6160683a4a8012f0d1cd30c145df18b4ca6f5176/packages/coding-agent/src/core/skills.ts)
  follows symlinks, deduplicates real files, and reads disable-model-invocation.
- [Hermes skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/)
  describes profiles, external directories, ownership, and invocation.
- [Hermes loader at b2aa855](https://github.com/NousResearch/hermes-agent/blob/b2aa855b626ff8688eb34b95c60ee8b6a4af3679/tools/skills_tool.py)
  and [directory traversal](https://github.com/NousResearch/hermes-agent/blob/b2aa855b626ff8688eb34b95c60ee8b6a4af3679/agent/skill_utils.py)
  establish catalog filtering and symlink traversal. No explicit-only frontmatter
  handling was found in that loader.

Installer tests exercise temporary profiles, policy parity, repeated application,
conflict preservation, check-only behavior, and relative resources. These are
repository integration tests plus upstream source inspection. Neither client was
installed on the verification host, so model-driven sessions and live catalog
rendering remain unverified. After installing a client, inspect its skill list,
load one ordinary skill and a supporting reference, and check explicit-only
behavior before relying on it for unattended work.
