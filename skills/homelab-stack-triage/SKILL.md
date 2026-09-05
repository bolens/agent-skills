---
name: homelab-stack-triage
description: Diagnose failures in self-hosted Docker Compose services across containers, dependencies, networks, reverse proxies, DNS, mounts, and host resources. Use for a degraded or unavailable homelab service; do not use for ordinary Docker development or repository-only review.
---

# Homelab stack triage

Establish the real request path and failure boundary before changing a running service. Default to read-only inspection. A request to diagnose does not authorize restarts, recreation, image pulls, migrations, volume changes, pruning, or deployment.

## Resolve ownership

Read repository guidance and locate the canonical Compose or stack file, environment-file contract, preparation script, shared-network documentation, reverse-proxy route, persistent-data mounts, health checks, and declared dependencies. Respect repository prohibitions on reading ignored runtime configuration before collecting evidence. Never print secret values. Use [sensitive-info-audit](../sensitive-info-audit/SKILL.md) on permitted, sanitized artifacts before sharing an incident bundle. A scanner does not grant permission to read excluded files.

Treat generated catalogs and topology diagrams as navigation aids, not runtime truth. Confirm live Compose labels, working directory, project name, image identity, and configuration files. Preserve unrelated containers and stacks.

## Trace the service path

Work from the user-visible symptom inward:

1. Confirm the exact URL, client path, failure time, and whether the problem is local, proxied, or remote.
2. Inspect permitted container state, health, restart count, and exit/OOM metadata using selected fields. Read bounded logs only when their source is permitted and output can be sanitized before display. Avoid unrestricted `docker inspect`, environment dumps, and raw resolved Compose output. If live configuration cannot be read, validate tracked examples and mark runtime configuration unverified.
3. Test each hop separately: client/DNS/TLS, reverse proxy, Docker network, target port, application health endpoint, dependency, and persistent mount.
4. Correlate failures by timestamp. A noisy log line or unhealthy dependency is not causal without a matching path or time.
5. Classify the boundary as host resource, mount/storage, Docker daemon, image/configuration, network/DNS, proxy/TLS, application, or dependency.

For permitted Compose checks, use [example-validation guidance](../homelab-stack-maintenance/references/example-validation.md) to distinguish public examples from live configuration and suppress value-bearing output. Inspect commands behind health checks and diagnostic helpers before running them. A validation helper may create a container, pull an image, mount private files, or reload monitoring. Do not execute those effects under diagnosis-only authority.

Prefer service-local probes and existing health checks. Avoid broad log dumps. Redact URLs containing credentials, authorization headers, cookies, tokens, private addresses when publication would expose topology, and environment values.

Use `workstation-health-triage` when failures span Docker and the host, storage, graphics, network, or system services. Use `managed-config-drift` when the live Compose deployment may differ from its repository. Use `diagnose-crash` only for a host process with a systemd coredump.

Use [network-exposure-verification](../network-exposure-verification/SKILL.md) when the question is which LAN, WAN, or VPN clients should reach a service, including expected denial. An availability diagnosis alone does not establish exposure policy.

If the supported fix changes committed stack files, use [homelab-stack-maintenance](../homelab-stack-maintenance/SKILL.md) to keep Compose, environment examples, preparation, metadata, ingress, and generated documentation consistent. Return the evidence to the current coordinator at the user's requested endpoint. If the user narrows the task to repository readiness, stop there without resuming live incident work. This handoff does not authorize deployment.

## Mutations

Before an authorized mutation, record the current generation, selected container metadata, permitted sanitized logs, configuration source identity, relevant mount/network roles, and image digest. Inspect resolved configuration only if permitted and keep value-bearing content out of shared output. Do not capture prohibited files as a rollback bundle. State the expected effect and rollback.

Treat preparation as a mutation when it creates files, synchronizes environment files, or creates networks, volumes, or directories. Never create a missing bind directory until the expected remote filesystem and mount source are verified. A local directory is not proof that storage is mounted.

Choose the narrowest action that matches the proven boundary. A restart tests transient state; recreation applies configuration; pulling changes software; migration changes data. Do not collapse them into one command. Never use `down -v`, prune, delete application data, or replace a database without explicit authorization and recovery proof.

For dependency or schema transitions, use [migration](../migration/SKILL.md). Before touching persistent data, use [backup-restore-verification](../backup-restore-verification/SKILL.md). After the action, replay the same path hop by hop and check restart counts and fresh logs.

## Report

Report the affected stack and service, observed path, failure boundary, decisive evidence, actions taken or proposed, rollback, and post-action verification. Separate confirmed cause from remaining hypotheses.
