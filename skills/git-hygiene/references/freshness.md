# Keep branches and checkouts current

Use when starting implementation, preparing or updating a PR, and completing a
feature. Freshness is a relationship between identified revisions, not a clean
`git status` or a recent-looking commit date. Carry existing authority forward
and keep read-only, offline, and local-only requests within their scope.

## Establish the source and checkpoint

Identify the intended base repository and branch, PR head repository and branch,
fetch and push destinations, local tracking configuration, and owning worktrees.
A fork can fetch its base from one remote and push its feature to another. A
review clone's `origin` can be a local path. Never infer the destination from the
remote name or change remote configuration to make it match an example.

At each meaningful checkpoint, fetch the relevant base and existing feature
refs from their verified destinations when network access is in scope. Use the
repository's configured refspec or an explicit bounded refspec that updates the
intended tracking ref. Check the result. Fetching only into `FETCH_HEAD` does not
make a different cached tracking ref current. Fetch does not update checked-out
files or merge new commits into local branches. [Git fetch documentation](https://git-scm.com/docs/git-fetch).

Record the fetched base SHA, feature SHA when present, local HEAD, and ahead/behind
relationship. Distinguish a genuinely new unpublished branch from an existing
head that disappeared. Treat failed lookups, an unexpected rewind, or a changed
remote identity as unresolved evidence. Do not call cached refs current after a
failed or prohibited fetch.

## Before creating or updating a PR

Start new feature work from the freshly verified intended base. Before submitting
a PR or pushing a repair, refresh the base and existing remote feature head again.
This catches intervening merges, host-side branch updates, and commits from other
agents. In a clean checkout owned by the task:

- If the remote feature advanced, preserve and reconcile its work before pushing.
  Fast-forward the local feature when possible. Review both sides of divergence.
- If the base advanced, integrate it using the repository's approved strategy,
  resolve conflicts, inspect the combined diff, and run relevant checks on that
  state before submission. Rebase only where policy and ownership allow it.
  Do not rewrite a shared or published branch merely to become current. If no
  authorized integration method is available, report the exact remaining step.
- If the host updated the PR branch, fetch and reconcile that new head locally
  before continuing edits. A host update does not synchronize the local checkout.

A comparison such as `git rev-list --left-right --count BASE_REF...HEAD` reports
base-only commits first and feature-only commits second. Replace `BASE_REF` with
the verified fetched base. Ahead of base is normal for a feature. Ahead of the
remote feature can mean unpublished commits. Do not confuse those comparisons.

Do not pull blindly, automatically stash another owner's work, reset local
commits, or force-switch a dirty checkout. Preserve local edits and use task
isolation when needed. A branch update changes the validation candidate, so do
not reuse affected tests or approvals from the old head.

Recheck relevant remote tips before the final push and merge. If they moved,
reconcile the new work and refresh affected evidence. Follow a repository's merge
queue or tested synthetic-merge contract when that owns integration. Record the
head and base actually tested rather than promise an impossible permanently
latest state. Keep [babysit](../../babysit/SKILL.md) as the delivery coordinator.

## When the feature is complete

For local-only work, leave the committed feature intact and report its relation
to the last verified base and upstream. Do not switch to the base, publish the
feature, or delete it just to make the checkout look synchronized.

After a verified remote merge, fetch the intended base again and confirm it
contains the recorded merge result. Locate the retained local base checkout and
any other task-owned checkout that should finish synchronized. Refreshing remote
refs alone is not completion. For each authorized, clean, inactive checkout:

1. Verify its branch and owning task. If switching from a completed feature,
   first establish merge evidence and preserve any extra work. Do not switch a
   branch that another worktree owns or change another agent's checkout.
2. Fast-forward the local base to the fetched target, using an explicit operation
   such as `git merge --ff-only BASE_REF` while on the verified local base branch.
   Stop on local commits or divergence instead of resetting or creating an
   incidental merge commit. [Git merge documentation](https://git-scm.com/docs/git-merge).
3. Confirm local HEAD equals the fetched target and status has no unexpected
   changes. Verify the merged result is contained, even when newer base commits
   landed after this feature. Recheck relevant installed links or generated
   contracts when the checkout supplies them.

Retain dirty, active, divergent, or deliberately pinned checkouts with an explicit
reason and remaining action. Updating an installed or deployed checkout can
itself apply configuration, so respect that surface's authority before switching
its contents. Do not repoint links, restart services, or synchronize every clone
as incidental cleanup.

Then use [branch cleanup](branch-cleanup.md) for verified completed branches and
temporary worktrees. Report merge, local synchronization, and cleanup separately.
Include the checked-out branch, local and fetched target SHAs, remaining local
changes or divergence, and any checkout intentionally left stale. A successful
merge does not justify reporting local synchronization that never happened.
