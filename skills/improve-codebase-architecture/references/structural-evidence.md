# Structural evidence

Use this procedure when an architecture audit needs dependency evidence or a
before/after comparison. Prefer the repository's existing analyzer and rules.
An authored Archify diagram can explain confirmed relationships, but cannot
establish which dependencies exist in the source.

## Establish coverage

Record the repository and revision, dirty changes, scan root, analyzer version,
language/parser versions, exclusions, and applicable rules. Distinguish discovered
files from successfully parsed files. Note unresolved imports, aliases, dynamic
registration, generated code, size limits, missing grammars, and truncated results.
An empty graph or zero violations with incomplete coverage is inconclusive.

Trace a reported cycle or boundary violation to concrete import sites and callers
before ranking it. Separate directory containment from functional dependency.
Check runtime registration and external consumers before interpreting an isolated
node as dead code. Import reachability does not prove execution or test coverage.

## Compare and constrain

Capture the baseline before an authorized structural change. Keep the baseline
and candidate on the same scope, parser versions, exclusions, and rule set.
Record new, removed, and unresolved edges or violations alongside any scores.
If the tool or scope changed, rerun both revisions with matching settings or
report the comparison as incompatible. Do not overwrite the earlier baseline
just to make a regression pass.

Prefer constraints tied to an ADR or observed failure, such as preventing imports
of core internals from the application layer. Confirm the rule's glob and layer
semantics. Exercise one allowed and one forbidden dependency in a small fixture
before making a new rule a CI gate. Check that the tool evaluated every intended
rule and returns a failing status for the forbidden case.

Treat aggregate scores as investigation leads. Splitting a file, adding an
interface, or moving a directory solely to raise a score needs an independent
maintenance or correctness benefit. A better total score cannot excuse a new
forbidden dependency. Existing violations need explicit scope and revisit
conditions rather than silent baseline acceptance.

An audit remains read-only. Hand an approved refactor to `safe-refactor`, carrying
the baseline, intended boundary change, and behavioral acceptance checks. Repeat
both the structural comparison and the behavioral proof. Stop when the requested
change is verified, not when an arbitrary score reaches its maximum.

## Optional Sentrux use

Use the [local Sentrux runner](../../audit-repo-fleet/references/sentrux.md) for
verified, isolated 0.5.7 snapshots and comparison identity on Linux x86_64 when
the selected language produces useful dependency evidence. It remains optional.
The [runtime audit](../../../docs/audits/2026-09-06-sentrux-runtime.md) records
executed fixtures, coverage limits, retained notices, and distribution boundaries.

Native Sentrux scans Git-tracked source and can miss new files. The runner copies
selected tracked and non-ignored untracked code into a temporary Git snapshot.
It retains scope, revision, content hashes, runtime identity, and baseline metrics
outside source. Do not substitute a partial graph or MCP rule response for full
policy coverage. Verify actual import sites and native behavior independently.

Before upgrading, review startup behavior, parser coverage, CLI/MCP differences,
artifact integrity, and license obligations again. The earlier
[source audit](../../../docs/audits/2026-09-05-netviz-sentrux.md) remains historical
evidence. A new runtime or scope requires compatible baselines from both sides.
