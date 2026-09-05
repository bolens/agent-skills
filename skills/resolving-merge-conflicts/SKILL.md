---
name: resolving-merge-conflicts
description: Diagnose and resolve an in-progress Git merge, rebase, cherry-pick, or revert conflict while preserving both sides' intent and unrelated work. Use when the user asks to inspect or resolve Git conflict markers or an interrupted integration operation.
---

# Resolve Git Conflicts

1. Read repository instructions. Inspect `git status`, the operation in progress, the conflict stages, relevant history, and the exact unmerged paths. Do not discard unrelated changes.
2. Trace each side to its primary source: commits, tests, specs, issues, and nearby code. Use remote issue or PR data only when access is available and needed.
3. Explain incompatible intent before choosing a side. Preserve both intents when they compose cleanly; otherwise follow the integration goal and record the trade-off. Do not invent unrelated behavior.
4. Edit only conflict-related files unless a small additional change is required to restore consistency. Remove all conflict markers and inspect the resulting diff.
5. Run the repository's relevant formatting, type, build, and test checks. Fix only failures caused by the resolution.
6. Stage resolved paths, continue the operation, or create a commit only when the user's request authorizes that step. Otherwise leave a clean working-tree resolution and give the exact next command.

Aborting may be the safest choice when the operation targets the wrong branch, the intended outcome cannot be established, or continuing would lose work. Never abort, reset, force-push, or discard changes without explicit authorization.

When conflict resolution belongs to a request to get an open PR ready to merge, merge it, or complete a release, automatically use [babysit](../babysit/SKILL.md) for the remaining audit, CI, and delivery steps. Return the resolved head and check evidence to an already active workflow. A local conflict-resolution request alone does not start follow-through or authorize a push.
