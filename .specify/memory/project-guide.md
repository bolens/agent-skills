# Agent skills project guide

Use this guide with [AGENTS.md](../../AGENTS.md) and the
[constitution](constitution.md) before Spec Kit planning or implementation.
It maps this collection's requirements to source ownership and acceptance
evidence. It is project-owned guidance, not an upstream-managed template.

## Source and ownership

| Surface | Role in a change |
| --- | --- |
| `skills/<name>/SKILL.md` | Task selection, invocation boundary, instructions, and handoffs |
| Skill references, scripts, and assets | Conditional detail, executable behavior, and reusable output |
| `UPSTREAMS.json` | Exact audited revisions, source paths, and local changes to preserve |
| `scripts/update-provenance.py` | Generates origin pointers, registry records, and install-target rules |
| `PROVENANCE.json` and `skills/*/UPSTREAM.md` | Generated provenance and installation contracts |
| `scripts/link-installed.py` | Checks or applies client-home symlinks |
| `scripts/validate.py`, `scripts/check-portability.py`, and `tests/` | Automated repository evidence |
| `Makefile` and `.github/workflows/ci.yml` | Shared local and CI validation entry points |
| `specs/` | Feature contracts, decisions, tasks, and verification history |

Read the affected skill's `SKILL.md` and `UPSTREAM.md` before planning changes.
Identify locally authored behavior, imported behavior, generated outputs, and
consumer skills. Preserve every recorded local customization during an import.
[CONTRIBUTING.md](../../CONTRIBUTING.md) describes regeneration and validation.

## Decisions to record

Use Spec Kit for new capabilities, architecture, security-sensitive behavior,
migrations, and coordinated changes needing a written contract. Keep narrow
fixes, dependency updates, and prose maintenance in the normal PR workflow.

For a new capability, identify the supported task, a nearby excluded task, the
skill that owns it, and any genuine handoffs. Record platform assumptions,
optional-tool behavior, authority boundaries, upstream ownership, and affected
installation targets. Explain why a new skill or shared helper is needed when
an existing one could otherwise own the task.

Put observable acceptance criteria in `spec.md`, source ownership and
constitution checks in `plan.md`, and implementation with its evidence in
`tasks.md`. Resolve material unknowns before dependent implementation. For
parallel work, assign shared manifests and generated outputs to one writer and
validate the combined result.

## Acceptance evidence

| Requirement | Evidence to collect |
| --- | --- |
| Task selection | A realistic invoking task and a nearby task that should stay elsewhere |
| Instructions and handoffs | A source walkthrough or bounded scenario showing scope and authority are preserved |
| Helper behavior | Relevant success and failure cases in the supported runtime |
| Optional tools and platform limits | Observed fallback, explicit skip, or supported boundary |
| Upstream import | Complete reviewed diff, preserved local changes, and audited revision |
| Provenance and installation | Regenerated records, resolving references, and applicable link verification |

Static validation cannot prove an agent follows instructions correctly. Choose
behavioral evidence proportional to the change. Distinguish source inspection,
simulated scenarios, actual tool execution, and live-system checks. Do not mark
a task complete merely because its instructions or tests were written.

## Validation and delivery

```sh
make check-fast
make check-fast test portability
```

Run `make check` in the canonical installed checkout before delivery. Its link
check can fail in an isolated worktree because the links belong to another
checkout. Report that boundary and use the portable gate there. Do not repoint
installed skills to hide the mismatch. Installing or replacing links is a
separate authorized action.

Mark checks completed, skipped, blocked, or manual according to the evidence.
Follow [RELEASING.md](../../RELEASING.md) for push, merge, installation verification,
cleanup, and recovery. Retain completed feature documents as decision history.
Do not backfill specifications for already finished work.

## Preserve managed integration files

Keep `.specify/templates/`, `.specify/scripts/`, and generated Codex skills under
their integration manifests. Regenerate managed files through Spec Kit instead
of editing generated copies to satisfy local style preferences. Put local
planning guidance here or in the constitution and verify that project-owned
memory survives an integration update.
