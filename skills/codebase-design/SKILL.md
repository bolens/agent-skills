---
name: codebase-design
description: Design or compare a specific module boundary, interface, dependency seam, or refactor. Use when the user wants concrete architecture options for a known design problem. For a broad repository audit that discovers and ranks architectural problems, use improve-codebase-architecture instead.
---

# Codebase Design

Read repository instructions, architecture docs, ADRs, specifications, and representative callers/tests before proposing structure. Established project terminology wins; use the vocabulary below only where it clarifies rather than replacing domain language.

Use this skill when the design target is already known. If the user wants you to search a wider codebase for opportunities, use `improve-codebase-architecture` first.

## Working vocabulary

- **Module**: code with an interface and implementation, at any scale.
- **Interface**: everything callers must know, including invariants and errors.
- **Seam**: a place behavior can vary without editing callers.
- **Adapter**: an implementation selected at a seam.
- **Depth**: useful behavior hidden behind a comparatively small interface.
- **Leverage**: capability gained by callers from that interface.
- **Locality**: related knowledge and change concentrated together.

Treat these as reasoning aids, not rules. A thin adapter can be valuable for isolation; a single adapter can justify a seam when tests, platform separation, security, or ownership require it.

## Analyze

1. Identify the change pressure, callers, dependencies, invariants, and current test surface.
2. Locate duplicated knowledge, leaked policy, pass-through abstractions, and changes that scatter across files.
3. Apply the deletion test: if removing a module merely redistributes its complexity to callers, it may be earning its keep.
4. Respect existing contracts and ADRs. Mark any proposal that would revise them.

## Design

Prefer small interfaces that hide policy and enable behavior-level tests. Dependency injection and pure returns are useful when they reduce coupling, but do not force them over idiomatic repository patterns.

For consequential designs, produce at least two genuinely different options and compare compatibility, migration cost, testability, locality, and operational risk. Read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md) and [DEEPENING.md](DEEPENING.md) when deeper alternatives are needed. Sub-agents are optional.

Do not implement, create ADRs, or update domain documentation during design analysis unless the user authorizes those changes.
