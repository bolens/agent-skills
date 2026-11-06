# Woodpecker portable CI handoff

Move the portable validation workload to an unprivileged Linux container without
changing installed skill links or granting PR code secrets or host access. Reuse
`make test-client-loaders` and `make check-fast test portability`; retain the
macOS installation, selected Archify/browser suites, image-building, source lint,
and workflow-security jobs in GitHub.

Add and activate the native pipeline first. Require its exact-head PR result and
all applicable GitHub checks before squash merge, then verify genuine main.
After both succeed, remove the duplicate portable workload from GitHub while
preserving its dependency join for selected browser/platform jobs. Native
failures block delivery; there is no fallback that turns them into a pass.

The README owns runtime requirements and manual image-pin review cadence.
RELEASING owns delivery and recovery. Correct or revert source through a PR;
there is no product tag, publication credential, live installation, or persistent
data migration in this change.

The local portable gate and workflow lint are submission evidence. Native
pinned-image execution and any final GitHub workload retirement remain delivery
gates, and must be recorded from actual host results.
