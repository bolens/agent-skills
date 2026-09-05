---
name: arch-update-recovery
description: Prepare, diagnose, verify, and recover Arch-family Linux upgrades involving pacman or AUR packages, pacnew files, kernels, initramfs, Btrfs snapshots, and bootloaders. Use for system-update readiness or failed-upgrade recovery; use omarchy for desktop customization.
---

# Arch update and recovery

This skill is intentionally Arch-family specific. Establish installed state, boot chain, snapshot tooling, package helpers, repositories, kernels, graphics drivers, and managed configuration before recommending a transaction. Default to reporting. Do not upgrade, downgrade, remove packages, regenerate boot artifacts, roll back snapshots, or edit live system configuration without explicit authorization.

## Before an upgrade

Read the distribution's current official notices and the local repository's update functions, package list, pacman configuration, snapshot hooks, bootloader configuration, and repository guidance. Confirm:

- no interrupted package transaction or stale lock with an active owner;
- adequate space in root, package cache, snapshot, EFI/boot, and temporary paths;
- current mirrors, keyring, time synchronization, and package database health;
- foreign/AUR packages and known rebuild-sensitive dependencies;
- kernel, initramfs, NVIDIA or other out-of-tree module compatibility;
- a usable pre-transaction snapshot and a boot or chroot recovery path.

Arch does not support partial upgrades. Do not refresh package databases and then selectively upgrade an unrelated subset as a repair. Treat unofficial helpers as clients of pacman, not separate package authorities.

Use `backup-restore-verification` when the safety case depends on backup recovery rather than a local snapshot alone. Use `managed-config-drift` to review `.pacnew`, `.pacsave`, generated config, and packaged-default changes. Use `sensitive-info-audit` before publishing system logs or configuration bundles.

Use [arch-package-maintenance](../arch-package-maintenance/SKILL.md) when a repair requires maintaining a PKGBUILD, rebasing a local patch, or validating the replacement for a pinned rebuild.

## Diagnose a failed upgrade

Capture the exact command, transaction log, pacman log window, current booted kernel, installed kernel/modules, initramfs and boot entries, failed units, filesystem and snapshot state, and package ownership of conflicting files. Classify the failure before acting:

- mirror, keyring, signature, or time;
- database lock or interrupted transaction;
- file conflict or package replacement;
- dependency/AUR rebuild;
- disk or filesystem pressure;
- kernel, initramfs, graphics module, or bootloader;
- configuration merge or service behavior.

Do not delete a lock while its owner is running, force package overwrites broadly, initialize a new keyring over an unexplained trust failure, or erase package caches needed for rollback. Prefer official package metadata and installed logs over forum recipes.

Use `workstation-health-triage` for broad post-upgrade instability and `diagnose-crash` for a specific coredump. Use `omarchy` when the remaining problem is Hyprland, UWSM, portal, lock/idle, bar, terminal, or other desktop behavior rather than the package transaction itself.

## Recovery and verification

Before an authorized repair, state the mutation, affected packages or boot artifacts, recovery route, and rollback. Apply one failure-boundary-sized change. For snapshot rollback, distinguish booting a snapshot from making it the persistent writable system and confirm how later snapshots and boot entries are regenerated.

Afterward verify package database consistency, the intended kernel and modules, initramfs, boot entries, failed services, mounts, networking, graphics session, and the original failing behavior. Report what was proven in the current boot and what still requires a reboot; never claim boot recovery was verified without actually booting the repaired generation.
