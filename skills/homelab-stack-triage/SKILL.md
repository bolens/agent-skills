---
name: homelab-stack-triage
description: Diagnose failures in self-hosted Docker Compose services across containers, dependencies, networks, reverse proxies, DNS, mounts, and host resources. Use for a degraded or unavailable homelab service; do not use for ordinary Docker development or repository-only review.
---

# Homelab stack triage

Establish the real request path and failure boundary before changing a running service. Default to read-only inspection. A request to diagnose does not authorize restarts, recreation, image pulls, migrations, volume changes, pruning, or deployment.

## Resolve ownership

Read repository guidance and locate the canonical Compose or stack file, environment-file contract, preparation script, shared-network documentation, reverse-proxy route, persistent-data mounts, health checks, and declared dependencies. Never print secret values. Use `sensitive-info-audit` before sharing logs, resolved configuration, or an incident bundle.

Treat generated catalogs and topology diagrams as navigation aids, not runtime truth. Confirm live Compose labels, working directory, project name, image identity, and configuration files. Preserve unrelated containers and stacks.

## Trace the service path

Work from the user-visible symptom inward:

1. Confirm the exact URL, client path, failure time, and whether the problem is local, proxied, or remote.
2. Inspect container state, health, restart count, exit/OOM details, recent bounded logs, and the resolved Compose configuration.
3. Test each hop separately: client/DNS/TLS, reverse proxy, Docker network, target port, application health endpoint, dependency, and persistent mount.
4. Correlate failures by timestamp. A noisy log line or unhealthy dependency is not causal without a matching path or time.
5. Classify the boundary as host resource, mount/storage, Docker daemon, image/configuration, network/DNS, proxy/TLS, application, or dependency.

Prefer service-local probes and existing health checks. Avoid broad log dumps. Redact URLs containing credentials, authorization headers, cookies, tokens, private addresses when publication would expose topology, and environment values.

Use `workstation-health-triage` when failures span Docker and the host, storage, graphics, network, or system services. Use `managed-config-drift` when the live Compose deployment may differ from its repository. Use `diagnose-crash` only for a host process with a systemd coredump.

## Mutations

Before an authorized mutation, capture the current generation, container state, relevant logs, resolved config, mounts, networks, and image digest. State the expected effect and rollback.

Choose the narrowest action that matches the proven boundary. A restart tests transient state; recreation applies configuration; pulling changes software; migration changes data. Do not collapse them into one command. Never use `down -v`, prune, delete application data, or replace a database without explicit authorization and recovery proof.

For dependency or schema transitions, use `migration`. Before touching persistent data, use `backup-restore-verification`. After the action, replay the same path hop by hop and check restart counts and fresh logs.

## Report

Report the affected stack and service, observed path, failure boundary, decisive evidence, actions taken or proposed, rollback, and post-action verification. Separate confirmed cause from remaining hypotheses.
