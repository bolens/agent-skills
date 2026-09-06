# Maintenance contract

Retrospective at `8e51a4f`, recorded 2026-09-05. See [scope](../spec.md).
The [coverage map](../coverage.md) identifies each owning skill.

## M-001: Canonical forks and installation

Maintain canonical skills under `skills/`, stable origins, exact audited revisions,
retained license bytes, preserve paths, and local customizations. Generated
PROVENANCE.json and UPSTREAM.md must agree with UPSTREAMS.json and source.
Install targets remain per-skill data. Check mode is read-only. Apply mode may
repoint symlinks but refuses real files/directories without explicit replacement.
The installer is not transactional and does not remove obsolete entries.

Acceptance: a disposable three-home installation resolves registered sources;
a conflicting real target is reported rather than replaced by default. Changed
license bytes or stale generated pointers fail the existing validation.

Source: scripts/update-provenance.py, scripts/link-installed.py,
scripts/validate.py, tests/test_repository.py, tests/test_licenses.py.

## M-002: Selective discovery and reviewed upstream maintenance

Compare candidate behavior with installed capabilities, inspect actual source,
and retain invocation policy and local changes. Revisit dated audit conclusions
using compatible identity and new evidence. Installed, host-discoverable, and
observed-used are separate states. No automatic pruning, imports, or publication.

Acceptance: an unused recovery skill is retained without evidence of redundancy;
a previously deferred candidate is reconsidered only against its recorded reason.

Source: find-skills, sync-skill-upstreams, scripts/audit-upstreams.py.

## M-003: Repository integration and delivery

Preserve unrelated work, isolate concurrent writers when permitted, validate the
integrated candidate, and distinguish local commits, pushed heads, PR checks,
verified merge, and cleanup. Follow current base/head evidence and action authority.
The detailed contracts remain [Git hygiene](../../001-git-hygiene/spec.md) and
[CI maintenance](../../003-ci-maintenance/spec.md).

Acceptance: a dirty independent worktree survives cleanup; stale green checks do
not prove the latest head; a read-only audit does not authorize a push.

Source: git-hygiene, babysit, resolving-merge-conflicts, audit-repo-fleet,
ci-maintenance, setup-pre-commit, triage-dependency-updates, RELEASING.md.

## M-004: Validation and managed integration

Use the shared Make targets for metadata, provenance, syntax, tests, portability,
and installed links. Keep the separate Archify and shared lint/security gates
explicit. Preserve generated Spec Kit integration through its managed update
workflow. Bounded source reading retains [feature 004](../../004-bounded-context/spec.md).

Acceptance: ordinary checks never claim full browser coverage; source excerpts
respect the byte/line ceiling; Spec Kit discovery finds the selected feature.

Source: Makefile, .github/workflows/, .specify/, tests/, scripts/.
