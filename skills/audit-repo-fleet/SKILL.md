---
name: audit-repo-fleet
description: Audit and maintain a directory containing multiple Git repositories by inventorying worktree state, branches, local upstream divergence, governance files, toolchains, CI, validation entry points, and maintenance risk. Use when the user asks for repository fleet health, cross-repo maintenance, stale or inconsistent repos, spec-kit/AGENTS drift, release readiness, or what to work on next across many repositories.
---

# Audit a Repository Fleet

Default to a read-only audit. Treat each repository's constitution, `AGENTS.md`, contributor docs, manifests, and native task runner as authoritative for that repository.

For broad source exploration, use [bounded context work](references/context-work.md):
search before reading, use the local bounded reader for source excerpts, and keep
durable corrections in existing project memory. The reference also defines
focused handoffs when delegation is permitted and checkpoint rules for explicitly
requested recurring reports.

## Inventory

Run `scripts/inventory.sh <workspace-root> [max-depth]` to collect local facts. The default depth of 3 finds ordinary repositories while avoiding vendored repositories and test fixtures buried inside them. Increase it deliberately for deeper layouts. The script does not fetch, install, test, or modify repositories; divergence is relative to existing local remote-tracking refs and may be stale.

Keep stderr and the exit status with the TSV. Failed discovery, invalid Git
markers, and failed worktree status return 1 while retaining available rows.
Failed status counts read `unknown`, never zero. Bare storage discovered through
a `.git` marker is explicitly excluded; inspect its linked worktrees separately.
Bare layouts without that marker are outside this scan. Rows represent worktrees,
not unique maintained repositories. The script does not deduplicate or establish
ownership, and directory enumeration order is not a comparison key.

Supplement the inventory only where it changes prioritization:

- inspect dirty diffs without overwriting or attributing them
- identify canonical check, generation, release, and security commands
- compare `AGENTS.md` against the constitution for duplication or contradiction
- locate dependency automation, action pinning, generated-file contracts, and release metadata
- distinguish archived/vendor mirrors from actively maintained repositories
- inspect nested repositories or unusual worktree layouts separately when they fall outside the bounded inventory scan

Never fetch every remote or run every repository's full suite merely to make the report look complete. Ask before network-heavy or long-running fleet operations.

For a repeat audit with prior evidence, read [comparing audit runs](references/comparing-runs.md).
Compare like-for-like repository identities and check scopes, and separate new
findings from rechecks, unresolved conflicts, and unavailable observations.
An omitted repository or failed check cannot close an earlier finding.

## Prioritize

Rank evidence-backed work into:

1. **Protect now** — secret exposure, destructive defaults, broken required CI, unsafe dependencies, corrupted generation contracts
2. **Unblock** — failing builds/tests, incompatible toolchain pins, unresolved migrations, broken release paths
3. **Prevent drift** — missing governance, stale generated artifacts, inconsistent automation, unowned update surfaces
4. **Improve later** — maintainability or documentation improvements without current failure evidence

For each recommendation include repository, evidence, impact, safe next action, validation, and whether external or destructive authorization is required. Do not equate age, churn, or a dirty worktree with a defect.

## Act only when requested

If the user asks to implement maintenance, work one risk-coherent batch at a time. Use [shared fixes](references/shared-fixes.md) to check the rest of the maintained fleet for the same cause or applicable improvement and complete confirmed matches within the authorized scope. This check is part of implementation, not an optional follow-up after the first fix. Re-read each repository's guidance, preserve unrelated changes, run focused validation, and report exact results. Follow its commit requirements for authorized implementation. Push, merge, publication, deployment, live-service changes, and bulk upgrades retain their own authorization boundaries.

For maintenance across repositories or long-running checks, use [execution evidence](references/execution-evidence.md) to record task state, native command results, candidate freshness, bounded retries, and dependency joins. The optional `scripts/evidence.py` helper keeps private records under each worktree's Git directory. It does not replace repository checks, authorization, or required CI.

For releases, audit version sources, generated artifacts, changelog/release notes, packaging, CI, signing, and rollback. When changelog quality or edits are in scope, use the changelog-maintainer skill for reader-facing history and generator checks. A readiness request authorizes reporting, not publishing.

Before making a repository public or publishing an artifact, use `sensitive-info-audit` across the exact publication boundary and committed history. Treat unresolved high-confidence secret findings as **Protect now** blockers.

When the fleet includes externally sourced hard-forked skills, use `sync-skill-upstreams` to check exact audited refs and preserve documented local changes during imports.

When the fleet includes runnable websites, use `web-quality-audit` for measured performance and accessibility, and `responsive-web-capture` for the requested visual viewport evidence.

When fleet work changes self-hosted homelab stack contracts, use [homelab-stack-maintenance](../homelab-stack-maintenance/SKILL.md) and return shared patterns to the fleet check. Keep image-pin-only changes in [triage-dependency-updates](../triage-dependency-updates/SKILL.md) and ordinary application Docker development in its existing workflow. For operational Compose stacks, use `homelab-stack-triage` for a live service incident rather than treating repository health as runtime health. Use `backup-restore-verification` when backup recoverability is the question.

When an Omarchy plugin fleet is being prepared for marketplace submission, verification, or update approval, use `audit-omarchy-plugin` for each candidate repository. Compare official findings and capabilities source-wide, but keep manual risks and dirty-worktree state repository-specific.

When authorized maintenance includes repairing or merging specific PRs or preparing or publishing repository releases, automatically use [babysit](../babysit/SKILL.md) for each selected target. Carry each repository's endpoint, authority, and evidence separately, and return to an already active workflow. A fleet inventory or release-readiness assessment alone does not start follow-through.

When fleet implementation adds or changes CI pipelines or shared workflow contracts, use [ci-maintenance](../ci-maintenance/SKILL.md) to resolve the applicable baseline and validate event, permission, and caller behavior. Return shared causes and affected consumers to the current fleet coordinator.
