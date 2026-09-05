# Independent focused reviews

The coordinating reviewer owns the full diff and the final evidence. Focused agents provide separate inspections, not votes on whether the change is good.

## Assign from the change

Choose at least two distinct focuses when a substantive PR supports them. Do not launch a fixed roster regardless of the diff.

| Focus | Inspect |
|---|---|
| Behavior and compatibility | Requirements, affected callers/consumers, schema and API contracts, backward compatibility, alternate paths |
| Tests and failure paths | Assertions and mocks, negative cases, concurrency, partial failure, cancellation, cleanup, reproduction quality |
| Security and authority | Trust boundaries, tenant/resource ownership, input sinks, credentials, CI permissions, agent/tool action authority |
| Build and delivery | Dependencies, generated output, packaging, runtime/platform support, CI filters, rollout and recovery |

Split by subsystem instead when that offers clearer ownership, but assign an owner for shared boundaries. A reviewer may inspect beyond its initial files to follow a contract. Specialized skills deepen only relevant concerns and retain the read-only review scope.

## Provide an independent starting point

Give each reviewer the same fixed base, target/head and merge-base when relevant, repository guidance, original requirements, full diff access, and its focus. For uncommitted work, provide a stable snapshot or patch plus source context that preserves the reviewed layers. Record the snapshot identity. Do not let concurrent edits silently change what reviewers are inspecting.

Use fresh reviewer contexts when the agent tooling supports them. Do not pass the implementer's conclusions, other reviewers' findings, or a desired verdict during the initial pass. Access to source and tests matters more than a summary. Review agents inspect and report; they do not modify shared files, commit, or post remote reviews. Run writable checks in separate scratch space when needed.

Ask every reviewer for:

- reviewed revision or snapshot, focus, and inspected boundaries
- actionable findings with severity, confidence, location, trigger, evidence, and smallest fix
- actionable nits as a separate category when requested by the caller, including babysit
- tests actually run and the state tested, plus unresolved questions and coverage gaps
- an explicit no-findings result if none are supported, never an invented minimum count

## Collect and reconcile

Track every assigned review as pending, completed, failed, or unavailable. Wait for all assigned reviews or report the missing review as a gap. If capacity requires waves, preserve the same candidate between waves. Do not finish when only the fastest reviewer has responded.

Collect the union of all findings, requested nits, questions, and coverage gaps. Preserve reviewer attribution and reviewed revision when deduplicating. Merge duplicate root causes without dropping a unique consequence or requested correction. One reviewer reporting no findings does not negate another reviewer's evidence.

The coordinator checks disputed claims against source or a focused reproduction. Resolve disagreements by evidence rather than majority vote or severity averaging. Cross-check producer/consumer interactions spanning reviewer assignments. Report materially unresolved disagreement and missing evidence explicitly.

Return the consolidated result to the caller. In a read-only review, corrections remain recommendations. During babysit, hand off every item for disposition and verification. After implementation changes, ask relevant reviewers to verify the affected fixes and new interactions against the updated candidate. Earlier conclusions apply only where their inputs and assumptions remain valid. Do not rerun unaffected reviews merely to multiply approvals.
