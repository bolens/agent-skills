---
name: triage-dependency-updates
description: Review, plan, and safely implement dependency updates across Node, Python, Go, Rust, Docker images, GitHub Actions, and system/configuration repositories. Use when the user asks to assess Renovate or Dependabot changes, upgrade packages or images, audit stale dependencies, resolve update conflicts, or batch dependency maintenance by compatibility and supply-chain risk.
---

# Triage Dependency Updates

Read repository guidance and identify the canonical manifest, lockfile, package manager, generated files, automation policy, and validation commands. Preserve unrelated work.

## Establish evidence

For each update record current and proposed versions, direct or transitive status, source registry/repository, release date, update class, and affected runtime/build/release surface. Use primary release notes, migration guides, advisories, and official registries for current facts.

Require an update candidate—a bot PR/diff, advisory, or user-supplied target—before claiming an actionable upgrade. In an offline or local-only review, inventory committed pins and policies, label freshness and advisory status **unknown**, and do not infer a newer version from installed caches. Distinguish:

- committed state: manifests, lockfiles, checksums, action SHAs, image digests
- installed state: `node_modules`, virtual environments, Go/Rust caches, local images
- generated or vendored state, which is not an update source unless repository guidance says otherwise

Treat Docker tag changes, GitHub Action SHA changes, system packages, plugins, and downloaded binaries as dependency updates even when no package manager is involved.

Check ecosystem-specific coupling when present: workspace catalogs and runtime/toolchain floors; minimum-release-age exceptions; lifecycle-script policy; Docker tag-plus-digest alignment; development versus container runtimes; reusable workflow and Action SHAs; generated clients; and platform package metadata.

## Assess risk

Raise risk for:

- major versions, runtime/toolchain floors, removed APIs, schema or config changes
- install/build scripts, new maintainers or registries, ownership transfer, young releases, mutable tags, lost signatures/checksums
- auth, networking, parsers, archives, package managers, CI permissions, deployment, or generated-code changes
- lockfile churn unexplained by the requested direct update
- updates spanning several ecosystems or requiring data/operational migration

Do not assume patch means safe or major means unsafe. Cite concrete evidence.

Prefer documented read-only validation commands. If a package-manager inspection needs writable caches or metadata databases, stop or use an explicitly isolated cache rather than mutating the user's environment merely to complete triage.

## Plan batches

Group updates only when they share a compatibility boundary and can be validated together. Isolate security-critical, major, migration-heavy, and supply-chain-uncertain changes. State ordering, rollback, focused checks, broader checks, and remaining platform gaps.

## Implement only when authorized

A review or triage request is read-only. When implementation is requested:

1. update through the repository's canonical tool and preserve pins/checksums
2. inspect manifest and lockfile diffs for unrelated resolution churn
3. apply required source/config migrations without opportunistic refactoring
4. run focused tests, then the repository's relevant gate
5. report exact versions, files, checks, skips, advisories, and residual risk

Use the changelog-maintainer skill when an update changes runtime requirements, compatibility, configuration, security exposure, or operator behavior. Keep routine dependency churn out of the changelog.

When the task includes repairing an open dependency PR, addressing its feedback, getting it ready to merge, or preparing or publishing a release, automatically use [babysit](../babysit/SKILL.md). Keep dependency assessment here and return versions, risk, and check evidence to that coordinating workflow. A dependency review or local upgrade alone does not start follow-through.

Do not disable lifecycle-script protections, signature/checksum verification, security gates, or dependency automation merely to land an update. Follow the user's and repository's commit instructions and stage only task changes. Push, merge, publish, deploy, or restart services only within the authority already granted for the task.

When a homelab image update also changes environment keys, mounts, health checks, ingress, or preparation, use [homelab-stack-maintenance](../homelab-stack-maintenance/SKILL.md) to update those source contracts together. Keep version and compatibility assessment here and return to the active delivery workflow. An image-pin-only update does not require the broader stack workflow.
