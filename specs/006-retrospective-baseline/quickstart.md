# Validate the retrospective baseline

Run from the canonical repository with Python 3.10+, Node, Bash, Make, and
ShellCheck. This procedure performs no external-model request or live-system
mutation. The existing test fixtures need permission to open loopback sockets.

1. Compare the skill rows in `coverage.md` with `PROVENANCE.json`. Require one row
   per registered name, no duplicates or extras, resolving canonical entrypoints,
   and an existing requirement ID or feature spec in every primary-owner link.
2. Check local Markdown destinations in this feature and `specs/README.md`,
   including contract and source links. URLs and same-page anchors require
   separate checks and are not proof of external availability.
3. Read `assessment.md` beside the nine baseline audits and pstack follow-up and named source files.
   Confirm that implemented means the adopted local behavior exists, and does
   not mean that an upstream runtime, benchmark, or host report was executed.
4. Run the domain contracts' scenarios as source walkthroughs. A new application
   implementation would need actual behavior tests in its own environment.
5. Discover the selected feature and run the repository gates:

```sh
.specify/scripts/bash/check-prerequisites.sh --json --require-spec --require-tasks --include-tasks
make check-fast
make check
```

For another selected feature, use `SPECIFY_FEATURE_DIRECTORY=specs/006-retrospective-baseline`
with the prerequisite command. Feature selection is local workflow state and
must not be mistaken for the current Git branch.

Existing Archify runtime code is unchanged. Its full fetched native/browser
suite remains the separate `make test-archify` gate described in RELEASING.md.
A small bundled CLI smoke check can establish availability but does not replace
that suite. No host health collector, backup restore, firewall change, Claude
report, Netviz application, or Sentrux process is required by this retrofit.

Record current results and manual limitations in tasks.md. Do not copy historical
check counts as evidence for this revision.
