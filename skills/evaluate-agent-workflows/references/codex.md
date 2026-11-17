# Codex evaluation

Read this when running model-driven skill tests in the Codex CLI.

## Prepare equivalent runs

- Put the intended catalog and supporting files in the disposable Git fixture's
  `.agents/skills` or in the dedicated user's skill home. Choose the location
  that matches the discovery behavior under test. Keep prompts, labels, and
  expected outputs out of the fixture. Include the full catalog when testing
  selection under competition.
- Use a dedicated profile or client home with the intended discovery settings.
  Disable unrelated plugins, tools, and user configuration unless one is part of
  the test. Keep authentication available to the client and outside the
  model-facing filesystem and tool environment. Do not print or capture secrets.
- Give the model a permission profile with access to the fixture and required
  binaries only. Use read-only access for plan and review scenarios. Grant
  fixture-only writes for tests that need them. Disable network and hosted tools
  that could act on live services, unless the user explicitly requests a live
  test. Confirm a fixture command succeeds under the same settings before
  interpreting any failed skill reads.
- Keep the model ID and reasoning effort explicit. Run with fresh sessions and
  separate output files. Use the same prompt and fixture across variants. Verify
  the installed CLI syntax and model access with a small preflight.

With the dedicated profile already configured, run:

```bash
codex exec --ephemeral --strict-config -C "$fixture" \
  -m "$model" -c 'model_reasoning_effort="low"' --json "$prompt" \
  </dev/null >"$trace" 2>"$diagnostics"
```

Apply the per-case deadline in the runner. Record exit status and use the
trace's completion event to distinguish a completed turn from an incomplete
stream. Keep diagnostics separate from JSONL. A requested model ID plus a
successful turn verifies that the CLI accepted the selection. Report whether
the harness independently emits the serving model identity.

## Score from events

Use `python3 scripts/summarize-codex-trace.py TRACE.jsonl` from the skill
directory for a conservative list of observed shell reads and their event IDs.
The helper stops on malformed JSON and does not emit command output. Inspect
ambiguous traces directly, including clients that inject a named skill without
a shell read.

Find completed command events that directly read the intended `SKILL.md`, or
skill-activation events if the client exposes them. Check the command and
result to distinguish reading an entrypoint from searching for its name or
trying to read it unsuccessfully. A missing event can be unobservable when a
client loads instructions internally.

Score the requested outcome from final text or fixture assertions, as appropriate.
When a workflow requires an action, use tool receipts and resulting state. Check
for unexpected skill loads and attempted writes or remote mutations separately.
Retain a short explanation for each miss or uncertain grade. Keep traces in
private task storage and publish only the evidence needed to explain results.

[OpenAI's guide to skill evaluations](https://developers.openai.com/blog/eval-skills)
describes explicit prompts, natural-language prompts, negative controls, and
deterministic assertion patterns for Codex events.
