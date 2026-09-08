# Feature specification: Linux platform skills

**Branch**: `feat/linux-platform-skills`
**Created**: 2026-09-07
**Status**: Implemented; local validation complete

The user requested useful Arch, CachyOS, Omarchy, and NixOS coverage following a
collection workflow audit. Add only platform decisions absent from existing
package-authoring, upgrade-recovery, and health workflows. No live host changes
are implied by these reusable instructions.

## Acceptance scenarios

1. An Arch service or package-selection request identifies configuration and
   package ownership, chooses a scoped change, and verifies runtime behavior.
   PKGBUILD work and failed transactions keep their existing specialist owners.
2. A CachyOS driver, optimized-repository, or scheduler request checks the actual
   installed tools, CPU compatibility, kernel/modules, and packaged defaults.
   It does not replace distribution policy with stock Arch or Omarchy commands.
3. A NixOS configuration request resolves the repository and named host, preserves
   its channel/flake and Home Manager model, and separates evaluation/build from
   test, boot, switch, rollback, and persistent-data migration.
4. A plain Arch/CachyOS terminal edit does not invoke Omarchy. A real Omarchy
   installation retains its packaged-file protection and desktop guides.
5. Existing user authorization survives specialist handoffs. Audit-only work stays
   read-only; build success does not authorize activation or prove a successful boot.
6. New skills have local provenance, resolving references, standard install targets,
   and pass repository checks. Scenario walkthroughs and source verification are
   explicitly distinguished from live-host execution and host discovery tests.
7. NixOS development VMs and integration tests reuse pinned system modules and
   isolated fixtures, prove runtime assertions, and never activate the host as
   an incidental test step. Ordinary Nix/devenv shells remain separate.

## Boundaries

No OS installation, disk partitioning, distro conversion, fleet expansion, skill
installation, or new release is part of this feature. Existing Arch upgrade and
package skills remain canonical. Nix package authoring and ordinary dev shells
are outside the NixOS system skill unless they affect a system configuration.
