# Delivery playbook

[Documentation](docs/README.md)

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

The Woodpecker `portable` pipeline runs the portable gate and client-loader
checks. The `validate` job in
[`.github/workflows/ci.yml`](.github/workflows/ci.yml) requires the exact trusted
native result on PRs, main pushes, and manual main runs, and requires the selected
Archify and native macOS jobs to succeed. Its weekly schedule still executes
the portable gate on GitHub to retain periodic environment coverage until a
reviewed native schedule replaces it. The separate
native `repository` lane runs the same language lint and workflow-security policy
as the disabled hosted Source lint workflow retained in source for rollback. Verify
current host protection settings as well as the committed workflows; YAML alone
does not establish which status names the host requires.
The native-status join retries transient HTTPS disconnects within its existing
deadline. Each retry reads a fresh combined status and history pair. Native
failures, invalid identities, authentication errors and malformed responses still
fail the gate.
Require applicable GitHub and Woodpecker checks on the current PR head. New commits or a base refresh
need checks for that updated state. A green run on an older head or a queued
merge is not completion evidence.

Before merge, verify the PR title and final squash message follow
[semantic conventions](skills/git-hygiene/references/semantic-conventions.md).
Preserve any breaking marker and migration footer in the resulting commit.

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

## Source lint

The disabled [Source lint workflow](.github/workflows/source-lint.yml) remains
tracked for rollback. The native `repository` lane checks Python and JavaScript
files selected by [`.github/source-lint.json`](.github/source-lint.json), then
runs actionlint and the zizmor security audit. It calls `bash scripts/ci/check-policy.sh` for the same policy, using the exact
SourceLint ref below and the matching hosted actionlint/zizmor versions.
`make check` does not run these shared tools. See the
[CI index](docs/woodpecker-transition.md#ci-organization) for prerequisites and
the retained platform, browser and publication boundaries.
Use the [shared local reproduction instructions](https://github.com/bolens/.github/blob/96705dc8d8147b92eee283dec1f43e91bd30c4e9/docs/source-lint.md)
with the same tooling revision pinned in
[the native helper](scripts/ci/check-policy.sh). Review exclusions when adding
source files; generated and imported files retain their native validation.
Require the applicable source and workflow-security checks to pass on the current
PR head before merging.

## Archify test coverage

With Node 22 active, `make test-archify` fetches the exact `UPSTREAMS.json` audited revision into a
temporary workspace, replaces its entire Archify directory with this local
fork, installs locked test dependencies, and runs the native generated-file,
golden, and complete Node test suite. The upstream parent directory supplies
website and release fixtures absent from the packaged skill. Its notice checker
requires this fork's pinned Simple Icons version and mirrors the packaged notice
into the temporary repository root; all disclosure and byte-match checks remain.
The temporary index includes the fork files, and its ZIP fixture is rebuilt for
the fork before reproducibility tests. It does not verify the upstream release
ZIP or publish an archive. Installed skills and links are untouched. Network
access is required.

Automated PR/main checks run the complete Node harness with real Chromium in
Woodpecker. Both legacy GitHub shard names join that full result; neither may
reuse the portable workflow's status. Manual and weekly GitHub runs retain two
exhaustive hosted shards. The separate serialized WebM/site integration job stays
hosted with real Chrome. Reproduce with `make test-archify
ARCHIFY_TEST_ARGS=--shard=1/2` (then 2/2), or `ARCHIFY_TEST_ARGS=--browser`.
Set `ARCHIFY_CHROME` to a headless Chrome executable for browser coverage.
Dorny selects these jobs for Archify, provenance, runner, or workflow changes;
main, scheduled, and manual runs validate the full fork. The existing required
`validate` job also requires every selected Archify job to succeed.

The current full harness contains 1,026 tests. With Chrome configured, its
ordinary run passes 1,022 and retains four existing skips: two serialized site
cases run in the separate WebM/site job, one needs an external MCO source fixture,
and one intentionally requires a Node major other than the canonical 22. Without
Chrome, a local run instead skips 27 tests; that incomplete browser result cannot
qualify the native lane. Record actual native workflow/child results, Chromium
version, and skip reasons before retiring hosted runtime work.

## Managed integration validation

`bash scripts/ci/check-spec-kit.sh` verifies the current Spec Kit manifests and
managed files without updating them. The existing native repository-policy
command, `bash scripts/ci/check-policy.sh`, includes this check in its existing
container and status context. It downloads only the public validator at
`bolens/.github@c161a6757130ea687def9eb1e81c6a4190488f07`, verifies its
SHA-256, limits the download to 64 KiB and 60 seconds, and bounds validation to
four minutes. Local reproduction needs Bash and Python 3 on Linux/macOS with
HTTPS access. It uses temporary files and requires no secrets or installed skill links.

Source/workflow policy now runs in Woodpecker. Duplicate GitHub policy workflows
are disabled, including manual and scheduled execution, after verified cutover.
Their tracked source remains available for rollback. The mixed
Spec Kit workflow stays active for manual read-only validation and its
scheduled/manual updater. Automatic PR/push validation is covered by the native
repository-policy gate after exact-head PR and genuine-main acceptance.

The repository maintainer reviews the validator pin during monthly dependency
maintenance and whenever a shared-validator security fix is published. Review
the immutable commit and SHA-256 together and require actual native validation
on the updated source. Existing dependency automation does not monitor this
embedded supplier pin. Preserve the current check names and publication/platform
boundaries.
