# Tasks and evidence

- [x] Inspect primary client docs and pinned loaders for discovery and invocation.
- [x] Implement optional targets and preserve explicit invocation policy.
- [x] Verify isolated installs, overrides, repeated apply, conflicts, and references.
- [x] Run repository checks and record runtime coverage limits.

Verification: all 159 repository tests, portability, installed links, fast metadata
checks, and Ruff checks for changed Python files passed. Five new installer tests
exercise isolated homes and policy parity. Applied and checked 58 Hermes and 65 Pi
links on this host. Neither agent executable was installed, so live client catalog
and model-driven execution were not tested. The compatibility guide records the
pinned upstream loader evidence and follow-up checks.

## Follow-through verification

- [x] Added bounded catalog checks and preflight planning without deleting independent skills.
- [x] Exercised Pi 0.73.1 native loader and Hermes b2aa855 native traversal in disposable profiles.
- [x] Verified Pi prompt policy, symlink deduplication, catalog membership, and filesystem resource access.
- [x] Documented OpenCode, Gemini CLI, and Copilot CLI discovery and policy boundaries.
- [x] Removed host-specific discovery/reload assumptions and documented the independent compression backend.

All 166 repository tests passed, including 12 focused installer/harness tests.
Fast metadata, portability, installed catalogs, and shared source lint passed.
The final opt-in native-loader target passed and removed its temporary profiles
and dependencies. No model sessions or client permission-gated reads were tested.
The full Pi package was inspected but excluded from the retained dependency graph;
the fixture fetches only integrity-verified loader modules plus two locked parsers.
No global client runtime was installed.

## Coordination amendment evidence

- [x] Normalize empty/relative profile inputs and reject aliased or nested catalogs.
- [x] Add JSON receipts, partial failure recovery, and cross-process catalog locks.
- [x] Share bounded YAML parsing across generator, validator, and catalog audit.
- [x] Declare actual runtime requirements and run pinned loaders in CI.
- [x] Clarify attempt identity, cancellation ownership, uncertain retries, and host browser capacity.

The 170-test repository gate, all installed client catalogs, pinned native loader
checks, Ruff and actionlint passed before the final partial-I/O regression was
added. Final verification is recorded below. Native model sessions, Windows apply,
and hosted CI execution remain outside the executed evidence.

Final gate: all 171 tests passed in 55.375 seconds, including partial-install
receipts and successful retry after a simulated disk failure. Metadata/provenance,
portability, installed links, and shared source lint passed. Pinned Pi/Hermes
loaders and the all-client JSON check passed. Actionlint accepted the CI change.

The related privacy-path fix installs a shared POSIX browser guard across eight
entrypoints. Three supervisor tests, TypeScript, guard Oxlint, and Python lint
passed. Its real main entrypoint refused a held lock before browser launch, and
one short Chromium cancellation probe confirmed worker and detached-browser exit.
That checkout's concurrent uncommitted application work was preserved. No full
browser matrix, hosted CI run, or production/browser-user session was started.
