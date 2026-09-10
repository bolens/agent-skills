# Changelog

All notable changes to this hard-fork collection are documented here.

## Unreleased

### Added

- Add internationalization guidance for messages, locale data, RTL, Unicode input,
  and deterministic verification. Connect content clarity, privacy, recovery, and
  authoritative standards references to their existing workflows.

### Fixed

- Coordinate concurrent skill installs with JSON receipts, preserve existing links
  on replacement failure, and handle POSIX catalog aliases. Keep task handoffs
  and shared browser workloads under one coordinator.

- Detect stale skill links, catalog conflicts, and excluded Hermes entries before
  installation. Add pinned native loader checks and clarify cross-client discovery,
  resource permissions, and helper backend requirements.

- Support optional Hermes and Pi skill homes while preserving existing installs
  and explicit-only invocation policies. Document client tool and discovery limits.

- Ground interface and workflow design in user, developer, and agent task completion,
  with guidance for discoverability, structured contracts, recovery, and measured benefit.

- Retry macOS zombie-group signals after reaping the owned child, preserve real
  permission failures, and include process inspection tools in the Linux dev image.

- Bound polluter progress and error reporting when output consumers stop reading.

- Bound test-polluter discovery and execution, skip dependency/cache trees,
  run tests in stable order, and stop owned descendants on timeout or cancellation.

- Cap capture command and server logs, preserve cancellation during process
  startup, and bound waits for cleanup. Exercise PNG size limits with a fixture
  that passes the PNG structure check.

- Preserve cancellation during health-probe cleanup, accept output exactly at
  its byte limit, and mark writable reports incomplete after total timeout.

- Remove GNU path-tool dependencies from health collection, verify cleanup on
  POSIX hosts without `/proc`, and stabilize audit finding order across scans.

- Reject oversized capture matrices and viewports before browser launch, and
  hash screenshots in bounded chunks with a PNG size limit.

- Avoid quadratic email scanning on long tokens and enforce file-read limits
  when audit candidates grow or change type during inspection.

- Bound workstation health probes, output, and collection time; clean up probe
  descendants and preserve existing report files. Use cached package checks
  without refreshing databases during health collection.

- Require Make and the correct writable Git root before devcontainer setup reports
  readiness, and explain Git, access, and Node-version failures.

- Correct competing environment-contract ownership, pending-input validation,
  runtime secret-file guidance, browser fallback selection, and performance examples.
- Prevent Archify acknowledgement-ordering fixtures from racing their short
  generic network deadline under suite load; retain production timeout behavior.

- Reject unrecorded Spec Kit core files and non-regular integration files, so
  removed manifest entries cannot hide existing files and named pipes cannot hang
  the integrity check.

- Check all Spec Kit integration files in the fast gate, detecting missing helpers,
  edited templates, and generated skill drift against their recorded manifests.

- Preserve parent commit and authorized reconciliation workflows; keep authenticated
  browser captures in their existing harness, performance remedies evidence-led,
  and Archify update notices scoped to maintenance or explicit discovery.

- Scope Omarchy desktop and crash-helper routing to the actual installation,
  and honor existing authorization for a requested configuration reset.

- Preserve neighboring files during compression and report incomplete directory,
  discovery, pollution-search, and health-report operations as failures.
- Align Caveman help with packaged behavior and keep unavailable reviewer or
  transcript evidence explicit in work logs.

- Stop fleet check descendants on SIGTERM and retain interruption evidence so
  cancelled checks release their retry locks.
- Reject incompatible or inconsistent fleet receipts instead of reporting a
  successful check from invalid saved evidence.

### Added

- Define acceptance contracts for the recent Spec Kit checker and editor-container
  setup scripts, with malformed-input, setup-failure, and preservation tests.

- Add reference-led CSS normalization/reset selection, cascade-layer integration,
  and browser/accessibility verification guidance.

- Add conditional environment precedence, bootstrap diagnostics, concurrent-service
  isolation/readiness, generated-contract checks, and optional SecretSpec guidance.

- Prefer `.env.spec` environment contracts and native schema-backed examples, with explicit validation and coordinated consumer migration.

- Prefer shared, pinned development tooling through mise, devenv, devcontainers,
  and applicable NixOS VMs in CI and related maintenance workflows.

- Add Arch system configuration, CachyOS repository/driver/tuning, and NixOS
  declarative configuration skills with explicit activation and recovery evidence.

- Add optional local Sentrux snapshots and structural comparisons on Linux x86_64,
  with verified runtime artifacts, retained license notices, and explicit source scopes.
- Specify all 62 registered skill capabilities, executable helpers, and Archify
  commands, viewer interactions, and export boundaries.

- Add `release-packaging` for language/build-conditional distribution targets,
  native source/binary/main variants, lean installations, and current-platform
  compatibility. Connect release, Arch, CI, dependency, and fleet workflows.

- Add bounded source excerpts, focused worker handoffs, and durable correction
  guidance to fleet maintenance.

- Add CI maintenance guidance for fleet baselines, reusable workflow contracts,
  event trust, required-check coverage, and repository-native validation.

- Add homelab stack maintenance for coordinated Compose, environment example,
  preparation, metadata, ingress, and generated documentation changes.

- Add `git-hygiene` for concurrent agent ownership, isolated worktrees, focused
  commits, and validation across repository surfaces.

- Add media preservation, Arch package maintenance, network exposure verification,
  and Quickshell development workflows.
- Add web security, technical SEO, and web-standard workflows, including native
  browser controls, compatibility fallbacks, and optional `llms.txt` verification.
- Add form and async-data guidance for preserving drafts, ordering requests,
  reconciling optimistic updates, and verifying failed or conflicting saves.
- Add web animation guidance for GSAP, Motion, browser-native transitions, and
  other existing framework runtimes, with separate Lottie/dotLottie and Rive workflows.
- Add static SVG design and reusable design-system workflows for icons, tokens,
  component variants, themes, and state verification.
- Add `babysit` to follow open PRs through separate audits, actionable review
  feedback, CI repairs, and repository-specific release preparation and verification.
- Add an SVG animation skill for geometry-safe, accessible, browser-native motion
  with multi-phase visual verification.
- Add a canonical repository for the personal skill collection with provenance records,
  validation, CI, pre-commit checks, and managed installation symlinks.
- Add workstation health, managed configuration drift, and sensitive-information
  audit skills.
- Add an Omarchy desktop-session diagnostic guide and focused cross-skill
  handoffs.
- Add audited upstream tracking, a weekly drift check, and a guarded sync skill.
- Add the Caveman `migration`, `safe-refactor`, and `verify-and-stop` skills to
  cover previously unowned workflows.
- Add audited hard forks of `web-quality-audit`, `performance`,
  `core-web-vitals`, and `accessibility` from Addy Osmani's Web Quality Skills.
- Add `homelab-stack-triage`, `backup-restore-verification`, and
  `arch-update-recovery` for operational gaps specific to this fleet.

### Changed

- Align commit messages and PR titles with Conventional Commits, and release
  version selection with SemVer across authoring, validation, and delivery skills.
  Preserve repository policies and native package version rules.

- Make skill selection boundaries clearer and load accessibility and performance
  guidance by observed issue. Keep broad audit coverage and make recurring
  maintenance opt-in.
- Give stalled Archify repairs one bounded diagnostic escalation while preserving
  validation and diagram meaning.
- Distinguish unavailable fleet inventory evidence from clean repositories,
  including invalid nested Git markers, and compare repeat audits using compatible
  observations.

- Add requirement-driven older-browser support guidance covering support matrices,
  syntax transforms, targeted polyfills, loading order, production delivery,
  minimum-version testing, and deliberate retirement of compatibility layers.

- Prefer latest stable web features and maintained tool versions across web
  standards, frontend design, design systems, animation, performance, and quality
  audits. Require legacy compatibility only for explicit contracts, retain current
  cross-engine verification, and remove dated browser-support percentages.

- Prefer immutable dependency pins paired with Dependabot version-update
  monitoring in CI maintenance, dependency triage, and repository fleet audits.
  Distinguish configured coverage from verified operation and record unsupported
  pins or existing updater choices.

- Add an explicitly requested retrospective Spec Kit baseline mapping all 61
  registered skills to contracts, source-audit dispositions, and evidence limits.
  Repair `blast-radius` steps that depended on unavailable companion workflows
  and correct its pstack origin and retained license after auditing the originals.
  See the [specification index](specs/README.md).

- Refine architecture audits with comparable structural evidence and web animation
  with deterministic playback-clock guidance after reviewing Netviz and Sentrux.
  Defer both application installs. See the
  [source assessment](docs/audits/2026-09-05-netviz-sentrux.md).

- Add wide-event and error-handling guidance to systematic debugging, with
  operation-local context, preserved failure semantics, sensitive-field
  exclusion before logging, and leak-test expectations. See the
  [source assessment](docs/audits/2026-09-05-wide-events.md).

- Refine repeat fleet audits and skill evaluations after reviewing the memory
  engineering article: compare compatible evidence, retain unresolved findings,
  and record why prior conclusions change. See the
  [audit](docs/audits/2026-09-05-memory-engineering.md).

- Refine CI and debugging guidance after auditing Paul Solt's app-building
  articles: preserve process failures through output pipelines, retain useful
  diagnostics, and bind runtime and API evidence to the tested build. See the
  [audit](docs/audits/2026-09-05-paul-solt-workflows.md).

- Refine skill discovery and maintenance after auditing Claude Code's built-in
  Skill Doctor: distinguish installed, listed, and invoked skills; qualify
  context and usage evidence; and verify routing before pruning. See the
  [audit](docs/audits/2026-09-05-skill-doctor.md).

- Refine security finding assessment and patch review after auditing Codex
  Security: preserve each claim, record counterevidence and unresolved coverage,
  verify original attack paths after fixes, and distinguish artifact integrity
  from report accuracy. See the [audit](docs/audits/2026-09-05-codex-security.md).

- Refine CLI browser evidence after auditing Obscura: verify backend effects,
  distinguish incomplete captures from fidelity differences, refresh snapshot
  references, and check control-session ownership. See the
  [source audit](docs/audits/2026-09-05-obscura.md).

- Refine coordinated work and verification with explicit dependency reasons,
  checks that can reject bad results, scoped correction receipts, and evidence
  reuse tied to dependency changes. Record the source assessment and validation
  in the [loops and graphs audit](docs/audits/2026-09-05-loops-and-graphs.md).

- Refine architecture design and audit guidance after reviewing Ponytail: compare
  concrete reuse options against required behavior, record revisit conditions,
  and require evidence before removing seams or tests. See the
  [audit and validation record](docs/audits/2026-09-05-ponytail.md).

- Restore missing fork and Spec Kit licenses, correct frontend-design's Anthropic
  provenance, retain bundled dependency notices, and check license-copy integrity.

- Clean up task-owned temporary evidence and screenshot directories at feature
  completion, preserving deliverables, visual baselines, and pending review evidence.

- Refresh base and feature revisions before PR submission, reconcile host-side
  updates locally, and verify eligible local checkouts are synchronized after merge.

- Include older completed feature branches and related remotes in scoped Git
  cleanup, verifying integration and ownership separately for every candidate.

- Check maintained peers for shared fixes and applicable improvements during
  fleet implementation, with per-repository validation and explicit coverage.

- Keep homelab incident evidence private, distinguish preparation and validation
  side effects, and connect stack fixes with exposure and dependency workflows.

- Have `babysit` complete verified post-merge branch and temporary local worktree
  cleanup through `git-hygiene`, preserving active or unintegrated work.

- Review changed contracts and consumers systematically, distinguish staged and
  working-tree evidence, and carry coverage gaps through terse reviews and PR delivery.
- Use independent reviewers with distinct focuses for substantive PRs when available,
  and reconcile findings and actionable nits from every review before readiness.

- Automatically route PR repairs and requested PR or release delivery from related
  skills to `babysit`, preserving local-only and read-only task limits.

- Align media preservation with the audio, image, video, and archive utility
  family, including image fidelity, archive extraction, and shared-tool validation.
- Extend backup verification with isolated service recovery drills and let
  `babysit` follow standalone releases without requiring an open PR.
- Make responsive captures preserve reruns, bound browser execution, isolate
  browser profiles, and record incomplete runs and requested motion settings.
- Focus CLI web evidence on application readiness, comparable rendering states,
  and bounded whole-page coverage, with detailed capture guidance loaded as needed.
- Ground frontend design in the product's existing identity, components, content,
  and interaction states instead of requiring a new visual direction for every edit.
- Verify animation geometry, instance cleanup, and runtime-specific reduced-motion
  states across the SVG, accessibility, performance, and browser-evidence workflows.
- Replace Bash-based repository maintenance helpers with cross-platform Python,
  support Git worktrees when installing hooks, and validate portable shebangs
  and line endings.
- Install skills into shared Agent Skills and Claude homes for use by Cursor,
  Gemini CLI, Copilot, OpenCode, Windsurf, Claude Code, and the Claude Agent SDK.
- Capture whole-page web evidence with scroll-triggered rendering, overlapping
  top-to-bottom frames when needed, and coverage metadata.
- Route SVG-specific motion work from frontend design and CLI web evidence to
  the SVG animation skill.
- Mark every maintained skill as a hard fork and retain links or local origin
  references for its source.
- Cross-reference web, workstation, configuration, fleet, homelab, backup, and
  Arch workflows only at their real diagnostic or verification handoffs.
- Bound fleet inventory discovery by configurable depth and prevent repositories
  without GitHub workflows from terminating the scan.

### Security

- Update Archify's `fast-uri` override to 3.1.6, resolving four high-severity
  URL parsing advisories reported by Dependabot.
