# Paul Solt app-workflow audit

Reviewed both linked articles on 2026-09-05:

- [Install These Skills Before Codex Touches Your Xcode Project](https://x.com/PaulSolt/status/2042716870512353294),
  posted 2026-04-10.
- [How I Build Apps With Codex Without Opening Xcode](https://x.com/PaulSolt/status/2040132557983936772).

Direct X retrieval returned HTTP 403. The public FxTwitter responses included
the full article blocks and linked URLs, which were inspected. The first article
surveys Swift skills and tools. The second describes a build/test workflow,
including failures hidden by output handling, focused tests, runtime logs, and
local documentation. Promotional claims were not treated as measured results.

## Source findings

**A formatter cannot supply its producer's exit status.** Inspected xcbeautify
at `513e4b12c3f6c965d1d3b66bd5cd9d635f03112d`: README, package manifest,
license, and the complete
[CLI entrypoint](https://github.com/cpisciotta/xcbeautify/blob/513e4b12c3f6c965d1d3b66bd5cd9d635f03112d/Sources/xcbeautify/Xcbeautify.swift).
It reads stdin and writes formatted output and optional reports. It does not
own the upstream build process. Its README explicitly recommends shell pipeline
failure handling. That is an integration responsibility, not an xcbeautify defect.
A report-write error can also fail independently of the compiler result.

Executed disposable Bash probes confirmed that a producer exiting 7 followed
by successful `cat` yields 0 without `pipefail` and 7 with it. A failed downstream
stage yields 9; when both stages fail, `pipefail` still yields the rightmost
nonzero status, 9. It does not promise the compiler's exact exit code. Make probes
confirmed that a separate recipe line setting `pipefail` leaves the next line's
pipeline able to pass falsely. Setting it in the pipeline's shell makes the
Make target fail. These exercised shell and task-runner behavior, not Xcode.

**Local documentation needs source identity and an explicit refresh boundary.**
Inspected DocSetQuery at `ba68aabe2c84e907789d4c0043f97568ec8cdcfd`: README,
license, full cache-sync script, index-building/loading excerpts, index tests,
and exporter metadata locations. The
[index code](https://github.com/PaulSolt/DocSetQuery/blob/ba68aabe2c84e907789d4c0043f97568ec8cdcfd/tools/docindex.py)
retains docset version and export time but loads an existing index without a
freshness comparison. Its documented rebuild step matters. An index hit locates
content; it does not prove current SDK availability. The sync helper can write
shell configuration in init mode or mirror deletions when selected. It was
read, not executed or installed. Both upstream index unit tests passed using
disposable Markdown fixtures; full Apple docset export was not exercised.

## Adoption decisions

| Idea | Decision for this setup |
| --- | --- |
| Reliable build/test status behind readable output | Add explicit pipeline and outer-runner failure checks to CI maintenance |
| Runtime logs and artifacts | Add scoped instrumentation and process/build identity to debugging |
| Local documentation lookup | Add version/freshness checks before trusting cached API evidence |
| Fast tests before expensive UI checks | Retain existing focused-check workflow and required handoff gates |
| Shared build commands | Already covered by repository-native Make/task commands; no new wrapper needed here |
| Swift/Xcode skill packs and tools | Defer until an Apple-platform task establishes a concrete need |
| Automatic app launch and warnings-as-errors defaults | Do not generalize across repositories; preserve task scope and existing policy |
| Rule loading and skill stacking | Existing conditional references and overlap review already cover the useful behavior |

This Linux skill-maintenance checkout has no demonstrated Xcode build need.
No Swift skill pack, hot-reload tool, simulator service, or Apple documentation
bundle was installed. AppCreator's linked landing page was inspected, but its
downloadable skill and deletion/Git guards were not obtained or audited. No signup
was submitted. The listed Swift packs, paid rule collection, videos, and UI-test
performance claims were not exhaustively audited. The unavailable rule-loader
URL was not treated as reviewed source. No Swift or Xcode build was performed.

## Local implementation and validation

Updated the existing `ci-maintenance` and `systematic-debugging` skills with
original prose and a conditional command-evidence reference. Their scopes and
local-original provenance remain intact. No external code or skill text was
imported, no upstream ref advanced, and no installation target changed. Both
inspected repositories declare MIT licenses. This is prose maintenance within
existing workflows, with no new runtime capability or CI gate.

Manual walkthroughs covered a hidden compiler failure, a failing formatter,
separate Make recipe shells, a clean build with a stale running app, and a cached
API reference from a different SDK. Existing checks remain proportionate to the
task rather than imposing UI suites or verbose logging on every edit.

`make check-fast` and `make check` passed: all 30 repository tests, provenance,
portability with ShellCheck, and installed links. Both edited skills passed
Skill Creator's quick validator. The six failure-path shell/Make probes and a
successful pipeline control passed, as did the two upstream index tests.
These checks do not establish Xcode integration or improved agent task outcomes.
