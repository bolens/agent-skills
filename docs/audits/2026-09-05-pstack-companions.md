# Original how, why, and arena audit

Audited 2026-09-05 at
[`cursor/plugins` revision `93b00b89ef425a9c1bac0d0b317dfc49c930ac99`](https://github.com/cursor/plugins/tree/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack).
The pstack plugin manifest identifies Lauren Tan, version 0.14.8, and MIT terms.
This is the source matching the companion names in this collection's blast-radius
skill, not an unrelated project sharing the name arena.

The earlier conversational judgment that all three workflows were sufficiently
covered was too broad. In particular, independent review does not reproduce
arena's competing-artifact synthesis, and Git history alone does not reproduce
why's cross-source historical investigation.

## What the originals actually implement

| Workflow | Actual procedure | Existing coverage and verdict |
| --- | --- | --- |
| [how](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/how/SKILL.md) | Explain mode traces runtime paths and produces a subsystem explanation. Complex questions use explorer agents and a synthesizer. Critique mode adds architectural critics with a rubric. Four reference prompts separate discovery, explanation, and criticism. | Source tracing is available directly; architecture critique overlaps improve-codebase-architecture. A standalone onboarding/explanation workflow is distinct from code-review, but mandatory agent synthesis for even simple questions does not establish enough benefit to install the original wholesale. |
| [why](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/why/SKILL.md) | Anchors a decision to code/history, searches seven evidence categories through available tools, and synthesizes direct, supported, inferred, speculative, and unknown claims. References cover Git, tickets, documents, chat, observability, errors, warehouse queries, and incidents. | The collection has local history/ADR checks and evidence discipline, but no equivalent cross-source rationale procedure. This is the strongest candidate for a selective future adaptation, particularly for thresholds, defensive code, and incident-driven decisions. It is not fully covered by codebase-design. |
| [arena](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/skills/arena/SKILL.md) | Frames one task, generates competing artifacts in separate locations, cross-judges completed candidates, selects a base, incorporates useful parts, and verifies the synthesis. It records rationales, rejections, and dropouts. | DESIGN-IT-TWICE covers contrasting interface proposals; independent code-review covers findings about one candidate. Neither is a full competitive implementation workflow. Defer a general arena skill until a task justifies duplicate implementations and synthesis cost. |

## Findings affecting adoption

1. **Host/model assumptions need adaptation.** All three use Cursor-specific Task
   arguments and configured or hardcoded model roles. Their entrypoints carry
   `disable-model-invocation: true`. They do not offer a complete local fallback
   for unavailable delegation. Do not copy those fields or model requirements
   into this collection without explicit host and invocation-policy decisions.

2. **Why's search posture is broader than the usual task needs.** It defaults to
   one investigator per available evidence category, normally followed by a
   synthesizer. Investigators use `readonly: false` to retain Cursor MCP access,
   while their prompts prohibit writes. Tool availability is not action authority.
   A local adaptation should select sources by the unresolved question and actual
   access, use read-only operations, and avoid automatic external-model calls or
   scans of unrelated private data.

3. **Why contains an inconsistent absence rule.** Step 3 says a null ticket search
   is evidence that the decision was not ticketed. Its epistemics reference warns
   against treating absence as proof, and source playbooks correctly identify
   retention and access gaps. The latter is the sound rule: a scoped empty search
   establishes only that no relevant result was found in that search. It cannot
   establish that no ticket ever existed.

4. **Historical correlation is useful but cannot establish intent by itself.**
   The Datadog, Sentry, and warehouse playbooks discuss release timing, changing
   instrumentation, sampling, schema/retention limits, and neighboring changes.
   Keep those qualifications. A matching p99 and threshold is a lead, not proof
   that an author chose the constant from that distribution. One incident copied
   into several systems is not several independent confirmations.

5. **Arena has meaningful isolation and completion rules.** Candidates write to
   separate worktrees/directories, and the judge waits until candidate generation
   finishes. It handles missing candidates and requires verification after the
   synthesis. Those are real benefits beyond ordinary review.

6. **Arena consensus remains weaker than verification.** Its agreement language
   is not evidence that independent implementations preserve all invariants.
   Shared prompts or assumptions can produce the same defect. A future adaptation
   needs a bounded rerun policy, preserved acceptance criteria, no model-family
   requirement, and verification of the final combined artifact.

## Present decision

Do not import the three skills unchanged. The question is not whether their names
overlap, but whether their additional procedure earns its operational cost.

- Keep direct explanation and existing architecture critique for how-like work.
- Treat why as a real capability gap worth selective adaptation when historical
  rationale across connected sources is needed. Preserve scoped search, competing
  explanations, citation checks, and explicit unknowns. A future implementation
  needs its own contract; this audit does not install it.
- Keep arena distinct from review. Use existing interface comparison for design
  alternatives and independent review for evaluating one change. A future
  competing-artifact task can justify adding the remaining synthesis procedure.

The current blast-radius repair supplies a complete local impact-assessment path.
Its use of code-review for broad assessment is an intentional scoped replacement,
not a claim that code-review implements all of arena. No unavailable original
workflow is necessary to carry out its local source/history and proof steps.

## Provenance correction

A byte comparison found that baseline `8e51a4f:skills/blast-radius/SKILL.md` equals
the upstream file after removing its single Cursor invocation flag. The earlier
local-original provenance was wrong. Corrected UPSTREAMS.json records the exact
repository, source path `pstack/skills/blast-radius`, revision, retained local
changes, and preserved agents directory. Generated PROVENANCE.json and UPSTREAM.md
now agree. The original pstack MIT license is retained in the skill with SHA-256
`bc957ca6bee02792566a1a028d105e02e247c6e77cf057061674273da77b200e`.
Current invocation policy remains unchanged. No newer upstream behavior was imported.

## Audit coverage and limits

Read the three complete entrypoints, all four how references, all twelve why
references including its eight source/incident playbooks, the arena entrypoint,
pstack manifest/license, and the matching blast-radius source. The three workflow
directories contain Markdown procedures, with no executable helper implementation
to build. Their prompts direct host tools and agents; those runtime behaviors were
not executed. No private connector, model runner, or host configuration was used.

Compared local code-review, its independent-review reference, codebase-design and
DESIGN-IT-TWICE, architecture-audit guidance, and blast-radius. Checked the complete
original-to-baseline blast-radius diff and reviewed the local repair. The original
branch was fetched once and pinned; this is not a claim about future updates.
