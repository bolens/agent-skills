# Agent guidance

Read `.specify/memory/constitution.md`, `README.md`, and the target skill's
`SKILL.md` and `UPSTREAM.md` before editing.

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
