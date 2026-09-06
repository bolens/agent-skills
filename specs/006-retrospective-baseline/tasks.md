# Tasks: retrospective collection baseline

These tasks track the retrofit, not the original implementation history.

## Phase 1: Setup

- [x] T001 Inspect baseline source and existing specs; record decisions in specs/006-retrospective-baseline/research.md.
- [x] T002 Specify the retrofit and its evidence boundary in specs/006-retrospective-baseline/spec.md and plan.md.

## Phase 2: Foundation

- [x] T003 Record the explicit-request backfill exception in AGENTS.md and .specify/memory/project-guide.md (FR-002, FR-008).

## Phase 3: US1 coverage

Independent test: all registered skills map to a source and requirement.

- [x] T004 [US1] Write the four domain contracts under specs/006-retrospective-baseline/contracts/ (FR-003).
- [x] T005 [US1] Map every registered skill and original feature in specs/006-retrospective-baseline/coverage.md (FR-001).
- [x] T006 [US1] Add specification discovery in specs/README.md and README.md (FR-001, FR-002).

## Phase 4: US2 completeness

Independent test: each audit has a source-backed implementation disposition.

- [x] T007 [US2] Trace all nine accepted audit adaptations and original feature tasks in specs/006-retrospective-baseline/assessment.md (FR-004, FR-005).
- [x] T008 [US2] Resolve any demonstrated local gaps or record exclusions and external limits in specs/006-retrospective-baseline/assessment.md (FR-005, FR-006).

## Phase 5: US3 validation

Independent test: feature discovery succeeds and current evidence is reproducible.

- [x] T009 [US3] Execute specs/006-retrospective-baseline/quickstart.md, including manifest/requirement/link checks, source scenarios, and repository gates (FR-007).
- [x] T010 [US3] Run convergence against specs/006-retrospective-baseline/spec.md, plan.md, and tasks.md; record evidence in tasks.md (FR-005, FR-007).

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
committed separately. The initial local completion did not include publication.

## Subsequent source delivery verification

PR #27 merged the retrofit at `cc9d07d227df429156e892437f59ee1b0192b02f`.
Later changes through `1785f954fbea2a5a30d1f923534c4e5ac23e5cef` retain that
baseline and passed CI, Source lint, and the main-push workflow. The current
portable gate passed all 53 tests, provenance/registry validation, and portability.
The canonical installed checkout's link check passed without repointing links.
These are distinct current-source and installation observations; historical counts
above remain attached to their original checks. No unavailable live-system or
external-agent procedure is promoted to completed runtime evidence.

## Phase 9: Capability extension, 2026-09-06

These tasks extend the audit to the current source; earlier completion statements
remain attached to their earlier scope.

- [x] T015 Inventory all 62 current registered entrypoints and map individual observable/negative contracts in legacy-capabilities.md (FR-001, FR-003).
- [x] T016 Map executable helper, Archify CLI/family/viewer/export and supporting maintenance contracts in legacy-helpers.md and legacy-archify.md (FR-003, FR-007).
- [x] T017 Reproduce neighboring-file destruction during compression; use owned staging and verify success, rejection and exception preservation (FR-009).
- [x] T018 Correct help for packaged selection/commit/review behavior and work-log instructions for available evidence and permitted review capabilities (FR-010).
- [x] T019 Reproduce incomplete tree comparison and report-opening false success; retain independent mapping progress and report failure truthfully (FR-011).
- [x] T020 Reproduce hidden file-discovery failures and inconclusive pollution searches; retain source/fixture state and distinguish observed creation from unavailable proof (FR-012).
- [x] T021 Preserve audited upstream refs and licenses, regenerate local-change provenance, and adopt paired verified shared Spec Kit workflow/tooling pins.
- [x] T022 Run final portable and selected Archify gates; review registry/link consistency and all task-owned changes (FR-005, FR-007).
- [ ] T023 Scan and commit the reviewed changes, merge after current PR checks, and record exact main-revision delivery evidence (FR-006).

T015–T016 establish scope; discovered T017–T020 precede T021–T023. Local
`make check-fast test portability` currently passes 81 tests with no skips.
The compression fixture failed all three new preservation cases before repair;
tree/report fixtures failed both cases; discovery fixtures reproduced five false
success/inconclusive outcomes, while observed creation already returned failure.
Model replies and optional host validators are synthetic fixture seams. Real
loopback socket tests run in a permitted environment. Current Archify and hosted
results remain pending until separately recorded.

Local extended verification: 81 portable tests passed with no skips. The full
Archify suite passed 1,022 tests with four explicit skips: external MCO checkout,
non-Node-22 packaging negative case, and two site cases delegated to browser
integration. The serialized browser gate passed seven tests. The skipped MCO
fixture and alternate Node runtime remain unexecuted here; no broader claim is
made. Shared source lint and 324 local spec destinations passed. Separate local
self-review inspected the complete candidate; no independent reviewer ran. The
value-redacting scan examined 663 files, with no secrets or skips; 18 privacy
review hits are existing attribution/example/test values, including the new
reserved fixture address. Commit-range scanners and hosted delivery follow.

Integration note: remote main advanced to `93c7301` with prospectively specified
Sentrux analysis. Rebased before publication, preserved both changelog entries
and original 009, and linked its helpers without importing or executing a runtime.
The range comparison showed only changelog context changed by integration.

The integrated portable gate passed all 95 tests with no skips, including the
existing Sentrux fixtures. The refreshed map has 330 local destinations and 62
unique registered skill contracts. Archify runtime/test bytes are unchanged by
the integration, so its completed native results remain applicable.

Hosted Docker verification exposed missing jq in the source-free development
image; host PATH had supplied it in native runs. Add jq and ripgrep, required by
the real HTML/plugin inspection fixtures, to the existing development tool set.
Fixture setup now rejects missing prerequisites instead of allowing a negative
case to pass for the wrong reason. Rebuild and run the same image gate.

- [x] T024 Repair the development image's missing inspection prerequisites and prove the full portable gate inside the rebuilt source-free Docker image.

The rebuilt local image passed all 95 tests, provenance and portability checks.
Docker build/load/run used the authorized pkexec wrapper. No installed client links
were repointed. The selected hosted check must still verify the updated PR head.
