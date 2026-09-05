# Changelog

All notable changes to this hard-fork collection are documented here.

## Unreleased

### Added

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
