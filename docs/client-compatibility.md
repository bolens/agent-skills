# Agent client compatibility

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
anything. Preflight conflicts prevent all planned writes. Later I/O failures can still leave
a partial installation. `--plan` reports intended changes without writing. Checks
also report obsolete links into this checkout, duplicate names, excluded Hermes
skills, and cycles. Catalog traversal stops at 10,000 entries per home. It never
removes those entries automatically and does not scan external directories named
in client configuration. Review those through the client's own catalog.

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
repository integration tests plus upstream source inspection. Native Pi loader and Hermes traversal checks now run through the harness below.
Model-driven sessions and live catalog rendering remain unverified. After installing a client, inspect its skill list,
load one ordinary skill and a supporting reference, and check explicit-only
behavior before relying on it for unattended work.


## Shared-home clients

The following primary docs describe support for ~/.agents/skills. Existing shared
links provide the files, so this repository does not create another set of copies.
Discovery alone does not establish invocation-policy or tool compatibility.

| Client | Verification and policy boundary |
| --- | --- |
| [OpenCode](https://opencode.ai/docs/skills/) | Inspect the native skill catalog and same-name sources. The documented frontmatter fields exclude disable-model-invocation. Use per-skill permission rules to hide or gate entries, rather than assuming Pi policy applies. An `ask` rule is approval gating, not explicit-only invocation. |
| [Gemini CLI](https://geminicli.com/docs/cli/skills/) | Run `gemini skills list --all` or `/skills list`, then `/skills reload` after changes. Workspace skills override user skills; the shared alias wins within its tier. Activation grants access to the skill directory, not necessarily sibling directories. Disable unwanted automatic skills through native settings and explicitly load files when needed. |
| [Copilot CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) | Use `/skills list`, `/skills info NAME`, and `/skills reload`. Current docs support disable-model-invocation and first-found name precedence; verify the installed version. CLI shared-home support does not install this collection in Copilot cloud agent or editor sessions. |

Use the existing seven explicit-only entries as the policy test set. Do not enable
them automatically because a client ignores an unknown metadata field. Keep
client-specific permission or exclusion changes reviewable and preserve unrelated
settings. No configuration changes for these clients were made by this task.

## Resource access and optional capabilities

For a sibling reference, activate that owning skill through the client's normal
mechanism first. If the resource is still outside the permitted roots, request
only the specific access the task needs or report that path as unavailable. Do
not work around denied reads through symlink aliases or shell tools. Permission
failures are separate from missing files. A package installation that copies one
skill may omit sibling skills entirely; install the required owner or preserve
the collection layout rather than duplicating shared manuals.

The find-skills workflow now uses the target client's install and refresh behavior.
The caveman-compress helper independently requires an Anthropic SDK/API-key setup
or authenticated Claude CLI. Loading it in another host does not replace that
backend or authorize sending file contents to a different provider.

## Repeatable native loader checks

```sh
mise exec -- make test-client-loaders
```

This opt-in POSIX harness needs Python 3.10+, Node.js 22+ and npm, and uses the
network to fetch integrity-verified inputs. It creates temporary profiles, runs
native loader functions, and removes its dependencies and profiles on completion
or handled interruption. Default `make check` remains offline with respect to
agent packages. Tests were executed with Python 3.14 and Node.js 26.8.1.

The harness loads Pi 0.73.1's unchanged published loader modules and Hermes's
pinned directory-traversal module. `tests/client-loaders/sources.json` records exact
revisions, archive integrity, file hashes, and the Pi module allowlist. The only
npm dependencies are the loader's locked `ignore` and `yaml` parsers. Full agent
installation, extension installers, credential stores, and session exporters are
not part of this fixture. Updates to the source manifest require source review
and rerunning this target; Dependabot monitors the parser dependency directory.

Checks cover catalog identity, Pi's explicit-only prompt filtering and symlink
deduplication, Hermes's filtered catalog, and ordinary filesystem reads of local
and sibling resources. They do not exercise Hermes skill_view, Gemini permission
checks, or a live model's decisions. Validate those with a client session when
that runtime and model access are available. Never describe the filesystem probe
as proof that a client's permission layer granted access.


## Automation and concurrent installation

`--json` emits one object with `schema_version: 1`, `mode`, canonical `source`,
`status`, `changes`, and `issues`. Status is `ok`, `failed`, or `partial`.
Each change includes `target`, `source`, `action`, and `applied`. Issue codes
include `missing_link`, `conflict`, `excluded_skill`, `stale_link`,
`scan_incomplete`, `busy`, and `operation_failed`. A partial result requires
inspection and a fresh check before retrying. Exit status is zero only on success.
Argument syntax errors still use argparse's stderr and exit status 2.

Empty profile variables use their default homes. Overrides must be absolute
paths after tilde expansion. Parent symlinks are normalized. Shared or nested
catalog destinations are rejected because client policies can differ.

Apply requires POSIX directory locking. Cooperating installers use nonblocking
locks in sorted path order and repeat preflight while holding all locks. Locks
are released by the OS on exit, including process termination. Check and plan
never create directories and take shared locks on existing catalogs when the
initial preflight passes. Apply may leave empty catalog directories if lock
acquisition fails. External tools that ignore locks remain outside this guarantee.
Do not repoint a live catalog from competing worktrees. Choose one installation
owner and a stable source checkout. Source edits must also pause during validation.

All repository metadata tools use the same bounded PyYAML reader. Install the
parser through `requirements-dev.txt` or the supplied development environment.
Its supported metadata follows the [Agent Skills specification](https://agentskills.io/specification),
with aliases and duplicate keys rejected to avoid client-dependent precedence.
Pinned loader checks now run in the normal CI validation job, including weekly
scheduled runs. Local `make check` remains offline.
