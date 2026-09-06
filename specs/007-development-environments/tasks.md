# Tasks

- [x] Add pinned devenv tools and native validation (59 tests and portability passed inside devenv).
- [x] Add source-free image export and engine selection with five adapter regression tests.
- [x] Document Linux/macOS and host-service boundaries.
- [x] Verify Docker and Podman execution; record Apple evidence limits.
- [ ] Pass native gates, merge with current CI, and clean owned task artifacts.

Podman passed the full portable gate; an additional UID 501 check verified the existing image home is writable without changing HOME. Docker and native macOS checks passed in CI run 34026992700 at b406edba64a1cb5da3178561e1ff5ee8be700459. Apple CLI execution requires an Apple-silicon Mac and remains unverified on this Linux host.
