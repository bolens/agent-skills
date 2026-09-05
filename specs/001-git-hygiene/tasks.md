# Tasks: Git hygiene

## Setup and foundation

- [x] T001 Confirm existing coverage and record design in specs/001-git-hygiene/research.md.

## US1: Preserve concurrent work

- [x] T002 [US1] Write ownership, isolation, and staging guidance in skills/git-hygiene/SKILL.md.
- [x] T003 [US1] Register skills/git-hygiene/UPSTREAM.md and PROVENANCE.json and add README.md discovery and conflict-resolution routing.

Independent check: unrelated staged changes survive the shared-checkout scenario.

## US2: Integrate and clean up

- [x] T004 [US2] Add cross-surface integration and cleanup guidance to skills/git-hygiene/SKILL.md.
- [ ] T005 [US2] Add verified post-merge cleanup to skills/babysit/SKILL.md and skills/git-hygiene/references/branch-cleanup.md.

Independent check: squash merge, advanced branch, active worktree, and separate repository scenarios preserve unfinished work.

## Validation and delivery

- [x] T006 Evaluate specs/001-git-hygiene/quickstart.md scenarios, run repository checks, and record evidence there.
- [ ] T007 Review task diffs, update CHANGELOG.md, and commit only task-owned changes.

## Dependencies and execution

T001 precedes writing. T002 and T004 share one file and run serially. T003 depends on that skill. T005 follows its ownership contract. T006 precedes T007. No parallel workers are needed for these short instruction edits. The MVP is US1, followed by integration and cleanup. All seven tasks have paths and evidence.
