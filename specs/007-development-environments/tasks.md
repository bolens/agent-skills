# Tasks

- [x] Add pinned devenv tools and native validation (59 tests and portability passed inside devenv).
- [x] Add source-free image export and engine selection with five adapter regression tests.
- [x] Document Linux/macOS and host-service boundaries.
- [x] Verify Docker and Podman execution; record Apple evidence limits.
- [x] Verify native Linux/macOS and Linux Docker checks on the recorded main revision.
- [x] Verify merged source delivery and the applicable main-revision workflows.

Historical pre-merge observation (superseded by the receipt below):
Podman passed the full portable gate; an additional UID 501 check verified the existing image home is writable without changing HOME. Docker and native macOS checks passed in CI run 34026992700 at b406edba64a1cb5da3178561e1ff5ee8be700459. Apple CLI execution requires an Apple-silicon Mac and remains unverified on this Linux host.

## Delivery verification — 2026-09-06

The [development workflow](https://github.com/bolens/agent-skills/actions/runs/34027928627) passed on
`f7232a0108e35bfd265baaf57b9f344a380d7a7c`. Both native platform jobs ran successfully;
the Linux job also executed and passed the Docker development-image check. All
applicable workflows observed for that main revision completed successfully.

Actual Apple container-engine execution remains unverified. Native macOS devenv
validation does not establish that engine's runtime behavior. Existing live-host
and optional dependency limits still apply. Checkout cleanup remains part of each
task's delivery procedure and is not inferred from CI success.
