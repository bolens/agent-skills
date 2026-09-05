# Feature specification: CI maintenance

**Branch**: `feat/ci-maintenance`
**Created**: 2026-09-05
**Status**: Accepted
**Input**: Add or improve CI guidance to implement changes against the fleet's current standards and implementations, with applicable best practices.

## User scenarios and testing

### US1: Implement repository CI, P1

A maintainer adds or improves CI using the project's existing checks and applicable shared standards.

Independent test: a mixed repository needs workflow lint/security and build/test checks. The agent identifies the native targets, inspects the selected shared workflow interface at its pinned revision, and implements compatible checks without copying unrelated jobs.

Acceptance: tool versions and runtimes are verified rather than hardcoded from this skill, local and CI checks share commands, and syntax validation is separated from actual workflow execution evidence.

### US2: Preserve trust and merge gates, P1

A maintainer changes events, permissions, or reusable jobs without exposing privileged execution to untrusted code or preventing required checks from reporting.

Independent test: a fork PR, filtered docs-only change, and optional merge queue exercise the event/check contract. The agent identifies which checks execute, which revisions they test, and which privileged operations must be isolated.

Acceptance: untrusted code cannot inherit publish credentials, reusable inputs and permissions remain compatible, required check names and event coverage are preserved, and missing remote evidence is reported.

### US3: Carry shared CI fixes through the fleet, P2

A shared workflow change reaches applicable consumers while respecting per-repository contracts.

Independent test: two consumers pin different revisions and one uses another runtime. The agent checks applicability, fixes the owning shared source, validates representative callers, and tracks remaining consumers without assuming text matches mean compatibility.

## Requirements

- FR-001: Add narrowly discoverable CI design/implementation guidance. Keep commit-time hooks, symptom diagnosis, dependency selection, and PR delivery in their existing workflows.
- FR-002: Separate repository policy, shared workflow contracts, observed examples, and current platform documentation. Resolve conflicts by authority and actual applicability, not majority use.
- FR-003: Preserve event, trust, permission, required-check, runtime, artifact, and reusable-interface contracts.
- FR-004: Reuse native validation and current verified immutable dependency identities. Do not hardcode a fleet tool roster into every repository.
- FR-005: Validate static configuration, relevant local behavior, and available host evidence separately, with explicit skips.
- FR-006: Use conditional handoffs with a single coordinator and existing authority. Fleet implementation checks maintained peers for applicable shared fixes.
- FR-007: Keep secrets, private runner topology, and credential values out of source and evidence.
- FR-008: Register and validate the new skill using existing provenance and installation conventions.

## Success criteria

Each scenario identifies the applicable checks, trust boundary, and validation limit. Ordinary hook-only work and isolated CI failure diagnosis retain their own workflows. Public artifacts contain no private values. Skill and repository validation pass, and any untested remote behavior remains explicit.

## Assumptions

GitHub Actions is the observed primary platform. Other CI providers use their own documented semantics. This task creates skill guidance, not a fleet-wide CI rollout or repository-settings change. No production job is dispatched for evaluation.
