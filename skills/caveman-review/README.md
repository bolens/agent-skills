# caveman-review

Terse presentation for the same systematic review performed by
[code-review](../code-review/SKILL.md). Use `/caveman-review` or request one-line
findings. Ordinary review requests use `code-review`.

Each finding keeps its location, impact, reachable failure, and smallest fix:

```text
save.ts:73: [P1] Save A's late response replaces newer B in the editor. Ignore responses for superseded revisions; reproduced with delayed A.
client.py:23: question: Does the server deduplicate POST retries? Confirm before retrying an ambiguous timeout.
```

Compression preserves evidence and uncertainty. Complex findings can use a
paragraph. A final receipt identifies scope, checks, and material coverage gaps.
Focused validation is allowed; edits and host review actions require authority.

See [SKILL.md](SKILL.md) for the full instructions.
