---
name: technical-writing
description: Write or review developer documentation, RFCs, READMEs, PR descriptions, and commit messages using plain language, deliberate document structure, and repository-verified facts. Use when the user explicitly invokes technical-writing or requests its named writing standard.
---

# Technical writing

Write for a tired engineer who needs the point on the first read. The codebase supplies the vocabulary and facts. Use real symbols, paths, flags, outputs, and limits.

Apply `unslop` as the final prose pass.

## Route the work

- For tutorials, how-to guides, reference material, or explanations, read [references/document-structure.md](references/document-structure.md).
- For sentence-level drafting and editing, read [references/sentence-style.md](references/sentence-style.md).
- Before claiming the document is correct, read [references/repository-verification.md](references/repository-verification.md).

Use the relevant references only. A PR description or commit message usually needs sentence style and repository verification, not a full document-mode analysis.

## Core rules

- Cut every word that does no work.
- Prefer the short, everyday word unless a technical term is more precise.
- Give one instruction per sentence and put its condition first.
- Call each thing by one name throughout.
- Preserve the repository's established terminology and documentation conventions.
- Do not force a document into a template when a mixed form helps the reader complete the task.

Create or edit only the artifact the user requested. Do not rewrite untouched prose for stylistic consistency unless asked.
