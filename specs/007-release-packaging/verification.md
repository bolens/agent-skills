# Packaging verification

Assessed 2026-09-06 against the task working tree based on `2d72d9c`.
The task adds reusable instructions, not application packages.

## Scenario review

A separate read-only evaluator applied the new skill and its references to the
six scenarios in [quickstart.md](quickstart.md). No blocking behavioral defect
was found. This is simulated instruction evidence, not native runtime testing.

| Scenario | Observed decision |
| --- | --- |
| Rust CLI across Linux/macOS/Windows | All targets assessed conditionally; native variants and Windows catalogs retained without universal source-mode claims |
| Python library with C extension | sdist/native wheels selected; untested OS/libc targets conditional; desktop formats require an application |
| Linux systemd/Wayland GUI | Platform dependencies prevent assumed Windows/macOS support; Flatpak eligibility differs from Flathub policy; main uses an owned remote |
| Binary-only Windows app | Binary packaging supported conditionally; source/main-source variants unavailable without inputs; WinGet remains explicit |
| Compiler leak, newer glibc, dynamic plugin | Remove accidental closure references, rebuild for declared current ABI targets, retain required plugin, and measure actual installation |
| Changelog-only edit | No packaging or publication workflow implied |

The evaluator identified one nonblocking coverage omission: native installer rows
did not explicitly name Mac App Store/Microsoft Store eligibility. Added a
conditional destination row, verified current primary distribution documentation,
and locally checked that it retains separate store acceptance and authority.

## Checks

- `make check-fast`: passed with 62 registered skills.
- Skill-creator validation for `release-packaging`: passed.
- `make check`: passed, including 53 tests, portability, and installed links.
- Managed installer: created only the three missing new-skill symlinks; existing
  links were already correct. No independent installed skill copies were edited.
- Separate Archify suite under Node 22: 1,022 passed, zero failed, four reported
  skips. Skips cover optional external MCO fixtures, an alternate-Node test, and
  site checks routed to separate integration. Serialized WebM smoke and all seven
  site integration tests passed with Chromium. These suites guard existing fork
  behavior; they are not application packaging evidence.
- No application build, cross-platform installation, signing, public registry
  submission, or store acceptance was tested or claimed.

## Requirement coverage

FR-001 through FR-004: target matrix, language assessment, and native variants.
FR-005 through FR-007: modern target contract, payload/closure checks, and clean
artifact verification. FR-008: recorded main commit and update ownership.
FR-009: release, Arch, CI, dependency, and fleet handoffs. FR-010: generated local
hard-fork provenance, 62-skill validation, and managed installation links.
