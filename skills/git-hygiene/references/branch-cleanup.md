# Clean up a merged feature branch

Use after a verified merge when completing authorized delivery or an explicit branch-cleanup request. Keep these rules here. Delivery skills should call this reference instead of maintaining their own deletion procedure.

## Verify the candidate

Inventory local branches, their upstreams, linked worktrees, and related remote refs within the authorized repository scope. Include old leftovers whose feature was merged earlier, even if its PR head branch or upstream is already gone. Age, a `gone` upstream, or a shared name only identifies a candidate; none proves the work is complete. Routine delivery covers leftovers for that feature. A broader cleanup request can cover other completed features, with separate evidence for each.

1. Confirm the host reports the PR as merged into the intended base. Record the PR, head repository, feature branch, merged head SHA, and resulting merge commit. Closed without merge is not sufficient. For local-only integration, verify the intended target contains the complete change.
2. Read current local and remote refs. Compare the feature tips with the recorded merged head. Retain a branch that has advanced or diverged until its additional work is reviewed and integrated. A missing remote branch may mean the host already cleaned it up. A failed lookup does not prove absence.
3. Check `git worktree list --porcelain` and task ownership. Retain branches used by active agents, dependent stacked PRs, release automation, or unfinished tasks. Never delete default, protected, release, or other long-lived branches as feature cleanup.
4. For merge commits or fast-forwards, check ancestry against the actual target. For squash or rebase merges, use host merge evidence tying the exact PR head to the resulting change. Do not infer non-integration solely from `git branch --merged`, or infer integration solely from a matching branch name.

## Remove only verified, completed work

Routine cleanup belongs to the authorized merge endpoint when the user or repository delivery policy includes it. Honor requests to retain branches and narrower endpoints such as readiness or local fixes. Carry existing cleanup authorization forward without asking again. If deletion authority is missing, complete the checks and report the exact remaining branch and action.

Before removing completed feature refs, follow [checkout freshness](freshness.md) to synchronize eligible retained local base checkouts and record any retained stale state. A fetched tracking ref is not proof that the checkout advanced.

Clean up temporary local worktrees as part of the same post-merge endpoint, even when the host already removed the remote branch. Retain the main checkout and worktrees used as installed or deployed paths. Do not repoint symlinks or services as cleanup.

Release only task-owned, inactive worktrees after inspecting staged, unstaged, untracked, and valuable ignored files. Preserve anything needed for recovery. Use `git worktree remove` without force for a temporary linked worktree. In a retained checkout owned by this task, switch to the intended base only when clean and no other agent uses it. If that base is checked out elsewhere, use a verified detached target or retain the checkout. Never switch another agent's checkout or force removal to unblock branch deletion.

Delete only the named local feature branch after rechecking its tip under the Git writer's ownership. Prefer `git branch -d -- BRANCH`. Its safety check may use the branch's upstream, so successful deletion is not independent proof of integration into the intended base. Establish that proof first. [Git branch documentation](https://git-scm.com/docs/git-branch).

After squash or rebase integration, `-d` may refuse even though the exact work was merged. Use `-D` only when cleanup is already authorized, the exact local tip is verified as integrated, the recorded commit remains recoverable, no dependent work remains, and repository policy permits forced local deletion. Otherwise retain it with the reason. Never turn a deletion refusal into an automatic force retry.

For each related remote branch, verify the actual repository and destination, including fork ownership and any additional remotes carrying that feature. Do not assume all remotes are owned by the user or that matching names contain the same work. Verify each tip's integration and completion independently, and delete only within existing authority. If already absent, record that and continue. If it exists, use a deletion guarded by the exact expected SHA so a concurrent push cannot be erased. Where Git and policy permit, the shape is:

```sh
git push --force-with-lease=refs/heads/BRANCH:VERIFIED_HEAD_SHA REMOTE :refs/heads/BRANCH
```

Replace the example values with the verified destination and head. This deletes one ref conditionally. A rejection requires fresh inspection, never a broader force push or unguarded retry. A host deletion API must provide equivalent expected-tip protection when other writers may update the ref. If the available tool cannot guard deletion, retain the branch until writes can be reliably excluded. [Git push documentation](https://git-scm.com/docs/git-push).

Do not bundle host merge and automatic branch deletion when doing so bypasses these ownership and tip checks. Do not enable repository-wide auto-deletion settings or sweep other branches as incidental cleanup.

## Verify and report

Re-query the exact local and remote refs and worktree list. Distinguish deleted, already absent, retained with a reason, and blocked by permissions or policy. Removing a remote-tracking ref or running fetch pruning is not deletion of a branch on the server. Report merge success separately from incomplete cleanup, and preserve the merged head and result in the delivery receipt.
