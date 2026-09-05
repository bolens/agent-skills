# Utility family integration

Use `audio-utils`, `image-utils`, `video-utils`, and the user's archive utility repository as the preferred implementation owners when available. Resolve the actual checkout and project identity: the archive project may be named `archive-utils` or `archiving-utils`. Do not assume a fixed home path, rename a repository, or mistake a missing sibling for a missing dependency.

## Discover the current contract

Read the target's AGENTS/constitution, architecture, requirements, tool inventory/catalog, relevant format documentation, and test guidance. Inspect the selected tool's implementation and supported flags before use. These repositories can be under active construction: distinguish implemented and tested operations from catalog entries, generated wrappers, planned documentation, and unavailable backends. Report missing evidence rather than inventing a command or treating a stub's successful exit as conversion proof.

`audio-utils` is the quality reference for shared pipelines, thin tools, explicit preservation checks, recoverable batches, documentation, and functional fixtures. Its Bash plugin APIs, FLAC conventions, delete flags, and Make targets are not automatically the interface of its siblings. Preserve each repository's current runtime and contract rather than copying the audio implementation wholesale.

For catalog-driven siblings, keep reusable behavior in their shared engine and thin per-tool wrappers. Update the authoritative catalog and regenerate tools/docs/site using the repository's actual generation command. Do not hand-edit generated files or duplicate inventories inside this skill. Verify generated drift with the native check. If referenced docs or targets do not exist yet, inspect available code and report that development gap.

## Run or extend a tool

Prefer existing validated operations. If the requested capability is missing, distinguish using a documented lower-level fallback from implementing a new utility. A request to process files does not authorize silently building out several sibling repositories. When tool development is requested, extend the target's shared abstractions and behavioral tests rather than adding a parallel batch runner.

Honor dry-run, `--apply`, source-retention, collision, and exit-status semantics exactly as implemented and documented. Carry forward the user's authorization for writes, but do not infer source deletion from conversion approval. In repos that retain sources and disallow overwrites, do not bypass those guarantees through a lower-level encoder invocation. Preserve filename bytes through argument arrays and the repository's serialization convention; do not introduce shell evaluation or lossy path normalization.

Use disposable fixtures and isolated HOME/XDG state for tests. Verify read-only/dry-run behavior, corrupt input, unsupported capabilities, unusual paths, output collision, interrupted work, and validation failure when changing shared execution logic. Mocked backend tests can prove orchestration, but real codec/extractor fixtures are needed to prove media preservation. Report dependency skips and unsupported formats distinctly from passing checks.

For a cross-repository pipeline, identify each stage's owning tool, input/output identity, preservation contract, and validation result. Do not delete intermediates still needed for recovery, reuse completed-stage results after inputs change, or mark the whole pipeline successful when one stage skipped validation. Network fetches, metadata enrichment, and uploads are separate capabilities, not implicit parts of local conversion.
