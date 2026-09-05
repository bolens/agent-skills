# Feature Specification: Git hygiene for concurrent agents

**Feature Branch**: `feat/git-hygiene`
**Created**: 2026-09-05
**Status**: Accepted
**Input**: Make skills support proper Git hygiene for multiple concurrent agents across repository surfaces.

## User Scenarios & Testing

### User Story 1 - Preserve concurrent work (Priority: P1)

A coordinator assigns separate changes without agents overwriting or committing each other's work.

**Independent Test**: Walk through two writers sharing a checkout containing unrelated staged and unstaged changes.

**Acceptance Scenarios**:

1. Given independent tasks, when assigning writers, then each has an explicit owner, workspace, base revision, file scope, and handoff.
2. Given a shared checkout, when one agent needs a commit, then one designated writer controls staging and commits while others pause affected writes. Unrelated staged and unstaged changes survive.
3. Given overlapping shared files, when scheduling work, then ownership is reassigned or edits are serialized before either writer proceeds.

### User Story 2 - Integrate across surfaces (Priority: P2)

A coordinator combines tested changes across packages or repositories without confusing local success with integrated correctness.

**Independent Test**: Walk through a producer and consumer change with a shared generated artifact and separate repository histories.

**Acceptance Scenarios**:

1. Given dependent changes, when integrating, then immutable revisions and dependency order identify the combined state to validate.
2. Given separate repositories, when delivering, then each repository has its own status, commits, and checks, and incomplete delivery remains visible.
3. Given a completed worker, when cleaning up, then active work and unintegrated commits remain recoverable.

### Edge Cases

Unknown staged changes, unexpected HEAD movement, unavailable worktrees or agent tools, interrupted Git operations, busy index locks, shared lockfiles, generated files, and tests sharing ports or databases.

## Requirements

- **FR-001**: Provide a discoverable workflow for Git hygiene and concurrent repository writes, without claiming ordinary message writing or read-only review.
- **FR-002**: Preserve unrelated work and coordinate shared repository mutations through explicit ownership.
- **FR-003**: Separate independent writer workspaces by default, with a serialized fallback when isolation is unavailable.
- **FR-004**: Review the complete candidate commit and validate the integrated state before claiming completion.
- **FR-005**: Track dependencies, shared generated outputs, and delivery state across repository surfaces.
- **FR-006**: Preserve existing authorization for commits and external actions. Never infer publication or destructive cleanup permission from concurrency.
- **FR-007**: Register source provenance and install targets using existing repository conventions.

- **FR-008**: After a verified merge, babysit cleans up the completed feature branch and temporary local worktrees within existing authority, preserving active worktrees and any post-merge commits. Squash/rebase merges require host evidence rather than ancestry alone.

## Success Criteria

- **SC-001**: All preservation scenarios retain unrelated changes and assign exactly one owner to each shared write.
- **SC-002**: Every integration handoff identifies its repository, base, final revision or patch, checks, and dependencies.
- **SC-003**: Positive invocation selects this workflow, while commit-message-only and read-only review requests retain their existing workflows.
- **SC-004**: Repository validation passes, with installation limitations explicitly distinguished from content failures.

## Assumptions

This is guidance for agents, not a lock service or Git wrapper. Existing agent tools are optional. Creation of this skill does not authorize installing links or publishing changes.
