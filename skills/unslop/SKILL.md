---
name: unslop
description: Draft or edit reader-facing prose when writing is the requested deliverable, such as a README, PR description, announcement, or email. Use for rewrites and copy edits that need clearer, more natural wording.
---

# Unslop

Use this editing pass when the user asks for a prose draft, rewrite, or style
review, invokes the skill by name, or an active workflow calls for it on a
specific artifact. Routine answers, progress updates, and prose incidental to
code, diagnosis, or verification use the task's normal writing guidance.

Cut generic phrasing while preserving exact code, identifiers, commands, errors,
quotations, citations, legal language, technical meaning, and required formats.

## Final pass

1. Delete filler, ceremony, repetition, fake transitions, and generic conclusions.
2. Replace vague claims with a fact, mechanism, number, named source, or honest uncertainty.
3. Replace canned phrasing with plain language that fits this specific subject.
4. Vary sentence length naturally. Break any sentence that makes the reader backtrack.
5. Read the result as a skeptical human. Rewrite anything that sounds generated, promotional, bloodless, or over-arranged.

For a rewrite, return the edited text in the requested format. Include critique
or a change summary when the user asks for one.

## Hard bans

Unless exact source text or a required house style forces one, remove:

- chatbot openings and closings such as "Of course", "Certainly", "Great question", "I hope this helps", and "Let me know if"
- praise used as social padding
- puffery and promotional adjectives
- vague attribution such as "experts believe" or "industry reports suggest"
- generic scene-setting, summaries that repeat the answer, and conclusions with no new fact
- "not just X, but Y", false ranges, forced trios, synonym cycling, and rhetorical questions used as transitions
- decorative emoji, title-case headings, excessive headings, excessive boldface, and restatement labels
- em dashes, semicolons, curly quotes, and parentheses used to hide a sentence that should be rewritten
- filler hedges such as "it is important to note", "in order to", "could potentially", "generally", "essentially", and "arguably"
- abstract AI nouns such as landscape, tapestry, testament, interplay, paradigm, substrate, nexus, vector, north star, flywheel, scaffolding, and endgame when a concrete noun exists
- stock AI verbs such as delve, leverage, utilize, facilitate, foster, showcase, underscore, harness, and elevate when a plain verb works
- fancy substitutes for "is", "has", "use", "help", "show", "change", "start", and "finish"

## Sentence rules

- State the answer first.
- Use active voice when the actor matters.
- Give one instruction per sentence.
- Keep conditions next to the action they govern.
- Keep "only", "not", and other limiters next to the word they modify.
- Name the same thing the same way throughout.
- Prefer the project's real symbol, file, command, metric, or behavior over a mood or metaphor.
- Cut adverbs that prop up weak verbs.
- Do not claim ease, speed, safety, quality, or importance without evidence.

## Human voice

Plain does not mean sterile. Use first person when it reflects actual judgment. State a view when the task calls for one. Admit uncertainty precisely. Let a short sentence land. Do not manufacture quirks, banter, slang, or emotion to simulate personality.

Specificity creates voice. "A column rename fails the build" is human because it says something. "Types that follow your schema" is slop because it could describe anything.

## Self-audit

Before sending, ask:

- Could this paragraph appear unchanged in an unrelated answer?
- Does any sentence praise, summarize, or transition without adding information?
- Did I arrange ideas into a suspiciously neat pattern?
- Did I use a banned word because it was precise, or because it arrived automatically?
- Does the prose sound like someone who inspected this exact problem?

If any answer exposes AI residue, rewrite again.
