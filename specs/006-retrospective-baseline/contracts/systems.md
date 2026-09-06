# System operation workflow contract

Retrospective at `8e51a4f`, recorded 2026-09-05. See [scope](../spec.md).
The [coverage map](../coverage.md) assigns primary owners. These workflows state
Linux/Arch/desktop or application-specific boundaries and do not claim portability
of live operations to unrelated platforms.

## S-001: Diagnose health and configuration ownership

Collect bounded read-only workstation evidence and narrow by incident time and
subsystem. Diagnose specific coredumps through their executable and stack evidence.
Classify live/repository/package drift and expected local state before changing
configuration. Desktop customization uses its existing Omarchy ownership rules.

Acceptance: a missing tool is reported as unavailable, not healthy; expected secret
state is not committed as drift; a health audit does not restart services by default.

Source: workstation-health-triage, diagnose-crash, managed-config-drift, omarchy.

## S-002: Packages, upgrades, and desktop components

Inspect package build inputs and source integrity before execution. Separate
PKGBUILD maintenance from system-upgrade readiness and recovery. Preserve boot,
snapshot, rollback, and configuration-merge evidence. Quickshell work tracks
reactive state, process ownership, outputs, and monitor/component lifetime.
Plugin audits bind findings to the exact candidate and declared capabilities.

Acceptance: no lock is removed while its owner is active; authored package fixes
retain source verification; destroying a shell component does not leave owned
processes; a marketplace policy source is not silently added as an audit target.

Source: arch-package-maintenance, arch-update-recovery, quickshell-development,
audit-omarchy-plugin.

## S-003: Homelab definitions and incident diagnosis

Keep Compose, environment examples, preparation, metadata, ingress, and generated
documentation consistent. Triage follows service dependencies, networks, mounts,
and host constraints without treating static validation as live service health.
The original [homelab feature](../../002-homelab-skill-gaps/spec.md) owns stack
maintenance detail. Secrets remain outside copied environment examples.

Acceptance: a stack definition change checks generated docs and interpolation;
a diagnosis distinguishes upstream dependency failure from local container failure.

Source: homelab-stack-maintenance, homelab-stack-triage.

## S-004: Recoverability and service exposure

Backups need source coverage, integrity, and bounded isolated restore evidence;
a successful schedule alone is insufficient. Network checks trace firewall,
container publishing, IPv4/IPv6, DNS/TLS, and intended client paths. A listening
socket alone does not prove intended reachability or isolation.

Acceptance: a restore sample never overwrites live data; an untested WAN or IPv6
path stays unverified; a network audit does not change firewall policy implicitly.

Source: backup-restore-verification, network-exposure-verification.

## S-005: Media preservation

Establish the preservation contract before transformation, including source
identity, metadata, ordering, quality, and container/codec boundaries. Use existing
utilities and verify outputs before replacing inputs or cleaning working evidence.

Acceptance: successful process exit without expected streams or preserved metadata
is not sufficient; destructive replacement needs the task's authority and proof.

Source: media-preservation.
