# Executable legacy contracts

Dated extension: 2026-09-06, source baseline `c0bfd04` with the corrective
requirements FR-009–FR-012. The [individual skill contracts](legacy-capabilities.md)
cover every registered procedure. This document covers their executable seams.
Source links identify ownership; named fixtures establish the stated scope only.
A helper's successful exit does not certify the whole workflow it supports.

## LH-001: Registry, provenance, installation, and maintenance

The [provenance generator](../../scripts/update-provenance.py) reconciles the
registered skill sources and audited upstream metadata into PROVENANCE.json and
UPSTREAM.md. `--check` detects drift without rewriting. Source identities,
licenses, local-change records, and current audited refs remain distinct; local
fixes must not pretend an upstream import occurred.

The [installer](../../scripts/link-installed.py) targets configured Codex, Agents,
and Claude skill roots, detects conflicting real directories, and reports an
unsatisfied mapping without deleting that directory. `--check` observes mappings;
normal mode changes eligible managed links. Worktree verification must not repoint
canonical installed links. [Validation](../../scripts/validate.py) checks registry,
entrypoint metadata, references, license/provenance consistency, and executable
syntax. [Portability](../../scripts/check-portability.py) checks supported Python,
Bash/ShellCheck, and Node sources; the shell wrapper forwards arguments and status.
[Upstream audit](../../scripts/audit-upstreams.py) compares recorded identities with
remote heads and reports drift; it does not import remote code or update audit refs.
[Hook installation](../../scripts/install-git-hooks.py) installs the repository's
check-fast gate at its configured Git hook location. Normal hook execution and
portable gates remain separate from installed-link checks.

The [shared editor tasks](../../.vscode/README.md), integrated from e62917e,
invoke check-fast, test, portability, links, check, or diff-whitespace explicitly
from the workspace. They preserve the same gate boundaries: links/check inspect
canonical installations and do not authorize repointing them to a worktree.
Recommendations do not install extensions or native tools automatically.

Acceptance: generated drift fails check mode; an installer conflict retains its
sentinel while independent mappings can proceed; invalid metadata and unavailable
required portability tools fail explicitly. Existing fixtures:
[test_repository.py](../../tests/test_repository.py),
[test_licenses.py](../../tests/test_licenses.py), and
[test_portability.py](../../tests/test_portability.py).

The [development-container adapter](../../scripts/development-container.py) builds
source-free Docker or OCI archives using devenv on x86_64/aarch64 Linux builders,
then loads the selected Docker, Podman, or Apple engine. Run mounts the explicit
checkout at `/workspace`, preserves the invoking uid/gid, uses Podman's keep-id,
and requests an interactive terminal only for interactive stdin. Reject comma
mount paths, unsupported Apple hosts, unavailable engines/devenv, and extra build
commands. Build failure must prevent load. See original
[007](../007-development-environments/spec.md) and
[test_development_container.py](../../tests/test_development_container.py).

## LH-002: Fleet inventory, source excerpts, and check receipts

[Inventory](../../skills/audit-repo-fleet/scripts/inventory.sh) searches a bounded
root/depth for Git markers, supports linked worktrees, excludes bare markers, and
reports local branch/upstream divergence, dirty/untracked counts, governance,
workflow/update presence, and root manifests. It does not fetch. Invalid discovery
or unreadable repository status must not become a clean row. Paths in its TSV are
intended for human inspection, not a general lossless filename interchange format.

[Context reader](../../skills/audit-repo-fleet/scripts/context-read.py) emits numbered
UTF-8 JSON with at most 350 lines and 24 KiB including encoding overhead. Explicit
ranges require both start and limit. An oversized, invalid, missing, or past-end
request returns 2 without a partial source response. Skipped oversized lines are
consumed in bounded chunks. Original [004](../004-bounded-context/spec.md) owns the
full contract; fixtures are [test_context_read.py](../../tests/test_context_read.py).

[Evidence](../../skills/audit-repo-fleet/scripts/evidence.py) binds commands to HEAD,
branch/index state and tracked/nonignored source fingerprints, stores private logs
and atomic receipts under the worktree's Git directory, and reserves identical
candidate/command retries. It executes argument arrays with closed stdin and a
bounded deadline, kills only its owned process tree on cancellation, and records
unavailable, timed-out, interrupted, failed, changed, or unverified outcomes.
A zero command exit with changed source cannot pass. `report` uses the latest
requested label and rejects missing, stale, malformed, or inconsistent receipts.
Retries of unchanged failures require a reason and obey the attempt limit.
Original [005](../005-fleet-evidence/spec.md) retains the detailed lifecycle;
[test_fleet_inventory.py](../../tests/test_fleet_inventory.py) and
[test_fleet_evidence.py](../../tests/test_fleet_evidence.py) cover disposable Git,
process, invalid receipt, cancellation, and retry cases.

The integration base advanced to `93c7301` during this audit. Its new optional
[prepare-sentrux.py](../../skills/audit-repo-fleet/scripts/prepare-sentrux.py) and
[sentrux.py](../../skills/audit-repo-fleet/scripts/sentrux.py) already have the
prospective [009 local-analysis contract](../009-sentrux-local-analysis/spec.md)
and [fixtures](../../tests/test_sentrux.py). Retain verified local binary/grammar
identity, explicit selected-source scope, offline isolation, immutable baselines,
and unavailable-versus-finding results. This retrofit neither imports a runtime
nor turns the optional analysis into a required fleet gate.

## LH-003: File compression and validation

The [CLI](../../skills/caveman-compress/scripts/cli.py) accepts one eligible prose
file, exits 1 for invalid invocation, 0 for unsupported/skipped content, 2 for
unsuccessful compression, and 130 on interruption. Extensionless detection,
known build-file exclusions, prose extensions, and `.original.md` backup exclusion
are owned by [detect.py](../../skills/caveman-compress/scripts/detect.py).

[Compression](../../skills/caveman-compress/scripts/compress.py) resolves the path,
rejects oversized (>500,000 bytes) and suspected sensitive paths, coordinates
backup identity with a bounded file lock where supported, and reads strict UTF-8.
Unsupported filesystem locking is an explicit warning, not a concurrency proof.
It preserves raw original bytes in a non-overwritten backup, newline policy and
permissions; frontmatter is excluded and fenced code is carried through markers.
External model requests use the configured Claude SDK/CLI seam, with a bounded
call timeout. This is an external content transfer requiring the invoking task's
authority; metadata/static tests do not prove model quality.

At most two candidates are validated (one repair request). Empty, unchanged,
marker-corrupt, or invalid results cannot overwrite the original. Validation uses
an owned temporary directory beside the source, never a predictable neighboring
file; success, rejection, and exception clean up that owned directory. Successful
promotion uses atomic replacement. Exhausted validation retains source bytes and
removes its own failed backup; an exceptional failure can retain the recovery
backup. A pre-existing backup aborts without overwriting it.

[Validation](../../skills/caveman-compress/scripts/validate.py) checks fenced-code
identity, heading text/order, URLs, paths and inline-code preservation; ambiguous
path/addition, heading-level and bullet-count changes can be warnings. Its standalone
CLI prints its result; callers must inspect the `valid` result rather than treat
that reporting CLI's zero status as a validation verdict. The compressor uses the
actual result. [Benchmark](../../skills/caveman-compress/scripts/benchmark.py) uses
tiktoken when installed and otherwise word counts; estimated savings are not
model-independent token guarantees.

Acceptance: a pre-existing `.caveman-staged` neighbor survives successful,
rejected, and exceptional candidates with its bytes unchanged; failed validation
preserves source bytes. [test_compression_staging.py](../../tests/test_compression_staging.py)
uses real files and a synthetic model response, without sending content externally.

## LH-004: Responsive browser evidence

[Capture](../../skills/responsive-web-capture/scripts/capture-responsive.py), also
available through its shell wrapper, accepts exactly one HTTP(S) URL or local
directory. Reject embedded URL credentials, control characters, unsafe name/phase
components, invalid ports/viewports, and unavailable Chrome. Custom viewport lists
override the quick/standard/comprehensive matrices and are deduplicated.

Each run gets its own evidence directory and each viewport a private browser
profile. A local static server binds loopback; occupied ports fail before capture.
HTTP readiness proves only an HTTP response, not application readiness. Browser
and montage commands have deadlines and owned process-group cleanup. Captures
must be complete PNGs of the exact requested dimensions, recorded with byte count,
SHA-256, URL and browser version in JSON/TSV. Interruption or failed capture keeps
an incomplete receipt. Optional contact-sheet failure retains original images and
is separately reported. Coverage is initial viewport only; interaction, all theme
states, and perceptual review require separate evidence. See
[test_responsive_capture.py](../../tests/test_responsive_capture.py).

## LH-005: Inspection and diagnostic helpers

| Helper | Observable behavior and failure boundary | Acceptance |
| --- | --- | --- |
| [Sensitive scan](../../skills/sensitive-info-audit/scripts/audit-sensitive.py) | Scan a file, tracked Git files (optional untracked), or non-Git tree. Inspect symlink text without following targets. Report detector and location with values redacted. Secret exit 1; skipped/incomplete exit 2; privacy-only review exit 0. Enforce positive size cap and reject failed traversal. | [test_sensitive_audit.py](../../tests/test_sensitive_audit.py): secret/skip precedence, symlink boundaries and incomplete discovery. Pattern absence is not comprehensive secret certification. |
| [Directory comparison](../../skills/managed-config-drift/scripts/compare-trees.py) | Compare repeated LIVE=MANAGED mappings by relative entry/type, symlink target and streaming SHA-256; exclude exact path components. Exit 0 equal, 1 differences, 2 unavailable/incomplete. Do not mutate either tree or follow nested directory symlinks. | Failed traversal yields UNAVAILABLE, continues a later mapping, retains sentinel bytes; [test_helper_failures.py](../../tests/test_helper_failures.py). |
| [Health collector](../../skills/workstation-health-triage/scripts/collect-health.sh) | Quick kernel/load/memory/storage/failed units/coredumps/mount/package-lock/session snapshot; full mode adds bounded journals, processes, network, sensors, graphics and package queries. Label missing commands and failed checks. Optional output uses restrictive creation permissions and reports opening/write failure. | Missing output parent returns nonzero without “wrote”; [test_helper_failures.py](../../tests/test_helper_failures.py). A completed snapshot can contain failed probes and private host details; review before sharing. |
| [Plugin preflight](../../skills/audit-omarchy-plugin/scripts/preflight.sh) | Check Git/HEAD, manifest/id/version/entrypoints, README install/removal, license; flag capabilities in selected runtime file types and optionally run installed `omarchy plugin validate`. Skip documented generated/test/docs trees. Discovery failure is incomplete. Error count controls status; review findings are not approvals. | Failed find cannot return successful preflight; [test_discovery_failures.py](../../tests/test_discovery_failures.py). Fixture stubs the host validator; no live plugin install/remove is claimed. |
| [HTML analyzer](../../skills/web-quality-audit/scripts/analyze.sh) | Static HTML doctype/charset/viewport/lang/title/img-alt/HTTP heuristics, JSON issues and warnings, 100 returned per category and 20 high-volume findings per file. Discovery or read failure returns structured failure; newline filenames remain one JSON finding. | Failed find returns `success: false`; [test_discovery_failures.py](../../tests/test_discovery_failures.py). `success: true` means analysis completed, not WCAG/performance/security compliance. This is not a DOM parser or a browser audit. |
| [Changelog checker](../../skills/changelog-maintainer/scripts/check-changelog.py) | Check current-directory CHANGELOG.md headings/categories, required Unreleased, release links and concise active-release entries; first two releases get 12-bullet/280-character limits and no PR/scope/skip-CI clutter. Print locations and exit 1 on violations. | Missing file and malformed release headings fail; older prose is not silently rewritten. This is an optional target-repository policy, not this collection's differently formatted changelog gate. |
| [Pollution search](../../skills/systematic-debugging/find-polluter.sh) | Discover matching files and run `npm test` sequentially, preserving any created target for inspection. Exit 1 on observed creator, 2 for unavailable discovery/no tests/pre-existing target/failed execution without a creator, 0 only after selected tests complete without the requested target. | Discovery, failed command, pre-existing target, and failed test that creates target are distinct fixtures in [test_discovery_failures.py](../../tests/test_discovery_failures.py). It neither deletes pollution nor proves all side effects absent. |
| [Work log](../../skills/show-me-your-work/scripts/log.sh) | Append six-argument TSV records to the explicit log, creating parents/header when needed. Replace tabs/newlines/CR and quote formula-leading cells; preserve earlier rows and append corrections. | Use only task-scoped evidence; unavailable model/reviewer/transcript sources remain gaps under FR-010. A row is an observation, not proof that its stated command actually ran. |

## Verification boundary

The portable gate exercises repository metadata, syntax and its named fixtures.
The [Archify contracts](legacy-archify.md) have a separate fetched upstream test
harness. Real external-model compression, live host probes, actual plugin
validation, browser application readiness and production deployment are not
established by the portable fixtures. Source-backed procedure acceptance and
executed runtime evidence must remain separately labeled.
