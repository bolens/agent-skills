# Development VMs and system tests

Use NixOS when the development environment must reproduce service configuration,
users, permissions, or network interactions across a complete system. For pinned
compilers and ordinary application dependencies, a Nix/devenv shell is usually
enough. Follow the shared [portable environment contract](../../ci-maintenance/references/development-environments.md).

Inspect the project's existing VM or NixOS test-driver entrypoint and pinned
nixpkgs API. Reuse modules with explicit development overrides rather than copying
a production configuration and its secrets. Keep fixture data, guest disks,
credentials, network endpoints, and optional host shares explicit and disposable.
Do not regenerate the developer's hardware configuration for a guest.

Check the runner's supported architecture, QEMU/KVM access, builder, and resource
limits. Build and start the selected guest or test through the repository command.
Wait for bounded service readiness, then assert an actual client/server operation
and an applicable failure or recovery path. For multiple nodes, identify which
node acts as the client and which owns each service.

Follow [NixOS VM integration testing](https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html)
at the pinned revision for test-driver APIs. Keep passing build, successful guest
boot, observed assertions, and physical-host verification distinct. Retain useful
driver logs, stop owned guests on success or failure, and remove only disposable
state. VM success does not prove physical GPU, firmware, or boot-device behavior.
