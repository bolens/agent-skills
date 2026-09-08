# Platform assessment

Sources checked on 2026-09-07. These are original local workflows informed by
primary documentation, not imported upstream skills. Future operations must
recheck installed-version behavior and current distribution notices.

| Source | Decision supported |
| --- | --- |
| [pacman manual](https://man.archlinux.org/man/pacman.8.en) | Query package ownership and inspect selected transactions before mutation |
| [Arch maintenance](https://wiki.archlinux.org/title/System_maintenance) | Avoid partial upgrades and use isolated update discovery; direct access was challenged, indexed primary-source text was available |
| [CachyOS repositories](https://wiki.cachyos.org/features/optimized_repos/) | CPU-tier compatibility and configured repository order need distribution-specific evidence |
| [CachyOS hardware detection](https://wiki.cachyos.org/features/chwd/chwd/) | Profile queries and driver-changing operations are different actions |
| [CachyOS kernel manager](https://wiki.cachyos.org/features/kernel_manager/) | Use installed kernel tooling rather than assuming stock Arch procedures |
| [CachyOS settings](https://wiki.cachyos.org/features/cachyos_settings/) and [sched-ext](https://wiki.cachyos.org/configuration/sched-ext/) | Inspect packaged defaults and active policy, measure changes, and separate diagnostic collection from uploads |
| [NixOS manual](https://nixos.org/manual/nixos/stable/) | Build, test, boot, switch, and generation rollback have different effects |
| [NixOS configuration](https://wiki.nixos.org/wiki/NixOS_system_configuration) | Resolve modules and declarative ownership |
| [state version source](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/misc/version.nix) | Preserve compatibility state versions during ordinary upgrades |
| [Nix flakes](https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-flake.html) and [input updates](https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-flake-update.html) | Track source inclusion and inspect scoped lockfile updates |
| [NixOS VM integration tests](https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html) | Reproduce OS/service behavior with declared guests and runtime assertions |

Existing `arch-package-maintenance` already owns package authoring, and
`arch-update-recovery` owns upgrades and recovery. Retain them. `arch-linux` fills
configuration ownership and routine system administration, `cachyos` adds only
its distribution-specific decisions, and `nixos` fills a distinct declarative
system/activation model. Do not add a generic Linux umbrella or duplicate package
recipes. Scope Omarchy by actual configuration ownership.
