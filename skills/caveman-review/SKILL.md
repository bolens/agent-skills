---
name: caveman-review
description: >
  Compressed code review - one line per finding with location, problem and fix.
  Use for /caveman-review or when the user requests terse, one-line review findings.
  Ordinary review requests use code-review.
---

# Terse review findings

Use [code-review](../code-review/SKILL.md) for scope, contract tracing, evidence, severity, and coverage. This skill controls presentation, not review depth. If code-review is already active, format its results without restarting the review. If unavailable, inspect the requested diff and affected callers, verify reachable failure scenarios, and disclose coverage limits.

## Format

Write one line per finding: `<file>:<line>: [P1] <trigger and consequence>. <smallest fix>.`

Use the repository's severity labels when defined. Keep exact symbols, evidence, and meaningful uncertainty. Severity describes impact, not confidence. Label a source-proven finding as such when it could be mistaken for an executed reproduction. Use `question:` for an unresolved assumption and `nit:` for an optional preference, never to disguise a speculative bug as a finding.

Group duplicate symptoms under their shared cause. Omit praise, restatements of the diff, generic cleanup advice, and arbitrary prescriptions such as a retry count unsupported by the operation's contract.

Examples, only when the stated behavior is established by inspection:

- `users.py:42: [P2] A missing user makes find() return None, then .email raises. Handle not-found before dereference; confirmed by source.`
- `save.ts:73: [P1] Save A's late response replaces newer B in the editor. Ignore responses for superseded revisions; reproduced with delayed A.`
- `client.py:23: question: Does the server deduplicate POST retries? Confirm before retrying an ambiguous timeout.`

A short finding still needs enough context to be checked. Use a paragraph when a security boundary, data-loss sequence, or architectural consequence cannot be explained accurately in one line. Resume terse output for other findings.

## Receipt and boundaries

End with a compact scope/checks/gaps line. Identify the reviewed revisions or local layers and material unreviewed boundaries. If no actionable findings remain, say so with any coverage limits; do not replace this with an approval claim.

Review without modifying product files, posting comments, or approving/requesting changes on the host unless authorized. Focused checks with autofix disabled may establish evidence. "stop caveman-review" or "normal mode" returns to normal review prose.
