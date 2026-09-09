# Work-unit dependencies and correction

Use for coordinating several units of implementation or repairing a failed
handoff. Keep the record in existing task notes or the project plan. A small
change needs no graph file, new orchestration framework, or extra agents.

## Define units and waits

Before assigning work, identify each unit's input revision, expected output,
owner, write boundary, acceptance evidence, and prerequisites. Split along
contracts or independently verifiable outcomes. Directory boundaries alone do
not separate shared policy or consumers.

For each wait, name its reason: a consumed artifact, shared mutable resource,
required order of side effects, authorization, or an integration prerequisite.
Independent outputs can still contend for an index, database, port, or rate
limit. Remove incidental ordering only after checking these constraints.
Parallel execution still depends on available capacity and delegation authority.

Use existing deterministic tools for mechanical work such as enumerating
changed paths, comparing declared exports, or matching exact identifiers.
Semantic conflict resolution, ranking by impact, and deciding whether findings
share a cause still require judgment. Successful parsing is not acceptance.

## Make acceptance actionable

Choose evidence that could reject the unit before its implementation starts.
Tie it to the unit's requirements and exact candidate, using the repository's
existing checks. A process exit code is useful only when the command exercises
the relevant behavior. Preserve any required review of behavior that those
checks do not establish.

Give each result a disposition and next action:

| Result | Coordination action |
| --- | --- |
| Accepted | Retain the candidate and evidence. Release only its satisfied dependents. |
| Failed | Return the defect to its owner and hold dependent work that requires the failed contract. |
| Unavailable or blocked | Record the missing tool, access, input, or authority. Continue independent permitted work. Do not treat missing evidence as a pass. |

Read-only review returns recommendations. A correction proceeds only when the
task includes fixes. Passing a unit does not authorize merging, publishing, or
external actions. Complete preparation already authorized before requesting
missing approval for a concrete remaining action. Consequence and reversibility
determine appropriate evidence and recovery preparation, not new authority.

## Correct the failed unit

Return the unit and candidate identity, failed condition, expected and observed
behavior, reproducible evidence, permitted edit scope, and check to rerun. Keep
unchanged accepted units and their receipts. Do not regenerate a whole batch
because one unit failed.

Trace the correction's impact before reusing earlier evidence. A changed shared
contract can invalidate accepted consumers even if their files did not change.
Recheck those consumers and the integrated candidate with required repository
gates. If the repair crosses ownership boundaries, revise the assignment with
the integration owner before editing those paths.

Bound retries by the task's existing time, cost, or attempt limit. If none exists,
choose a proportionate limit before repeated retries. Stop blind repetition when
the same evidence recurs or progress stalls. Inspect inputs, checks, environment,
and the decomposition before another correction. Attempt count alone does not
identify the cause. Report the remaining condition if no permitted repair is
available, while completing independent work.

## Carry forward supported lessons

Record a confirmed failure's cause, affected contract, correction, and proof
with the unit's receipt when it informs later work. Update pending briefs that
depend on that contract so the same run benefits from the finding.

For durable guidance, state the applicability condition and supporting evidence
in the repository's existing test, decision, or instruction location when that
maintenance is authorized. A passing attempt alone does not establish a general
rule. Keep one-off workarounds scoped, omit secrets and raw logs, and revise a
lesson when its assumptions change. Do not automatically rewrite global skills
or convert every failure into a permanent restriction.

## Attempts, cancellation, and uncertain outcomes

Give each assignment an attempt identifier alongside its input revision. Include
both in progress reports and the final receipt. A delayed result from a replaced
attempt cannot release dependents or overwrite the current candidate. Reconcile
its useful evidence explicitly. A receipt names changed paths, final revision,
checks and their tested revision, owned running processes, and retained artifacts.

Cancellation requests do not transfer ownership. Wait for the worker and its
owned child processes to stop writing, then inspect the resulting files before
reassignment or cleanup. Missing heartbeats and elapsed time do not prove that a
writer is dead. Use the coordination channel or OS ownership evidence. If the
owner cannot be reached, keep overlapping mutations blocked and continue work
that does not depend on that resource.

After a timeout or lost acknowledgement of a mutation, inspect its actual outcome
before retrying. A commit, link change, upload, or service start may have succeeded.
Prefer operations with inspectable state and idempotent retries. Report partial
completion per resource and preserve evidence needed to recover it.

Catalog installers, generators, shared browser checks, and deployment helpers
need resource ownership beyond the Git index. Acquire locks in a stable order,
fail or wait within a declared budget, and release them only after child cleanup.
Keep validation inputs stable throughout the check. Independent worktrees still
share installed client homes, browser capacity, and external services. Avoid
starting a second full browser matrix when a relevant run is already owned.
Use a focused check while iterating and have the integration owner run the final
matrix once against the agreed candidate. Never accept evidence from another
revision merely to avoid rerunning a necessary check.
