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
