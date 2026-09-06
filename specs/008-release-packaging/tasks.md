# Tasks: Portable release packaging

**Input**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md),
[data-model.md](data-model.md), and [receipt contract](contracts/packaging-receipt.md).

## Phase 1: Setup

- [x] T001 Read repository and affected-skill guidance; record scope in specs/008-release-packaging/spec.md.

## Phase 2: Foundation

- [x] T002 Verify native ecosystem semantics and user portability preferences in specs/008-release-packaging/research.md.

## Phase 3: User story 1 - Supported variants

**Goal**: Map all conditional targets without invented store support.
**Independent validation**: Trace a tagged and main-tip release across the target matrix.

- [x] T003 [US1] Create skills/release-packaging/SKILL.md with scope, variant identity, and evidence workflow.
- [x] T004 [US1] Create skills/release-packaging/references/targets-and-variants.md for all requested and added ecosystems.
- [x] T005 [US1] Create skills/release-packaging/references/language-and-build-options.md with capability-based selection.

## Phase 4: User story 2 - Lean modern portability

**Goal**: Keep runtime payload lean while supporting current platforms.
**Independent validation**: Detect leaked build tools and unsupported ABI without removing required runtime behavior.

- [x] T006 [US2] Create skills/release-packaging/references/lean-portability.md covering target environments, payload/closure measurements, and artifact checks.
- [x] T007 [US2] Record modern cross-platform preference in .specify/memory/project-guide.md and skills/triage-dependency-updates/SKILL.md.

## Phase 5: User story 3 - Workflow integration

**Goal**: Route relevant work and retain delivery authority.
**Independent validation**: Walk release, Arch, CI, fleet, and excluded changelog-only tasks.

- [x] T008 [US3] Add handoffs in skills/babysit/references/release-follow-through.md, skills/arch-package-maintenance/SKILL.md, skills/ci-maintenance/SKILL.md, and skills/audit-repo-fleet/SKILL.md.
- [x] T009 [US3] Regenerate PROVENANCE.json and skills/release-packaging/UPSTREAM.md; verify managed install targets through scripts/link-installed.py.
- [x] T010 [US3] Update README.md, CHANGELOG.md, and specs/README.md with the packaging workflow and feature.

## Phase 6: Verification and commit

- [x] T011 Validate bounded scenarios from specs/008-release-packaging/quickstart.md and record review evidence in specs/008-release-packaging/verification.md.
- [x] T012 Run skill validation and repository checks, inspect the final diff, and commit task-owned paths; record results in specs/008-release-packaging/verification.md.

## Dependencies and execution

T001 -> T002 -> T003-T006 -> T007-T010 -> T011 -> T012.
US1 is the first useful increment; deliver all stories in this task. References
T004/T005 could be drafted independently after T003. US2 analysis and US3 caller
inspection may proceed independently, but shared source edits and registry writes
stay with one owner. Research agents return evidence only. No parallel writes.
