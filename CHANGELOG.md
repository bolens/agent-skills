# Changelog

All notable changes to this hard-fork collection are documented here.

## Unreleased

### Added

- Add a canonical repository for 30 personal skills with provenance records,
  validation, CI, pre-commit checks, and managed installation symlinks.
- Add workstation health, managed configuration drift, and sensitive-information
  audit skills.
- Add an Omarchy desktop-session diagnostic guide and focused cross-skill
  handoffs.
- Add audited upstream tracking, a weekly drift check, and a guarded sync skill.
- Add the Caveman `migration`, `safe-refactor`, and `verify-and-stop` skills to
  cover previously unowned workflows.

### Changed

- Mark every maintained skill as a hard fork and retain links or local origin
  references for its source.

### Security

- Update Archify's `fast-uri` override to 3.1.6, resolving four high-severity
  URL parsing advisories reported by Dependabot.
