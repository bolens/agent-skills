# Specification index

Original feature records describe work planned before implementation. The
retrospective baseline was added on explicit user request on 2026-09-05 and
identifies existing behavior, source coverage, and verification limits.

| Record | Scope |
| --- | --- |
| [001 Git hygiene](001-git-hygiene/spec.md) | Ownership, isolation, integration, and cleanup |
| [002 Homelab skill gaps](002-homelab-skill-gaps/spec.md) | Coordinated stack-definition maintenance |
| [003 CI maintenance](003-ci-maintenance/spec.md) | Reusable pipeline, trust, and validation contracts |
| [004 Bounded context](004-bounded-context/spec.md) | Source excerpts, handoffs, and durable corrections |
| [005 Fleet evidence](005-fleet-evidence/spec.md) | Bounded checks tied to repository revisions |
| [006 Retrospective baseline](006-retrospective-baseline/spec.md) | Collection coverage and completion assessment at `8e51a4f` |

The retrospective baseline contains contracts for
[maintenance](006-retrospective-baseline/contracts/maintenance.md),
[engineering](006-retrospective-baseline/contracts/engineering.md),
[web and visuals](006-retrospective-baseline/contracts/web-visual.md), and
[system operations](006-retrospective-baseline/contracts/systems.md).
Use its [coverage map](006-retrospective-baseline/coverage.md) to locate each
registered skill and its [assessment](006-retrospective-baseline/assessment.md)
to distinguish completed adaptations from deferred tools and unverified hosts.

Preserve original history. New capabilities need their own prospective contract
or an explicit amendment. Ordinary prose maintenance remains in the normal
workflow. A spec, a checked task, and a passing static test are different evidence.

- [Development environments](007-development-environments/spec.md): [plan](007-development-environments/plan.md),
  [tasks and delivery evidence](007-development-environments/tasks.md).
