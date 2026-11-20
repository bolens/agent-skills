# Evaluate agent workflows

## Contract

Use the skill to compare model or client behavior on frozen prompts and
fixtures. It covers skill selection, task completion, and authority boundaries.
App-specific launch and browser runbooks remain with create-verification-skill.

## Acceptance

- Register a discoverable local skill with instructions for positive,
  adjacent, explicit, and negative cases.
- Compare GPT-6.2 Sol and Astra on [the first-pass prompts](cases.json),
  covering the 13 entrypoints edited in the model audit and two controls.
- Score observed routing and answer requirements separately. State fixture
  permissions, scope, one-sample limits, and any unavailable evidence.
- Run the portable repository checks without requiring authentication or
  model calls.
