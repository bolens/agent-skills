---
name: code-review
description: Perform a read-only review of a branch, pull request, commit range, staged changes, or working-tree diff for correctness, regressions, security, maintainability, test coverage, repository standards, and specification compliance. Use when the user asks to review code, a PR, a diff, work in progress, or changes since a revision.
---

# Code Review

Lead with actionable findings, ordered by severity. Do not modify files, stage changes, post comments, or create reports unless the user explicitly asks.

## Establish scope

1. Read the applicable `AGENTS.md`, contributor docs, and relevant source-of-truth files.
2. Use the fixed point supplied by the user. Otherwise infer the safest useful scope:
   - staged or unstaged request: corresponding local diff
   - branch/PR request: merge-base with its upstream/default branch
   - ambiguous repository-wide request: ask rather than reviewing an arbitrary range
3. Verify the reference and inspect both the diff and commit list. Preserve awareness of unrelated dirty-worktree changes.
4. Find the originating spec or issue when locally available. A missing spec does not block correctness review.

## Review lenses

- Correctness: logic errors, edge cases, error paths, compatibility, and regressions
- Safety/security: trust boundaries, secrets, permissions, destructive behavior, and unsafe defaults
- Tests: missing behavioral coverage and tests that cannot detect the regression
- Repository standards: explicit local rules, generated-file contracts, architecture, and canonical tooling
- Spec: missing requirements, wrong behavior, and unrequested scope
- Maintainability/performance: only concrete problems introduced or exposed by the diff; avoid taste-only feedback

Use independent sub-agents only when the user or active environment permits them and the diff is large enough to benefit. The review must work fully in one agent.

When the reviewed repository is an Omarchy plugin and the request concerns marketplace submission, verification, update approval, or release readiness, also use `audit-omarchy-plugin`. Keep its official scanner disposition separate from broader code-review findings.

## Output

For each finding provide severity, confidence, `file:line`, the concrete failure scenario, and the smallest viable fix. Avoid compliments and summaries that bury findings. If no findings exist, say so and note residual risks or tests not run.

Keep Spec and Standards labels when they clarify the source, but rank all defects by impact so the user knows what to fix first. Follow an explicitly requested output style such as `caveman-review`.
