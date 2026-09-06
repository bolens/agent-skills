# Implementation plan

Own the reusable Python runner and usage reference in `skills/audit-repo-fleet`.
Route structural comparisons from `improve-codebase-architecture` to that runner.
Keep inventory, runtime, and evidence in a private workspace directory. Read
repository-owned guidance when selecting scopes. Use snapshot Git indexes so
Sentrux sees selected untracked files without staging the original repository.

Pin Sentrux 0.5.7 Linux x86_64 and its release grammar archive by SHA-256. Verify
all extracted grammar bytes against a runtime manifest at each invocation.
Run inside Bubblewrap with an isolated home and network namespace. Store evidence
and metrics outside source. Comparison identity excludes changing revision/content
but includes source identity, scope, runner version, binary, and grammar hashes.

Constitution: canonical skill ownership and existing local provenance preserved.
No imported implementation or new skill. Linux-specific runner is documented.
Validate failure behavior with unit tests and real runtime fixtures, then run the
portable repository gate. Existing installed links stay with the canonical checkout.
