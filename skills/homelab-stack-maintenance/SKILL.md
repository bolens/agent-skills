---
name: homelab-stack-maintenance
description: Add or change self-hosted Compose stack definitions while keeping environment examples, preparation, metadata, ingress, and generated documentation consistent. Use for homelab repository maintenance, not live incident diagnosis, image-only updates, or ordinary application Docker development.
---

# Homelab stack maintenance

Deliver a consistent repository change without silently applying it to a host. Read repository guidance, the target stack's README, and its tracked source files. Local stack instructions override nearby conventions. A repository change does not itself authorize image pulls, preparation on the live host, deployment, reloads, or data migration.

## Establish the source contract

Inventory tracked paths before reading contents. Exclude ignored runtime files, local helper overrides, private keys, live ingress snippets, and application data. Follow any prohibition on reading those files, not merely on printing them. Do not source environment files as shell code. Derive examples from documented requirements with placeholders, never by copying production values and redacting afterward.

Identify the stack lifecycle: maintained Compose, optional profile or override, CLI-only entry, or externally generated bundle. Do not force every directory into the same layout. Treat catalogs and topology diagrams as intended relationships, not proof of deployed resources.

Map the change across the sources that exist in this repository:

| Source | Contract to preserve |
|---|---|
| Compose and includes | Services, image pins, ports, dependencies, health checks, mounts, networks, profiles, and runtime requirements |
| Environment examples | Required key names, defaults, interpolation inputs, container environment, and secret placeholders |
| Preparation | Copy ownership, generated environment mirrors, external prerequisites, repeat-run behavior, and optional actions |
| Stack metadata | Lifecycle, exposure, data and backup needs, runtime-security exceptions, resources, and placement |
| Ingress examples | Protocol, service/network identity, upstream container port, authentication, and intended client reachability |
| README and generated output | Setup and upgrade instructions, source inventories, catalog, topology, diagrams, and published guides |

Update only affected surfaces. A port change may affect health checks and proxy upstreams even when no host port should be published. A new external volume needs ownership and backup guidance as well as a declaration. Do not mark a privileged or floating-image exception acceptable solely because metadata matches Compose.

## Preserve preparation and storage behavior

Read the complete wrapper and shared helper chain before running it. Preparation can create files, host directories, networks, or external volumes even when it never starts a container. Inspect default paths and environment inheritance. Running a helper named audit, validate, or smoke-check is not evidence that it is read-only.

Preserve existing operator-authored runtime files. Where a helper intentionally synchronizes a generated environment mirror, identify its source of truth and document that write separately. Do not overwrite an independently maintained env file or replace a secret with an example default. New keys need an explicit operator update path that reports key names without values.

Do not create a bind directory when an absent remote mount could be the cause. Verify the intended filesystem, mount source, and access before an authorized preparation or deployment. Treat named-volume-to-bind changes as data migrations. Never delete shared external networks or volumes during routine cleanup.

Optional GPU, device, host-network, privileged, or alternate-image configuration stays opt-in. Preparation must not silently activate it. Validate changed preparation in a fresh fixture using public examples, temporary paths, and a stubbed runtime where feasible. Verify repeat execution preserves existing values and does not start containers. If isolation cannot prevent live writes, use source inspection and report execution as unverified.

## Validate the examples and generated output

Read [example validation](references/example-validation.md) before rendering Compose or choosing repository helpers. Keep interpolation separate from container env-file injection. Prevent local environment values and ignored files from entering the validation process or output.

Use the repository's focused validators, then its required gate. Preserve the real paths, optional env-file semantics, profiles, and include ownership in the checks. If a validator normalizes paths or skips generated bundles, record what was omitted. Passing YAML parsing is not proof that Compose renders, and rendering is not proof of service health.

For added or renamed stacks, update the owning catalog/topology source and regenerate affected outputs. A diagram, inventory, and published site may have different source files. Do not hand-edit generated sections or assume one generator refreshes all of them. Review the complete generated diff for stale links, unrelated churn, and private values. Shared helper or schema changes require checks across their consumers.

## Use related workflows at the affected boundary

Keep one coordinating task. Pass the stack, allowed source files, intended behavior, validation evidence, and remaining authority to a related skill, then return its result without starting a recursive handoff.

- For a live failure or post-deployment symptom, use [homelab-stack-triage](../homelab-stack-triage/SKILL.md). Repository checks alone cannot diagnose runtime state.
- For an image/version candidate, use [triage-dependency-updates](../triage-dependency-updates/SKILL.md) for release evidence and compatibility, then maintain affected stack contracts here.
- For changed ingress, published ports, or network membership, use [network-exposure-verification](../network-exposure-verification/SKILL.md) to establish intended access and denial. Live probing or policy changes keep their existing scope.
- Before a persistent-data transition, use [backup-restore-verification](../backup-restore-verification/SKILL.md) for recoverability and [migration](../migration/SKILL.md) for ordering, compatibility, and rollback. A Compose edit does not prove data is safe to move.
- When deployment ownership differs from committed examples, use [managed-config-drift](../managed-config-drift/SKILL.md) only for permitted paths. Ignored secrets are expected local state, not drift to copy into Git.
- Use [sensitive-info-audit](../sensitive-info-audit/SKILL.md) on the bounded shareable artifacts before publication. Never widen it to ignored runtime files against repository guidance.
- Use [git-hygiene](../git-hygiene/SKILL.md) for concurrent stack writers sharing helpers or generated outputs. Use [babysit](../babysit/SKILL.md) only when the requested endpoint includes PR or release follow-through.

Report changed contracts, checks and skips, private evidence not accessed, and remaining deployment or data work. Commit under repository policy. Distinguish repository readiness from runtime verification.

During active fleet-wide implementation, use [the fleet shared-fix workflow](../audit-repo-fleet/references/shared-fixes.md) when a stack change reveals a shared helper, environment, ingress, or metadata issue. Check other maintained stacks and repositories using that contract, fix confirmed matches, and keep private runtime files outside the search. A request limited to one stack keeps that limit.
