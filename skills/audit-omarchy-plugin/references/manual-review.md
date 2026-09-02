# Manual review guide

Use this after deterministic validation. Follow only the sections relevant to the plugin.

## Long-lived shell state

- Inventory arrays, maps, models, strings, collectors, caches, histories, notification batches, and retry state retained by `Service`, bar widgets, and keep-loaded components.
- For each producer, prove what drains or replaces retained state when a helper hangs, never starts, emits malformed output, or exits without the expected signal.
- Require explicit count and byte bounds where input size varies. Rejecting one oversized item must not erase already accepted work.
- Define overflow semantics: newest-wins, oldest-wins, coalescing, deduplication, or rejection. Preserve clear/reset ordering.
- Bound subprocess stdout/stderr collection and line framing. A process timeout alone does not cap output accumulated before termination.
- Prevent overlapping timers, retry storms, orphaned processes, stale callbacks, and results published after settings or generation changes.

## Commands and trust boundaries

- Build commands as argument arrays. Treat shell strings and `bash -c` as review surfaces.
- Validate IPC, environment, settings, helper output, paths, URLs, service names, package names, and identifiers at the boundary where they become trusted.
- Pin remote Git execution to a full commit and verify detached checkout state. Avoid download-to-shell paths.
- Check symlink and traversal resistance before reads, writes, deletion, archive extraction, or permission changes.
- Use owner-only runtime/state directories for process identity and sensitive metadata. Never trust predictable shared `/tmp` PID or command files across privilege boundaries.

## Privilege and host mutation

- Enumerate every `sudo`, `pkexec`, package-manager, service-manager, sudoers, polkit, udev, system configuration, and root-owned helper path.
- Keep privileged helpers root-owned, narrow, allowlisted, and independently input-validating.
- Avoid passwordless access to general command surfaces or user-controlled arguments.
- Require explicit consent before overwriting user configuration. Back up or merge where documented, and make removal scope precise.
- Confirm install/remove symmetry without deleting user data by surprise. Document persistent data that intentionally remains.

## Packaging and repository evidence

- Confirm manifest ID, version, entry points, kinds, dependencies, and lifecycle instructions match actual behavior.
- Ensure the README documents installation, removal, external dependencies, privileges, network access, binaries, services, user-data paths, and destructive actions.
- Confirm license coverage and provenance for bundled code, binaries, fonts, images, and previews.
- Validate from a clean archive so ignored or untracked local files cannot hide missing runtime dependencies.
- Tie changelog, tag, release assets, checksum, attestation, Pages metadata, and marketplace request to one exact commit.

## Regression-test standard

Prefer a runtime test that reproduces the failure condition, plus a narrow static contract when removal would be easy to miss. For a stalled subprocess queue, hold ownership busy without starting the helper, enqueue beyond each limit, assert the exact retained set, submit an oversized item, verify existing work survives, and test clear/supersession. Also test the normal drain and failure-recovery paths.
