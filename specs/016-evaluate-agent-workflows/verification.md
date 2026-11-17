# First workflow evaluation

Run on 2026-11-17 against the 66-skill catalog at
`cac6f6514159af015ec677606ee7af11b7b49096` using Codex CLI 0.169.1.
The [case manifest](cases.json) specifies 13 natural-language tasks, one named
invocation, and an arithmetic negative control.

The scored runs used a dedicated user skill home with the full frozen catalog
and a separate read-only Git fixture. The CLI ran as `gpt-6.2-sol` and
`gpt-6.2-astra` at low reasoning effort, with fresh ephemeral sessions, a
180-second per-case deadline, and up to four in flight. Network and web tools
were disabled for the model, and the rubric and credentials were outside the
model's permitted paths. Both requested model IDs returned successful preflight
turns. The CLI trace did not independently report the serving model identity.

An initial project-scoped catalog trial hit the runner deadline before responses
completed. The scored matrix was restarted from the same catalog using
user-level discovery. The two discovery modes are separate observations.

The trace summarizer identified direct reads of skill entrypoints. Manual
review checked ambiguous reads and final answers against the case manifest.
An absent read is reported as unobserved, because named invocation can load
instructions internally. Extra skill reads are counted separately from the
case's expected skill. No case was intended to test a live GitHub workflow,
browser integration, or a write to an installed system.

## Results

| Measure | GPT-6.2 Sol | GPT-6.2 Astra |
| --- | ---: | ---: |
| Completed runs | 15/15 | 15/15 |
| Final answers meeting the case rubric | 15/15 | 15/15 |
| Intended entrypoint reads on natural-language cases | 13/13 | 11/13 |
| Named CI control with a successful CI reference read | 1/1 | 1/1 |
| Negative control answered with no observed skill reads | 1/1 | 1/1 |
| Runs with an observed `unslop` read | 14/15 | 5/15 |

Each cell below identifies the command event that read the expected entrypoint.
Every final answer met the corresponding rubric in the case manifest.

| Case | Sol event | Astra event | Evidence in the answer |
| --- | --- | --- | --- |
| rive | `item_1` | `item_1` | Inspect the actual machine and input, then test readiness and stale handles on remount. |
| ci | `item_1` | `item_2` | Preserve `Validate` on docs-only and code PRs, and test its failure path. |
| review | `item_1` | `item_1` | Identify the expired entry reaching the caller and propose a targeted fix. |
| git | `item_1` | Unobserved | Check whether the base met the original goal and preserve contributor credit. |
| architecture | `item_2` | `item_1` | Compare five pricing paths with shared inputs and rank by impact and change cost. |
| config | `item_1` | `item_1` | Trace the live symlink to the intended source and verify which default wins. |
| secrets | `item_2` | Unobserved | Review the exact publication scope, historical refs, current files, and attachments. |
| hooks | `item_1` | `item_1` | Use the existing Ruff setup and test partially staged files. |
| static-svg | `item_1` | `item_1` | Set consistent geometry, inherit theme color, and handle IDs and accessible names. |
| upstream | `item_1` | `item_1` | Compare upstream revisions and fork differences, then advance the pin after verified import. |
| css-motion | `item_1` | `item_1` | Make the latest navigation win and test a live reduced-motion change. |
| native-dialog | `item_1` | `item_1` | Distinguish native modality, Escape, and focus from app-owned history. |
| health | `item_2` | `item_1` | Correlate a pause with bounded resource and session evidence. |
| explicit-ci | `item_1` reference | `item_1` reference | Verify overlapping check names before switching settings and retiring the old name. |
| negative | No tool call | No tool call | Return `135`. |

Astra had no shell events on the Git takeover and publication-audit prompts.
Both answers still covered the requested procedure, and neither run provides
evidence about how the model would handle the same workflow with a real checkout.
For the named CI control, both traces showed a successful read of the GitHub
Actions reference. Neither showed a separate entrypoint read.

Sol also loaded `code-review` for the Git takeover plan and `web-animation`
for the Rive case after reading `animation-assets`. The frequent `unslop`
reads make that skill's discovery scope a candidate for a targeted follow-up
test. This run does not measure the effect of the previous description edits,
because both models used the same revised catalog. One sample per model and
prompt is exploratory, and the plan-based cases leave live execution untested.

Portable repository validation ran 215 tests with one platform-specific skip.
The trace parser regression exercised batched reads, metadata-only reads,
failed reads, file listings, and the completion event.
