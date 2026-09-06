# Agent guidance

Before Spec Kit planning or implementation, read
`.specify/memory/project-guide.md` with the project constitution. It maps
requirements to this repository's source, acceptance evidence, and validation.

Read `.specify/memory/constitution.md`, `README.md`, and the target skill's
`SKILL.md` and `UPSTREAM.md` before editing.
Use `RELEASING.md` for push, merge, delivery, and recovery guidance.

- Treat every skill as a hard fork. Preserve its upstream link and source path.
- Keep `PROVENANCE.json`, `UPSTREAM.md`, and install targets synchronized.
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

## Spec-driven changes

Use Spec Kit for new capabilities, architecture, security-sensitive behavior,
migrations, and coordinated changes needing a written contract. Keep narrow
fixes, dependency updates, and prose maintenance in the normal PR workflow.
Retain completed feature directories under `specs/` as decision history. Do not
backfill completed work unless the user explicitly requests it. Label requested
retrofits as retrospective, record the assessed revision and evidence limits,
and preserve original feature history.

## Context and handoffs

- Locate source with targeted searches before reading. For exploratory reads of
  files over 350 lines, select relevant ranges. Read required guidance and actual
  source before edits or correctness claims; summaries do not replace them.
- When delegation is permitted, give each worker one question or concrete output,
  allowed paths, and a check. Return findings with source locations, changed paths,
  and verification gaps. Keep final review with the coordinating agent.
- Record durable user corrections in the [project guide](.specify/memory/project-guide.md)
  or owning contract with scope, reason, and evidence. Replace superseded advice;
  read relevant corrections before reusing assumptions. Keep temporary progress
  in task notes and preserve existing authority rules.
