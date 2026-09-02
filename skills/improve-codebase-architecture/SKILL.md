---
name: improve-codebase-architecture
description: Audit a repository or broad subsystem for architectural friction, then rank evidence-backed improvement opportunities. Use for architecture reviews, technical-debt surveys, or requests to decide what structural work matters next. For a known interface or refactor that needs concrete design options, use codebase-design instead.
---

# Improve Codebase Architecture

Produce evidence-backed opportunities, not a generic refactoring wishlist.

Use this skill to discover and prioritize problems across a broad scope. Once the user selects a specific boundary or refactor, hand the design work to `codebase-design`.

## Scope and inspect

1. Read `AGENTS.md`, architecture docs, specifications, ADRs, and domain documentation.
2. Use the scope named by the user. Otherwise identify likely hot spots from recent history, recurring changes, defects, and tests; do not assume churn alone means poor design.
3. Inspect representative callers, implementations, dependencies, and tests. Use `codebase-design` as a vocabulary and reasoning reference while preserving repository terminology.
4. Note friction such as duplicated policy, scattered changes, leaky interfaces, unclear ownership, hard-to-test behavior, and shallow pass-through modules. Apply the deletion test and consider operational constraints.

Sub-agents are optional and may be used only when available, authorized, and useful for a large scope.

## Report

Default to a concise Markdown report in the response. Create a file only when the user requests an artifact. For each candidate include:

- affected paths and evidence
- current failure or maintenance cost
- proposed direction, without prematurely specifying a final interface
- compatibility and migration risks
- expected testability/locality benefit
- confidence: strong, worth exploring, or speculative

Rank candidates by expected benefit, risk, and relevance to likely future changes. Explicitly identify proposals that conflict with an ADR.

If the user requests a visual HTML report, read [HTML-REPORT.md](HTML-REPORT.md), write it under a temporary directory, and provide its path. Do not load CDN assets or open a browser without appropriate network/GUI authorization.

## Explore a candidate

After the user selects a candidate, use `grilling` for consequential unresolved decisions and `codebase-design` for alternative interfaces. Use `domain-modeling` only when the work truly changes domain concepts. Do not edit code, glossaries, or ADRs until the user authorizes implementation or documentation changes.
