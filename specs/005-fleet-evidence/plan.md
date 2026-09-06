# Implementation plan

The existing `audit-repo-fleet` skill owns the helper and its instructions.
Store immutable per-run records under the selected worktree's Git directory,
with restrictive permissions and atomic receipt replacement. Hash Git identity,
index state, and tracked/nonignored working files; never follow source symlinks
outside the checkout. Use argument arrays, native subprocess status, monotonic
elapsed time, and bounded process cleanup. No model API or automatic retry loop.

Extend the existing Git and review handoffs through a short execution reference:
record acceptance and ownership first, schedule only independent work together,
join on observed evidence, and preserve blocked/dependent work. Delegation remains
conditional on the session's authorization and available capabilities.

Validate behavior with disposable Git repositories and subprocess fixtures:
success, failure, missing executable, stale and changed candidates, ignored
outputs, timeout cleanup, repeated failures, and independent worktrees. Run the
repository's portable gate before submission, then its protected PR workflow.

Constitution: source remains under `skills/`; preserve local hard-fork provenance;
no upstream import; use Python's standard library; existing CI runs the new tests.
