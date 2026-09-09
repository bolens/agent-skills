---
compatibility: Linux probes require Bash, Python 3.9+, and POSIX process groups. Individual system tools are optional and unavailable checks are reported.
name: workstation-health-triage
description: Collect and correlate a read-only Linux workstation health snapshot across services, logs, coredumps, resources, storage, mounts, packages, networking, graphics, and the desktop session. Use for broad desktop health checks, recurring instability, post-update verification, or when the failing subsystem is unclear. Do not use for a single known application crash when diagnose-crash is sufficient.
---

# Workstation health triage

Establish current facts before proposing repairs. Keep collection read-only and distinguish a failed check from a check unavailable because of permissions, sandboxing, missing tools, or no active graphical session.

## Modes

- **Quick:** Run `scripts/collect-health.sh quick` for identity, pressure, disk space, failed units, recent coredumps, mounts, package-manager locks, and session basics.
- **Full:** Run `scripts/collect-health.sh full` when the quick pass is inconclusive. This adds bounded journal, kernel, sensor, network, graphics, and package checks.
- **Incident:** Start with the quick snapshot, then narrow evidence around the reported time and subsystem. Use `diagnose-crash` for a specific coredump.

The shell entry point requires Bash and Python 3.9+ and supervises probes sequentially.
It resolves symlinks with Python and does not require GNU path utilities. Probe
commands target Linux. Process supervision requires POSIX process groups. Defaults
are 8 seconds per probe, a 60-second collection budget, and 64 KiB of output per
probe. Use `--probe-timeout`, `--total-timeout`, and `--max-bytes` for a bounded
increase after identifying missing evidence. Timeouts and truncated output are
marked and return a nonzero collection status. Unavailable or failed individual
checks remain labeled in a completed report.

`--output PATH` creates a new private file and refuses existing paths, including
symlinks. Keep evidence under `/tmp` unless the user requests a durable artifact.
Partial reports remain available after interruption or failure. On total timeout,
the collector allows up to 0.1 seconds to append an incomplete marker when the
output destination remains writable. Review reports
with `sensitive-info-audit` before sharing or committing them.

Cancellation, timeout, output limits, and normal probe exit all clean up the
probe's process group, including remaining descendants. Cleanup allows 0.1 seconds
for TERM before KILL and up to 0.5 seconds to reap the direct child. The collection
budget also bounds pipe backpressure. Processes stuck in uninterruptible kernel
I/O cannot be forcibly reaped on a deadline, and descendants that deliberately
create another session are outside process-group cleanup. Do not use this helper
to launch daemons. No scratch directories or background collectors are created.

Full mode reads pending updates from existing pacman databases without refreshing
them. Treat that result as cached information, not update-readiness evidence.

## Interpret evidence

Correlate signals by time and subsystem. A failed unit without relevant logs is not automatically the cause. Mount verification inside a container or sandbox may not describe the host namespace. Missing session variables may mean the collector did not inherit the desktop environment.

Rank findings as active failure with corroborating evidence, degraded or risky state, unavailable check needing host confirmation, or informational context.

Do not restart services, mount filesystems, repair packages, delete caches, update the system, or change configuration without explicit authorization. Give the exact proposed mutation, expected effect, rollback, and verification first.

## Handoffs

- Use `omarchy` and its desktop-session guide when Omarchy owns the affected desktop. Hyprland or PipeWire alone does not establish that installation.
- Use [arch-linux](../arch-linux/SKILL.md) for Arch system configuration, [cachyos](../cachyos/SKILL.md) for CachyOS-specific repositories, drivers, kernels, or tuning, and [nixos](../nixos/SKILL.md) for declarative NixOS configuration and generations. Keep generic health collection here.
- Use `managed-config-drift` when symptoms may come from live configuration diverging from a managed repository or packaged default.
- Use `arch-update-recovery` for Arch-family upgrade readiness, failed package transactions, boot-chain recovery, or post-upgrade verification.
- Use `homelab-stack-triage` when the failing surface is a Compose service or its proxy, network, mount, or dependency path.
- Use `backup-restore-verification` when the question is recoverability rather than general storage health.
- Use `sensitive-info-audit` before publishing diagnostic bundles.
