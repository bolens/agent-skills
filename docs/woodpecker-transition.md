# Woodpecker portable CI handoff

Move the portable validation workload to an unprivileged Linux container without
changing installed skill links or granting PR code secrets or host access. Reuse
`make test-client-loaders` and `make check-fast test portability`; retain the
macOS installation, serialized Archify WebM/site suites, image-building, source lint,
and workflow-security jobs in GitHub.

The portable native pipeline has passed its PR and genuine-main acceptance. GitHub’s
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

## Full Archify harness proposal

The second native workflow uses the same pinned Node 22 image as portable CI,
distribution Chromium, and the unchanged `make test-archify` command. It follows
portable validation, so one repository does not occupy both workflow slots while
its prerequisites are pending. It needs no host privileges, socket mounts,
publisher credentials, or custom image. Its PR path list is checked against
GitHub's selector; every main push and native manual run includes the full harness.

Automated GitHub Archify shard names join `ci/woodpecker/pr/archify` or the genuine
main push equivalent. The helper allowlists only `portable` and `archify`, still
binding the exact revision, repository, trusted publisher and latest status ID.
The final numeric URL component is a positive workflow index, not a fixed `1`:
adding a second workflow can change its position. One workflow's result cannot
satisfy the other workflow's context. Manual and scheduled GitHub runs retain the
existing actual runtime shards; they do not substitute an older push result.

Actual hosted evidence at source `12bf7f2` contains 1,022 passes and four skips
across both shards. Twenty-three real Chrome tests execute there; two site cases
run in the separate serialized WebM/site gate, and the remaining two skips require
an external MCO checkout or a noncanonical Node major. The earlier local 999-pass,
27-skip result is incomplete browser evidence and cannot qualify this migration.

This expansion remains unpublished until a bounded, corrected-budget native
canary runs the full harness with real Chromium and all its actual child results
are reviewed. Verify both new context routing and the existing portable handoff
against real multi-workflow status payloads before the GitHub retirement is
published. Current dependency PRs retain their frozen heads throughout this work.

The first actual native full harness identified a test-fixture watchdog race:
the empty-precheck ordering case deliberately pauses two checks behind filesystem
and fetch barriers, but shared its unrelated 50 ms network-failure watchdog. That
watchdog fired under the two-CPU allocation after 95 ms, producing a silent result.
Both actors now use the existing bounded two-second child-check watchdog and the
case has the existing five-second parent deadline. The explicit ordering barriers,
exactly-one-GET and successful-update assertions remain intact. Cache tests,
production timeout behavior and its separate tests are unchanged.

The retained hosted WebM/site job on merged source `b299925` was cancelled after
its 30-minute job deadline: Ubuntu's Azure mirror took 29m8s to fetch 50.9 MB
of FFmpeg packages (29.1 kB/s), leaving only 30 seconds for actual integration
tests. This did not establish a test assertion failure. The exact hosted image
was Ubuntu 24.04 `20261101.360.1`; its [provider configuration](https://github.com/actions/runner-images/blob/ubuntu24/20261101.360/images/ubuntu/scripts/build/configure-apt-sources.sh)
uses an Azure-first `mirror+file:/etc/apt/apt-mirrors.txt` source.

The bounded correction selects the official HTTPS Ubuntu archive for that exact
provider token or known archive URI, preserving security sources, suites and
signing policy. It applies only in disposable GitHub-hosted Ubuntu jobs, before
the existing vendor-feed isolation. FFmpeg installation has its own five-minute
failure bound; the 30-minute job limit and every browser/WebM/site assertion are
unchanged. Manual and scheduled browser/client-loader paths remain selected as
before. A successful old-source retry is not substituted for current-source
validation of this correction.
