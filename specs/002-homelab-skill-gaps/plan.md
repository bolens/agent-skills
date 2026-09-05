# Implementation plan: Homelab skill gaps

Branch: `feat/homelab-skill-gaps` | Date: 2026-09-05 | [Spec](spec.md)

## Summary

Add homelab-stack-maintenance for repository contract edits. Tighten existing homelab-stack-triage where the source audit demonstrated unsafe evidence and helper assumptions. Keep environment rendering detail in one maintenance reference.

## Technical context

Markdown guidance, generated JSON provenance, existing Python validators. No new executable or live Docker dependency. Use tracked-source inspection and synthetic decision scenarios, plus existing repository checks. Git and Docker documentation support CLI semantics.

## Constitution check

Before and after design: source stays under skills/, local-original provenance uses the existing generator, no upstream content is imported or changed, commands name optional tools honestly, and existing Make gates remain authoritative. No changes to the audited homelab checkout. New client links use the managed installer when authorized.

## Ownership and structure

- skills/homelab-stack-maintenance/SKILL.md: US1 contract workflow and routing.
- skills/homelab-stack-maintenance/references/example-validation.md: secret-free example validation and helper classification.
- skills/homelab-stack-maintenance/UPSTREAM.md and PROVENANCE.json: generated local origin and client targets.
- skills/homelab-stack-triage/SKILL.md: US2 evidence, helper, and mount boundaries.
- skills/network-exposure-verification/SKILL.md and skills/triage-dependency-updates/SKILL.md: conditional return to maintenance for changed stack contracts.
- README.md and CHANGELOG.md: discovery and behavior changes.
- specs/002-homelab-skill-gaps/: source audit, scenarios, contract, and evidence.

## Delivery strategy

Commit the new maintenance capability with its provenance and documentation, then the triage corrections in a separate focused commit. Run make check-fast during implementation and make check before completion. No push or merge is inferred from the previous completed task.
