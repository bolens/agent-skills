# Woodpecker portable CI handoff

Move the portable validation workload to an unprivileged Linux container without
changing installed skill links or granting PR code secrets or host access. Reuse
`make test-client-loaders` and `make check-fast test portability`; retain the
macOS installation, selected Archify/browser suites, image-building, source lint,
and workflow-security jobs in GitHub.

The native pipeline has passed its PR and genuine-main acceptance. GitHub’s
stable `validate` job joins the exact source’s native result while
preserving its dependency join for selected browser/platform jobs. Native
failures block delivery; there is no fallback that turns them into a pass.

The README owns runtime requirements and manual image-pin review cadence.
RELEASING owns delivery and recovery. Correct or revert source through a PR;
there is no product tag, publication credential, live installation, or persistent
data migration in this change.

The local portable gate and workflow lint are submission evidence. Native
pinned-image execution and any final GitHub workload retirement remain delivery
gates, and must be recorded from actual host results.

The handoff checks the latest combined status and exact matching raw status ID,
repository, SHA, event context, publisher and pipeline URL. A newer pending result
cannot reuse an older success. Missing/pending statuses wait within a bounded
deadline; failure/error statuses fail immediately. Manual GitHub runs must use
main and its genuine native push result. Archify/macOS prerequisites still fail
the aggregate before waiting on native status. The weekly GitHub schedule retains
its existing portable workload until equivalent native periodic coverage exists.
