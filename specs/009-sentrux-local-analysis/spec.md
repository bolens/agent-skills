# Feature Specification: Local Sentrux analysis

**Feature Branch**: `feat/sentrux-local-analysis`
**Created**: 2026-09-06
**Status**: Implemented locally
**Input**: Implement the locally installed Sentrux across applicable fleet repositories.

## User scenarios and testing

### Scoped structural evidence (P1)
An operator selects a repository and code scope and obtains local structural
measurements without modifying source or contacting an external service.
Acceptance: include selected tracked and non-ignored untracked code, preserve
working-tree changes, reject missing grammars and oversized inputs, and record
revision, content hashes, selected files, scope, and parser identity.

### Comparable sessions (P2)
An operator saves a baseline before a change and compares afterward.
Acceptance: refuse an existing baseline destination, reject a changed scope,
repository, binary, or parser identity, and retain the original evidence.

### Selective fleet use (P2)
An operator maintains a private list of repositories and scope profiles.
Acceptance: classify unsupported primary languages and configuration-only
repositories explicitly. Partial scans never claim whole-product coverage.

## Requirements

- FR-001: Use an explicitly installed binary and independently verified grammar archive.
- FR-002: Disable networking and isolate application state during scans on Linux x86_64.
- FR-003: Do not install required CI gates or launch persistent MCP/GUI services.
- FR-004: Preserve native correctness checks and treat scores as investigation leads.
- FR-005: Fail closed for empty, oversized, unsupported, or incompatible selected inputs.
- FR-006: Keep private paths, source snapshots, and fleet identities out of public commits.

## Success criteria

Real allowed/forbidden fixtures return success/failure respectively. An unchanged
comparison passes. New untracked code appears in the manifest. Runtime and scope
mismatches fail before analysis. Every inventoried repository has a disposition.

## Assumptions

Local use is the authorized endpoint. Linux x86_64 with Python 3.10+, Git and
Bubblewrap is the implemented runner platform. Other platforms retain native
Sentrux usage subject to equivalent verification. Parser success is not semantic
completeness. Native application tests remain authoritative.
