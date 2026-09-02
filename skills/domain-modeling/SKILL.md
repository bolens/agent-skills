---
name: domain-modeling
description: Clarify a repository's domain concepts, terminology, ownership, invariants, context boundaries, glossary, and architectural decisions. Use when the user asks to model a domain, reconcile terminology, create or update CONTEXT.md, map contexts, or record an ADR.
---

# Domain Modeling

Treat code, specifications, existing glossaries, ADRs, and user statements as evidence with potentially different authority. Surface contradictions instead of silently choosing one.

## Clarify

- Distinguish domain concepts from implementation mechanisms.
- Replace overloaded words with precise terms only after checking established project language.
- Stress-test definitions with concrete edge cases, lifecycle transitions, ownership, and invalid states.
- For multiple contexts, identify what each owns and how information crosses between them.

Do not create terminology merely to satisfy a template. Small infrastructure or configuration repositories may not benefit from a domain glossary.

## Record

When the user asks for documentation changes, follow the repository's existing location and format. Use [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md) or [ADR-FORMAT.md](ADR-FORMAT.md) only when the repository has no established convention.

Before writing, show or clearly describe the intended changes. Do not update `CONTEXT.md`, `CONTEXT-MAP.md`, or ADRs merely because terminology arose during an unrelated task.

Offer an ADR only when the decision is consequential, hard to reverse, non-obvious, and based on a real trade-off. Do not create one without authorization.
