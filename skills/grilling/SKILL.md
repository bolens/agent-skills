---
name: grilling
description: Stress-test a plan, design, decision, or idea through focused questions and evidence. Use when the user asks to be grilled, challenged, interviewed, or wants assumptions and trade-offs examined before implementation.
---

# Grill a Decision

Map the decision tree, but ask only questions whose answers materially change the outcome.

- Find discoverable facts from repository files and tools instead of asking the user. Use sub-agents only when available and genuinely beneficial.
- Ask one to three independent questions per round. Give a concise recommended answer and its trade-off for each.
- Do not repeat settled questions or pursue branches made irrelevant by earlier answers.
- Distinguish facts, assumptions, preferences, and irreversible decisions.
- Stop when remaining uncertainty is low-risk or implementation can resolve it cheaply. Summarize decisions, open risks, and the recommended next action.
- Do not mutate repositories or external systems during grilling unless the user separately authorizes implementation.

Use this format when useful:

```text
Q1 — Decision: question
Recommendation: answer — key trade-off
```
