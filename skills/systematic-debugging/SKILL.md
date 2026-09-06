---
name: systematic-debugging
description: Diagnose reproducible bugs, test failures, build failures, performance regressions, and unexpected technical behavior by gathering evidence and tracing the failure before changing code. Use when the user asks to debug, investigate, diagnose, or fix a technical failure.
---

# Systematic debugging

Explain the failure with evidence before changing code. Scale the investigation to the risk: a clear typo needs less ceremony than an intermittent production fault.

Read repository instructions and use its normal diagnostics. Keep probes minimally invasive. Never print secrets; report presence or redacted metadata.

## Investigate

1. Capture the exact error, relevant logs, command, inputs, environment, and observed result.
2. Reproduce the failure when safe. If it is intermittent, characterize when it occurs instead of guessing.
3. Inspect recent changes, configuration, dependencies, and a nearby working example.
4. Trace the bad state backward to its source. At component boundaries, verify what entered, what left, and which configuration crossed the boundary.
5. State one falsifiable hypothesis and the evidence supporting it.

Read [root-cause-tracing.md](root-cause-tracing.md) when the symptom appears far from its source. Read [condition-based-waiting.md](condition-based-waiting.md) for timing failures. Read [defense-in-depth.md](defense-in-depth.md) only after finding the root cause and deciding where validation belongs.

## Test the hypothesis

Run the smallest safe probe that can distinguish the hypothesis from plausible alternatives. Change one relevant variable at a time. A failed probe is new evidence, not a reason to stack another speculative fix on top.

For contradictory build or test results, inspect the original process status and
raw output before trusting a formatter or wrapper summary. Trace status through
the shell and task runner using [command evidence](../ci-maintenance/references/command-evidence.md).

When runtime state is missing, add temporary, scoped instrumentation at the
suspected boundary. Correlate events with the actual process/build and request
or object, exercise the failing scenario, then remove or reduce diagnostic noise
after the hypothesis is resolved. For ongoing error diagnostics, read
[wide events and safe error handling](references/wide-events.md). Prefer useful
structured context over scattered messages or raw object dumps. Keep retained
diagnostics bounded and exclude sensitive data before it enters logging buffers.
For uncertain API behavior, check the project's dependency or SDK version against
the relevant primary documentation section. A local documentation cache needs
source/version identity and freshness checks; a search-index hit is a locator,
not proof that the API exists on the target runtime.

If repeated hypotheses fail, reassess assumptions, reproduction fidelity, and component boundaries. Consider an architectural cause only when evidence shows shared state, coupling, or a broken contract. The number of failed attempts alone proves nothing.

## Fix and verify

When the user authorized a fix:

1. Add the narrowest practical regression test or deterministic reproduction.
2. Fix the source of the failure without unrelated cleanup.
3. Run the focused check, then the repository's proportionate validation.
4. Confirm the original behavior now works and report any verification gaps.

Use `tdd` when the user requests test-first work or a full red-green-refactor loop adds value. If diagnosis was requested without implementation, stop after explaining the cause and supported options.

## Stop conditions

Carry forward authorization already given in the conversation. Ask only when the next action needs authority that has not been granted, missing access, or a consequential product decision that cannot be inferred. Prepare a concrete proposed change and complete independent diagnostics before requesting approval for a production mutation or destructive recovery. If the issue remains unresolved, report what is known, what was ruled out, and the next discriminating probe.

When asked to repair CI on an open PR or carry a fix through PR or release delivery, automatically use [babysit](../babysit/SKILL.md) to coordinate the current head, audit, and remote checks. Keep diagnosis here and return the cause, fix, and verification evidence to an already active workflow. A diagnosis, status lookup, or local bug fix alone does not start follow-through.

When this fix belongs to active fleet-wide implementation, return the confirmed cause and applicability conditions to [the fleet shared-fix workflow](../audit-repo-fleet/references/shared-fixes.md). Check maintained peers for the same cause and implement confirmed matches within that scope before closing the batch. A single-repository diagnosis or fix keeps its original scope.
