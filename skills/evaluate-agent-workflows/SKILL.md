---
name: evaluate-agent-workflows
description: Evaluate skill routing and agent task behavior across models, clients, or instruction revisions. Use for skill regression tests or model comparisons on agent workflows.
---

# Evaluate agent workflows

Use a fixed set of realistic prompts and observable outcomes to test an agent's
selection, actions, and follow-through. Start with failures or decisions that
matter to the user. For app-specific launch and interaction runbooks, use
[create-verification-skill](../create-verification-skill/SKILL.md).

1. Pick a small set of tasks. Pair intended routes with nearby requests that
   belong elsewhere, and include an explicit invocation if the client supports
   it. For each case define the expected outcome, allowed side effects, and
   evidence needed to prove the behavior. Keep the rubric outside agent reach.
2. Freeze the input and vary one dimension at a time. Record the skill revision
   and discoverable catalog, client version, exact model, reasoning effort,
   permissions, and tool availability. Use fresh sessions and equivalent
   disposable fixtures. Keep live repositories, personal data, and write
   credentials outside the fixture. Keep ordinary local validation independent
   of paid model calls.
3. Run the requested matrix within a stated budget and per-case deadline. For
   Codex traces and permission setup, use [the Codex procedure](references/codex.md).
   If the requested model or client is unavailable, record that cell as blocked.
4. Score routing separately from task completion. Use a successful skill read
   or client activation event for routing, and tool receipts or artifact checks
   for actions. A model's claim that it loaded a skill or ran a command is
   insufficient. Mark missing evidence as unobserved. Score plans as plans.
5. Report counts and per-case misses, distinguishing runner failures from agent
   behavior. Flag out-of-scope actions even when the deliverable is correct.
   Label single-sample results as exploratory. When a failure prompts an
   instruction change, rerun the original case and its nearest control on the
   same client and model settings.

Keep a reviewable summary with prompt IDs and evidence pointers. Screen traces
for private data before sharing or committing any part of them.
