# Feature Specification: Portable release packaging

**Feature Branch**: `007-release-packaging`

**Created**: 2026-09-06

**Status**: Implemented and validated as skill guidance

**Input**: Create or update release skills for portable, lean packaging across Arch/pacman, Nix, Flatpak/Flathub, Scoop, Homebrew, Chocolatey, DEB, RPM, and WinGet. Prefer tagged source, tagged binary, and main-tip variants using `package`, `package-bin`, and `package-git` where supported. Include additional ecosystems for comprehensive coverage, with every target conditional on the language and available build options. WinGet remains explicitly included where possible.

## User Scenarios & Testing

### User Story 1 - Select supported package variants (Priority: P1)

A maintainer preparing a release gets a complete target matrix and a truthful mapping of source, binary, and development variants to each ecosystem.

**Why this priority**: A universal suffix scheme can produce invalid store submissions or misrepresent source support.

**Independent Test**: Walk through a tagged release and a main-tip build for all nine requested ecosystems. Each has a native mapping or a documented unsupported variant and alternative destination.

**Acceptance Scenarios**:

1. **Given** a portable application with tagged releases, **When** packaging is planned, **Then** all nine defaults and additional targets receive a supported, conditional, or inapplicable disposition based on language, build tooling, application type, platform, and destination.
2. **Given** a source-building ecosystem with variant support, **When** variants are created, **Then** the tagged source, tagged binary, and main-tip options are distinct and their package names or native build modes are documented.
3. **Given** an installer catalog or store that disallows one variant, **When** mapping the default variants, **Then** the maintainer sees the native equivalent or limitation rather than an invented source-build capability.

### User Story 2 - Ship lean portable artifacts (Priority: P1)

A maintainer can verify that each package contains the runtime payload needed by its users without build tools, unrelated features, or accidental host dependencies.

**Why this priority**: File size alone cannot prove an installation is lean or portable.

**Independent Test**: Walk through an artifact with leaked build dependencies and one requiring a newer host ABI. Both must fail the packaging evidence gate until resolved or explicitly excluded from supported targets.

**Acceptance Scenarios**:

1. **Given** a Linux artifact, **When** portability is assessed, **Then** CPU, architecture, libc, loader, shared libraries, installation paths, and declared platform requirements are checked against clean target environments.
2. **Given** a package recipe with build tools in runtime dependencies, **When** the payload is reviewed, **Then** build-only dependencies are separated and required licenses, security controls, runtime features, and integration remain intact.
3. **Given** source and binary variants for one release, **When** validating size and compatibility, **Then** each has measured artifact, installed, and dependency costs as applicable, with variant-switch, upgrade, and removal behavior assessed.

### User Story 3 - Integrate packaging into release work (Priority: P2)

Existing release and CI workflows route packaging work to one owner while preserving the requested delivery endpoint and dependency update policy.

**Why this priority**: Packaging guidance must be found during real release work without starting duplicate publication workflows.

**Independent Test**: Review routing for release preparation, Arch-only repair, CI packaging jobs, and a nearby changelog-only task. Only relevant packaging work enters the new skill.

**Acceptance Scenarios**:

1. **Given** release preparation, **When** artifacts need packaging, **Then** the packaging evidence returns to the existing release coordinator and no publication is implied.
2. **Given** a tip-of-main package, **When** it is built, **Then** the resolved revision and monotonically ordered version are recorded, and repeatable inputs and update ownership are identified.
3. **Given** a project suited to additional ecosystems, **When** coverage is assessed, **Then** direct archives, AppImage, Snap, Alpine, Gentoo, Guix, FreeBSD, native installers, language registries, and OCI images are considered conditionally.

### Edge Cases

- A Linux-only application cannot produce native Windows packages without a port.
- Multiple available versions do not establish safe simultaneous installation.
- A store prohibits nightly builds or upstream binary repacks.
- A source derivation served from a binary cache remains a source recipe.
- A mutable main reference must become an identified snapshot for each built artifact.
- Source archives may need generated files or vendored inputs absent from an automatic tag archive.
- A required runtime increases download size but prevents unsupported system-library assumptions.
- Signing credentials or target runners are unavailable. Preparation continues with explicit evidence gaps.

## Requirements

### Functional Requirements

- **FR-001**: Guidance MUST assess all nine default ecosystems and the additional targets, conditioning selection on repository language, available build options, application type, supported platforms, and destination rules. Language detection alone MUST NOT establish portability.
- **FR-002**: Guidance MUST distinguish source build recipes, upstream binary repacks, package-manager built binaries, main-tip snapshots, parallel versions, and coinstallation.
- **FR-003**: Guidance MUST prefer `package`, `package-bin`, and `package-git` where ecosystem and destination rules allow, using documented native equivalents otherwise.
- **FR-004**: Each artifact MUST identify its release tag or resolved main commit, native version, architecture, target environment, source/payload checksum, and build provenance.
- **FR-005**: Guidance MUST prioritize current stable and rolling distributions, supported runtimes, and cross-platform compatibility over legacy dependency support. It MUST address CPU and libc baselines, target-native dependencies, installation layout, and clean-environment runtime validation. Existing explicit compatibility promises require deliberate migration rather than silent removal.
- **FR-006**: Lean packaging MUST separate build/check dependencies from runtime dependencies, inspect payload and closure size, and justify retained optional features without deleting required functionality or licensing.
- **FR-007**: Guidance MUST verify install, representative runtime operation, upgrade, variant transition, and removal where supported, recording unavailable environments as unverified.
- **FR-008**: Mutable development inputs MUST resolve to recorded commits per build, retain immutable published artifacts, and have update monitoring with Dependabot preferred where supported.
- **FR-009**: Existing release, Arch, CI, and fleet workflows MUST route relevant packaging work without expanding authority or duplicating coordination.
- **FR-010**: The new skill MUST retain local hard-fork provenance, default install targets, narrow discovery, and repository-native validation.

### Key Entities

- **Target**: Ecosystem, operating system, architecture, destination, support status, and native policy.
- **Variant**: Tagged source, tagged upstream binary, or main-tip source snapshot with native identity and installation relationship.
- **Evidence receipt**: Inputs, artifact identity, checks, size measurements, dependency closure, and remaining gaps.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All nine requested ecosystems have explicit mappings for all three requested variants or documented limitations.
- **SC-002**: Every packaging scenario identifies the exact source and separates preparation from publication.
- **SC-003**: Each tested lean/portability failure scenario is caught without disabling required functionality or verification.
- **SC-004**: Release preparation, Arch repair, CI packaging, and fleet assessment route consistently, while unrelated tasks retain their current owner.
- **SC-005**: Repository gates and bounded behavioral review pass, with live platform tests clearly distinguished from instruction validation.

## Assumptions

- This task changes reusable skills, not an application's packages or public repositories.
- The nine targets are default assessment/build targets when the application supports their platforms. A target needs an explicit reason to be excluded.
- The user explicitly included the additional systems and made all targets conditional on repository language and build options. None is a mandatory publication destination for an incompatible project.
- A main-tip source build may be distributed as a prebuilt snapshot where clients only install binaries.
- Native ecosystem and destination policy governs names and accepted artifacts. Unsupported variants remain visible in the matrix.
- Current-system cross-compatibility is the user preference. Older systems are supported only where an explicit project contract warrants the cost.
- Existing user authorization and repository policy determine commits, installations, signing, and publication.
