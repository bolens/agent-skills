# Feature Specification: Recent code contracts

**Feature Branch**: `feat/recent-code-contracts`
**Created**: 2026-09-08
**Status**: Implemented and verified
**Input**: "check for new code surfaces that need spec defined and fully tested and do it"

This explicitly requested retrospective assesses `72ec45220597b16a38e2ee842821f4af96b36518`, with prospective fixes for discovered failures. The inventory compares the retained legacy extension at `fbf0826` with this revision and preserves earlier feature history.

## User Scenarios & Testing

### User Story 1 - Trust the integration check (Priority: P1)

A maintainer checks the local Spec Kit integration before using or updating it. Success means recorded content is intact and existing core files are recorded.

**Why this priority**: A false success can hide damaged workflow instructions.
**Independent Test**: Check disposable integrations with intact, changed, missing, malformed, and unrecorded content. Verify status, diagnostics, and unchanged input bytes.

**Acceptance Scenarios**:

1. **Given** an intact integration, **When** checked, **Then** it succeeds without modifying content or local planning guidance.
2. **Given** changed or unavailable content, **When** checked, **Then** it fails with the affected path and still reports independent problems.
3. **Given** an existing core file omitted from its manifest, **When** checked, **Then** it fails while allowing project-owned overrides.
4. **Given** invalid metadata or a special file, **When** checked, **Then** it fails without a traceback, blocking read, or successful verdict.

### User Story 2 - Know whether container setup is ready (Priority: P1)

A developer opens the editor container or reruns setup. Readiness requires a usable mounted checkout and required tools.

**Why this priority**: Setup success should let a developer start the documented repository checks.
**Independent Test**: Run both setup entrypoints in disposable checkouts with controlled tools and real Git, then exercise the actual container image.

**Acceptance Scenarios**:

1. **Given** a writable checkout and supported tools, **When** either entrypoint runs from another directory, **Then** it finds its own checkout and succeeds.
2. **Given** a missing required tool or unsupported runtime, **When** setup runs, **Then** it fails with a useful diagnostic and no readiness message.
3. **Given** a read-only checkout, missing Git metadata, or a directory merely nested inside another repository, **When** setup runs, **Then** it fails.
4. **Given** existing source and private runtime files, **When** setup runs repeatedly, **Then** their bytes remain unchanged and no dependency installation or host-service action occurs.

### Edge Cases

Wrong integration identity, invalid JSON/encoding/field types, malformed digests, traversal and noncanonical paths, symlink files and parents, directories, named pipes, simultaneous failures, spaces in checkout paths, failed Git, read-only roots, missing tools, and wrong Node major.

## Requirements

### Functional Requirements

- **FR-001**: Check both required manifests and every recorded file. Reject missing or malformed metadata, mismatched integration names, invalid digests and paths, and changed bytes.
- **FR-002**: Require existing core templates, Bash helpers, and generated Spec Kit entrypoints in their owning manifest. Keep project-owned memory, nested overrides, and unrelated skills independent.
- **FR-003**: Reject symlinks and non-regular files before reading manifests or content. Convert expected read failures into path-specific diagnostics. A static named pipe must fail within five seconds.
- **FR-004**: Return success only without findings, aggregate independent findings, and preserve all input content on success and failure.
- **FR-005**: Setup must require a writable repository root belonging to its mounted checkout, resolve it independently of the caller's directory, and propagate failure through the post-create wrapper.
- **FR-006**: Setup must verify every tool in its readiness contract, including the repository check runner, and reject an unsupported Node major with an actionable diagnostic.
- **FR-007**: Setup must be repeatable and observation-only. Do not install dependencies, overwrite runtime values, start services, or repoint installed links.
- **FR-008**: Every added executable surface in the dated inventory must have an owning contract and executable success/failure evidence. Distinguish controlled fixtures, actual container execution, and unexecuted platforms.

### Key Entities

- **Integration manifest**: Integration identity and recorded path/content hashes.
- **Managed surface**: Content governed by recorded hashes and core inventory.
- **Setup readiness result**: Checkout, tool, and runtime verdict, separate from a test-suite verdict.
- **Evidence record**: Source revision, requirement, executed check, result, and limits.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every acceptance scenario has a passing automated case and named evidence location.
- **SC-002**: All controlled damaged-input cases fail with a diagnostic and no successful verdict. Named pipes fail within five seconds.
- **SC-003**: Repeated setup and checks preserve fixture source and runtime-file bytes.
- **SC-004**: Every added executable surface since the comparison revision has a contract, with container build/runtime evidence separate from fixture results.

## Assumptions

The comparison covers changes since the retained legacy extension, not every unchanged helper. Integrity is relative to recorded manifests, not upstream authenticity. Removing both a file and its entry requires review. Concurrent adversarial filesystem replacement is outside this local maintenance check. The devcontainer targets its declared Linux image and Node 26. Other native and Nix workflows retain their contracts. Host link repair, publication, upstream imports, and live services are excluded.
