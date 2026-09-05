# Feature specification: Homelab skill gaps

**Branch**: `feat/homelab-skill-gaps`
**Created**: 2026-09-05
**Status**: Accepted
**Input**: Audit skills against the homelab implementation and implement evidence-backed gaps without leaking sensitive information.

## User scenarios and testing

### US1: Maintain a stack contract, P1

A maintainer changes a Compose stack while keeping its configuration examples, preparation, metadata, ingress, and generated documentation consistent.

Independent test: a stack adds a required environment key and external volume. The workflow updates every affected source, preserves existing runtime configuration, and validates examples without deploying.

Acceptance: service env files and interpolation sources are distinguished, preparation side effects are identified before execution, generated output is refreshed through its owner, and optional or external stacks retain their documented lifecycle.

### US2: Diagnose without disclosing or changing runtime state, P1

An agent investigates a failed stack while respecting a repository prohibition on reading ignored live configuration.

Independent test: a helper called validation reloads monitoring and a missing bind path may be an absent remote mount. The agent declines those mutations during diagnosis and uses permitted metadata or public examples without reading runtime secrets.

Acceptance: neither raw resolved configuration nor unrestricted inspection/log output enters a shared report. Mount directories are not created to mask storage failure. Unavailable runtime evidence remains unproven.

## Requirements

- FR-001: Add a narrowly selected stack-maintenance workflow, separate from outage triage, image-only updates, backups, and exposure verification.
- FR-002: Derive recommendations only from committed source or explicitly permitted evidence. Never read ignored live configuration to fill a gap.
- FR-003: Maintain all affected source contracts and generated outputs together without copying private values.
- FR-004: Distinguish repository validation, preparation, and deployment. Inspect helper side effects and record skips accurately.
- FR-005: Preserve existing runtime state and shared storage, networks, volumes, and optional overrides.
- FR-006: Tighten triage evidence collection and preparation/mount boundaries without claiming live operational verification.
- FR-007: Connect maintenance with triage, exposure repair, and dependency transitions through conditional handoffs that retain the coordinator and current endpoint.
- FR-008: Keep canonical source, generated provenance, and declared client install targets consistent.

## Success criteria

All scenario decisions preserve runtime secrets and state. Each implemented gap cites a committed source contract. Existing skills retain their distinct selection boundaries. Repository checks pass or report an exact environmental limitation. No private values enter the skill or audit artifacts.

## Assumptions and scope

The homelab checkout is evidence, not an authorized deployment target. No live configuration, container operations, image pulls, monitoring reloads, or homelab edits are required. This task ends with committed skill changes, not external publication. Reuse existing backup, migration, network, and dependency skills where they already cover the requirement.
