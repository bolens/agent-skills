# Agent-history suggestions assessment

Assessed on 2026-09-06 against agent-skills base
`ab05a515d6fa5f6a8a7ed5295c6209bacea3f0d0` and the shared fleet policy base
`c38a2f6`. The implementation is a focused inventory fix and prose maintenance.

## Source and decisions

The user supplied this [suggestions image](https://pbs.twimg.com/media/HRe1Lx9aIAALrNj?format=jpg&name=medium)
and its [tweet](https://x.com/EXM7777/status/2096343368121164050).
The image was downloaded and visually inspected. The tweet returned HTTP 403,
so its surrounding text and replies were not assessed.

The image proposes reviewing agent history with evidence limits, sampling,
counterexamples, privacy controls, interviews, and measured process experiments.
Adopt the distinction between claims and observations, independent events,
explicit gaps, and reassessment of improvements. These strengthen the existing
fleet comparison workflow. Preserve the archive-scope and redaction boundary if
conversation analysis is later requested.

Do not import the personal interview workflow into repository maintenance.
Fixed session counts and 30-day experiments do not establish causality or suit
every repository. The image's extra approval steps do not override this user's
authorization to implement improvements. No conversation archives were read,
personal patterns inferred, scheduler enabled, or new history-analysis skill added.
These are selective conceptual adaptations, not a copied prompt or upstream import.

## Confirmed defect and repair

`inventory.sh` discarded failures from both Git status and discovery. A failed
status therefore produced zero changes, and invalid `.git` markers or bare
storage could appear as clean checkouts. The workspace scan demonstrated the
problem without relying on an agent's earlier completion claim.

The fix preserves successful TSV rows, reports failed status counts as `unknown`,
returns failure for incomplete discovery or invalid repository markers, and
identifies bare-storage exclusions on stderr. It retains the existing columns
and read-only behavior. Consumers must keep stderr and exit status with stdout.
Discovery still requires a `.git` marker within the selected depth. It does not
deduplicate worktrees, establish maintenance ownership, or refresh remote refs.

The comparison reference now distinguishes multiple records of one event from
recurrence, asks for counterevidence, and ties process changes to an observed
baseline and reassessment point. The shared `.github/RELEASING.md` applies that
rule at the existing fleet policy boundary without copying new policy into every
application repository.

## Fleet applicability and outcome

The retained maintenance inventory contained 42 repository entries. Tracked-source
searches covered 39 available references for copies of the selected inventory
logic and shared execution-evidence policy. Only agent-skills and `.github`
contained those sources. Three entries lacked retained checkouts and remain
uninspected. These results establish applicability for this fix, not general
fleet health. Only the two changed repositories' main refs were freshly fetched.
Per-repository paths, revisions, and search results remain in private task evidence.

At scan depth 2, the original workspace inventory emitted 31 data rows. The
corrected run emitted 27, explicitly excluded three bare-storage locations,
reported one invalid marker, and exited 1. The unavailable observation is now
visible rather than counted as a healthy repository. The next comparable fleet
audit should retain those exclusions and confirm that unavailable observations
never become zero-change claims. Changes in scan scope require a new comparison.

## Validation

- Three regression cases failed against the original helper and passed with the
  fix: invalid marker, corrupted index, and bare storage with a linked worktree.
- A fourth case verifies that partial discovery returns failure while preserving
  readable repositories.
- `make check-fast test portability` passed with 63 tests. The first sandboxed
  run failed because existing responsive-capture tests could not open local
  sockets. The rerun outside that restriction passed, including shell lint.
- Shared policy validation passed 17 tests, actionlint, and offline zizmor with
  no findings under its configured policy.
- The instruction walkthrough keeps a repeated audit in the existing comparison
  workflow. Multiple records of one fix cannot establish recurrence. A request
  merely to assess an external prompt does not trigger archive collection.

The changed worktrees do not own installed skill links. No installation, remote
CI, publication, or future productivity benefit is claimed by these local checks.
