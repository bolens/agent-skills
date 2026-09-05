# Tasks: Homelab skill gaps

## Setup

- [x] T001 Record committed-source audit and selection decisions in specs/002-homelab-skill-gaps/research.md.

## US1: Stack maintenance

- [x] T002 Write skills/homelab-stack-maintenance/SKILL.md and references/example-validation.md.
- [x] T003 Generate PROVENANCE.json and skills/homelab-stack-maintenance/UPSTREAM.md and update README.md discovery.

## US2: Private incident evidence

- [x] T004 Tighten skills/homelab-stack-triage/SKILL.md and add conditional handoffs in skills/network-exposure-verification/SKILL.md and skills/triage-dependency-updates/SKILL.md.

## Verification and completion

- [x] T005 Evaluate specs/002-homelab-skill-gaps/quickstart.md scenarios and record checks and privacy results there.
- [x] T006 Review diffs, update CHANGELOG.md, and commit task-owned changes.

Dependencies: T001 precedes T002 and T004. T003 follows T002. T005 follows all edits and precedes T006. US1 can be validated by the stack-contract scenarios, US2 by the secret and mutation scenarios. Implementation is serial because the work is short. An independent scenario evaluation can run alongside local checks when available.
