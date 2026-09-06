# Engineering workflow contract

Retrospective at `8e51a4f`, recorded 2026-09-05. See [scope](../spec.md).
The [coverage map](../coverage.md) assigns primary owners.

## E-001: Architecture discovery, design, and domain decisions

Broad architecture audits rank source-backed friction; focused design compares
specific boundaries. Preserve repository domain terms, invariants, ADRs, behavior,
and retain-current-design options. Simplification names the replacement and its
semantic gaps. Structural comparisons record revision, scope, parser coverage,
and rule coverage. Scores alone neither justify a refactor nor prove correctness.

Acceptance: a higher score with a forbidden import remains a violation; different
parser versions require compatible rescans; one implementation does not by itself
justify deleting an interface. A design review remains read-only until authorized.

Source: improve-codebase-architecture and references/structural-evidence.md,
codebase-design, domain-modeling, grilling.

## E-002: Bounded changes and verification

Refactors preserve interfaces, errors, ordering, and behavior. Migrations retain
compatibility and a rollback path. Test-first work demonstrates failure before a
fix where feasible, using behavioral assertions. Verification stops at the agreed
acceptance boundary. A requested project verification skill reflects real app
surfaces, prerequisites, safe fixture state, and reproducible evidence.

Acceptance: a green structural check does not replace behavioral proof; a
validation-only request creates no unrelated refactor or dependency upgrade.

Source: safe-refactor, migration, tdd, verify-and-stop, create-verification-skill.

## E-003: Diagnosis and privacy-aware error evidence

Trace reproducible failures before fixes. Preserve process/exception outcomes
through logs and pipelines. Wide events use operation-local, allowlisted context,
opaque correlation, stable failure classification, bounded output, and redaction
before buffers/exporters. Logging failure cannot mask the original outcome.

Acceptance: concurrent operations retain separate context; cancellation and retries
keep their semantics; a future logger implementation tests synthetic sensitive
sentinels across every enabled sink, including fallback output. A generic scanner
alone cannot prove the absence of sensitive data in application logs.

Source: systematic-debugging and references/wide-events.md, sensitive-info-audit.
This is a guidance contract, not a bundled logger or an application leak-test suite.

## E-004: Review and security boundaries

Review actual callers, trust boundaries, preconditions, exploitability, and affected
versions. Separate a report's claims from confirmation and repair evidence. Keep
reviews read-only unless fixes are authorized. Use controlled accounts and fixtures
for boundary tests; separate local proof from deployed behavior and host evidence.

Acceptance: a plausible security report without a reachable caller remains
unconfirmed; a fix preserves the authorized path and rejects the unauthorized path;
terse review still identifies severity, location, evidence, and coverage limits.

Source: code-review, caveman-review, web-security, sensitive-info-audit.

## E-005: Writing and decision records

Keep technical prose factual, concise, and tied to source. Changelogs describe
meaningful delivered changes. Concise commit/review formats preserve technical
meaning. Requested compression preserves a readable backup and literal code or
required identifiers. Long-running decision records retain reasons and evidence
within the requested publication boundary.

Acceptance: stylistic compression does not erase a required caveat or alter a
command; an intent-only commit message still names the coherent change.

Source: technical-writing, unslop, changelog-maintainer, caveman, caveman-commit,
caveman-compress, caveman-help, show-me-your-work.

## E-006: Change impact without unavailable companions

Trace cross-module, wire-format, configuration, and lifecycle consumers beyond
the immediate diff. Identify the facts on which safety depends and exercise the
real code in an isolated fixture when feasible. Mark unproven assumptions and
unavailable runtime evidence. Inspect local history directly and use the existing
code-review workflow for review scope and permitted independent checks.

Acceptance: without `how`, `why`, or `arena` skills, an impact assessment still
completes through direct source/history inspection. Unavailable delegation falls
back to local review. Executable probes do not grant permission for live writes,
external model calls, or publication.

Source: blast-radius. At the retrospective baseline, this skill depended on those
unprovided companion procedures. E-006 is a scoped repair requirement discovered
during this retrofit, not a claim that the baseline already satisfied it.
