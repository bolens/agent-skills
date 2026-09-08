---
name: nixos
description: Configure, diagnose, and safely update NixOS hosts and reproducible development VMs through modules, pinned inputs, generations, and activation. Use for NixOS system configuration, recovery, or OS-level integration tests, not ordinary Nix shells, package recipes, nix-darwin, or standalone Home Manager on another OS.
---

# NixOS configuration and recovery

Resolve the target host and configuration source before editing. A machine with
the Nix package manager is not necessarily NixOS. Distinguish the current host,
a remote deployment target, and an offline configuration repository.

## Find the declarative owner

Read repository instructions, module imports, hardware configuration, deployment
commands, and the selected host output. Identify flake inputs and `flake.lock`,
or the existing channel/NIX_PATH model. Preserve that model rather than introducing
flakes as a side effect of a service fix. Resolve the named configuration instead
of inferring it from the local hostname.

Inspect options against the pinned nixpkgs revision and its module definitions.
An option in today's online manual may not exist at the repository's revision.
Trace merged definitions before using `mkForce` or overriding an assertion.
Keep host hardware, shared policy, secrets, and user configuration in their
established modules. Determine whether Home Manager is integrated or activated
separately before editing its source or promising a system rebuild applies it.

Read [the NixOS configuration guide](https://wiki.nixos.org/wiki/NixOS_system_configuration)
for module structure. Edit the source that generates a file, not its `/etc` link
or immutable `/nix/store` target. Keep secrets out of store-bound expressions and
generated text. Use the project's existing runtime secret mechanism.

## Change inputs and configuration deliberately

For a local option edit, preserve the lockfile. For an authorized input update,
update only the intended inputs using the installed Nix CLI, then inspect the
resolved revision and complete lockfile diff. Use
[input and evaluation guidance](references/inputs-and-evaluation.md).

Preserve `system.stateVersion` and any Home Manager state version during routine
upgrades. These select compatibility behavior for state, not the desired package
release. Change them only for a deliberate, documented state migration. Read the
[option's source contract](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/misc/version.nix)
and the corresponding module at the pinned revision.

## Build, activate, and recover

For reproducible development systems or OS-level integration, use
[development VMs and tests](references/development-vms.md). Keep guest activation
separate from host changes. Ordinary toolchain shells stay with the project's
Nix/devenv setup rather than becoming full NixOS machines.

Read [activation and recovery](references/activation-and-recovery.md) before
selecting a rebuild or deployment action. Use the repository's wrapper when it
exists, after inspecting its effects and target flags. Evaluation and build are
preparation. `test` changes the running system, `boot` changes the next boot,
and `switch` changes both; none is an interchangeable verification command.

Continue activation already authorized for the identified host and change. Ask
only when that authority or a consequential target choice is missing. Do not run
an activating command to satisfy a source-only review or build request. A remote
network, SSH, boot, or storage change needs a usable recovery path before activation.

After authorized activation, verify the active generation, affected services,
and original user path. A completed build, evaluation, or VM test does not prove
the target's boot, hardware, or network behavior. A failed switch can leave some
services changed; inspect actual state before retrying or claiming rollback.

Report target and source revision, changed inputs/options, build result, activation
mode and generation when applied, runtime checks, and remaining boot or hardware
evidence. Generation rollback does not restore mutable application data. Use
[backup-restore-verification](../backup-restore-verification/SKILL.md) when recovery
depends on that data, and [migration](../migration/SKILL.md) for its transition.
