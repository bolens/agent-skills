# Feature specification: retrospective collection baseline

**Created**: 2026-09-05
**Status**: Retrospective baseline completed and locally validated
**Input**: Finish partial implementations and retrofit Spec Kit specs to missing areas.
**Baseline**: `8e51a4f`, including the Netviz/Sentrux audit.

This is an explicitly requested retrospective contract. It describes existing
capabilities and current evidence, not a claim that those capabilities were
specified before implementation. Feature records 001 through 004 remain the
original decision history and retain authority for their detailed scope.

## User scenarios and testing

### US1: Find the contract for an installed workflow, P1

A maintainer can locate each registered skill's owning contract and source without
guessing whether it has been specified. This makes future changes reviewable.

Independent test: compare the coverage inventory with the registered collection.

1. Given any registered skill, its coverage row identifies an existing feature
   spec or a retrospective domain requirement and links to its source.
2. Given a host-bundled or generated integration skill, the inventory states why
   it is outside this collection's registered baseline.
3. Given an existing feature spec, the retrospective record links to it without
   rewriting its historical task completion or validation claims.

### US2: Distinguish incomplete implementation from limited evidence, P1

A maintainer can decide what needs finishing without reinstalling rejected tools
or treating documentation as proof of live behavior.

Independent test: trace each recent source audit to its adopted source and verdict.

1. Given an adopted behavior, the assessment identifies its source and records
   whether it is implemented, partial, or missing within the accepted scope.
2. Given a deferred runtime or a blocked host report, it remains an explicit
   exclusion or verification limit until its decision or authority changes.
3. Given a demonstrated partial implementation, a task identifies its requirement,
   source, repair, and acceptance evidence before it is marked complete.

### US3: Keep the baseline usable for later maintenance, P2

A maintainer can follow the usual planning workflow and tell a historical record
from current test evidence.

Independent test: use Spec Kit prerequisite discovery and the repository gates.

1. Given this feature is selected, prerequisite discovery finds its spec, plan,
   and task list.
2. Given completed review work, the record distinguishes executed checks, source
   walkthroughs, skipped runtime checks, and external blockers.
3. Given a future change, documentation keeps ordinary prose maintenance narrow
   and requires a new or amended contract for substantive capability changes.

### Edge cases

- A skill serves more than one domain: assign a primary owner and link genuine
  secondary requirements without duplicating the skill or changing its trigger.
- A script contains an illustrative placeholder or an upstream deferred feature:
  do not label it a local implementation gap without an accepted requirement.
- A passing static gate does not establish browser, desktop, production, or
  external-model behavior.
- Network topology and systems architecture overlap. Diagram-tool selection
  depends on generated artifacts versus manual editing, not those subject labels.

## Requirements

- **FR-001**: Cover every skill registered at the baseline with an owning contract
  and a resolving source reference. Cover maintenance tooling separately.
- **FR-002**: Identify retrospective records, baseline revision, user authority,
  existing specs, and evidence limits without inventing historical planning.
- **FR-003**: Define acceptance scenarios for maintenance, engineering, web/visual,
  and system-operation workflows in domain contracts.
- **FR-004**: Trace the nine baseline source audits dated 2026-09-05 and the
  user-requested pstack follow-up to behavior, exclusions, and verification limits.
- **FR-005**: Assess named requirements against present source. Finish demonstrated
  local implementation gaps and retain deliberate deferrals as deferrals.
- **FR-006**: Preserve fork provenance, licenses, installation targets, managed
  integration templates, unrelated work, and existing action authority.
- **FR-007**: Provide a repeatable validation guide and distinguish static,
  behavioral, manual, and unexecuted evidence.
- **FR-008**: Keep the default no-backfill rule, with an explicit-user-request
  exception requiring honest retrospective labeling.

## Key entities

- Coverage entry: registered skill, owning requirement, source, evidence boundary.
- Adoption assessment: source audit, accepted behavior, implementation state,
  deliberate exclusions, and verification limits.
- Feature record: original or retrospective contract, plan, tasks, and evidence.

## Success criteria

- **SC-001**: Every registered skill has exactly one primary coverage entry and
  every entry resolves to its source and owning requirement.
- **SC-002**: All nine baseline source audits and the pstack follow-up have an
  implementation or adoption disposition.
- **SC-003**: No demonstrated in-scope implementation gap is left without a repair
  and evidence or an explicit external blocker.
- **SC-004**: Repository gates pass and every claimed check has its method and
  limit recorded. No deferred application is represented as installed.

## Assumptions

The requested scope is this canonical collection, not every repository in the
fleet. A skill can be a complete guidance workflow without bundling an application.
The user requested retrospective specs, but did not authorize new external-model
context transfers or publishing. Netviz remains a candidate for manual editing;
Archify remains the generated-diagram default for both network and system topics.
