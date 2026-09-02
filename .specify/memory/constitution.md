# Agent Skills Constitution

## Core principles

### I. Repository is canonical

All maintained skill content lives under `skills/`. Installed locations are
symlinks, never independent editable copies.

### II. Hard-fork provenance

Every skill is explicitly labeled as a hard fork. Original URLs, source paths,
and local-origin references remain recorded in `PROVENANCE.json` and the
skill's `UPSTREAM.md`.

### III. Reviewed updates

Upstream changes are imported manually and reviewed as code. Synchronization
must not overwrite local behavior or silently change invocation policy. Every
external skill records an exact audited commit plus local changes that must be
reapplied. Scheduled checks may report drift but never merge it.

### IV. Portable by default

Scripts avoid machine-specific paths and GNU-only behavior when practical.
Platform-specific skills state their boundary instead of claiming unsupported
portability.

### V. One validation contract

Local hooks and CI call the same repository targets. Validation checks skill
metadata, provenance, generated pointers, script syntax, portability rules,
and symlink state.

## Governance

Exceptions require a documented reason in the affected skill. Amendments use
semantic versioning.

**Version**: 1.1.0 | **Ratified**: 2026-09-02
