# Packaging research

Assessed 2026-09-06. Primary documentation and separate bounded research passes
covered native variant semantics. No application builds or store submissions ran.

## Decisions

- **Decision**: Use one new `release-packaging` owner and focused handoffs.
  **Rationale**: `babysit` owns delivery, Arch owns PKGBUILDs, and CI owns pipeline
  contracts. None owns cross-ecosystem artifact selection or installation cost.
  **Alternative**: Expanding babysit would load packaging detail during unrelated PR repair.
- **Decision**: All targets are conditional, including the original nine.
  **Rationale**: The user's follow-up makes language and available build options
  controlling inputs. Native dependencies, GUI/runtime requirements, and target
  OS still need evidence. No language alone guarantees a working package.
  **Alternative**: A fixed all-platform build matrix would create unsupported artifacts.
- **Decision**: Distinguish logical variants from native publication identities.
  **Rationale**: Nix source recipes may use substitutes, Homebrew uses bottles and
  HEAD modes, and installer catalogs may have no source recipe model.
  **Alternative**: Forcing three suffixes everywhere misstates native semantics.
- **Decision**: Resolve main once per candidate and publish immutable snapshots.
  **Rationale**: A live recipe may track main, but each resulting build needs exact
  revision evidence and native version ordering. Stable releases must not drift.
  **Alternative**: Reusing mutable nightly URLs loses artifact identity.
- **Decision**: Measure payload and runtime closure separately.
  **Rationale**: Small wrapper packages may install large runtimes. Shared runtimes
  and binary caches can reduce incremental cost without shrinking all dependencies.
  **Alternative**: Minimizing archive bytes alone can break runtime behavior.

- **Decision**: Prioritize current stable and rolling platforms rather than legacy dependency floors.
  **Rationale**: The user explicitly prioritizes broad modern cross-compatibility.
  Select an ABI floor within the declared current target set and validate it.
  **Alternative**: An automatic oldest-LTS build policy spends effort on support
  the user did not request. Existing explicit promises still need migration.

## Primary evidence

- Arch [VCS guidelines](https://wiki.archlinux.org/title/VCS_package_guidelines)
  and [submission rules](https://wiki.archlinux.org/title/AUR_submission_guidelines):
  native VCS suffixes, versioning, conflicts, and VCS metadata update boundaries.
- Debian [source packages](https://www.debian.org/doc/debian-policy/ch-source.html)
  and [shared libraries](https://www.debian.org/doc/debian-policy/ch-sharedlibs.html):
  source packages produce binary DEBs; build/runtime dependencies differ.
- RPM [spec format](https://rpm.org/docs/latest/manual/spec.html): source inputs,
  build requirements, runtime requirements, and subpackages. Fedora policy pages
  were access-blocked, so current destination-specific Fedora acceptance must be
  checked when a concrete package is prepared.
- Nix [Nixpkgs manual](https://nixos.org/manual/nixpkgs/unstable/): derivations,
  substitutes, output separation, and binary patching.
- Homebrew [formula cookbook](https://docs.brew.sh/Formula-Cookbook),
  [bottles](https://docs.brew.sh/Bottles), and
  [acceptance policy](https://docs.brew.sh/Acceptable-Formulae): native source,
  bottle, and HEAD modes, with core restrictions on binary-only formulae.
- Flathub [requirements](https://docs.flathub.org/docs/for-app-authors/requirements):
  source builds for source-available software and dependencies, subject to approved
  exceptions; no nightly/development snapshots in stable or beta. Use an owned
  Flatpak remote for those unsupported variants.
- Scoop [manifests](https://github.com/ScoopInstaller/Scoop/wiki/App-Manifests),
  Chocolatey [package creation](https://docs.chocolatey.org/en-us/create/create-packages/),
  and WinGet [installer schema](https://github.com/microsoft/winget-pkgs/blob/master/doc/manifest/schema/1.10.0/installer.md):
  native installer/portable semantics, scripted source possibilities in owned
  Scoop/Chocolatey feeds, and no native WinGet source-build model. WinGet Channel
  is unimplemented in the assessed schema; distinct IDs are the documented route.
- AppImage [concepts](https://docs.appimage.org/introduction/concepts.html),
  Snap [channels](https://documentation.ubuntu.com/snapcraft/8.14.1/reference/channels/),
  FreeBSD [ports and packages](https://docs.freebsd.org/en/books/handbook/ports/),
  and the linked target reference cover conditional distribution paths.

The maintained skill references contain the operational mappings and additional
language sources. Documentation is checked again for the actual packaging task;
this dated assessment does not promise permanent store policy or acceptance.
