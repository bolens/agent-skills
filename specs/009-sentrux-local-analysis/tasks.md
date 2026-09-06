# Tasks

- [x] Inspect installed binary, source, release digests, and fleet inventory.
- [x] Prove allowed/forbidden import behavior in isolated runtime.
- [x] Implement snapshot runner and comparison identity.
- [x] Configure applicable fleet scopes and record exclusions.
- [x] Exercise real baselines/comparisons and runner failure behavior.
- [x] Validate repository gates and commit the reviewed implementation.

## Verification

Eight focused unit tests cover snapshot membership, unstaged preservation, context
inputs, symlink and size rejection, comparison identity, archive integrity, and
license retention. Six real runtime scenarios cover allowed/forbidden imports,
untracked code, unchanged comparison, baseline replacement, and scope mismatch.
The portable repository gate passes with local socket access for existing browser
fixtures. Linux x86_64 runtime only. No PR, release, CI gate, or runtime redistribution.

The private fleet trial inspected 42 non-archived inventory entries, selected 26
scopes, then deferred four with empty dependency graphs. Twenty-two remaining
scopes produced accepted baselines and successful unchanged comparisons. Those
results describe selected local source snapshots, not complete parse success or
up-to-date remote default branches. See the runtime audit for provenance limits.
