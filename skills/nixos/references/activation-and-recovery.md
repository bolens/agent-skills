# Activation and recovery

Use the installed `nixos-rebuild --help`, repository deployment command, and
[NixOS manual](https://nixos.org/manual/nixos/stable/#sec-changing-config).
Resolve local/build/target hosts and the named configuration before execution.
Flags and wrapper semantics can differ across installed versions.

| Action | Effect |
| --- | --- |
| `build` | Builds a candidate without activating it |
| `test` | Activates now without making it the boot default |
| `boot` | Selects the next boot configuration without activating now |
| `switch` | Activates now and selects the boot default |

For example, `nixos-rebuild build --flake .#HOST` is a preparation command only
after replacing `HOST` with the repository's actual output. Prefer its native
wrapper when that owns target selection. Never mechanically advance from build
to test to switch without checking the requested endpoint.

Record the current system path, candidate output, retained known-working
generation, and affected service or boot behavior. Compare the closures with
available Nix tooling when the change is substantial. Keep the previous generation
and its store paths until acceptance; do not combine a risky upgrade with garbage
collection or deletion of old generations.

Before a remote SSH/firewall/network change, establish console or other recovery
access and any repository-supported rollback mechanism. A build machine is not
the deployment target. VM checks can exercise configuration behavior but do not
establish physical storage, GPU, bootloader, or remote connectivity correctness.

After activation, inspect failed units, relevant logs, and the specific application
or network path. Record running and boot-selected state separately. Kernel and
early-boot changes still require reboot evidence. User services may require their
own application path; a system rebuild does not prove every user session reloaded.

Use the retained generation and documented rollback command when rollback is
authorized, then verify its actual effects. Activation scripts and applications
may already have modified databases or files under `/var`. Restoring system
software cannot reverse those writes. Identify required data recovery separately.
