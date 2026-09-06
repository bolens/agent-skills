---
name: code-review
description: Perform an evidence-led, read-only review of a branch, pull request, commit, staged changes, or working-tree diff. Trace affected callers and contracts to find correctness, security, compatibility, lifecycle, test, and delivery regressions. Use for code or diff review; use improve-codebase-architecture for a broad architecture survey.
---

# Code review

Lead with actionable findings ordered by impact. Keep the review read-only unless the user authorizes fixes or artifacts. Do not stage changes, post comments, or submit a host review merely because review was requested. A full review examines the changed behavior and affected contracts, not only edited lines.

## Fix the review boundary

Read applicable `AGENTS.md`, contributor guidance, requirements, and nearby source. Resolve the user's requested scope before choosing a diff:

| Requested scope | Comparison |
|---|---|
| Staged changes | `git diff --cached` against `HEAD`, including staged additions and deletions |
| Unstaged tracked changes | `git diff` against the index |
| All uncommitted work | Inspect both layers and the combined tracked diff against `HEAD`; inventory untracked files and include relevant source without reading ignored data indiscriminately |
| One commit | That commit against its parent; for a merge commit establish which parent or integration result the user means |
| Two explicit revisions | Compare their trees with `git diff <old> <new>` unless the user requested a commit series or branch proposal |
| Branch or PR proposal | Resolve actual target and head, record their SHAs and merge-base, then use `git diff <target>...<head>` |

For a root commit, compare against the empty tree using Git's root-diff support. For a requested commit series, inspect both the net change and relevant intermediate commits. Do not substitute the remote default for a PR's actual target, or the feature branch's tracking ref for its integration base. If scope remains ambiguous, ask for the missing boundary after inspecting available local context. An empty diff is not a clean review until its scope is confirmed.

Record source freshness. Local remote-tracking refs may be stale. Do not claim current remote readiness without checking the host. A branch proposal diff does not prove compatibility with target changes since the merge-base; inspect those interactions when relevant and identify any tested merge result.

Read and execute against the reviewed state. For staged work, unstaged fixes must not mask index defects. Use Git objects for inspection and an isolated snapshot when execution would otherwise include unrelated changes. Preserve modes, symlinks, and dependencies needed for that snapshot. Record what state a command actually tested. Do not stash, reset, or alter the user's checkout merely to review it.

## Map changes to contracts

Inspect the full file inventory and diff, including additions, deletions, renames, permissions, symlinks, configuration, dependencies, generated output, tests, and documentation. Do not silently omit large or binary files; inspect their source or generation contract and mark unavailable evidence.

For each meaningful change, trace the entry point through the changed implementation to its callers, data stores, external consumers, and tests. Search beyond the diff for affected call sites and alternate implementations. Identify the contract being changed: accepted inputs, output shape, error behavior, state transition, ownership, compatibility, or execution authority. For cross-file changes, verify both producer and consumer agree.

Maintain a compact working coverage map: changed behavior, affected boundary, inspected source/tests, result, and remaining evidence. Keep this in working notes unless an artifact was requested. Scale it to the task; a typo does not need a full matrix. Missing requirements are uncertainty to report, not permission to invent product behavior.

## Review in passes

1. **Behavior and requirements.** Trace normal, boundary, and failure paths against the old behavior and stated requirements. Check removals and alternate entry points. Separate intentional behavior changes from regressions.
2. **Boundary interactions.** Follow the applicable probes in [references/seam-probes.md](references/seam-probes.md) for interface compatibility, async state, persistence, trust, runtime, and delivery seams. Load deeper specialist guidance only where changed behavior crosses that boundary.
3. **Tests and execution evidence.** Ask which concrete defect the existing tests would catch. Inspect assertions, fixtures, mocks, skipped cases, and whether the tests exercise the changed implementation. A passing test that duplicates the algorithm or mocks out the affected boundary is weak evidence. Use the smallest existing check or disposable reproduction that resolves a real uncertainty. Inspect commands before running them; a test label does not make live mutations or untrusted install hooks safe.
4. **Challenge and reconcile.** Try to disprove each candidate finding by checking guards, callers, documented invariants, and the base version. Verify that the proposed correction would preserve valid behavior. Reconcile duplicates and finish the coverage map before issuing a verdict.

Do not demand new tests for every changed line. Report a test gap as actionable when it leaves a specific important behavior unverified, with the scenario and appropriate test boundary. Do not implement tests during a read-only review unless separately authorized; temporary reproductions may live outside the worktree.

## Independent focused reviews

For PRs with separable concerns, use multiple independent reviewer agents when available and delegation is permitted. Select distinct focuses from the actual changes, typically behavior/contracts and tests/failure paths, adding security or delivery review when those boundaries are affected. This is the default for substantive PRs, not a requirement to invent extra work for trivial edits. With limited slots, run reviewers in waves or combine related concerns. Read [references/independent-reviews.md](references/independent-reviews.md) for assignments, isolation, and reconciliation.

If independent review is unavailable or prohibited, complete the review yourself and state the limitation. Do not call self-review independent or treat an unavailable reviewer as a clean result. Honor an explicit requirement for independent review by leaving that requirement pending while completing other permitted work.

## Qualify findings

A finding needs a reachable trigger, affected behavior, supporting source or reproduction, and a practical correction. State whether it was reproduced or established by source reasoning. Keep unresolved suspicions as questions or evidence gaps, with what would settle them. Low confidence does not make a hypothetical failure a defect.

Compare against the base before attributing a defect to the change. Report pre-existing issues separately only when material to the requested scope. Group symptoms that share one cause and fix. Prefer a precise changed location and cite unchanged callers when they establish impact; identify old-side locations for deleted code.

Use the repository's severity scale when defined. Otherwise:

- **P0:** immediate, broadly reachable severe outage, data loss, or compromise requiring urgent containment.
- **P1:** major supported-path failure or security/data-integrity defect that should block delivery.
- **P2:** bounded correctness, compatibility, reliability, or meaningful verification defect needing correction.
- **P3:** low-impact supported defect. Optional style preferences are nits, not blocking defects.

Severity follows impact and reachability; confidence is separate. Do not require a vulnerability identifier to report a security defect or rank every possible race as a confirmed bug. Never invent findings to satisfy a quota, and do not stop at the first defect while unreviewed relevant changes remain.

For consequential patches, distinguish the impact of a wrong change, regression
likelihood, relevant test protection, recoverability, and confidence in the
assessment. Strong tests can reduce uncertainty and likelihood without reducing
the consequence of failure. Neither a short diff nor high confidence grants
merge authority. Keep this assessment separate from a vulnerability's severity.

## Report and hand off

For each finding give severity, confidence, location, trigger and consequence, evidence, and the smallest viable fix. Distinguish required corrections, optional nits when requested, and unresolved questions. Follow a requested terse format through [caveman-review](../caveman-review/SKILL.md), retaining enough evidence to assess each claim.

After findings, give a brief receipt: reviewed revisions or local layers, important boundaries covered, checks and their tested state, and material gaps. Say "no actionable findings" when supported; if coverage is incomplete, state that alongside the result. Passing CI or a small defect count is not proof of comprehensive review. Do not claim independent verification for a self-review.

When the task includes addressing PR findings, getting a PR ready to merge, or preparing or publishing a release, automatically use [babysit](../babysit/SKILL.md) to coordinate that endpoint. Return findings, coverage, checked revisions, and unresolved gaps to an already active workflow. Keep this review pass read-only. A one-off review does not start follow-through.
