# Changelog

All notable changes to this hard-fork collection are documented here.

## Unreleased

### Added

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
