---
name: audit-repo-fleet
description: Audit and maintain a directory containing multiple Git repositories by inventorying worktree state, branches, local upstream divergence, governance files, toolchains, CI, validation entry points, and maintenance risk. Use when the user asks for repository fleet health, cross-repo maintenance, stale or inconsistent repos, spec-kit/AGENTS drift, release readiness, or what to work on next across many repositories.
---

# Audit a Repository Fleet

Default to a read-only audit. Treat each repository's constitution, `AGENTS.md`, contributor docs, manifests, and native task runner as authoritative for that repository.

## Inventory

Run `scripts/inventory.sh <workspace-root>` to collect deterministic local facts. The script does not fetch, install, test, or modify repositories; divergence is relative to existing local remote-tracking refs and may be stale.

Supplement the inventory only where it changes prioritization:

- inspect dirty diffs without overwriting or attributing them
- identify canonical check, generation, release, and security commands
- compare `AGENTS.md` against the constitution for duplication or contradiction
- locate dependency automation, action pinning, generated-file contracts, and release metadata
- distinguish archived/vendor mirrors from actively maintained repositories
- inspect nested repositories or unusual worktree layouts separately when they fall outside the bounded inventory scan

Never fetch every remote or run every repository's full suite merely to make the report look complete. Ask before network-heavy or long-running fleet operations.

## Prioritize

Rank evidence-backed work into:

1. **Protect now** — secret exposure, destructive defaults, broken required CI, unsafe dependencies, corrupted generation contracts
2. **Unblock** — failing builds/tests, incompatible toolchain pins, unresolved migrations, broken release paths
3. **Prevent drift** — missing governance, stale generated artifacts, inconsistent automation, unowned update surfaces
4. **Improve later** — maintainability or documentation improvements without current failure evidence

For each recommendation include repository, evidence, impact, safe next action, validation, and whether external or destructive authorization is required. Do not equate age, churn, or a dirty worktree with a defect.

## Act only when requested

If the user asks to implement maintenance, work one risk-coherent batch at a time. Re-read that repository's guidance, preserve unrelated changes, run focused validation, and report exact results. Do not stage, commit, push, publish, deploy, update live services, or bulk-upgrade dependencies unless explicitly authorized.

For releases, audit version sources, generated artifacts, changelog/release notes, packaging, CI, signing, and rollback. When changelog quality or edits are in scope, use the changelog-maintainer skill for reader-facing history and generator checks. A readiness request authorizes reporting, not publishing.

Before making a repository public or publishing an artifact, use `sensitive-info-audit` across the exact publication boundary and committed history. Treat unresolved high-confidence secret findings as **Protect now** blockers.

When the fleet includes externally sourced hard-forked skills, use `sync-skill-upstreams` to check exact audited refs and preserve documented local changes during imports.

When an Omarchy plugin fleet is being prepared for marketplace submission, verification, or update approval, use `audit-omarchy-plugin` for each candidate repository. Compare official findings and capabilities source-wide, but keep manual risks and dirty-worktree state repository-specific.
