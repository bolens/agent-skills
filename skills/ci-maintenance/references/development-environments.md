# Portable development environments

Use when configuring development tools, reproducing environment-sensitive CI,
or auditing local/editor/CI drift. Prefer mise, devenv or another established
portable environment, and devcontainers when they reduce setup work and version
drift. Choose the smallest useful combination; their presence is not itself an
acceptance criterion. Preserve a working project choice unless a scoped migration
has a concrete benefit.

## Choose ownership once

| Need | Preferred fit |
| --- | --- |
| Pinned language runtimes and standalone development tools | Repository-owned mise configuration and supported lockfile |
| Native libraries, reproducible system packages, isolated development services | Existing devenv/Nix shell or equivalent declarative environment |
| Reproducible OS configuration and multi-service system integration | NixOS development VM or NixOS test-driver scenario |
| Portable editor onboarding and a repeatable Linux userspace | Dev Container configuration backed by the same tools and tasks |
| Kernels, drivers, boot, hardware, or native desktop integration | Appropriate host/VM verification alongside portable checks |

Keep each tool's version authoritative in one place where practical. If Nix,
mise, and a container must each declare a version, document why and check their
alignment or intended differences. Do not stack managers that each install a
competing copy of the same tool. Keep the repository's Make, package-manager, or
other native targets as the check contract; an environment wrapper calls them.

## mise and CI

Prefer project `mise.toml` over unrelated global installs for repository tooling.
Inspect configuration, task hooks, and backend sources before trusting them.
Pin tool versions and mise itself when its behavior is part of the build contract.
Use supported lockfiles and verify artifact coverage for each intended OS/CPU;
a Linux lock entry does not prove a macOS or Windows install. See
[mise lockfiles](https://mise.jdx.dev/dev-tools/mise-lock.html).

Run the same commands through `mise exec -- COMMAND` or existing mise tasks in
local development and CI. Shell activation is unnecessary in CI. With a supported
committed lockfile, use `mise install --locked`; check installed-version support
before adding flags. Pin a setup action by full SHA, preserve its cache/trust
boundary, and keep the tool versions in repository configuration rather than
duplicating them in workflow inputs. See [mise CI guidance](https://mise.jdx.dev/continuous-integration.html).

Keep updater coverage explicit. Dependabot support for an action or Dockerfile
does not establish coverage of `mise.toml`, `mise.lock`, `devenv.lock`, or flake
inputs. Check the chosen updater's current support; retain Renovate or a documented
review workflow when it owns those files. Test resolved updates before delivery.

## devenv and related Nix environments

Reuse existing `devenv.nix`, `devenv.yaml`, `devenv.lock`, or flake definitions.
Pin the environment inputs and CLI, inspect the input diff on update, and use the
project's noninteractive entrypoint in CI. Do not migrate channels/flakes or add
daemon trust keys merely to reproduce a test.

`devenv test` executes the configured environment tests and can start its declared
processes. Inspect `enterTest`, tasks, ports, data directories, and cleanup first.
Have it call the native gate, not merely print tool versions. Keep service state
task-scoped and confirm cleanup after failure. See [devenv tests](https://devenv.sh/tests/)
and [input pinning](https://devenv.sh/pinning/).

## NixOS development systems and VM tests

Prefer a NixOS development VM or integration test when reproducibility includes
systemd units, users/permissions, service topology, networking, or OS configuration.
Use [nixos](../../nixos/SKILL.md) for the modules, pinned host output, generation,
and activation contract. A normal `nix develop` or devenv shell does not reproduce
an entire operating system, and a container shares its host kernel.

Keep the development/test configuration in the repository and pin nixpkgs and
other inputs. Reuse production modules with explicit test overrides, synthetic
credentials, disposable disks, isolated networking, and bounded readiness checks.
Use the existing VM/test command locally and in suitable CI runners. Verify
virtualization/architecture prerequisites and inspect any host mounts or forwarded
ports before launch. Do not run `nixos-rebuild switch` on the developer's host to
test a guest configuration.

Prove the important behavior after the guest boots: service readiness, an actual
client operation, and the relevant rejection or recovery path. A VM derivation
that builds is not a passing integration test. Preserve the test-driver logs and
clean up only owned guests and scratch disks. Missing KVM or a compatible builder
is an explicit coverage gap, not permission to disable assertions. Add this layer
only when the OS boundary earns its startup and maintenance cost.

## Devcontainers

Inspect `devcontainer.json`, its actual Dockerfile/image/Compose source, Features,
workspace mount, user/UID behavior, and lifecycle commands. Review inherited image
metadata too. Some initialization runs on the host; setup is not necessarily
confined to the container. Use the
[Dev Container specification](https://github.com/devcontainers/spec/blob/main/docs/specs/devcontainerjson-reference.md)
for execution order and ownership.

Pin image digests and supported Feature dependencies. Reuse the same mise or
devenv declarations where practical, keeping system packages in the appropriate
layer. Preserve a non-root development user, writable workspace, correct base path,
and locked dependency install. Re-running setup must preserve user files and data.
Do not bake checkout secrets into images, mount the whole home, grant privilege,
or expose a Docker socket without a demonstrated need and existing authority.

Build the actual devcontainer image, exercise setup/lifecycle behavior with a
disposable checkout, then run the native gate inside it. A successful Dockerfile
build does not prove post-create commands or editor attachment. A separate Nix
container is not validation of `.devcontainer/Dockerfile`. Include the actual
environment paths in CI selection and require the selected checks to finish.

Use [prebuilt images](https://containers.dev/guide/prebuild) when measured setup
cost justifies maintenance. Define who refreshes their inputs and how clients
select the verified digest. Building for verification and pushing an image are
separate actions; do not publish from untrusted PR validation.

## Environment contracts and specification-based examples

Prefer a tracked `.env.spec` over `.env.example` or `.env.sample` when adding or
improving an environment contract. Document each key's purpose, required/optional
status, type or constraints, safe default, scope, and secret classification.
Keep real credentials and operator values in the existing ignored runtime file or
secret provider. A required secret has no usable example credential or fallback.

The filename alone provides no validation or automatic loading. Inspect the
project's loader and validator and choose a supported syntax. For a plain dotenv
contract, comments can describe constraints, but they are documentation until a
validator enforces them. Tools that interpret annotations may treat assigned
strings as descriptions rather than runtime defaults; never blindly source or
copy that contract into a runtime environment. See the concrete
[Runme environment specification example](https://runme.dev/blog/substitute-yaml-with-nouns-verbs)
for one tool-specific implementation, not a universal format.

Make `.env.spec` authoritative for the contract, with the existing application
schema enforcing it or a supported validator checking it. Avoid independently
maintained lists of keys. Wire setup, documentation, CI and container checks to
that owner. When migrating an existing example, update all consumers and explicit
env-file paths together. Keep a generated compatibility example only if a consumer
requires it; verify it stays synchronized. Do not rename files by extension alone,
overwrite live `.env` files, or assume mise, Compose, devenv, or a devcontainer will
automatically discover `.env.spec`.

Validate with synthetic fixtures: a valid minimal environment, missing required
keys, malformed values, and optional defaults. Report key names and constraint
failures without values. Keep interpolation inputs distinct from variables passed
to a service. Prove setup preserves an existing runtime file on repeat execution.

Apply the same principle to other examples when it prevents drift: derive API
examples from an existing OpenAPI contract, check configuration fixtures against
their JSON Schema or native schema, and validate Compose examples with Compose.
Reuse the ecosystem's actual specification and filename; do not invent `.spec`
extensions for every file. Keep useful runnable examples, generate them where
practical, and test representative success and rejection cases against their
owning contract. A schema check does not establish runtime service behavior.

For environment precedence, repeatable setup/diagnostics, concurrent services,
generated-output drift, or optional SecretSpec integration, read
[setup and runtime contracts](setup-contracts.md). Keep these checks scoped to
the environment path being introduced or repaired.

## Verify the developer path

Start from a clean environment or disposable checkout that cannot borrow the
maintainer's global tools, caches, credentials, or generated files unnoticed.
Verify bootstrap, actual versions, dependency installation, native checks, and
repeat setup. Test a known failing command through the wrapper when introducing
it so an environment success message cannot hide failed application checks.

Record platform coverage and compare cold/warm setup time or removed manual steps
when that motivated the change. Cache keys should reflect tool/input identity,
OS/architecture, and trust scope. A warm cache is an optimization, not a substitute
for locked inputs. Report untested editor, engine, native-host, and offline paths
without promising that every environment is equivalent.
