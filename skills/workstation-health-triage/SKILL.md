---
name: workstation-health-triage
description: Collect and correlate a read-only Linux workstation health snapshot across services, logs, coredumps, resources, storage, mounts, packages, networking, graphics, and the desktop session. Use for broad desktop health checks, recurring instability, post-update verification, or when the failing subsystem is unclear. Do not use for a single known application crash when diagnose-crash is sufficient.
---

# Workstation health triage

Establish current facts before proposing repairs. Keep collection read-only and distinguish a failed check from a check unavailable because of permissions, sandboxing, missing tools, or no active graphical session.

## Modes

- **Quick:** Run `scripts/collect-health.sh quick` for identity, pressure, disk space, failed units, recent coredumps, mounts, package-manager locks, and session basics.
- **Full:** Run `scripts/collect-health.sh full` when the quick pass is inconclusive. This adds bounded journal, kernel, sensor, network, graphics, and package checks.
- **Incident:** Start with the quick snapshot, then narrow evidence around the reported time and subsystem. Use `diagnose-crash` for a specific coredump.

The collector accepts `--output PATH`. Keep evidence under `/tmp` unless the user requests a durable artifact. Review it with `sensitive-info-audit` before sharing or committing it.

## Interpret evidence

Correlate signals by time and subsystem. A failed unit without relevant logs is not automatically the cause. Mount verification inside a container or sandbox may not describe the host namespace. Missing session variables may mean the collector did not inherit the desktop environment.

Rank findings as active failure with corroborating evidence, degraded or risky state, unavailable check needing host confirmation, or informational context.

Do not restart services, mount filesystems, repair packages, delete caches, update the system, or change configuration without explicit authorization. Give the exact proposed mutation, expected effect, rollback, and verification first.

## Handoffs

- Use `omarchy` and its desktop-session guide for Hyprland, UWSM, portals, PipeWire, Quickshell, display, or lock/idle problems.
- Use `managed-config-drift` when symptoms may come from live configuration diverging from a managed repository or packaged default.
- Use `arch-update-recovery` for Arch-family upgrade readiness, failed package transactions, boot-chain recovery, or post-upgrade verification.
- Use `homelab-stack-triage` when the failing surface is a Compose service or its proxy, network, mount, or dependency path.
- Use `backup-restore-verification` when the question is recoverability rather than general storage health.
- Use `sensitive-info-audit` before publishing diagnostic bundles.
