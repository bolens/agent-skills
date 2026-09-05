# Scenario validation

1. A repository has native checks and a fleet reusable lint workflow: reuse both without introducing competing tools; inspect the security-audit input at the selected ref.
2. A docs-only PR hits workflow path filters: determine whether required checks will report, and avoid leaving merge permanently pending.
3. Merge queue is enabled: include the applicable merge-group validation and confirm required job names. Do not add unused queue assumptions to every repository.
4. A privileged metadata workflow proposes checking out fork code: preserve privilege separation and avoid executing the untrusted checkout.
5. A shared workflow adds a required input: inspect callers at their pinned refs, stage compatible changes, validate representative consumers, and track the rest through fleet scope.
6. CI fixes a tooling bug also present in maintained peers: propagate confirmed applicability under fleet authorization, not from a standalone PR alone.
7. A hook-only request: keep setup-pre-commit as owner. A flaky existing test: start with systematic-debugging, not a pipeline redesign.
8. An unavailable runner, scanner, or remote check: report unavailable coverage, not a green gate. Do not dispatch a publish workflow just to obtain execution evidence.
9. A workflow downloads an executable or builds container images: verify identity and affected trust boundary; no floating version copied from this skill.
10. A cache or artifact crosses from an untrusted job into publishing: treat its contents as untrusted and prove identity before use.

Run skill quick validation and make check-fast, then make check. Evaluate the scenarios independently where available. Scan changed artifacts and final commits for secrets without printing finding contents.

## Evidence, 2026-09-05

Source walkthrough covered all ten scenarios. An independent evaluator exercised three compound decision scenarios: optional shared security audit with docs-only filtering and merge queue, incompatible shared inputs/permissions across pinned consumers, and privileged fork execution with artifact publication. No blocking defect was found. Its artifact-publication clarity nit was applied so direct publication is covered alongside execution.

Skill quick validation, make check-fast, and full make check passed. All 26 tests, portability, provenance, references, and installed symlinks passed. The new skill is linked in all three managed client homes. No real CI workflow, runner, secret, host setting, or deployment was changed or dispatched for this evaluation. Host event behavior remains unexecuted scenario coverage.

Changed-artifact scan: 17 files, zero secrets, zero privacy indicators, zero skips. Gitleaks found no leaks in the same isolated fixture.
