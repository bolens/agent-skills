# Agent skills

Personal agent skills for software development, repository maintenance, web
interfaces, and Linux homelab operations. This is the source of truth for the
skills I use across my repositories, with shared instructions for concurrent
agents, fleet-wide fixes, CI, review, and delivery.

The collection includes locally authored skills and customized third-party
skills. Every skill is maintained as a hard fork with recorded provenance.
Upstream changes are reviewed manually so they preserve local behavior.

Licenses remain specific to each source. See [LICENSE.md](LICENSE.md) for retained
notices, bundled material, and the requirements for copying or updating a fork.

## Find a workflow

Start with the skill that owns the task. Its `SKILL.md` describes when to use it,
the evidence to collect, and when to bring in another skill. Supporting scripts
and references live beside it. Browse the [complete collection](skills/) for
specialized workflows.

| Task | Start here |
| --- | --- |
| Evaluate skill additions or review upstream changes | [find-skills](skills/find-skills/SKILL.md), [sync-skill-upstreams](skills/sync-skill-upstreams/SKILL.md) |
| Coordinate concurrent agents, branches, and worktrees | [git-hygiene](skills/git-hygiene/SKILL.md) |
| Audit repositories and carry shared fixes across the fleet | [audit-repo-fleet](skills/audit-repo-fleet/SKILL.md) |
| Build or improve CI and reusable workflow contracts | [ci-maintenance](skills/ci-maintenance/SKILL.md) |
| Set up local commit checks | [setup-pre-commit](skills/setup-pre-commit/SKILL.md) |
| Diagnose failures and assess dependency updates | [systematic-debugging](skills/systematic-debugging/SKILL.md), [triage-dependency-updates](skills/triage-dependency-updates/SKILL.md) |
| Review changes and follow PRs through delivery | [code-review](skills/code-review/SKILL.md), [babysit](skills/babysit/SKILL.md) |
| Find architectural friction or plan a focused redesign | [improve-codebase-architecture](skills/improve-codebase-architecture/SKILL.md), [codebase-design](skills/codebase-design/SKILL.md) |
| Refactor, migrate, or verify existing work | [safe-refactor](skills/safe-refactor/SKILL.md), [migration](skills/migration/SKILL.md), [verify-and-stop](skills/verify-and-stop/SKILL.md) |
| Check publication content for secrets and private information | [sensitive-info-audit](skills/sensitive-info-audit/SKILL.md) |
| Design web pages, shared components, and data interactions | [frontend-design](skills/frontend-design/SKILL.md), [design-system](skills/design-system/SKILL.md), [forms-and-data-state](skills/forms-and-data-state/SKILL.md) |
| Improve accessibility, performance, security, and discoverability | [web-quality-audit](skills/web-quality-audit/SKILL.md), [web-security](skills/web-security/SKILL.md), [technical-seo](skills/technical-seo/SKILL.md) |
| Create SVG artwork or integrate interface animation | [svg-design](skills/svg-design/SKILL.md), [svg-animation](skills/svg-animation/SKILL.md), [web-animation](skills/web-animation/SKILL.md), [animation-assets](skills/animation-assets/SKILL.md) |
| Verify browser behavior across screen sizes | [cli-web-evidence](skills/cli-web-evidence/SKILL.md), [responsive-web-capture](skills/responsive-web-capture/SKILL.md) |
| Maintain Compose stacks or diagnose a live homelab service | [homelab-stack-maintenance](skills/homelab-stack-maintenance/SKILL.md), [homelab-stack-triage](skills/homelab-stack-triage/SKILL.md) |
| Verify backups and network exposure | [backup-restore-verification](skills/backup-restore-verification/SKILL.md), [network-exposure-verification](skills/network-exposure-verification/SKILL.md) |
| Maintain Arch packages, desktop components, and media utilities | [arch-package-maintenance](skills/arch-package-maintenance/SKILL.md), [quickshell-development](skills/quickshell-development/SKILL.md), [media-preservation](skills/media-preservation/SKILL.md) |

## How the skills work together

For concurrent implementation, `git-hygiene` establishes worktree and file
ownership, focused commits, and validation of the integrated result. It checks
base and feature freshness before PR submission and synchronizes eligible local
checkouts after a merge. It also owns cleanup of completed local branches,
related remote branches, and temporary worktrees, including older leftovers.
At feature completion, it removes task-owned temporary evidence and screenshot
directories while preserving deliverables and artifacts still needed for review.

During authorized fleet-wide implementation, `audit-repo-fleet` checks maintained
peers for the same cause or applicable improvement. Read-only fleet audits stay
read-only. Repeat audits compare repository identity, revisions, and coverage
before replacing earlier findings. Its [context guidance](skills/audit-repo-fleet/references/context-work.md)
and bounded source reader support targeted inspection. Each repository retains
its own validation and delivery requirements.

`code-review` traces changes through callers, contracts, and failure paths.
Substantive PRs use independent reviewers when available and permitted.
`babysit` carries findings, actionable nits, CI repairs, and post-merge cleanup
through the requested delivery endpoint.

For diagnostics, `systematic-debugging` covers process-status propagation and
[wide events with sensitive-data controls](skills/systematic-debugging/references/wide-events.md).
`web-security` separates reported claims, supporting evidence, and fix verification.
Browser evidence workflows verify observed behavior and backend capabilities
before treating screenshots or successful protocol responses as acceptance proof.

[Source audits](docs/audits/) record which external ideas were adopted, deferred,
or rejected and what was actually checked. They are dated evidence, not promises
that every mentioned tool is installed or every external claim remains current.

A skill handoff preserves the task's scope and existing authority. Audit-only
requests stay read-only. Pushes, merges, releases, deployments, and live-system
changes require authority for that action and destination.

## Install from this checkout

Keep this repository at a stable path. The installer links the skills registered
in [PROVENANCE.json](PROVENANCE.json) into these homes:

| Home | Purpose |
| --- | --- |
| `~/.codex/skills` | Codex skills |
| `~/.agents/skills` | Shared Agent Skills home for compatible clients |
| `~/.claude/skills` | Claude skills |

Each skill's `install_targets` is authoritative. All registered skills target
the shared and Claude homes. The nine skills listed in `NO_CODEX_TARGET` in
[the provenance generator](scripts/update-provenance.py) omit an additional Codex-home
link. This installer does not manage host-bundled/plugin skills or the separate
Spec Kit integration under `.agents/skills/speckit-*`.

From the repository root:

```sh
python3 scripts/link-installed.py --apply
python3 scripts/link-installed.py --check
```

`--apply` creates missing links and repoints existing symlinks to this checkout.
It refuses existing files or directories unless `--replace` is supplied.
`--replace` deletes those copies, so preserve any independent edits first.
Installation applies to the registered collection, not an individual skill.
It is not transactional: other links can be updated even if one target is
refused. It does not remove unregistered or obsolete entries from client homes.
Inspect reported problems and rerun `--check` after resolving them.

Set `CODEX_HOME`, `AGENTS_HOME`, or `CLAUDE_HOME` to override the corresponding
home directory. Edit the source under `skills/`, never an installed copy.
Because installation uses symlinks, source edits are immediately visible to the
clients using them. Skill discovery and invocation depend on the client.

## Maintain and validate

Use Python 3.10 or newer, Node.js 18 or newer for JavaScript syntax checks, Bash,
Git, and Make for repository maintenance. Install ShellCheck for full portability
coverage. The separate Archify suite uses Node 22, downloaded test dependencies,
and Chrome for browser checks; see [its reproduction guide](RELEASING.md#archify-test-coverage).
Individual skills may need additional tools for their tasks.

```sh
make check-fast                    # Metadata, provenance, and script syntax
make check                         # Also tests, portability, and installed links
make audit-upstreams               # Query remote tips without importing
```

In CI or a checkout that does not own the installed links, use the portable gate:

```sh
make check-fast test portability
```

Validation checks repository contracts, syntax, provenance, portability, and
installation state. Local-link tests cover skill entrypoints, not remote URL
availability or section anchors. These checks do not prove every skill's runtime
behavior; validate changed workflows with relevant task evidence too.

`make check` does not include `make test-archify`, Source lint, actionlint, or
zizmor. [CI](.github/workflows/ci.yml) runs the portable gate and selects Archify
jobs for relevant PR paths, including provenance changes; main and scheduled CI
run them in full. [Source lint](.github/workflows/source-lint.yml) separately calls
shared source and workflow-security checks. See [RELEASING.md](RELEASING.md) for
the complete merge gate and local reproduction requirements.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before editing and
[RELEASING.md](RELEASING.md) for PRs, merges, and recovery. Reviewed changes are
delivered on `main`. This repository does not publish versioned packages or
represent its forks as upstream releases.

## Source and provenance

| Path | Contents |
| --- | --- |
| [skills/](skills/) | Canonical instructions, references, scripts, and per-skill `UPSTREAM.md` records |
| [PROVENANCE.json](PROVENANCE.json) | Skill origins, source paths, fork status, and install targets |
| [UPSTREAMS.json](UPSTREAMS.json) | Audited upstream revisions and local changes to preserve |
| [scripts/](scripts/) and [tests/](tests/) | Maintenance tools and repository contract tests |
| [Specification index](specs/README.md) | Original feature history and the explicitly requested retrospective coverage baseline |
| [docs/audits/](docs/audits/) | Dated source assessments, adoption decisions, and validation limits |
| [Project guide](.specify/memory/project-guide.md) | Source ownership, acceptance evidence, and Spec Kit integration boundaries |
| [Project constitution](.specify/memory/constitution.md) | Maintenance principles |
| [CHANGELOG.md](CHANGELOG.md) | Changes to the collection |

The scheduled upstream audit reports drift without importing or merging it.
Review the complete upstream diff before updating a fork, preserve its recorded
local changes, and keep provenance and installation targets synchronized.

See [SECURITY.md](SECURITY.md) for sensitive reports.

## Reproducible development

Use the [development environment guide](docs/development-environments.md) for the pinned devenv shell and local Docker, Podman, and Apple container adapters. The portable Make targets remain the validation contract.
