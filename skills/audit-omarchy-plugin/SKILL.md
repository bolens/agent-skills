---
name: audit-omarchy-plugin
description: Audit an Omarchy plugin repository before marketplace submission, verification, update approval, or release. Check marketplace structure and scan policy, exact-commit readiness, declared capabilities, install/remove behavior, long-lived Quickshell safety, bounded subprocess and queue behavior, tests, documentation, and release evidence. Use for pre-submission checks and approval triage; do not use for ordinary end-user plugin installation or configuration.
---

# Audit an Omarchy plugin

Default to a read-only audit. A readiness request does not authorize fixes, pushes, releases, marketplace issues, or approval-label actions.

## Establish the candidate

1. Resolve the repositories the user owns or explicitly placed in scope. Do not infer that a marketplace, dependency, sibling checkout, or every repository matching `omarchy-*` is an audit target. If ownership is ambiguous, inspect remotes and state the proposed target list before doing substantial work.
2. Treat marketplace sources only as policy evidence. Do not audit, test, modify, or inventory the marketplace repository unless the user separately asks for that work.
3. Read each target's repository instructions, `manifest.json`, README, license, contributor guidance, testing docs, and release automation.
4. Identify whether this is a new listing, recorded-snapshot verification, or newer-commit update. Record the repository root URL, plugin ID set, full candidate SHA, default branch, and dirty-worktree state.
5. Treat the exact public commit as the approval subject. Uncommitted or later upstream changes are not covered.
6. Before an actual submission or verification request, refresh the marketplace policy from its `main` branch. Use [references/marketplace-policy.md](references/marketplace-policy.md) as a dated guide, not as a substitute for the current source.

## Run deterministic checks

Run `scripts/preflight.sh <repository>` first. Then run the repository's canonical suite and `omarchy plugin validate <repository>` when available. Do not install, enable, or execute untrusted plugin code merely to audit it.

For an ordinary audit, refresh only the authoritative marketplace text and scanner-policy modules needed to understand current rules. Prefer the GitHub API or raw-file requests pinned to the current `main` SHA. Do not clone or download the whole marketplace repository merely to inspect policy.

For an actual submission simulation, run the marketplace's current Automated Security Baseline against the exact public commit when the user requests that depth or a suitable scanner checkout already exists. Use the marketplace's own scanner rather than copying its regexes. A new checkout is supporting tooling, not an audit target: explain why it is needed, obtain any required authorization, keep it temporary and minimal, and do not run its unrelated tests. If practical execution would require a large checkout or unrelated assets, report the official scan as unavailable and continue with policy-source review and the plugin's own checks. Record the scanner's policy version, enforcement mode, disposition, findings, capabilities, and scan limits.

Run tests from a path compatible with repository assumptions. If an isolated copy under `/tmp` triggers intentional temp-path or fleet-layout guards, do not label that as a plugin failure. Confirm the failure is path-specific, use a safe non-temporary worktree when justified, or cite successful CI for the exact SHA; report the environmental limitation explicitly.

## Review beyond the scanner

The marketplace baseline is deliberately narrow. Read [references/manual-review.md](references/manual-review.md) and trace each relevant lifecycle:

- install, update, enable, disable, and remove
- every `Process`, detached command, watcher, timer, retry, and helper
- every queue, pending collection, buffered collector, cache, log, and history store
- network downloads, Git sources, package managers, services, privilege boundaries, sudoers, shared temporary state, and executable assets
- settings and user-data writes, configuration overwrite behavior, path validation, symlinks, permissions, and rollback
- inputs from IPC, QML settings, subprocess output, files, network responses, and environment variables

For long-lived Omarchy Shell code, require an explicit bound or supersession rule for retained work. A helper that can hang must not prevent a queue from draining indefinitely. Check count and byte bounds, oversized-item behavior, eviction semantics, cancellation or timeout ownership, collector output bounds, and recovery after failure.

## Judge tests by failure detection

Require behavioral regression coverage for each material risk. For asynchronous queues, tests should hold the worker busy or stalled, exceed count and byte limits, verify retained work, exercise oversized input, and confirm clear or supersession semantics. Static source-contract tests may prevent accidental removal of a bound but do not replace runtime behavior tests.

Run graphical QML tests against a real Wayland session when the repository requires them. Report environmental skips separately from passing tests.

## Report

Lead with blockers, then `review-required` capabilities, then manual-review risks. For each item include evidence, impact, smallest fix, and the test that would prevent recurrence.

Finish with:

- candidate repository, plugin IDs, and full SHA
- marketplace policy version and source commit inspected
- predicted disposition: `passed`, `review-required`, `needs-fixes`, or unavailable
- official scanner findings and capabilities, kept separate from manual findings
- commands run and exact results
- residual gaps, including tests not run and code excluded from the official scan
- submission/update metadata still needed

Do not describe a clean baseline as a security audit or guarantee approval.
