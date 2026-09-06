# Record model

## Coverage entry

A row in `coverage.md` has a unique registered skill name, its canonical
`SKILL.md` link, and one primary requirement reference. A requirement reference
identifies a domain contract and its stable ID, or an original feature spec.
The manifest remains authoritative for names, provenance, and installation.
Coverage rows do not become another install registry.

## Requirement

IDs use M for maintenance, E for engineering, W for web/visual, and S for systems.
Each requirement has an observable scenario and source ownership. A link to an
original spec preserves its more detailed contract. Domain requirements describe
baseline behavior and are not a claim of exhaustive runtime verification.

## Assessment

Each audit row identifies adopted source, implementation disposition, and limits.
States are implemented, partial, missing, deferred, or externally unverified.
A guidance implementation can coexist with a deferred runtime and unverified
host behavior. Only partial/missing accepted behavior creates a repair task.

## Evidence and task state

Evidence records method, scope, result, and omissions. Checked tasks refer to
work actually completed in this retrofit. Historical tasks are not rewritten.
A new source or capability requires reassessing its coverage and evidence.
