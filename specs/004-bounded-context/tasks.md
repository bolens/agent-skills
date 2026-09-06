# Tasks

- [x] Implement bounded local source reads and behavior tests.
- [x] Add shared handoff and durable-context guidance.
- [x] Roll narrow guidance across 31 available maintained repositories in isolated worktrees.
- [x] Run portable validation and inspect consumer diffs and memory links.
- [x] Record evidence and local delivery limits below.

## Validation evidence

The portable gate `make check-fast test portability` passed: 61 skills validated,
38 tests passed including eight reader cases, and portability passed with
ShellCheck available. The initial sandbox run could not open loopback sockets
for existing capture tests; the permitted rerun passed. Targeted Ruff E9/F checks
and the skill creator validator passed. All 31 consumer worktrees passed the
shared Spec Kit 1.0.3 validator and whitespace checks. Their existing guidance
was compared with each base and preserved, and every project-guide link resolves.

A real source excerpt returned the requested lines and next unread line. Source
walkthroughs checked that a survey returns evidence, an edit requires direct
source, and unavailable or unauthorized delegation falls back to local reads.
No model-routing experiment, scheduled run, token benchmark, or live operation
was performed. Installed links still point to the existing canonical checkout.
This change is prepared in local feature worktrees, with no push or merge.
