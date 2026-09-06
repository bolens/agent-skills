# Bound context during fleet work

Read required repository guidance, then use tracked paths and focused `rg`
queries to locate the relevant source. Avoid recursive workspace dumps that
include linked worktrees, generated output, dependencies, and runtime files.
Inspect actual source before editing or making correctness claims.

## Local source reader

Run the skill's `scripts/context-read.py` with Python 3.10 or newer:

```sh
python3 scripts/context-read.py path/to/source.py
python3 scripts/context-read.py path/to/source.py --start 120 --limit 80
```

Resolve the script relative to this skill, not the target repository. The first
form accepts whole files up to 350 lines. The second selects a one-based range
of at most 350 lines. Both cap the complete UTF-8 JSON response at 24 KiB.
Output includes numbered source lines and `next_start` when another line exists.
Overflow, invalid arguments, non-UTF-8 selected source, and unavailable files
exit 2 without printing partial source. Empty whole files are valid. An explicit
start past EOF is an error. Stderr explains how to narrow an oversized read.

This is an output bound on this helper, not a tool hook or security sandbox.
Other readers remain available, including for required guidance. It neither
summarizes source nor calls a model. The 350-line threshold is a starting point
for exploration, not permission to omit required contracts or final review.

## Focused worker handoffs

Use workers only when session instructions permit delegation and a bounded task
can run alongside useful local work. Keep small reads local. Use an available
lower-cost model only when model selection is permitted and its capability fits
the task. Do not hardcode a provider, infer permission, or weaken review to save
tokens.

| Task | Supply | Return | Coordinator verification |
| --- | --- | --- | --- |
| Source survey | One question, repository/revision, allowed files, read-only scope | Findings with paths and symbols, evidence, unknowns, no file dumps | Open the relevant source ranges before editing or deciding correctness |
| Mechanical draft | Concrete output path, behavior specification, required reference example, allowed writes, native check | Changed paths, concise diff summary, checks and gaps | Inspect the actual diff and source, run relevant checks |

Record task ownership through Git hygiene. A reader has no write assignment.
Use runtime tool restrictions when available, and do not describe a prose rule
as an enforced permission. A writer saves directly to its owned worktree but
does not commit other work or publish. Debugging, architecture, concurrency,
security-sensitive decisions, and final review remain with the coordinator.
Worker summaries are navigation aids, not authoritative source or test results.

## Durable context and recurring reports

Keep reusable repository facts in the existing project guide or owning contract.
When a user correction affects future work, update that source with its scope,
reason, and supporting evidence. Read relevant corrections before using the old
assumption. Replace superseded advice instead of accumulating contradictory rules.
Keep temporary progress and private operational values out of shared guidance.

For an explicitly requested recurring report, define sources, successful prior
run boundary, named output, and delivery authority. Cover activity since the last
successful run, including missed runs. Repeat an unresolved blocker only with
its age and current evidence. Report unavailable sources as gaps. Advance the
checkpoint only after successful output, and consume completed predecessor
results rather than assuming a fixed time gap guarantees ordering. Reuse an
existing scheduler when available. Do not enable a schedule as a side effect
of an ordinary fleet task.

These adaptations draw on the [source-reading example](https://x.com/undefinedKi/status/2095942506433089832/photo/1)
and [persistent-context article](https://x.com/undefinedKi/status/2095876609689498067).
No fleet token-savings benchmark or Portal integration is implied.
