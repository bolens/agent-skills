# Command status and diagnostic output

Use for build/test wrappers and pipelines whose readable output can obscure the
actual result. Keep the repository's task runner and existing validation commands.
A new Makefile or output formatter is useful only when it resolves a concrete gap.

## Preserve the result through every layer

Trace the producer, formatter, log writer, shell, task runner, and CI step.
A successful final command can hide an earlier failure. Neither an empty error
summary nor a generated report establishes that compilation or tests passed.

In Bash, `pipefail` makes a pipeline fail when a stage fails. Its status is the
rightmost nonzero stage status, which is not necessarily the producer's code.
When individual outcomes matter, capture `PIPESTATUS` immediately after the
pipeline, before another command overwrites it, and account for `errexit` when
arranging that capture. Retain formatter/logging failures as separate evidence.

Confirm the executing shell supports the selected mechanism. Make normally
executes separate recipe lines in separate shells, so setting an option on one
line may not govern the pipeline on the next. Scope the option and command to
the same shell or use a reviewed wrapper with an explicit runtime. Do not change
all recipe semantics to repair one command without checking other targets.

If pipeline control is unsuitable, run the producer into a task-owned log,
capture its status, then render that log and return the appropriate failure.
Avoid catch-all success fallbacks and test-marker searches as substitutes for
the producer's status. Preserve structured result bundles when the test contract
requires them, including evidence that relevant tests actually ran.

## Keep diagnostics useful

Present a short result with the failing stage and relevant diagnostic location.
Retain raw stdout/stderr in a bounded, access-appropriate artifact when filtering
could remove necessary evidence. Keep credentials out of logs and check the
artifact before external publication. Distinguish warnings from failures under
the repository's existing policy rather than enabling warnings-as-errors by default.

Before trusting a new wrapper, exercise producer failure with a successful
formatter, formatter failure, and ordinary success in disposable state. Also
check the outer task/CI status. Use focused tests while iterating, then required
handoff gates. A successful build alone does not prove that a freshly built
application launched or that its runtime behavior passed.
