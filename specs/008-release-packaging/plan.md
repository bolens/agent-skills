# Implementation Plan: Portable release packaging

**Branch**: `007-release-packaging` | **Date**: 2026-09-06 | **Spec**: [spec.md](spec.md)

## Summary

Create `release-packaging` as the owner of target selection, native variant mapping,
portable builds, lean installations, and artifact evidence. Keep `babysit` as the
release coordinator and `arch-package-maintenance` as the Arch implementation owner.
Prioritize current stable/rolling systems over legacy dependency compatibility.
All ecosystems are assessed conditionally from language, build tools, application
kind, supported OS/ABI, and destination policy. WinGet is explicitly retained.

## Technical Context

**Language/Version**: Markdown skill instructions and generated JSON provenance.
**Primary Dependencies**: Existing provenance generator, installer, repository checks, and current primary packaging documentation.
**Storage**: Canonical `skills/` and prospective `specs/008-release-packaging/`.
**Testing**: Static gates, bounded scenario review, skill validation, installed-link verification.
**Target Platform**: Linux plus conditional macOS, Windows, FreeBSD, and language/runtime targets.
**Project Type**: Reusable skill collection, no actual application packaging in this task.
**Performance Goals**: Measurable package/installed/closure cost guidance, without an invented universal byte budget.
**Constraints**: Preserve functionality, licenses, hardening, source traceability, native policy, and publication authority.
**Scale/Scope**: Nine requested ecosystems plus direct archives, AppImage, Snap, Alpine, Gentoo, Guix, FreeBSD, native installers, language registries, and OCI.

## Constitution Check

- Canonical source: new and updated instructions remain under `skills/`.
- Hard forks: generate local origin and all standard install targets; no upstream import.
- Reviewed updates: preserve existing origins and all upstream records.
- Portability: explicit platform/ABI and ecosystem boundaries, no universal wrapper script.
- Validation: use repository gates, skill checks, and a bounded scenario review.

Pre-research and post-design checks pass. No constitutional exceptions.

## Project Structure

```text
skills/release-packaging/
  SKILL.md
  UPSTREAM.md                       # generated
  references/
    targets-and-variants.md
    language-and-build-options.md
    lean-portability.md
skills/babysit/references/release-follow-through.md
skills/arch-package-maintenance/SKILL.md
skills/ci-maintenance/SKILL.md
skills/triage-dependency-updates/SKILL.md
skills/audit-repo-fleet/SKILL.md
specs/008-release-packaging/
  spec.md
  plan.md
  research.md
  data-model.md
  contracts/packaging-receipt.md
  quickstart.md
  tasks.md
  checklists/requirements.md
  verification.md
```

**Structure Decision**: One focused owner with conditional references avoids
repeating platform policy in every release skill. No executable helper or package
recipe template is justified without a concrete application. Register through
`scripts/update-provenance.py`; use `scripts/link-installed.py` for new links.
