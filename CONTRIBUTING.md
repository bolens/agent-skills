# Contributing

This repository is the canonical source for the installed skill collection.
Change instructions under `skills/<name>/`, preserve their origin and local
customizations, and validate the behavior the change is meant to support.

Read the [constitution](.specify/memory/constitution.md),
[agent guidance](AGENTS.md), and affected skill's `SKILL.md` and `UPSTREAM.md`
before editing. Use [RELEASING.md](RELEASING.md) for PRs, merges, and recovery.
Report sensitive findings through [SECURITY.md](SECURITY.md).

## Choose the scope

Use the normal PR workflow for focused fixes, dependency updates, and prose
maintenance. New capabilities, architectural changes, security-sensitive
behavior, migrations, and coordinated changes needing a written contract use
Spec Kit. The [project guide](.specify/memory/project-guide.md) maps those plans
to source files and acceptance evidence.

Keep skill descriptions narrow enough to distinguish neighboring tasks. Put
conditional detail in linked references and add scripts only when they make a
repeated operation more reliable. Document runtime or operating-system limits.
A relevant handoff to another skill should preserve the user's task and authority.

For concurrent work, assign file ownership and use separate worktrees where
appropriate. Shared manifests and generated files need one writer. Follow
[git-hygiene](skills/git-hygiene/SKILL.md), inspect existing changes before staging,
and commit only the files and hunks belonging to the task.

## Edit the source of truth

| Change | Authoritative source |
| --- | --- |
| Skill instructions, references, and helpers | `skills/<name>/`, excluding generated files |
| Audited upstream revision and local changes to retain | `UPSTREAMS.json` |
| Provenance rendering and install-target rules | `scripts/update-provenance.py` |
| Generated registry and per-skill origin pointers | Regenerate `PROVENANCE.json` and `skills/*/UPSTREAM.md` |
| Project-specific planning guidance | `.specify/memory/project-guide.md` and the constitution |
| Spec Kit integration files | Their integration manifest and normal update mechanism |

After adding or removing a skill, changing upstream metadata, or changing
install-target rules, regenerate the registry and pointers:

```sh
python3 scripts/update-provenance.py
make check-fast
```

Review the generated diff. Hand edits to `PROVENANCE.json` or `UPSTREAM.md` will
be replaced by the generator. A locally authored skill has no `UPSTREAMS.json`
entry and receives a local-origin record. An imported skill needs a reviewed
upstream entry with its source path, exact audited revision, and local changes.
Preserve the upstream license and notices.

Installed directories are symlinks to this checkout. Edit the source instead of
copying changes into client homes. Installation is a separate action documented
in the [README](README.md#install-from-this-checkout).

## Checks

Maintenance requires Python 3.10 or newer, Node.js 18 or newer, and Bash for shell
syntax validation. Install ShellCheck for the shell lint coverage used in CI.
Individual skills may need additional tools for behavioral validation.

| Command | Evidence |
| --- | --- |
| `make check-fast` | Metadata, generated provenance, and Python, shell, and JavaScript syntax |
| `make test` | Repository contracts and helper behavior covered by the test suite |
| `make portability` | Paths, shebangs, line endings, managed shell hashes, and shell lint |
| `make links` | Registered installation targets resolve to this checkout |
| `make check` | All of the above |
| `make check-fast test portability` | Portable gate used by CI and isolated checkouts |

Run `make check-fast` while editing and `make check` before delivery from the
canonical installed checkout. In an isolated worktree, run the portable gate
and report that installation links belong to another checkout. Do not repoint
them to make validation pass. Report a missing ShellCheck as a coverage gap,
not a completed shell lint pass.

These checks do not run every skill's runtime workflow. For changed instructions,
walk through a realistic task and a nearby task that should not invoke the skill.
For changed helpers, exercise the affected behavior and failure paths. Distinguish
source inspection from commands actually executed. Avoid tests that only match
new prose or mirror the implementation.

To install the repository's `check-fast` pre-commit hook:

```sh
make hooks-install
```

The installer uses Python 3.10 APIs and is also exercised by `make test`.
It overwrites the `pre-commit` file at the hooks path resolved by Git.
Inspect existing hooks before running it. Linked worktrees may share that path.
The hook runs the fast gate only. It does not replace the full delivery check.

## Upstream updates

Use [sync-skill-upstreams](skills/sync-skill-upstreams/SKILL.md) for imports.
`python3 scripts/audit-upstreams.py` queries upstream branch tips and reports
whether they differ from the audited revisions. It does not import changes or
establish that a candidate is compatible. `--check` also returns failure when
an update is available. Lookup errors are reported separately.

Review the complete upstream diff before importing selected changes. Preserve
every recorded path and local change, inspect affected callers and generated
outputs, and update the audited revision only after that review. Regenerate
provenance, validate the result, and describe reader-visible behavior changes in
[CHANGELOG.md](CHANGELOG.md). Routine dependency churn belongs in Git history.

Keep one coherent purpose per commit. A PR should explain the changed behavior,
the evidence supporting it, and any remaining limitations. Do not describe a
local fork as an upstream release.
