# Delivery playbook

Agent Skills continuously delivers reviewed hard forks from `main`. It does
not publish versioned packages or represent local forks as upstream releases.
Skill provenance remains authoritative in `PROVENANCE.json`, `UPSTREAMS.json`,
and each skill's `UPSTREAM.md`.

## Prepare and validate

Branch from current `origin/main` in a clean worktree. Preserve local fork
behavior and invocation policy. Review upstream diffs before importing them.
Update provenance and reader-visible changelog entries when affected.

```sh
make check-fast
make check
```

`make check` includes installed-symlink verification on the maintainer machine.
An isolated checkout may not own those links. Report that limitation and run
`make check-fast test portability`, the portable CI gate, without repointing
installed skills merely to make a check pass. Required CI is the `validate` job
in `.github/workflows/ci.yml`.

## Push and merge

Follow the [fleet push and merge steps](https://github.com/bolens/.github/blob/main/RELEASING.md#push-and-merge).
Review the staged diff, commit focused changes, and confirm `origin` points to
`bolens/agent-skills` before pushing the feature branch:

```sh
git push --set-upstream origin HEAD
```

Open a PR against `main`. Review the complete diff, require applicable checks
on the current head, resolve conversations, and squash-merge. Never push
directly to `main`, force-push, skip failing hooks, or bypass protection.
Verify CI on the merged SHA and remove the merged branch.

## Deliver and verify

The reviewed main commit is the delivery boundary. There is no release tag or
artifact publication workflow. Installing or repointing skill symlinks is a
separate authorized action. After an authorized installation, run
`python3 scripts/link-installed.py --check` in the canonical installed checkout
and verify the affected skill's instructions and referenced resources resolve.
An edit in an already linked checkout is immediately visible to its clients.

## Recover

Correct or revert faulty content through another PR. Preserve upstream
provenance and local customizations. For an authorized installation rollback,
restore the previously verified checkout or link target and verify the links.
Do not overwrite independent installed copies or reset unrelated local work.

Fleet policy: <https://github.com/bolens/.github/blob/main/RELEASING.md>.
