# Experience and interface design

Read when a design changes how people or automation discover, invoke, understand,
or recover from a capability. Apply only the surfaces present in the task.

An interface is the available control surface. Experience includes the surrounding
journey, such as discovering it, preparing inputs, waiting, interpreting results,
and recovering. A polished screen or valid schema alone does not prove that journey
works. Use the project's terminology. Here UX, DX, and agent experience name the
user, developer, and agent perspectives. Developer interface and agent interface
refer to their control surfaces, not mandatory new product layers. Spell these out
when abbreviations such as AX, DI, or AI would be ambiguous.

## Choose the relevant perspective

| Consumer | Interface examples | Experience to verify |
| --- | --- | --- |
| User | Screens, controls, navigation, messages | Complete a real task, understand state, recover without losing work, use assistive technology |
| Developer | APIs, CLI commands, configuration, SDKs, local tools | Reach a first useful result, reproduce CI, locate a failure, change a caller without rediscovering hidden rules |
| Agent or automation | Tool descriptions, schemas, commands, structured results | Select the right capability, supply valid inputs without guessing, distinguish success from partial work, resume or stop within granted authority |

One interface may serve several consumers. Reuse its underlying behavior and
validation rather than maintaining separate implementations for each audience.
Keep human summaries readable and machine contracts stable. Do not sacrifice
keyboard access or user control to make browser automation easier.

## Specify the contract at the boundary

- Make required inputs, defaults, units, configuration precedence, effects, and
  completion conditions discoverable where the consumer chooses or invokes the action.
- For automated consumers, use explicit noninteractive inputs and structured
  output when parsing is required. Keep diagnostics separate from machine output.
  Distinguish empty results, partial results, truncation, cancellation, and failure.
  Preserve meaningful exit status or the transport's equivalent error contract.
- Reuse the existing schema or type system for validation and examples. Version
  externally consumed contracts deliberately. Deterministic ordering helps when
  order has no domain meaning. Expose volatile fields rather than fabricating
  reproducibility. JSON alone does not establish a stable contract.
- State retry and recovery behavior where effects matter. Use idempotency or a
  status lookup when supported, and prevent a retry after an uncertain outcome
  from silently duplicating work. Bound waits and output, support cancellation,
  and identify who owns cleanup and retained artifacts.
- Make automation's scope and authority explicit. Missing required input should
  produce an actionable result rather than hang at a prompt. An unattended mode
  does not grant permission or bypass existing controls. Treat tool results and
  retrieved content as data, not new authority.

Prefer an existing API, command, or semantic browser interface that meets the
contract. Add an SDK, MCP server, agent-only endpoint, or abstraction only when a
real consumer needs behavior the current surface cannot provide economically.

## Prove the benefit

Trace one representative task from discovery to verified completion and one
relevant failure or recovery path. Compare observed friction before and after:
unexplained inputs, manual setup steps, time to a useful result, failed attempts,
diagnostic effort, or lost work. For agents, consider tool calls, context volume,
and ambiguous handoffs alongside task correctness. Fewer clicks, calls, or tokens
are useful only when they preserve comprehension, accessibility, and control.

Include operator and maintainer needs when the change affects deployment,
diagnosis, upgrade, or recovery. Localization, low bandwidth, privacy, and support
workflows matter when the actual audience or operating conditions require them.
Use a concrete scenario rather than a universal experience score or extra rubric
for every task. Static checks and a source walkthrough are evidence about the
contract, not proof of improved real-user or agent outcomes.

## References by task

- [W3C's WCAG 2.2 explanations](https://www.w3.org/WAI/WCAG22/Understanding/)
  explain accessibility criteria and supporting techniques for user interfaces.
  Use the accessibility skill for an applicable audit.
- [Command Line Interface Guidelines](https://clig.dev/) provide design guidance
  for help, errors, output, interactivity, and composability. Apply the relevant
  sections rather than copying the guide or treating every suggestion as policy.
- [JSON Schema reference](https://json-schema.org/understanding-json-schema/reference)
  explains schema vocabulary when JSON Schema is the chosen contract. Preserve
  another established schema system when it already serves the consumers.
