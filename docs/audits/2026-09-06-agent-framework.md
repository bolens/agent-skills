# Microsoft Agent Framework assessment

Reviewed Microsoft Agent Framework at commit
[`2c49f50cf08ebb6c1687146336f039051f159333`](https://github.com/microsoft/agent-framework/tree/2c49f50cf08ebb6c1687146336f039051f159333).
This is a selective source assessment, not an audit of the whole framework.
The changes are locally written adaptations. No Microsoft code, package, or
deployment service was imported.

## Adopted patterns

The workflow runner [cancels and awaits its active iteration](https://github.com/microsoft/agent-framework/blob/2c49f50cf08ebb6c1687146336f039051f159333/python/packages/core/agent_framework/_workflows/_runner.py#L137)
when its parent is cancelled. The fleet evidence runner handled keyboard
interruption and timeout but had no SIGTERM cleanup. A subprocess regression
confirmed that terminating the runner left a descendant alive. The runner now
records cancellation, stops its owned process group, saves an interrupted
receipt, and releases its retry lock. Signal handlers defer cleanup so they
cannot raise halfway through child creation or receipt persistence.

The framework's [checkpoint compatibility tests](https://github.com/microsoft/agent-framework/blob/2c49f50cf08ebb6c1687146336f039051f159333/python/packages/core/tests/workflow/test_checkpoint_validation.py)
reject resuming a changed workflow graph. The local equivalent is validating
saved evidence before reusing it. Source fingerprints already invalidate old
checks, but the receipt reader ignored its format version and accepted
inconsistent successful outcomes. Regression tests reproduced both cases.
It now validates version, consumed field types, known states, and the successful
result's exit code and final candidate. Atomic receipt replacement already
existed and remains unchanged.

## Applicability

| Pattern | Decision and reason |
| --- | --- |
| Cancellation propagation | Fix the shared fleet runner, where a subprocess reproduction demonstrated orphaned work. |
| Checkpoint compatibility | Reject incompatible or inconsistent receipts in the existing evidence reader. |
| Durable resume | Clarify that interrupted writes need reconciliation before retry and saved checks do not authorize replay. |
| Bounded workflow execution | Already covered by finite timeouts, attempt caps, retry reasons, and candidate identity. Preserve those controls. |
| Sensitive telemetry disabled by default | The framework's observability source documents this boundary. Keep local private receipts and existing log warnings. No remote exporter is justified by this task. |
| Agent providers, graph orchestration, middleware, approval stores | No matching application migration was established in the inspected fleet. Adding this runtime would add dependencies without a demonstrated requirement. |

The maintained GitHub inventory and retained Gitea source checkouts were searched
at recorded local revisions for the shared helper and framework integration.
The helper has one maintained owner, `audit-repo-fleet` in this collection.
Consumers can use that shared helper without copied application patches.
Detailed revisions and unavailable checkouts remain in the private task record.
Only this repository's base was freshly fetched. Other cached revisions do not
prove current host-wide coverage. Archived projects were excluded.

## Verification boundary

The regression suite exercises real child processes for SIGTERM and SIGINT,
checks descendant cleanup, interrupted receipts, lock release, and retry reasons.
It also checks receipt incompatibility and inconsistent successful outcomes.
Existing timeout, candidate drift, log permissions, and worktree isolation tests
remain part of the same gate.

POSIX process groups are verified on Linux. Native Windows termination and
uncatchable process or host failure are outside this evidence. These fixes do
not provide transactional rollback, process sandboxing, or authenticated receipts.
The work uses the normal focused-fix workflow and retains the existing
[fleet evidence specification](../../specs/005-fleet-evidence/spec.md).
