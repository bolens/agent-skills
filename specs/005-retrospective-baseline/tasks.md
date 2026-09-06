# Tasks: retrospective collection baseline

These tasks track the retrofit, not the original implementation history.

## Phase 1: Setup

- [x] T001 Inspect baseline source and existing specs; record decisions in specs/005-retrospective-baseline/research.md.
- [x] T002 Specify the retrofit and its evidence boundary in specs/005-retrospective-baseline/spec.md and plan.md.

## Phase 2: Foundation

- [x] T003 Record the explicit-request backfill exception in AGENTS.md and .specify/memory/project-guide.md (FR-002, FR-008).

## Phase 3: US1 coverage

Independent test: all registered skills map to a source and requirement.

- [x] T004 [US1] Write the four domain contracts under specs/005-retrospective-baseline/contracts/ (FR-003).
- [x] T005 [US1] Map every registered skill and original feature in specs/005-retrospective-baseline/coverage.md (FR-001).
- [x] T006 [US1] Add specification discovery in specs/README.md and README.md (FR-001, FR-002).

## Phase 4: US2 completeness

Independent test: each audit has a source-backed implementation disposition.

- [x] T007 [US2] Trace all nine accepted audit adaptations and original feature tasks in specs/005-retrospective-baseline/assessment.md (FR-004, FR-005).
- [x] T008 [US2] Resolve any demonstrated local gaps or record exclusions and external limits in specs/005-retrospective-baseline/assessment.md (FR-005, FR-006).

## Phase 5: US3 validation

Independent test: feature discovery succeeds and current evidence is reproducible.

- [x] T009 [US3] Execute specs/005-retrospective-baseline/quickstart.md, including manifest/requirement/link checks, source scenarios, and repository gates (FR-007).
- [x] T010 [US3] Run convergence against specs/005-retrospective-baseline/spec.md, plan.md, and tasks.md; record evidence in tasks.md (FR-005, FR-007).

## Phase 6: Delivery

- [x] T011 Update CHANGELOG.md, review all task-owned diffs, and commit the retrofit (FR-006).

## Dependencies and strategy

T001-T003 precede coverage. T004 precedes T005-T006. T007-T008 follow coverage.
T009-T011 follow the assessment. Start with traceable coverage, then classify
remaining work, then validate the integrated record. Domain contract drafting
could be parallelized by file, but this implementation is local and sequential.

## Evidence

- `make check-fast` and `make check` passed after the provenance correction:
  61 registered skills, all 39 tests, portability with ShellCheck, and installed
  link verification. Existing capture tests used permitted loopback sockets.
- A manifest/Markdown validation pass checked 61 unique primary coverage rows,
  their canonical entrypoints, requirement IDs and anchors, all ten audit links,
  and 160 local destinations across the feature, index, and follow-up audit.
  No unresolved scaffold markers remained.
- Spec Kit prerequisite discovery found spec.md, plan.md, tasks.md, research,
  data model, contracts, and quickstart. No extension hooks were configured.
  `.specify/feature.json` is ignored local selection state, not a tracked change.
- Skill Creator validation passed for blast-radius. An exact baseline comparison
  proved its source identity after removing only the Cursor invocation flag.
  The retained MIT license matches its registered SHA-256.
- An executed disposable-home installer check preserved a conflicting real
  directory and sentinel, reported failure, and applied unrelated target links.
  No actual client-home link was changed by that fixture.
- Manual source scenarios: missing PR access/delegation permits a local impact
  assessment with explicit gaps; a failed probe remains unproven; a log sentinel
  is excluded before collection; a partial scan is inconclusive; a missing WAN
  check remains unverified. These are instruction walkthroughs, not live-system
  or independent-agent executions.
- Original how/why/arena prompts and their references were audited as source.
  Their agent fan-outs and private connector queries were not executed. The
  initial overlap claim was corrected in the source audit and project guide.
- The full Archify fetched/browser suite and shared Source lint were not run.
  The provenance correction changes CI path selection, so selected PR checks
  will still be required if publication is requested. No runtime change was
  made to Archify, and no current full-suite result is claimed.

## Phase 7: Discovered implementation repair

- [x] T012 [US2] Replace unavailable companion procedures in skills/blast-radius/SKILL.md with direct history inspection and available review routing; verify local fallback and evidence boundaries (E-006, FR-005).

T012 was discovered during T007 and must finish before T009-T011.

## Phase 8: Original-source audit requested during implementation

- [x] T013 [US2] Audit pstack's original how, why, and arena workflows and record corrected coverage judgments in docs/audits/2026-09-05-pstack-companions.md.
- [x] T014 [US2] Correct the proven blast-radius origin in UPSTREAMS.json, retain its license, regenerate provenance, and update LICENSE.md (M-001, FR-006).

T013-T014 follow the user's source-verification request and precede final validation.

## Completion and convergence

The source/contract convergence pass checked eight feature requirements, four
success criteria, nine user-story scenarios, twenty domain requirements, the
plan's source/validation decisions, and all five constitution principles. No
additional missing, partial, contradictory, or unrequested implementation was
identified within this feature's accepted scope. No empty convergence task phase
was appended. The completion bookkeeping here is maintained by implementation.

The blast-radius source/provenance repair and original-source audit were committed
as `07d2625`. The retrospective records, discovery, and policy exception are
committed separately. No push or merge is part of this completion.
