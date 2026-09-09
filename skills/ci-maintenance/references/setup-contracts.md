# Development setup and runtime contracts

Read when implementing or diagnosing bootstrap, configuration loading, concurrent
local services, generated examples, or secret-provider integration. Reuse the
project's tools and native tasks; add only contracts that address its actual setup.

## Resolve environment precedence

Trace the actual launch path from shell/editor/CI through mise or devenv, container
configuration, and the application's loader. Record each supported profile, loaded
file, override order, and treatment of unset versus empty values. Check the working
directory and inherited parent configuration. There is no universal precedence
order across these tools. Inspect the installed versions and verify collisions
using synthetic values through each supported entrypoint.

Keep Compose interpolation inputs separate from the container's environment;
a host `.env` key is not automatically passed to the application. See
[Compose precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/)
and [mise environments](https://mise.jdx.dev/environments/).

Diagnostics should report key names, missing/invalid status, and the source that
won when it can be established, without printing values or entire environments.
Report unknown origins honestly if the loader discards that information. Avoid
unfiltered resolved Compose output with real secrets. Do not read private files
forbidden by repository guidance just to explain precedence.

## Repeatable bootstrap and useful diagnostics

Prefer the existing setup task and a read-only diagnostic entrypoint, conventionally
called `doctor`, when recurring onboarding failures justify one. Check required
versions, accessible runtimes/builders, configuration presence, and relevant ports
or permissions. Distinguish required failures from unavailable optional features;
give an exact scoped repair command and a useful nonzero status for blockers.
Inspect hooks before claiming a wrapper is read-only: environment activation can
itself install dependencies or execute tasks. Do not resolve secret values merely
to test whether a provider is configured.

Bootstrap installs the committed inputs and creates only missing owned local
state. Repeating it must preserve operator values and data. Keep input updates,
service startup, and destructive reset as explicit actions rather than hidden
setup steps. Reuse native Make/package/mise/devenv tasks instead of adding a second
task runner for naming consistency. Verify a fresh setup, a repeat run, a missing
prerequisite, and an interrupted run followed by recovery; preserve failure status
through wrappers. Do not make diagnostics silently fix the machine.

## Isolate concurrent checkouts and services

A Git worktree isolates source/index state, not ports, databases, containers, or
writable caches. Assign a stable per-checkout identity using a collision-resistant
suffix; a branch slug alone can collide after normalization or across clones.
Use it for owned Compose project names, database/schema names, temporary/state
paths, sockets, and generated outputs as supported by the project. Check explicit
container/volume names, external resources, and bind mounts that bypass a Compose
project namespace. Share caches only where their locking and content identity
support concurrent use.

Prefer runtime-assigned ports and pass the actual endpoint to clients, tests,
and browser capture. Avoid probing a free port and assuming it stays free before
binding. If the application requires fixed ports, detect conflicts and isolate or
serialize that path. Never attach tests to an unrelated server merely because its
port answers. Preserve application identity checks and checkout-owned receipts.

Use the existing process supervisor and its dependency/readiness facilities. See
[devenv processes](https://devenv.sh/processes/) for its supported manager contract.
Wait with a deadline for the behavior the client needs: database query readiness,
a completed migration, or the expected application response. A running PID, open
port, or fixed sleep alone is insufficient. Keep fixture initialization and schema
migrations scoped to the disposable test service.

On timeout or interruption, retain bounded diagnostic logs and stop only owned
processes/resources. Cleanup must be safe to repeat and preserve other checkouts,
external volumes, and operator data. Verify two simultaneous checkouts can start,
exercise independent fixture data, and stop one without breaking the other when
introducing this isolation. Otherwise report concurrency support as unverified.

## Check generated contracts for drift

Keep `.env.spec`, schema-backed fixtures, and generated documentation under the
[environment contract](development-environments.md#environment-contracts-and-specification-based-examples).
Pin the generator and inputs. Regenerate into a disposable checkout or use its
native non-mutating check mode. Include the actual candidate inputs, including
owned uncommitted/new source files; a checkout of HEAD alone cannot verify pending
schema edits. Preserve unrelated work when constructing that candidate. Compare
the complete owned output set, including new, changed, and deleted files. A tracked-only diff can miss newly generated files.
Avoid tests that silently repair expected output before comparing it.

Run the same drift check locally and in CI. When output changes, inspect its owning
contract and regenerate rather than hand-editing the output. Check representative
valid and invalid fixtures against the configured schema dialect and validator.
[JSON Schema annotations](https://json-schema.org/understanding-json-schema/reference/annotations)
such as `default` and `examples` do not themselves apply runtime defaults or prove
examples valid. Test default application and coercion in the actual loader when
these are part of the contract; keep ordinary schema validation distinct.

## Optional secret contracts

Consider `secretspec.toml` when multiple developers or CI need the same declared
secrets from different providers, or preserve the project's existing equivalent.
See [devenv's SecretSpec integration](https://devenv.sh/integrations/secretspec/).
Check the pinned tool's provider/profile behavior before configuring it. Declare
requirements in one place; if `.env.spec` also describes these keys, generate or
check the overlap rather than maintaining conflicting required/default rules.
Secret declarations and ordinary non-secret configuration may have distinct owners.

Prefer runtime injection into only the process needing the secret. Keep values
out of Nix store-bound expressions, generated build outputs, whole-session exports,
logs, and shared artifacts. If the application requires a runtime secret file,
use the existing provider or private runtime mount with restricted permissions
and owned lifecycle; never bake it into an image or commit it. Retain existing
provider access and avoid provisioning accounts or changing CI secrets as an incidental setup step. Verify missing-provider and
missing-required-secret failures with a fake provider or synthetic fixtures;
assert that diagnostics stay value-free. An offline fixture is not proof that a
real provider's access, rotation, or production integration works.

## Browser workload ownership

Use one shared resource identity across every relevant entrypoint, checkout, and
agent client. Ephemeral ports and isolated profiles prevent address or data
collisions but do not limit CPU and memory use. Acquire capacity before launching
browsers or expensive setup. Prefer the repository's supported lock or supervisor
to a second skill-specific limiter. An isolated output directory is not permission
to bypass the host limit. Existing runs started before enforcement need separate
owner-coordinated completion or cancellation.

For advisory file locks, retain the lock inode across release and reacquisition.
Unlinking a held lockfile can let another process lock a different inode at the
same path. Distinguish a retained lockfile from an active OS lock. Never steal
ownership based only on a file's age or a missing progress message. State platform
limits explicitly and test the actual ownership primitive where it runs.

Surface contention as a distinct non-passing outcome in the outer task runner,
with the resource and available owner/run identity. Use a bounded wait or fail
promptly. The coordinator can resume after release while doing independent work.
Avoid tight retries and automatic relaunch loops. Preserve failure, timeout,
cancellation, and partial-result status through wrappers and package scripts.

Use focused suite and engine selection while iterating, then have the integration
owner run the final matrix against stable inputs. Combine pending requests only
when candidate inputs, runtime, build identity,
and requested coverage match. One run can return evidence to several task owners.
A running focused suite cannot satisfy broader coverage it did not execute.
Queue the missing scope or rerun affected checks after inputs change. Keep each
run's evidence separate even when execution is serialized, so the next owner
does not overwrite screenshots still needed for review.

Separate the execution deadline from graceful shutdown and forced cleanup budgets.
Allow existing cleanup hooks to finish before escalating: a native accessibility
runner's shutdown may need longer than an ordinary headless browser's. Hold capacity
until owned cleanup finishes. Test the full launch chain with contention, nonzero
exit, timeout, cancellation, and a child that ignores graceful termination. Verify
lock reacquisition and surviving owned browser processes, not just worker exit.
Browser libraries may launch separate process groups, so preserve their graceful
shutdown handlers and verify escaped-child limits. Never terminate personal
browser sessions or another task's processes as incidental cleanup.
Use lightweight fixtures for most supervisor regressions and a short native probe
for library-specific shutdown. Do not start another full matrix to test the limiter.

Return accepted proof, busy dependencies, or failed conditions through the existing
[task coordinator](../../git-hygiene/references/work-units.md#continue-through-the-requested-endpoint).
Lower process priority can reduce desktop interference but does not replace
capacity control or prove that checks became faster.
