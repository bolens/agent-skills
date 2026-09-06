# Clean up temporary feature evidence

At the requested feature or task endpoint, remove task-created temporary evidence
and screenshot directories that are no longer needed. This also applies to
local-only completion and readiness work, independently of branch deletion or
merge authority. Keep audit-only work read-only except for its own scratch output.

Record exact output paths and task ownership when creating captures, traces,
logs, comparison images, or validation reports. Include ignored directories in
the checkout and task directories outside it. During a handoff, pass these paths
and any retention needs to the completing owner.

Before cleanup:

1. Confirm the task has reached its requested endpoint and no active process,
   agent, review, or unresolved diagnosis still needs the candidate artifacts.
2. Separate disposable runs from requested deliverables, tracked visual baselines,
   repository-required evidence, and recovery material. Preserve required files
   and receipts in the designated artifact location and verify they are readable
   before removing temporary copies. Do not publish or upload them without the
   existing authority for that destination.
3. Inspect each candidate's contents and resolved path. Delete only exact paths
   established as disposable output owned by this task. A temporary-looking name,
   age, ignored status, or location under `/tmp` is not ownership proof. Do not
   follow symlinks into other directories or sweep shared evidence roots.

Remove eligible run directories, including superseded screenshots and completed
diagnostic runs, before the final handoff. Remove a task-created parent only when
it is empty. Do not use blanket `git clean`, wildcard deletion, or worktree force
removal. Use [branch cleanup](branch-cleanup.md) for the worktree itself.

Verify deleted paths are absent and retained artifacts remain readable. Report
cleanup and any retained paths with their reason and remaining cleanup owner or
condition. Final evidence links must point to retained files, never deleted
scratch paths. If ownership or retention is unclear, preserve that candidate and
complete cleanup of the known disposable paths.
