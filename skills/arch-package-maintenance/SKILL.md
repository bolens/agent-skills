---
name: arch-package-maintenance
description: Maintain Arch PKGBUILDs, local package patches, source verification, clean builds, package metadata, and retirement of pinned rebuilds. Use for package authoring or repair, not routine system upgrades or general dependency updates.
---

# Arch package maintenance

Identify the package source, local patch contract, and intended installation target before executing a build recipe. This workflow is Arch-specific. Use installed Arch packaging tools and current official documentation.

## Inspect before execution

Read repository instructions, PKGBUILD, install scripts, patches, source URLs, checksums/signature policy, `.SRCINFO`, and the reason for any local pin. A PKGBUILD is executable shell code. Review its top-level commands and every build/install hook before sourcing it or invoking tooling that evaluates it. A clean chroot isolates dependencies but does not make untrusted code safe.

Determine whether the task changes upstream version, packaging revision, build flags, or local patches. Use the package's existing versioning and architecture conventions. Check runtime/build/check dependencies, `provides`, `conflicts`, split packages, configuration backup paths, and installed file ownership. Do not claim a package provides an ABI or kernel headers it does not supply. [PKGBUILD reference](https://man.archlinux.org/man/PKGBUILD.5.en).

## Build and inspect

Read [patches and build evidence](references/patches-and-builds.md) for clean-build selection, patch rebases, and pinned packages. Preserve patch provenance and the bug each patch addresses. Verify downloaded sources against the established trust source. Do not replace checksums or use `SKIP` merely to make a mismatch disappear.

Use the repository's packaging command and an appropriate clean Arch build environment. Select installed `devtools` commands for this package's repository layout, architecture, and toolchain. `pkgctl build` is one option, not a universal command for every AUR/local checkout. Run as an unprivileged builder with only the tool's necessary privilege boundary. [Arch build tooling](https://man.archlinux.org/man/extra/devtools/pkgctl-build.1.en).

Regenerate `.SRCINFO` from the reviewed final PKGBUILD when maintained by the repository. Inspect the built archive's metadata, file list, permissions, dependencies, hooks, and configuration handling. Use available package linting and targeted install/upgrade/removal tests in a disposable environment. A successful compile does not prove the package is installable or that a patch fixes its target defect.

Preparing a package does not authorize installing it on the workstation, changing `IgnorePkg`, uploading to AUR, signing, or publishing. Carry out those steps when the user has authorized them. Route live package transactions and boot/kernel recovery to [arch-update-recovery](../arch-update-recovery/SKILL.md), and release follow-through to [babysit](../babysit/SKILL.md).

Report source/version, patch decisions, build environment, package checks, regression evidence, and remaining installation or publication work.
