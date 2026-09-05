# Validation guide

Read the skill and evaluate these scenarios without modifying a live repository:

1. Two writers, separate packages, shared lockfile: assign isolated branches and one lockfile owner. Integrate contracts before regenerating and testing consumers.
2. Shared checkout, another person's staged edit: serialize Git operations, preserve that entry, and block the commit until ownership is resolved or use isolation.
3. Another agent changes HEAD during testing: invalidate the claim for the old candidate and inspect the new state before restaging and retesting.
4. Producer and consumer in separate repositories: record both SHAs, order compatible changes, and report partial integration independently.
5. Worktrees or agent tools unavailable: continue serially. Do not pretend isolation or delegation succeeded.
6. Busy index lock or interrupted operation: identify its owner, preserve it, and avoid deleting locks or aborting another task.
7. Cleanup with untracked files or unintegrated commits: retain the worktree and branch pending verified recovery and ownership.
8. Verified squash merge with unchanged feature tips: use exact host head-to-merge evidence, remove eligible temporary local worktrees, and delete branches only under verified ownership and existing cleanup authority. An advanced remote tip must reject conditional deletion.
9. Host already deleted the remote branch: finish eligible local branch and temporary worktree cleanup. Retain the main checkout and installed paths.
10. Request only a commit message or read-only review: keep those workflows without acquiring writer ownership.

Run `make check-fast`, then `make check`. If new install links are absent, report that exact limitation and run `make check-fast test portability` without installing them.

## Evidence, 2026-09-05

Manual evaluation of all ten scenarios: the instructions assign shared writes, preserve unrelated index entries, recheck changed revisions, separate repository delivery, serialize when isolation is unavailable, preserve foreign operations and locks, retain unfinished work, distinguish squash integration, finish local cleanup after host deletion, and keep message-only/read-only requests out of the writer workflow.

Disposable Git repositories verified four mechanisms: selected staging retains preexisting entries, separate worker commits preserve unrelated staged and unstaged layers, squash integration can produce the same tree without feature-head ancestry, and non-force worktree removal refuses untracked files. A local bare remote also verified that expected-SHA deletion rejects an advanced branch tip. All assertions passed. No live branches or worktrees were removed.

`make check-fast` and skill-creator quick validation passed. The first sandboxed full check could not open loopback sockets. Re-running `make check` with that restriction lifted passed all 26 tests and portability checks, then failed only on the three absent git-hygiene client symlinks. Installation was not performed. Existing contract tests verified installation in temporary client homes. No external-interface contracts or runtime code were added.
