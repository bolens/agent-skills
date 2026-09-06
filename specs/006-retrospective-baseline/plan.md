# Implementation plan: retrospective collection baseline

Date: 2026-09-05. Contract: [spec.md](spec.md). Baseline: `8e51a4f`.

## Summary

Add a collection-level retrospective feature with four domain contracts and a
complete skill-to-requirement inventory. Preserve original specs 001-004. Inspect
the adopted source-audit work, repair demonstrated gaps, and record deferrals.
The immediate missing implementation is the specification and traceability layer.
No new application runtime is proposed by this plan.

## Technical context

This is a Markdown collection maintained with Python 3.10+, Node syntax checks,
Bash, Make, and Spec Kit 1.0.3. The current manifest registers 61 skills. Existing
unit tests cover provenance, installation, selected helpers, and portability.
Use the existing tools and disposable fixtures, without new dependencies.
Installed skills are symlinks into the canonical checkout. Host execution,
production services, and external-model usage are separate evidence boundaries.

## Constitution check

- I: Edit canonical source and project-owned documentation only.
- II: Retain original source identities, licenses, and generated records.
- III: Import no upstream behavior. Correct the discovered blast-radius origin
  against its matching original source and retain the audited license.
- IV: Use existing portable tooling. Domain contracts name Linux/browser limits.
- V: Run `make check-fast` and `make check`; add no competing validation gate.

The explicit user retrofit request overrides the usual repository no-backfill
rule for this work. Record a narrow explicit-request exception in AGENTS.md and
the project guide. The constitution itself requires no amendment. The post-design
check has the same outcome: no constitutional exceptions or new runtime boundary.

## Source ownership and artifacts

- `contracts/maintenance.md`: fork maintenance, install/check behavior, delivery.
- `contracts/engineering.md`: design, review, diagnostics, security, concise prose.
- `contracts/web-visual.md`: web work, evidence, animation, Archify output boundary.
- `contracts/systems.md`: workstation, package, backup, network, and media work.
- `coverage.md`: exactly one primary row per registered skill and direct links.
- `assessment.md`: nine baseline audit dispositions plus the pstack follow-up and concrete remaining-work decisions.
- `research.md`, `data-model.md`, `quickstart.md`: decisions, record semantics,
  and reproducible validation.
- `tasks.md`: new work in this turn, not fabricated historical implementation tasks.
- `AGENTS.md`, `.specify/memory/project-guide.md`, `README.md`, `CHANGELOG.md`,
  `specs/README.md`: scoped policy exception and discovery.
- `skills/blast-radius/SKILL.md`: discovered E-006 repair for unavailable companion
  procedures, with a local fallback and explicit execution boundary.
- `UPSTREAMS.json`, generated provenance, `skills/blast-radius/LICENSE`, and
  `LICENSE.md`: correct the proven pstack origin without importing newer behavior.
- `docs/audits/2026-09-05-pstack-companions.md`: requested original-source audit,
  including corrected comparisons and remaining adoption decisions.

Managed `.specify/templates`, scripts, and generated integration skills remain
unchanged. `.specify/feature.json` selects the new feature using its supported
contract. Prior specs and audit records remain historical evidence.

## Execution and validation

Finish the design and traceability inventory before asserting coverage. Compare
accepted audit behavior with its owning source. Treat full application installs,
live Skill Doctor output, and fleet delivery outside this checkout as exclusions
or external limits. If source contradicts a contract, append a repair task with
acceptance evidence before editing it.

Use `quickstart.md` for a manifest comparison, local path and requirement checks,
Spec Kit discovery, and existing repository gates. Manual domain scenarios verify
instruction consistency only. Report skipped application and host tests. No new
unit tests are needed for prose-only changes; existing behavioral tests still run.
