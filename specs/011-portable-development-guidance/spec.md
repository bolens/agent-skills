# Feature specification: Portable development guidance

**Created**: 2026-09-07
**Status**: Implemented; local validation complete

The user prefers mise, portable development environments such as devenv, and
devcontainers where they improve developer experience, reproducibility, and
maintenance. Apply that preference to CI and relevant maintenance skills without
requiring every repository to adopt every tool.

The user also explicitly included NixOS for reproducible development where
applicable. Select a NixOS VM or system test when the OS/service boundary matters,
with pinned inputs, disposable guest state, and observed runtime assertions.

Acceptance:

- A new toolchain setup considers mise before ad hoc global language installs.
- Existing Nix/devenv, devcontainer, and native tooling stays authoritative unless
  a scoped migration has a demonstrated benefit.
- Local, editor/container, and CI paths share pinned inputs and native check
  commands; intentional runtime differences are documented and tested.
- CI changes select affected environment paths, preserve required check names,
  and distinguish image builds from lifecycle/setup and application checks.
- Tool pins have verified update coverage or an explicit review owner. Secrets,
  host state, and release authority are not inherited by development setup.
- Scoped diagnostic and audit requests do not trigger environment migrations.

No change to this repository's CI execution model or host Nix daemon is required
by this instruction feature. Host development-tool installation is a separate
user-authorized action already in progress.

The user additionally requests `.env.spec` environment contracts and specification-based examples where useful. Acceptance includes explicit loader/validator support, coordinated consumer migration, private runtime preservation, and schema-backed synthetic success/failure fixtures rather than filename-only changes.
