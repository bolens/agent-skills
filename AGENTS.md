# Agent guidance

[Documentation](docs/README.md) maps architecture, deployment, state, and document ownership.

Read the target skill's `SKILL.md` before changing its instructions. Use
[README.md](README.md) to locate workflows and [CONTRIBUTING.md](CONTRIBUTING.md) for validation and source
ownership. Read the constitution for maintenance-policy changes and the affected skill's `UPSTREAM.md` with `UPSTREAMS.json` when changing fork provenance, imported content, or local
customizations. Use [RELEASING.md](RELEASING.md) for push, merge, delivery, and recovery.

- Treat every skill as a hard fork. Preserve its upstream link and source path.
- Keep generated provenance, per-skill upstream pointers, and install targets synchronized.
- Do not update a fork from upstream without reviewing the complete diff.
- Preserve every path and local change recorded in `UPSTREAMS.json` during an import.
- Keep skill descriptions narrow and discriminating. Remove scaffold TODOs.
- Prefer portable scripts. Document intentional OS or runtime boundaries.
- Do not edit installed skill directories directly. Edit `skills/` here; the
  installed directories are symlinks managed by `scripts/link-installed.py`.
- Run `make check-fast` while iterating and `make check` before release.
- When a task is complete, commit all changes made for that task. Split the work
  into focused commits when it contains more than one independently meaningful
  change. Each commit should contain one coherent purpose and include its related
  tests and documentation.
- Before committing, inspect the diff and repository status. Stage only the files
  and hunks that belong to the current task; preserve unrelated user changes.
- Use concise commit messages that state the intent of the change. Do not leave a
  completed task uncommitted unless the user explicitly asks you not to commit.
- Do not push, tag, or publish unless explicitly requested.

## Planning and evidence

Use the [project guide](.specify/memory/project-guide.md) and
[constitution](.specify/memory/constitution.md) for substantial changes. The guide
owns Spec Kit scope, retained history, retrospective requirements, and acceptance
evidence. Prose maintenance uses the normal repository workflow.

## Context and handoffs

- Search before reading. Use bounded source excerpts for exploratory reads over
  350 lines, and inspect required guidance and actual source before editing.
- When delegation is permitted, assign a bounded question or output, paths, and
  check. Return source locations, changes, and verification gaps for final review.
- Keep durable corrections in the [project guide](.specify/memory/project-guide.md)
  or owning contract. Replace superseded advice and read it before reuse.
  Temporary progress belongs in task notes. Preserve existing authority rules.
