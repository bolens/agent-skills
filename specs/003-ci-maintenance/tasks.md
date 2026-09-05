# Tasks: CI maintenance

- [x] T001 Record baseline evidence and boundaries in specs/003-ci-maintenance/research.md.
- [x] T002 [US1] Write skills/ci-maintenance/SKILL.md and register generated provenance.
- [x] T003 [US2] Add skills/ci-maintenance/references/github-actions.md for trust and gate contracts.
- [x] T004 [US3] Add conditional CI routing in skills/audit-repo-fleet/SKILL.md, skills/setup-pre-commit/SKILL.md, skills/babysit/SKILL.md, and skills/triage-dependency-updates/SKILL.md.
- [x] T005 Validate specs/003-ci-maintenance/quickstart.md scenarios, privacy, repository checks, and installed links.
- [x] T006 Update README.md and CHANGELOG.md, review the diff, and commit task-owned changes.

Dependencies: T001 before writing; T002 and T003 establish the target before T004; T005 before T006. Implement serially. An independent evaluator may run alongside local checks. US1 tests baseline reuse, US2 tests event/trust boundaries, and US3 tests shared-consumer coverage.
