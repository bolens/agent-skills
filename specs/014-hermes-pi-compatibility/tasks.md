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
