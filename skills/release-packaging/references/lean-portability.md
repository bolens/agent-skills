# Lean builds and current-platform portability

Portability means the declared targets work, not that one archive runs on every historical system. Prioritize current stable and rolling distributions and current supported runtimes. Choose a common compatibility floor within that target set or build separate artifacts where ABI/runtime differences require it. Support older systems only when explicitly required by the user or repository. Do not silently remove an existing support promise.

## Define the target contract

Record OS/distribution family, release/runtime policy, CPU architecture and instruction baseline, libc/ABI, loader, shared libraries, graphics/display stack when relevant, and install layout. Verify current versions instead of copying static versions from this guide. Candidate Linux coverage includes current Arch, a current DEB distribution, and a current RPM distribution; add Alpine/musl and NixOS when those targets are selected. Choose macOS, Windows, and FreeBSD environments only where the product supports them.

Prefer standards-based APIs and portable build/install interfaces. Avoid accidental GNU-only shell utilities, hardcoded home paths, build-machine paths, or assumptions that systemd, Bash, glibc, `/usr/lib`, or a writable application directory exists everywhere. Platform-specific integration may be necessary; keep it in target-specific recipes rather than exporting the assumption to every build. Support configurable install prefixes and staged installs when the build system permits.

For generic native binaries, avoid host CPU tuning such as `-march=native`. Inspect executable format, architecture, interpreter, needed libraries, symbol-version requirements, RPATH/RUNPATH, and embedded paths. Use tools that inspect artifacts without executing untrusted code. A successful build on a current rolling host can still require newer glibc symbols than another current supported distribution supplies. Choose an appropriate build environment or native per-target build, then test it.

Do not treat glibc and musl as interchangeable. Static linking is conditional on libraries, licensing, plugins, DNS/NSS, certificate lookup, and other runtime behavior. Test those paths before removing dynamic dependencies. On macOS verify deployment target and library paths; on Windows verify runtime DLLs and installer behavior. Cross-build output needs target execution evidence, whether native or explicitly qualified emulation.

## Keep runtime cost explicit

Define the smallest feature profile that still meets the product contract. Disable unused optional backends, examples, benchmarks, and developer tools at build configuration time where possible. Do not remove required functionality, accessibility, cryptography, hardening, crash diagnostics, dynamic plugins, or localization merely to shrink a number.

Separate build/check dependencies from runtime dependencies using native recipe fields. Keep compilers, headers, static development archives, test frameworks, package caches, VCS metadata, and temporary source/build trees out of ordinary binary installations unless they are part of the product. Split development, documentation, debug, plugin, and optional integration packages or outputs when the ecosystem supports them. Preserve licenses, attribution, required source offers, metadata, and useful user help.

Distinguish install footprint from source-build prerequisites. A source build can need a compiler without making that compiler a runtime dependency. Keep source releases complete enough to rebuild, including required generated sources and vendored inputs for offline builds. Do not prune source archives using a binary payload allowlist.

Prefer system runtime dependencies for native distribution packages when ABI and distribution policy permit. For Flatpak/Snap use the appropriate shared runtime/base and bundle only missing dependencies. For Nix/Guix inspect references that keep build tools in the runtime closure. For AppImage, standalone executables, and framework bundles include the dependencies absent from declared targets. A required runtime is not automatically bloat.

Use production/release builds. Consider dead-code elimination, LTO, symbol splitting, and runtime trimming only when supported and measured. Preserve distribution hardening flags. Do not universally force maximum compression, static linking, panic-abort, disabled runtime checks, AOT, or executable packers. Smaller bytes can increase startup cost, build cost, diagnostic loss, or compatibility failures.

## Measure the actual installation

For each materially different target/variant, record compressed download size, unpacked package size, installed payload size, and runtime dependency closure as available. Distinguish cold install cost from incremental cost when a shared runtime or dependency is already installed. Deduplicate shared dependencies when reporting closure cost and state the measurement method. A tiny manifest that downloads a large installer is not a tiny installation.

Compare with the previous release of the same target/profile. For new packages establish an initial budget from the actual required payload. Investigate unexpected growth, duplicate libraries/runtimes, debug or source leakage, and unnecessary optional dependencies. Record the reason for retained cost. Build one shared payload only where target contracts genuinely match; do not combine every architecture, debug build, or runtime into every installer for convenience.

Useful native evidence includes archive file listings, DEB/RPM/APK metadata, Arch package metadata, `nix path-info --closure-size`, `guix size`, Flatpak app/runtime breakdowns, and installer staging manifests. Select installed tools and verify their current syntax. Host measurements alone cannot certify remote target behavior.

## Verify artifacts in clean target environments

1. Rebuild from the published source candidate with declared tools and dependencies. Verify input identities, configured features, and repeatability limits.
2. Inspect native recipe/schema lint results, archive contents, permissions, runtime dependencies, licenses, metadata, and hashes.
3. Install the exact binary artifact on each supported target or representative equivalent justified by its ABI contract. Test version output and real work, including plugins, network/TLS, fonts, desktop integration, or service behavior as relevant.
4. Test upgrade from the prior supported release, snapshot version ordering, variant switching/coinstallation rules, and removal. Preserve user data/configuration and verify that commands/services are not left pointing at another variant's removed files.
5. Record passed, failed, skipped, and unavailable checks with target environment and artifact hash. Keep untested platforms explicitly unverified; a green cross-compile or package lint is not runtime proof.

Use unprivileged builds and disposable containers/VMs where appropriate. Review package hooks before execution. Native package tests do not authorize changing the workstation's installed packages or publishing to a store.
