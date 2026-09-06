# Native targets and variant mappings

Read the sections for targets selected by the capability assessment. These mappings separate package-manager mechanics from public repository policy. Verify current rules for the actual destination before preparing a submission. An owned tap, overlay, feed, or remote still needs valid metadata and safe install behavior.

## Arch/pacman

Use `package` for tagged source, `package-bin` for an upstream release binary, and `package-git` for a live main source recipe. pacman installs the built package in every case; it does not compile a PKGBUILD during installation. Declare accurate `provides`/`conflicts`, including collisions among variants, and reserve `replaces` for real migrations. Keep build and check dependencies out of runtime `depends`.

Pin release inputs and use architecture-specific binary hashes. For a VCS source, declare the intended branch and capture the checked-out commit and derived `pkgver`. Native VCS entries may use `SKIP` for a mutable source; this does not authorize skipping verification of release archives or other downloads. Preserve signature verification where configured. Regenerate `.SRCINFO` for recipe changes; AUR live packages do not need metadata-only commits for every new main commit. Use [Arch maintenance](../../arch-package-maintenance/SKILL.md), [VCS guidelines](https://wiki.archlinux.org/title/VCS_package_guidelines), and [AUR submission rules](https://wiki.archlinux.org/title/AUR_submission_guidelines).

## Nix

An owned flake or overlay can expose `package`, `package-bin`, and `package-git` attributes. The ordinary source derivation can be served by binary substitutes; reserve `-bin` for repackaging upstream binaries. Pin both release and main-snapshot sources to revisions and hashes. `nixpkgs-unstable` is not a promise to track the application's main branch. Treat official nixpkgs inclusion and naming as a separate policy question.

Separate runtime, development, documentation, and debug outputs. Inspect `meta.outputsToInstall` and runtime closure for accidental compiler/build-tree references. Repacked ELF files may need interpreter/RPATH repair for Nix; test them on NixOS rather than assuming a generic Linux archive works. See the [Nixpkgs manual](https://nixos.org/manual/nixpkgs/unstable/).

## Flatpak and Flathub

Map variants to the application's valid ID, remote, and branch instead of inventing three store IDs. Users install binary Flatpaks even when the manifest builds from source. Flathub requires source-available applications and bundled runtime dependencies to build from source, subject to approved exceptions. Do not submit a routine duplicate `-bin` repack to Flathub.

Flathub's current requirements prohibit nightly/development snapshots in both stable and beta. Use a project-controlled Flatpak remote for main snapshots and unsupported binary-repack variants. Do not treat beta as an unrestricted nightly channel or assume Flathub accepts every CLI, library, or service. Confirm eligibility and current branch policy in [Flathub requirements](https://docs.flathub.org/docs/for-app-authors/requirements).

Use an appropriate supported runtime, build with the SDK, and ship neither the SDK nor dependencies already provided by that runtime. Prune build-only output through manifest cleanup while retaining required licenses and integration metadata. Minimize permissions and verify portals and actual application functions. See [dependencies](https://docs.flatpak.org/en/latest/dependencies.html), [manifest cleanup](https://docs.flatpak.org/en/latest/manifests.html#cleanup), and [hosting a remote](https://docs.flatpak.org/en/latest/hosting-a-repository.html).

## Homebrew

Prefer one formula with tagged source, matching bottles, and `head` on main. Native modes map to source via `--build-from-source`, binary installation through a compatible bottle, and main via `--HEAD`. Record the resolved HEAD commit. A bottle is a build of the formula, not a distinct upstream binary repack. An owned tap can maintain alternate formula identities when needed; do not force redundant `-bin`/`-git` formulae into core.

Core acceptance requires source builds or eligible platform-independent output and a stable release. Binary-only platform-specific software does not become a valid core formula merely by adding a hash. Use casks for eligible macOS applications, not as a Linux binary channel. Separate build/test dependencies and verify bottle OS/CPU compatibility and relocation. See [Formula Cookbook](https://docs.brew.sh/Formula-Cookbook), [bottles](https://docs.brew.sh/Bottles), and [Acceptable Formulae](https://docs.brew.sh/Acceptable-Formulae).

## Scoop

For Windows applications, prefer architecture-specific archives with verified hashes, minimal command shims, and optional integrations as suggestions. An owned bucket can carry `package`, `package-bin`, and `package-git` identities, but source builds require reviewed custom scripts and an explicitly supported toolchain. They are not a native source mode. Keep compiler requirements out of the binary manifest. A main snapshot may instead install a prebuilt binary of the recorded commit.

Wire and test native `checkver`/`autoupdate` for supported manifests, ensuring URL and checksum updates agree. Check actual bucket acceptance and variant collisions. See [app manifests](https://github.com/ScoopInstaller/Scoop/wiki/App-Manifests) and [autoupdate](https://github.com/ScoopInstaller/Scoop/wiki/App-Manifest-Autoupdate).

## Chocolatey

Use a suitable Windows installer or portable payload. Native `.install` and `.portable` suffixes describe installation form, not source versus binary. Prefer native prerelease versions or deliberate separate package IDs for development builds according to feed policy. Do not assume same-ID side-by-side installation is supported; separate IDs still need collision-safe application paths and shims.

An owned feed may implement source/bin/git identities through reviewed PowerShell packaging scripts, but a source variant is conditional on a supported build toolchain and feed policy. Do not add compilers to ordinary binary installs. Reuse declared runtime dependencies and avoid embedding duplicate installers or optional components. See [package creation](https://docs.chocolatey.org/en-us/create/create-packages/) and [automatic packaging](https://docs.chocolatey.org/en-us/create/automatic-packages/).

## WinGet

Assess WinGet explicitly whenever the application has a supported Windows build. Use a validated manifest for the tagged installer or portable artifact, architecture, scope, version, and `InstallerSha256`. Native manifests install binaries; there is no native source-build recipe equivalent. Keep the source-build route in the repository or another suitable ecosystem rather than manufacturing a compiler-installing wrapper to claim WinGet source support.

Map stable and main-snapshot binaries to distinct identities where accepted, such as `Publisher.Package` and `Publisher.Package.Nightly`. Use an immutable, versioned artifact for each snapshot. The assessed manifest schema marks `Channel` unimplemented, so do not rely on that field without checking current support. Verify public winget-pkgs acceptance or use an appropriate owned source. Test silent install, upgrade detection, uninstall, architecture selection, and command aliases. See [WinGet manifest documentation](https://github.com/microsoft/winget-pkgs/blob/master/doc/manifest/schema/1.10.0/installer.md).

## DEB

A native source package, such as `.dsc` plus source/packaging archives, builds installable binary `.deb` files. Keep these under the normal source/binary relationship. An ordinary `.deb` is not an install-time source build and does not need `-bin` just because it contains machine code.

For an owned repository that needs separate source-built and upstream-repacked products, use explicit `package`/`package-bin` identities and a `package-git` snapshot identity where policy allows, or isolated stable/development suites. Record that deviation. Define version ordering and `Provides`, `Conflicts`, `Breaks`, or `Replaces` only as appropriate to the actual transition. Do not claim safe coinstallation from different names alone.

Separate `Build-Depends` from generated/verified runtime dependencies, split development/docs/debug payloads where useful, and preserve conffiles and maintainer-script behavior. Build and test against each declared current distro/ABI target rather than converting one foreign package. See Debian [source packages](https://www.debian.org/doc/debian-policy/ch-source.html), [shared libraries](https://www.debian.org/doc/debian-policy/ch-sharedlibs.html), and [relationships](https://www.debian.org/doc/debian-policy/ch-relationships.html).

## RPM

A spec and source RPM describe the source build; binary RPMs are its installable products. Keep that native relationship. In an owned repository, distinct source-built, upstream-binary, and main-snapshot products may use the logical suffixes or separate repositories if the target distribution permits. Native `Version`/`Release` ordering must preserve upgrades across snapshots and tagged releases.

Separate `BuildRequires` from runtime `Requires`, retain automatic dependency detection, use target macros and hardening, and split development/docs/debug output as appropriate. Verify package relationships, scriptlets, configuration handling, and install/upgrade/removal on each declared RPM distribution. Fedora and openSUSE policies and environments are not interchangeable. Check current destination rules in addition to the [RPM spec format](https://rpm.org/docs/latest/manual/spec.html).

## Additional targets, selected conditionally

| Target | Applicability and native variant mapping | Lean and portability checks |
| --- | --- | --- |
| Direct archives | Buildable tagged source archive, per-target tagged binary archive, and immutable commit-labeled main snapshots. Use `.tar.*` or `.zip` as appropriate | Stage only installable payload; document runtime requirements, checksum, baseline, and install/remove steps. Source archive must actually rebuild |
| AppImage | Linux runnable applications suited to a self-contained image. Source recipe/archive is separate from the binary image; publish release and main-snapshot images distinctly | Bundle dependencies absent from declared current targets, without blindly bundling libc/graphics drivers. Verify FUSE/extraction behavior and real GUI/CLI execution. [Concepts](https://docs.appimage.org/introduction/concepts.html) |
| Snap | Applications/services compatible with snap runtime and confinement. Source recipe builds the installed snap; tagged releases use stable and main snapshots use edge where appropriate | Native channels replace forced suffixes. Distinguish build, stage, and prime content; preserve required base/content runtime and interfaces. [Channels](https://documentation.ubuntu.com/snapcraft/8.14.1/reference/channels/), [project format](https://documentation.ubuntu.com/snapcraft/latest/reference/project-file/snapcraft-yaml/) |
| Alpine APK | Application and dependencies support musl/BusyBox. APKBUILD builds binary APKs; distinct repacks/snapshots belong in an appropriate owned repository when needed | Freeze main snapshots, use native checksums such as `sha512sums`, separate build/check/runtime dependencies and split outputs. A glibc binary is not a musl build. [APKBUILD](https://wiki.alpinelinux.org/wiki/APKBUILD_Reference) |
| Gentoo | Source ebuild for the release; `package-bin` for a distinct upstream binary; live main is normally the same package at version `9999`, mapping logical `-git` to that form | Use an appropriate overlay for live recipes, record revision, declare build/runtime dependencies and optional USE flags, and test binary installs. Portage-built binary packages differ from `-bin` repacks. [Ebuild format](https://devmanual.gentoo.org/ebuild-writing/file-format/index.html), [VCS sources](https://devmanual.gentoo.org/ebuild-writing/functions/src_unpack/vcs-sources/index.html) |
| Guix | Source definition with binary substitutes under the same identity; main variant resolves to a fixed commit in a maintained channel | Upstream binary repacking is conditional on compatibility and distribution policy, not equivalent to substitutes. Split outputs, separate native/runtime inputs, and measure `guix size`. [Manual](https://guix.gnu.org/manual/en/guix.pdf) |
| FreeBSD ports/pkg | Only when application and dependencies support FreeBSD. A port builds the binary package; snapshot or alternate ports require appropriate naming and policy | Linux compilation is not FreeBSD evidence. Use native dependencies/options, stage checks, and clean build/install verification. [Ports and packages](https://docs.freebsd.org/en/books/handbook/ports/) |
| Native macOS installers | Supported macOS application and packager: app bundle, DMG distribution image, or PKG installer as appropriate; separate source recipe/archive and opt-in snapshot identity | Minimal runtime/framework set, supported architectures/deployment target, relocation, signing/notarization when required, and clean install/remove checks |
| Native Windows installers | Supported Windows application and packager: MSI, MSIX, EXE, or portable ZIP according to product needs; source route remains separate | Reuse the verified artifact across catalogs when contracts match. Validate scope, runtime dependencies, repair/upgrade/uninstall, architecture, signatures, and snapshot identity |
| Mac App Store / Microsoft Store | Conditional destinations for eligible native applications, assessed separately from producing a DMG/PKG/MSI/MSIX/EXE. Use accepted release/testing identities; do not assume public nightly or source-build channels | Verify current store policy, sandbox/entitlements, signing, installer/update model, and review requirements. Keep unsupported variants in direct/project-owned distribution. [macOS distribution](https://developer.apple.com/macos/distribution/), [Windows packaging](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/packaging/) |
| Language registries | A publishable library, CLI, or component with appropriate metadata. Use native source/binary artifacts and immutable versions/prerelease channels, not universal suffixes | See [language and build options](language-and-build-options.md); avoid publishing internal workspace modules just because a manifest exists |
| OCI images | Deployable service or container-oriented CLI with a supported image runtime. Source/build recipe plus immutable release and main-snapshot image digests | Multi-stage build, minimal final runtime, native architecture images, no compiler/cache/source leakage. Preserve certificates, user/timezone data, libraries, and health behavior that the application needs. [OCI image specification](https://github.com/opencontainers/image-spec) |

For targets with no native source or upstream-binary mode, mark that variant unsupported and provide the build recipe/source archive as a separate route. Do not hide that limitation behind a renamed binary. Verify update discovery for every maintained recipe, feed, manifest, base image, and development channel.
