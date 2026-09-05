# agent-skills Spec Kit project guide

Canonical hard forks of agent skills, with explicit upstream provenance and installed
symlinks.

Read this guide with `AGENTS.md` and `.specify/memory/constitution.md` before
specifying, planning, or implementing a substantial change. It is project-owned
guidance, not an upstream-managed template.

## Source and ownership map

- `skills/`
- `PROVENANCE.json`
- `UPSTREAMS.json`
- `scripts/validate.py`
- `scripts/link-installed.py`

## Specification and plan decisions

Identify the skill, supported task, invocation boundary, and upstream ownership before
planning changes. Read that skill's SKILL.md and UPSTREAM.md. Distinguish local
instructions from imported upstream behavior and preserve every declared local
customization.

## Acceptance evidence

Give a task that should invoke the skill and a nearby task that should not. Verify
referenced resources, portable command assumptions, provenance updates, and behavior
when optional tools are absent. Upstream imports require a reviewed source diff.

## Validation and operational limits

```sh
make check-fast
make check-fast test portability
```

Run make check in the canonical installed checkout before delivery. Its link check can
legitimately fail in an isolated worktree; do not repoint installed skills to hide that
mismatch. Installing or replacing links is a separate authorized action.

## Working through Spec Kit

Use Spec Kit for new capabilities, architectural or security-sensitive changes,
migrations, and coordinated changes that need a written contract. Keep narrow fixes,
dependency updates, and prose maintenance in the normal PR workflow.

For a new feature, record observable acceptance criteria in `spec.md`, source ownership
and constitution checks in `plan.md`, and evidence-bearing work in `tasks.md` under the
feature directory created by Spec Kit. Resolve material unknowns before implementation.
Mark tasks complete only after their stated verification, and distinguish completed,
skipped, blocked, and manual checks. Retain completed feature documents as decision
history; do not backfill feature specifications for already finished code.

Keep `.specify/templates/`, `.specify/scripts/`, and generated Codex skills under their
integration manifests. Use this guide and the constitution for local customization.
Regenerate managed files through Spec Kit and verify that project-owned memory survives
updates. Follow `RELEASING.md` for push, merge, release or delivery, and recovery.
