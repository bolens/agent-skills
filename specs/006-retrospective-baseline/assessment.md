# Implementation completeness assessment

Assessed 2026-09-05 from baseline `8e51a4f` and current canonical source. This is
a scoped source/contract assessment, not a new full audit of upstream applications.

## Accepted source-audit work

All nine adoption records have corresponding local guidance. No accepted runtime
installation was found half-complete. Source locations below are relative to
`skills/`; each audit retains exact upstream identity and historical evidence.

| Audit | Implemented source and behavior | Deliberate exclusion or verification limit |
| --- | --- | --- |
| [Ponytail](../../docs/audits/2026-09-05-ponytail.md) | `codebase-design/SKILL.md`, `DEEPENING.md`, and `improve-codebase-architecture/SKILL.md`: concrete replacements, retained behavior, revisit conditions. E-001. | No mode hooks, scoreboard, prompt server, or claimed benchmark savings. |
| [Loops and graphs](../../docs/audits/2026-09-05-loops-and-graphs.md) | `git-hygiene/references/work-units.md` and `verify-and-stop/SKILL.md`: owned units, dependency waits, evidence-led correction, bounded verification. M-003, E-002. | No new orchestration framework or automatic extra agents. |
| [Obscura](../../docs/audits/2026-09-05-obscura.md) | `cli-web-evidence/SKILL.md` and `responsive-web-capture/SKILL.md`: verify backend capabilities and actual artifacts. W-003. | Obscura engine not installed; protocol compatibility is not browser equivalence. |
| [Codex Security](../../docs/audits/2026-09-05-codex-security.md) | `web-security/references/finding-assessment.md`, its entrypoint, and `code-review/SKILL.md`: claim disposition, boundary proof, consequence versus confidence. E-004. | No autonomous scanner installed; SDK and some upstream skill-body inspection were partial and remain labeled. |
| [Skill Doctor](../../docs/audits/2026-09-05-skill-doctor.md) | `find-skills/references/usage-and-context.md` and CONTRIBUTING.md: separate installed, discoverable, and observed-use evidence. M-002. | Live report remains unexecuted after automatic approval review rejected possible context transfer. No new call attempted in this retrofit. |
| [Paul Solt workflows](../../docs/audits/2026-09-05-paul-solt-workflows.md) | `systematic-debugging/SKILL.md` and `ci-maintenance/references/github-actions.md`: process status, retained diagnostics, tested build/command identity. E-003, M-003. | No Xcode/Swift workflow or remote builder installed. |
| [Memory engineering](../../docs/audits/2026-09-05-memory-engineering.md) | `audit-repo-fleet/SKILL.md` and `find-skills/SKILL.md`: compare revision-bound evidence and reassess prior verdicts. M-002, M-003. | No memory service, transcript store, or pruning loop installed. |
| [Wide events](../../docs/audits/2026-09-05-wide-events.md) | `systematic-debugging/references/wide-events.md`: operation-local fields, preserved errors, pre-buffer sensitive-data exclusion, sentinel-test expectations. E-003. | This collection supplies guidance, not an application logger. Runtime leak tests belong to future instrumented applications. |
| [Netviz and Sentrux](../../docs/audits/2026-09-05-netviz-sentrux.md) | `web-animation/references/playback-clocks.md` and `improve-codebase-architecture/references/structural-evidence.md`: clock continuity and comparable dependency evidence. W-004, E-001. | Both applications remain deferred. Archify handles generated network and system diagrams. Netviz's distinct possible role is manual editing. |

## Demonstrated implementation gap

`blast-radius/SKILL.md` referred to `how`, `why`, and `arena` procedures absent
from the registered collection and the available skill catalog. Its purpose was
implemented, but history inspection and broad-review steps depended on those
unprovided companions.

T012 repairs that adaptation: direct Git history and available PR context,
code-review scope, optional permitted independent inspection, and an explicit
local fallback. The real-code proof requirement remains. A manual scenario with
no PR access or delegation still produces source-backed findings and labels
unproven assumptions. No upstream import, provenance change, or live execution
is needed for the instruction repair. The follow-up original-source audit found
that its local-origin label was incorrect and repairs provenance separately.

## Follow-up original-source audit

The user then requested verification of the original companion implementations.
The [pstack audit](../../docs/audits/2026-09-05-pstack-companions.md) corrects the
earlier overlap judgment: why provides a distinct cross-source rationale procedure,
and arena generates and combines competing artifacts. Neither is fully reproduced
by ordinary code review. Their wholesale adoption remains deferred, with why the
stronger selective-adaptation candidate. This is an audited decision, not a partial
implementation of a newly accepted feature.

The same audit proves blast-radius's pstack origin by exact baseline comparison.
T014 corrects provenance and retains the original MIT license, preserving current
invocation policy and local adaptations.

## Original feature records

Specs 001-004 have completed task lists and their named owning files exist.
Their detailed historical evidence remains unchanged. Current source retains
Git ownership/cleanup, homelab stack consistency, CI trust/gates, and the bounded
reader/handoff implementation. Current repository tests exercise the reader,
installation, and relevant helper contracts. This review does not independently
revalidate past claims about every fleet consumer or prior host merge.

## Limits and disposition

The missing specification/traceability layer is completed by this feature's
domain contracts and coverage map. The identified local skill adaptation is
repaired by T012. No other partial implementation was demonstrated in the
reviewed requirements and recent adopted guidance. This is not a statement that
every line in all 61 skills or every bundled dependency has been exhaustively
audited. In particular, no full Archify suite, external browser deployment,
workstation operation, restore, or upstream Sentrux/Netviz application was run.

The Skill Doctor report is an external verification limit, not a missing local
implementation. The earlier approval rejection remains documented in its audit.
Revisit it only with explicit authority for the external context transfer.

Current executed checks and manual scenario results are recorded in
[tasks.md](tasks.md). Completion of this retrofit does not authorize publication.
