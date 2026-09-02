---
name: managed-config-drift
description: Audit drift between live Linux configuration, version-controlled configuration repositories, symlink farms, and packaged defaults. Use when configuration ownership is unclear, a desktop behaves differently from its repo, symlinks may be broken, generated files may be stale, or an update may have overwritten local state. Default to reporting and do not synchronize or replace files automatically.
---

# Managed configuration drift

Build an ownership map before comparing content. Identify the live path, intended source repository, generated-file contract, packaged default, and deployment mechanism such as symlinks, copy scripts, GNU Stow, or hooks.

Use `scripts/compare-trees.py LIVE=MANAGED [...]` for bounded tree comparisons. It reports missing paths, type changes, symlink-target changes, and content differences without modifying either tree. Use `--exclude NAME` for caches, secrets, runtime state, or generated artifacts that the repository explicitly excludes.

## Classification

- **Broken ownership:** dangling link, missing source, wrong owner, or unexpected writable target.
- **Uncommitted live drift:** live content differs from its declared managed source.
- **Expected local state:** secrets, caches, device state, or host-specific overrides documented as untracked.
- **Generated drift:** output differs because its declared generator has not run.
- **Packaged-default drift:** an upstream update changed a default that the local overlay depends on.

Read repository guidance and generator commands before judging a difference. Never copy, replace, delete, relink, refresh Omarchy configuration, or run a generator merely to make the audit clean. Propose an owner and direction for each reconciliation, then seek authorization.

Use `omarchy` before touching live Omarchy or Hyprland configuration. Use `sensitive-info-audit` before adding previously untracked live configuration to Git.
