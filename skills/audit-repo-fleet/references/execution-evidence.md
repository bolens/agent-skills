# Keep execution evidence across fleet work

Use this contract for authorized implementation that spans repositories or long
checks. Keep the current repository's native commands, permissions, review, and
delivery playbook. This helper does not create a sandbox, grant permissions,
start agents, or replace the host's required CI checks.

## Record the work before running it

Keep a private task ledger with the repository, worktree, base SHA, owned paths,
acceptance conditions, native checks, dependencies, and intended delivery endpoint.
Distinguish pending, running, passed, failed, blocked, and not-applicable work.
Record a reason for exclusions and missing evidence. A successful subprocess is
one observation, not proof that all acceptance conditions have been met.

Use the ownership and dependency rules in
[git-hygiene](../../git-hygiene/SKILL.md). Run independent reads or checks together
when they do not share writable state. Serialize edits, formatters, generators,
and tests that use the same external resources. Delegate only when permitted by
the session. Join dependent work on recorded outcomes rather than elapsed time
or an agent's assertion that it finished.

## Run a native check with a receipt

From the skill directory, use the repository's documented command:

```sh
python3 scripts/evidence.py --repo /path/to/repository run \
  --label fast --timeout 900 -- make check-fast
python3 scripts/evidence.py --repo /path/to/repository report --label fast
```

Replace the path, label, timeout, and command with that repository's actual gate.
For a pnpm repository, the command might be `pnpm run verify`. A PowerShell
repository may require `pwsh -NoProfile -File` and its own validation script.
Do not impose pytest, a formatter, or a new runtime on unrelated applications.

The command runs once with an argument array and closed stdin. It inherits the
current environment. Choose the pinned toolchain and isolated test resources
before invoking it. Interactive commands and publication actions belong in their
existing workflows.

Receipts and stdout/stderr logs live in `fleet-evidence/` under the selected
worktree's Git directory. They are not tracked source files. On POSIX systems,
the helper creates evidence directories with mode 0700 and files with mode 0600.
Commands can emit secrets. Inspect and redact any selected evidence before
sharing it, and never pass credentials in command arguments or retry reasons.
Do not publish whole evidence directories or private fleet inventories.

The fingerprint includes HEAD, branch context, index state, and tracked or
nonignored working files. Ignored generated output does not invalidate evidence.
Symlink targets outside source ownership are not dependency contents. Record
external dependencies separately. Hashes avoid retaining copies of source text;
they do not make repeated tool output free of context or token cost.

`report` checks the latest receipt for every requested label against the current
candidate. It returns nonzero for missing, stale, running, failed, unavailable,
timed-out, interrupted, or changed results. A formatter that exits successfully
but changes source requires another stable validation run. A receipt does not
certify future toolchain, environment, service, dependency, or host-CI state.
Refresh those checks when their inputs change.

Receipts use format version 1. Unknown versions, malformed ordering fields, and
inconsistent successful results fail closed instead of revealing an older pass.
Keep incompatible receipts for diagnosis and use the matching producer version
or run a fresh check in an isolated worktree. Do not relabel their version or
rewrite their outcome to make a report pass.

## Diagnose before retrying

There are no automatic retries. An identical failed candidate and command require
`--retry-reason` on the next invocation. The default cap is three attempts, with
an explicit maximum of ten. A timeout is finite, defaults to 900 seconds, and
cannot exceed one day. Select a limit appropriate to the native gate.

Changing source creates a new candidate. For an unchanged retry, record the
observed transient failure and why another attempt is useful. Do not raise caps
or rotate labels to hide a persistent failure. Continue independent work while
an external prerequisite is unavailable.

Concurrent identical commands are rejected while their run lock exists. SIGINT
and SIGTERM during command execution stop the child process tree, save an
interrupted receipt, and release the run lock. Their exit codes are 130 and 143.
Cancellation remains accepted through final candidate verification and the first
terminal receipt write. The runner then seals the outcome, applies any cancellation
already received, and finishes receipt and lock cleanup without accepting another
cancellation. A completed write cannot be rolled back by a later signal.
An uncatchable kill or host failure can leave a running receipt and lock. Inspect
the recorded PID and ownership before removing that exact stale lock. Never infer
completion from a missing process or delete another invocation's lock.

Timeout and cancellation cleanup kill the command process group on POSIX systems.
Windows uses `taskkill /T /F`; validate that path on Windows before claiming native coverage.
Processes that deliberately escape their process group require an external
sandbox or supervisor. This command runner is not a security boundary.

After interruption, reconcile the recorded command's actual outputs before
retrying. Cancellation cannot roll back a completed write. A receipt is check
evidence, not a queue of actions to replay or permission to repeat publication.
Keep existing authorization when its scope still applies. Changed destinations
or operations need their own authority under the owning repository's rules.

## Review and deliver

Use [code-review](../../code-review/SKILL.md) to trace changed behavior, callers,
edge cases, and delivery risks. Add regression tests for actual defects and
meaningful failure cases. Do not append generic null or large-input tests that
lack a contract. Label self-review honestly when independent review is unavailable.

Use [babysit](../../babysit/SKILL.md) for the authorized PR and release endpoint.
Verify checks on the current head and the resulting merged revision. Keep
source validation, independent review, merge, release, installation, and cleanup
as separate outcomes. Passing tests do not establish zero defects.

Retain receipts needed for review or diagnosis. Once delivery is verified, remove
task-owned temporary evidence under the existing cleanup authorization. Preserve
recovery material and evidence for unfinished work.
