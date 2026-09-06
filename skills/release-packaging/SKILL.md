---
name: release-packaging
description: Design, implement, and verify portable release packages, source/binary/main variants, and lean installations across native package managers, app stores, and language registries. Use for packaging strategy, new distribution targets, release artifact preparation, or package portability and size work. Keep publication coordination, isolated dependency updates, and live system upgrades with their existing owners.
---

# Portable release packaging

Build packages appropriate to the repository's language, build tooling, application type, and supported platforms. Prefer broad compatibility across current stable and rolling systems over support for legacy dependency versions. Read the repository's release and compatibility contracts first. Preserve explicit support promises until an authorized migration changes them.

A packaging audit stays read-only. Implementation authorizes scoped recipes, builds, and isolated verification. Signing, store submissions, public tags, publication, and installation on a live host retain their existing authority requirements. Complete a reviewable candidate before asking for missing delivery authority.

## Select targets from actual capabilities

Inspect manifests, lockfiles, build and install commands, release workflows, native dependencies, runtime requirements, existing artifacts, and available target runners. In a monorepo, assess each release unit rather than treating every detected language as a publishable product. Review executable packaging hooks before running them.

Read [language and build options](references/language-and-build-options.md) to identify available outputs. Assess Arch/pacman, Nix, Flatpak/Flathub, Scoop, Homebrew, Chocolatey, DEB, RPM, and WinGet by default. Also assess direct archives, AppImage, Snap, Alpine APK, Gentoo, Guix, FreeBSD ports/pkg, native macOS/Windows installers, applicable language registries, and OCI images. Every target is conditional on actual capabilities and intended use. A language with a Windows compiler does not establish that the application's native dependencies work on Windows.

Record each target as **supported**, **conditional**, or **inapplicable**, with the reason, OS/architecture/libc, artifact/recipe format, destination, and validation needed. Separate technical build support from public-repository acceptance and available evidence. Do not silently omit WinGet or other requested targets, force desktop packaging onto a library, or treat missing credentials as proof that a platform is unsupported.

Use [semantic conventions](../git-hygiene/references/semantic-conventions.md) for SemVer release versions, prerelease identity, and immutable publication. Preserve native package revisions and test their ordering independently of upstream SemVer. A main-tracking build needs an ordered native snapshot version, not only changed build metadata.

## Map variants to native behavior

Read [targets and variants](references/targets-and-variants.md) for the selected ecosystems. Use this logical contract:

| Variant | Meaning |
| --- | --- |
| `package` | Build from the source of a tagged release |
| `package-bin` | Install the matching upstream prebuilt tagged-release payload |
| `package-git` | Build from the resolved tip of main, with the exact revision recorded |

Prefer those names where the packaging system and destination allow distinct identities. Otherwise record the native equivalent: build mode, source/binary companion artifacts, live ebuild, branch, or prerelease identity. Binary caches and bottles built from a source recipe do not require a separate upstream-binary package. Multiple available versions do not imply that variants can coexist. Define file, command, service, and application-ID conflicts or a deliberate coinstallation layout.

Resolve a release tag to its immutable commit and verify source/payload hashes. A main-tracking recipe may follow main at update/build time, but each candidate must freeze or record the actual resolved commit before producing artifacts. Coordinate all platform jobs around that same candidate. Use native monotonic versioning and test ordering against prior snapshots and stable releases. Keep development channels opt-in and published artifacts immutable; do not move a public release tag or overwrite a version to refresh main.

Prefer SHA-pinned build dependencies and Dependabot monitoring where supported, following [dependency update guidance](../triage-dependency-updates/SKILL.md#prefer-immutable-pins-with-update-monitoring). Use each ecosystem's native integrity algorithm and updater when needed. Record uncovered recipe inputs, SDK/runtime updates, and snapshot-refresh ownership. A floating development source is a deliberate variant, not a reason to float the rest of the toolchain.

## Build for current platforms with lean runtime payloads

Read [lean builds and portability evidence](references/lean-portability.md) before choosing flags, bundling dependencies, or trimming outputs. Select a documented compatibility floor within the current target set. Do not automatically choose an obsolete build image or freeze old dependency versions to maximize historical reach. Recheck current official platform and tool documentation when implementing a concrete target.

Use native package dependencies and layouts where available. Keep build/check tools out of runtime dependencies and shipped files. Bundle only what the target's runtime model requires. Preserve application behavior, hardening, required plugins/assets, licenses, and repair/upgrade support. A smaller archive is not sufficient evidence of a lean installation.

Build and inspect source and binary variants separately where their dependency or feature profiles differ. Publish complete buildable source inputs, including required generated files or vendored sources. Use clean target environments and measure compressed payload, installed files, runtime closure, and incremental install cost as applicable. Explain regressions against the prior release or initial declared budget.

## Verify and hand off

Validate the exact artifacts, not just a build directory. Run native recipe/schema linting and clean install, representative runtime, upgrade, variant-transition, and removal checks where supported. Verify CPU/ABI, dynamic dependencies, configuration/data preservation, permissions, and native version ordering. Record missing runners or inaccessible store checks as unverified. Cross-compilation alone does not prove runtime portability.

Return a concise receipt: capability-based target matrix, native variant mapping, tag/commit and input identity, artifact hashes, target baselines, measured sizes/closure, checks and their environments, update coverage, publication state, and remaining work. Reuse the repository's release evidence format.

Use [arch-package-maintenance](../arch-package-maintenance/SKILL.md) for PKGBUILDs and clean Arch builds, [ci-maintenance](../ci-maintenance/SKILL.md) for build matrix/trust changes, and [sensitive-info-audit](../sensitive-info-audit/SKILL.md) for actual publication boundaries. When preparing or publishing a concrete release, use [babysit](../babysit/SKILL.md) as the delivery coordinator and return packaging evidence to the active workflow. A packaging strategy or local recipe edit alone does not start publication follow-through.
