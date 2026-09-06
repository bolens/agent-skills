---
name: git-hygiene
description: Coordinate Git writes, worktree isolation, focused commits, and integration for concurrent agents across repository surfaces. Use for shared-checkout work, parallel implementation, mixed staged changes, branch handoffs, PR freshness checks, or post-merge synchronization and cleanup. Commit-message-only requests and read-only reviews keep their own workflows.
---

# Git hygiene for concurrent agents

Preserve each contributor's work and make the integrated result traceable. Apply this workflow alongside the task's implementation skill. It does not authorize spawning agents, publishing changes, or changing repository policy.

## Establish ownership before writing

Read applicable repository instructions and delivery guidance. Inspect the repository root, branch, HEAD, staged and unstaged changes, untracked files, worktrees, and any operation already in progress:

```sh
git rev-parse --show-toplevel
git status --short --branch
git rev-parse HEAD
git diff --stat
git diff --cached --stat
git worktree list --porcelain
```

Inspect full diffs for paths the task may touch. Treat existing changes as owned by someone else until their purpose is established. A clean status does not prove no other agent is working. Confirm assignments through the available coordination channel. Stop mutations on an unexpected HEAD change, overlapping edits, or an operation owned by another task, while continuing independent inspection.

Record assignments in the existing task channel or repository convention:

| Field | Required information |
|---|---|
| Identity | Task, owner, repository root, worktree, branch, base SHA |
| Write scope | Owned paths, shared paths, and excluded paths |
| Dependencies | Producer/consumer contracts and prerequisite revisions |
| Verification | Relevant checks, generated outputs, isolated test resources |
| Handoff | Integration owner, expected commit or patch, remaining work |

Assign shared manifests, lockfiles, schemas, migrations, generated clients, root configuration, and changelogs explicitly. Separate directories can still share a contract. Give each shared file one writer at a time. Agree on interface changes before consumers depend on them. Workers request a scope change before editing outside their assignment.

For work with several dependent units or a failed handoff, use [work-unit dependencies and correction](references/work-units.md). Define acceptance evidence before assignment, preserve unaffected accepted work, and return failures to their responsible owner. This applies to serial coordination too and does not grant permission to delegate.

## Choose workspace isolation

Prefer a distinct branch and worktree for each independent writer. Select a verified base SHA and unused branch and directory names. For example, after replacing the values with this task's assignment:

```sh
git worktree add -b task/api-change ../repo-api-change VERIFIED_BASE_SHA
```

Run every worker command in its assigned worktree. Never force checkout of a branch used by another worktree. A new worktree contains committed state, so transfer required uncommitted dependencies deliberately through reviewed commits or a scoped patch that includes needed new files.

Linked worktrees have separate HEAD and index state but share repository data including branch refs and configuration. Coordinate branch deletion, remote changes, and repository maintenance. `git worktree lock` prevents administrative pruning or removal. It is not a mutex for editing or committing. [Git worktree documentation](https://git-scm.com/docs/git-worktree).

Isolate test ports, databases, generated output directories, and writable caches when tests use shared resources. Worktrees alone do not isolate external services. Check repository support before using linked worktrees with submodules. Use a separate clone or serial work when the layout or tooling cannot support them.

If agents must share one checkout, designate one Git writer for staging, committing, switching branches, merging, rebasing, and other repository mutations. Other agents edit only their assigned non-overlapping files and hand back changed paths and verification. Pause affected writers while collecting a stable diff, staging, running checks, and committing. Broad formatters and generators also count as writers. If coordination is unavailable, serialize writes rather than claim isolation.

## Keep the working state current

Use [branch and checkout freshness](references/freshness.md) when starting implementation, before submitting or updating a PR, and when a feature completes. Refresh the verified base and existing feature refs, reconcile intervening work under the assigned Git writer, and validate the resulting candidate. After a merge, fast-forward eligible task-owned local base checkouts and verify their actual HEAD and status. Fetching refs or merging on the host alone does not synchronize local files. Preserve dirty, active, divergent, or pinned checkouts and report any remaining synchronization work.

## Make focused commits

Recheck HEAD, status, and ownership immediately before staging. Review the working diff and stage only task-owned paths or hunks. Selected paths do not exclude unrelated changes already in the index. Inspect the entire staged diff and candidate file list before committing. [Git add documentation](https://git-scm.com/docs/git-add).

Use explicit paths with `--`, or inspect interactive hunks when a file mixes work. Avoid blanket `git add .`, `git add -A`, and `git commit -a` in a mixed checkout. Never clear someone else's index entries to make your commit easier. If unrelated staged changes remain, coordinate with their owner or move the task to isolation before committing.

Validate the state the commit will contain. Unstaged fixes can hide staged failures. Use a stable isolated snapshot when the index and working tree differ materially. If a formatter or hook changes files, inspect the result and repeat affected checks before claiming that candidate passed. A Git index lock serializes individual commands, not the whole review-stage-test-commit sequence.

Follow the repository's commit policy and the user's endpoint. Keep one purpose per commit with its related tests and documentation. Preserve authorship when integrating another contributor's commits. Use `caveman-commit` only for message wording when appropriate. After committing, inspect `git show --stat HEAD` and status to verify the committed scope and remaining changes.

Do not stash another agent's work, reset or restore unrelated paths, clean unknown files, amend another task's commit, bypass hooks, or rewrite shared history to tidy a checkout. Identify the owner of a busy lock before retrying. Never remove a lock merely because an operation is blocked.

## Integrate across surfaces

Have one integration owner collect each worker's repository, base SHA, final SHA or patch identity, changed paths, checks, dependencies, and unresolved concerns. Freeze the handed-off revision. Working-tree edits after that point are new work.

Integrate reviewed commits in dependency order into the designated branch using repository policy. Inspect both the complete diff and affected producer/consumer contracts. Resolve semantic conflicts even when Git merges cleanly. Regenerate shared outputs under their assigned owner, then run checks on the combined state. Worker checks alone do not prove integration.

For multiple repositories, record a separate branch, revision, status, and check result for each. Do not cherry-pick across unrelated histories. Order compatible producer and consumer changes explicitly and report partial integration or delivery per repository. There is no atomic cross-repository merge.

Use [resolving-merge-conflicts](../resolving-merge-conflicts/SKILL.md) for an owned interrupted integration. Use [babysit](../babysit/SKILL.md) when the requested endpoint includes PR follow-through or release work. Push, merge, and publication require the existing authority for that destination and action.

## Handoff and cleanup

At feature completion, including local-only endpoints, use [temporary evidence cleanup](references/evidence-cleanup.md) to remove task-owned scratch evidence and screenshot directories. Carry exact paths and retention needs across handoffs. Preserve deliverables and evidence still needed for review or diagnosis, and report removed or retained artifacts.

Report integrated revisions, checks for that state, remaining changes and their owners, and retained worktrees or branches. After a verified merge, use [branch cleanup](references/branch-cleanup.md) to remove completed local feature branches, related remote branches, and temporary worktrees within existing authority. Include older leftovers for the completed feature; for a requested repository cleanup, apply the same checks to each older candidate. Do not equate a closed PR with a merge or a clean worktree with integrated commits.

Before removing a task-created worktree, confirm its owner has finished, no processes depend on it, tracked and untracked work is preserved, and its commits are integrated or deliberately retained elsewhere. Inspect ignored outputs for anything valuable. Remove only that worktree using Git without force. Never run fleet-wide pruning, delete another task's branch, or remove active worktrees as incidental cleanup.
