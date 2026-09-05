# Delivery playbook

This collection delivers reviewed hard forks through `main`. There are no
versioned packages, release tags, or release-artifact publication steps.
Provenance remains authoritative in `UPSTREAMS.json`, generated
`PROVENANCE.json`, and each skill's `UPSTREAM.md`.

The [fleet delivery policy](https://github.com/bolens/.github/blob/main/RELEASING.md#push-and-merge)
sets the shared push and merge rules. This guide supplies the repository's
validation, installation boundary, and recovery steps. Existing authorization
carries forward. A readiness-only task does not authorize a push or merge.

## Prepare and validate

Start a feature branch from current `origin/main` in a clean worktree. Verify
that `origin` points to `bolens/agent-skills` and preserve unrelated local work.
Use [CONTRIBUTING.md](CONTRIBUTING.md) for source ownership, provenance generation,
and upstream imports. Keep one coherent purpose per commit and review the
complete staged diff before committing.

From the canonical installed checkout, run:

```sh
make check-fast
make check
```

An isolated checkout does not own the installed symlinks. Run the portable CI
gate there and record that installation verification remains with the canonical
checkout:

```sh
make check-fast test portability
```

Do not repoint installed skills to hide a link-check mismatch. Run any additional
behavioral checks needed by the affected skill, and report skipped tools or
unexecuted paths. Review the publication boundary using [SECURITY.md](SECURITY.md).

## Push and merge

Before submission or an update, follow [Git freshness](skills/git-hygiene/references/freshness.md)
to refresh the intended base and existing feature head, reconcile intervening
changes, and validate the resulting candidate. Push the reviewed feature branch
when authorized:

```sh
git push --set-upstream origin HEAD
```

Open a PR against `main`. Describe the resulting behavior, relevant validation,
and remaining limitations. Review the full diff separately from implementation
and resolve actionable feedback, including review nits. For substantive changes,
use the [independent review workflow](skills/code-review/references/independent-reviews.md)
when reviewers are available and permitted.

The repository's required CI check is `validate` in
[`.github/workflows/ci.yml`](.github/workflows/ci.yml). It runs the portable gate.
Require applicable checks on the current PR head. New commits or a base refresh
need checks for that updated state. A green run on an older head or a queued
merge is not completion evidence.

Squash-merge without bypassing protection. Do not push directly to `main`, rewrite
shared history, or skip failing hooks. Confirm the host reports the PR as merged,
record the resulting main SHA, and verify CI on that revision. Diagnose failures
before retrying; repair source through a corrective PR.

## Deliver and verify

The reviewed main commit is the delivery boundary. Installation or repointing
links is a separate authorized action. Source changes in an already linked
checkout are immediately visible to its clients, even before a merge. Keep that
checkout at a stable path and do not remove it as temporary-worktree cleanup.

After merge, fetch the verified base and fast-forward the clean, task-owned
canonical checkout to that target. Confirm its HEAD and status, preserving and
reporting any dirty, active, or divergent checkout that cannot be synchronized.
Do not mistake refreshed remote-tracking refs for updated local files.

After an authorized installation or synchronization of the canonical checkout:

```sh
python3 scripts/link-installed.py --check
```

Verify the affected skill and its referenced resources resolve. Repository CI
does not prove installation on the maintainer's machine.

Use [Git hygiene's branch cleanup](skills/git-hygiene/references/branch-cleanup.md)
for completed local branches, related remote branches, and temporary worktrees.
Verify the exact work was merged, including squash-merge evidence. Preserve
advanced tips, dependent tasks, dirty or valuable ignored files, installed paths,
and default or protected branches. Recheck ownership before removal and guard
remote deletion against a concurrently changed tip. A host-deleted branch can
still have a local branch or worktree to clean up.

Record the PR, merged SHA, check results, installation evidence when applicable,
and cleanup outcome. Explain retained work without treating a successful merge
as proof that every delivery step finished.

## Recover

Before merge, fix the feature branch and repeat the affected checks. After merge,
correct or revert the faulty content through another PR. Preserve upstream
provenance and local customizations. Do not rewrite published history.

For an authorized installation rollback, restore a previously verified checkout
or link target and recheck the links and affected skill resources. Preserve any
independent installed copy and unrelated working changes. A repository rollback
does not undo external actions an agent already performed. Assess and recover
those through the affected system's own workflow.
