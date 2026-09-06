# Implementation plan

Keep the executable and handoff reference in the existing audit-repo-fleet skill.
Add behavior tests under tests/ and run the existing portable validation gate.
No new skill registry entry or installed-link change is needed.

Update only project-owned AGENTS.md in maintained consumers. Use their existing
project-guide.md for durable corrections, without modifying managed Spec Kit
templates or adding empty ruling files. Keep consumer changes local to isolated
feature worktrees and preserve per-repository commit rules.

Constitution check: provenance is unchanged, Python uses the standard library,
and tests use disposable files. No new external capabilities or permissions.

Validation includes overflow without output, exact boundary success, numbered
ranges, bounded long-line handling, UTF-8, missing/non-file inputs, and invalid
arguments. Walk through a bulk survey, direct edit, and unpermitted delegation
to check that the instructions preserve judgment and authority.
