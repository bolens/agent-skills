# Unslop routing before and after

Evaluated on 2026-11-17 with Codex CLI 0.169.1 against the 67-skill catalog
at `df093fe0ec71c39f151c3a22e31ad4412ab2b0aa`. The before and after catalogs
differed only in `unslop/SKILL.md`. Its Git blob changed from
`e37278e2171441008c5e608865c73b50c18878f4` to
`dd24bca3a454c62ca55712a7e39338c87fc193d8`.

The revised skill routes to prose drafts, rewrites, style reviews, named
invocation, and handoffs for a specific artifact. It leaves incidental prose
to each task's usual writing guidance. Invocation settings remain the same.

Each [case](unslop-cases.json) ran on both variants and both requested model IDs
at low reasoning effort. The runs used fresh sessions, separate user catalogs,
the same read-only Git fixture, disabled tool networking, and a 180-second
deadline. The fixture excluded the rubric and credentials. Two follow-up
cases broadened editing coverage and made the named entrypoint read observable.
The original seven cases remain in the comparison.

The [trace summarizer](../../skills/evaluate-agent-workflows/scripts/summarize-codex-trace.py)
counted only successful shell reads of the entrypoint. Named injection can
supply instructions without a shell read, so the plain named invocation has a
separate observability check. Final answers were graded against the case
rubric separately. The named rewrite and the named read controls are excluded
from the automatic-routing counts.

## Observed reads

| Case | Sol before | Sol after | Astra before | Astra after |
| --- | --- | --- | --- | --- |
| Short customer update | — | — | — | — |
| README copy edit | `item_0` | `item_1` | — | — |
| PR body draft | `item_1` | `item_1` | — | `item_1` |
| Longer rollout-note edit | `item_1` | `item_1` | `item_1` | `item_1` |
| Named rewrite | — | — | — | — |
| Named rewrite with requested read | `item_1` | `item_1` | `item_1` | `item_1` |
| Code review | `item_1` | — | `item_1` | — |
| CI plan | `item_2` | — | `item_2` | — |
| Rive diagnosis | `item_1` | — | `item_2` | — |

A dash means the trace contains no observed entrypoint read. On the four
implicit writing cases, Sol read the intended skill in 3 of 4 before and
after, and Astra went from 1 of 4 to 2 of 4. Both read the revised skill for
the PR draft and longer edit. Both also read it when the named prompt requested
a file read. Both completed the naturally worded named rewrite, whose traces
did not expose a separate read.

Each model went from 3 of 3 to 0 of 3 incidental reads on the technical
controls. The final answers still met all three technical rubrics on both
variants. Both models wrote the short customer update correctly without an
observed read. Astra's short README edit retained the phrase “It is important
to note” in both variants. It preserved the command and the warning, but
missed that part of the editing rubric. Those were the only two answer
misses across the 36 runs.

This is a one-sample comparison. It shows that the revised trigger can
preserve selection on substantive drafting and editing while avoiding the
technical controls sampled here. It does not guarantee a read on every
short writing task or test changes to the editing rules in isolation.
