# Tasks: Recent code contracts

## Phase 1: Setup

- [x] T001 Inventory additions since fbf0826 and record scope in specs/013-recent-code-contracts/research.md.
- [x] T002 Define scenarios, design, and quality checklist in specs/013-recent-code-contracts/spec.md and plan.md.

## Phase 2: Foundation

- [x] T003 Verify existing unittest discovery and ignored build state in Makefile and .gitignore.

## Phase 3: US1 integration verdict

Independent check: tests/test_speckit.py must distinguish intended error classes and preserve fixture content.

- [x] T004 [US1] Strengthen invalid-input assertions and add missing failure cases in tests/test_speckit.py.
- [x] T005 [US1] Run the complete checker contract and repair reproduced defects in scripts/check-speckit.py if needed.

## Phase 4: US2 setup verdict

Independent check: tests/test_devcontainer_setup.py must exercise both entrypoints, checkout identity, tool failures, and preservation.

- [x] T006 [US2] Add shell/Git readiness fixtures in tests/test_devcontainer_setup.py and observe failures before repair.
- [x] T007 [US2] Fix reproduced readiness defects in .devcontainer/smoke.sh and correct .devcontainer/README.md and post-create.sh descriptions.
- [x] T008 [US2] Build the declared image and exercise repeated setup plus the portable gate in a disposable checkout; record results in specs/013-recent-code-contracts/verification.md.

## Phase 5: Completion

- [x] T009 Run focused lint and make check; map each requirement to evidence in specs/013-recent-code-contracts/verification.md.
- [x] T010 Add the feature to specs/README.md, review task-owned diffs, and commit.

## Dependencies and execution

T001-T003 precede both stories. T004 precedes T005. T006 precedes T007 and T008. Both stories precede T009-T010. The story tests touch separate files and could run independently, but this implementation is sequential. Deliver US1 first as the smallest independently verifiable increment, then US2 and combined evidence.
