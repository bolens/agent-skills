# Skill workflow audit

The initial review covered discovery descriptions and entrypoint workflows for
the 62 skills at `7816ad7`, then inspected supporting references for concrete
findings. PR 43 subsequently merged as `c3a2658`, changing only the devcontainer's
Node image and smoke expectation. This is a source/scenario audit, not a claim
that all skill scripts or runtime workflows were executed.

The collection already has useful boundaries between architecture discovery and
design, code review and terse presentation, stack source maintenance and live
diagnosis, and verification and delivery. Preserve these distinctions. The useful
improvements concern specific routing and duplicated instructions, not indiscriminate
skill removal or a new orchestration layer.

## Changes implemented under the follow-up requests

- **Platform ownership:** Omarchy formerly claimed terminal, Hyprland, and almost
  any `~/.config` edit. Its entrypoint and health/configuration handoffs now require
  identified Omarchy ownership. An explicitly requested reset retains existing
  authority rather than always asking again.
- **Missing platform procedures:** Added `arch-linux` for configuration/package
  ownership, `cachyos` for optimized repositories, profiles, kernels, and measured
  tuning, and `nixos` for declarative systems, activation/recovery, and development
  VMs. Retained existing Arch package-authoring and upgrade-recovery owners.
- **Crash diagnosis:** Check the distribution, core availability, and matching
  symbols. Omarchy notification-muting advice is now conditional on its watcher
  and the user's notification problem.
- **Portable developer setup:** One conditional reference in `ci-maintenance`
  owns mise, devenv/Nix, devcontainers, and applicable NixOS VMs/tests. Relevant
  skills route there without inventing another coordinating skill. It covers
  pinned inputs, native commands, updater coverage, setup execution, CI selection,
  and the distinction between guest and host behavior. Environment contracts prefer
  `.env.spec`, with explicit syntax/validation and coordinated consumer migration;
  other examples use their native schemas when this prevents drift.

The prospective [platform](../../specs/010-linux-platform-skills/spec.md) and
[portable-development](../../specs/011-portable-development-guidance/spec.md)
records contain source assessment and verification limits.

## Remaining recommendations, in priority order

### 1. Narrow commit-message discovery

[caveman-commit](../../skills/caveman-commit/SKILL.md) advertises “write a commit”
and `/commit`, while its boundary permits only generating a message and explicitly
forbids staging or committing. A request to create a commit can select a workflow
that stops short of the requested action. [git-hygiene](../../skills/git-hygiene/SKILL.md)
already correctly treats it as a wording helper.

Limit its description to message-writing requests and the explicit named command.
When used inside an authorized commit workflow, return the message to that owner
rather than letting the wording skill terminate the task. Validate “write a commit
message” separately from “commit these changes.” Preserve the existing invocation
policy and host install targets.

### 2. Make browser capture routing agree in both directions

[cli-web-evidence](../../skills/cli-web-evidence/SKILL.md) prefers the repository
harness but then routes viewport PNGs unconditionally to `responsive-web-capture`.
[responsive-web-capture](../../skills/responsive-web-capture/SKILL.md) opens with
the bundled helper, then later says to use the existing harness first. That helper
starts fresh profiles and does not wait for application state or preserve auth.

For an authenticated dashboard screenshot, the established browser harness should
keep ownership. Route to the bundled helper only for suitable unauthenticated
initial renders without app-specific readiness. Move that decision before helper
invocation in both entrypoints. Retain the matrix/receipt guidance without forcing
a second browser path. Validate authenticated, hydrated, and simple static pages.

### 3. Remove unconditional performance recipes from audit entrypoints

[core-web-vitals](../../skills/core-web-vitals/SKILL.md) says to measure first but
its LCP checklist requires adding Speculation Rules with moderate eagerness. Its
earlier text correctly describes prerendering as conditional and distinct from
fixing the current page's LCP. The entrypoint also includes framework quick fixes
beside separate metric references. [web-quality-audit](../../skills/web-quality-audit/SKILL.md)
repeats category prescriptions such as preconnecting third-party origins and
preloading assets without tying each one to observed resource contention.

Keep the broad skill responsible for evidence, category selection, prioritization,
and reporting. Route metric remedies to their owning references, and express
checklists as measured conditions rather than changes every site must receive.
Validate a poor-LCP image case, a slow interaction case, and a healthy page where
no additional resource hint or prerender should be introduced. Keep substantive
guidance; moving repeated examples is more useful than shortening every skill.

### 4. Align Archify update notices with hard-fork maintenance

[Archify](../../skills/archify/SKILL.md) requires an update check after creating the
first diagram candidate. Its packaged checker manages its own cache and upstream
release notice, while this repository explicitly maintains reviewed hard forks
through [sync-skill-upstreams](../../skills/sync-skill-upstreams/SKILL.md). The
notice does not establish that a new upstream release preserves this fork's changes.

Make update awareness conditional on maintenance work or an explicit user request,
and route any available update through the fork's diff/provenance review. This
removes an unrelated network/cache/notification step from ordinary diagram work.
Preserve the checker and its contracts until its callers and upstream customization
record are reviewed. Validate offline diagram generation and a separate update audit.

### 5. Preserve authorization through config-drift reconciliation

[managed-config-drift](../../skills/managed-config-drift/SKILL.md) correctly keeps
audits read-only, but its reconciliation paragraph ends with an unconditional
instruction to seek authorization. If the parent task already authorizes a named
reconciliation, this wording can cause an unnecessary approval stop.

Separate diagnosis-only authority from an existing repair request, following the
pattern already used by `systematic-debugging` and `babysit`. Still establish the
owner and direction before writing. Validate “audit this drift” versus “reconcile
these named managed files.” This is a wording risk established by source review,
not an observed live invocation failure.

## Evidence and limits

The host-visible skill listing did not expose this cloned collection during the
audit. No usage history or before/after host invocation experiment was available.
Do not interpret missing invocations as evidence that a skill should be deleted,
or word counts as measured token/cost savings. The collection now contains 65
registered skills after the three requested additions.

The portable gate passed through mise with 95 tests and no skips, including
ShellCheck. The full Archify harness passed 1,022 tests with four intentional skips;
its serialized browser gate passed seven tests. New and edited entrypoints passed
skill validation. These checks cover
metadata, provenance, syntax, links, and tested helper behavior; they do not prove
the remaining recommendations change model behavior. Platform and environment
scenario receipts separately identify unexecuted NixOS, hardware, and editor paths.

PR 43 received a separate local review with no unresolved feedback. Its actual
devcontainer built and passed the smoke check and portable gate in a disposable
writable checkout. All applicable current-head and post-merge GitHub checks passed.
The feature branch was removed by the host and the completed local branch was
deleted after matching the merged head. Local `main` was advanced to `c3a2658`.
New skill work remains a separate local feature, not an implied publication.

## Follow-through after user authorization

The user subsequently requested implementation of the recommendations. All five
findings above are addressed in source: commit-message discovery and parent
continuation, browser harness ownership, conditional performance remedies,
maintenance-only Archify update awareness, and existing reconciliation authority.
Their original descriptions remain as the audit record, not current open findings.

The additional six developer-flow suggestions are implemented in
[setup and runtime contracts](../../skills/ci-maintenance/references/setup-contracts.md):
environment precedence, checkout isolation, bootstrap diagnostics, service
readiness, generated-contract drift, and optional secret-provider declarations.
The [follow-through verification](../../specs/012-workflow-guidance/verification.md)
records source scenarios, executed regression checks, and remaining runtime limits.
