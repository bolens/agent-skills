# Feature specification: bounded agent context

**Created**: 2026-09-05
**Status**: Implemented and locally validated
**Input**: Implement useful ideas from the two undefinedKi posts across the fleet.

## User scenarios and testing

### US1: Read a useful source excerpt, P1

An agent locates a symbol before loading source. A local reader returns numbered
UTF-8 lines for a small file or an explicit range. A whole-file request exceeding
350 lines, or any response exceeding 24 KiB, fails without printing source.
Tests cover both boundaries, targeted reads, long lines, invalid inputs, and
unavailable files. Direct source remains necessary for editing and review.

### US2: Preserve context between tasks, P1

Repository guidance points to existing project memory for durable corrections.
A correction records its scope, reason, and evidence, replacing stale guidance
instead of creating another competing rule file. One-off task status stays in
task notes. Existing repository requirements and session authority remain intact.

### US3: Bound a permitted worker task, P2

The shared fleet skill describes focused reader and mechanical writer handoffs.
Workers receive a question, allowed paths, output contract, and verification.
Only concise findings and evidence return. The coordinator reads actual changed
source and retains debugging, architecture, security, and final review judgment.
When delegation is unavailable or unauthorized, bounded local reads still work.

## Requirements

- A Python 3.10+ standard-library helper performs local reads only, with no model
  credentials, network, file writes, or installation required.
- Whole-file overflow and invalid requests produce no partial source on stdout.
- Explicit ranges preserve one-based source line numbers and report the next
  unread line when more content exists. Huge lines cannot consume unbounded RAM.
- Guidance explains that this helper bounds its own output, not other tools.
- Fleet consumers retain their repository policies and generated Spec Kit files.
- No Portal integration, provider/model pin, automatic scheduling, live-service
  changes, or publication is part of this implementation.

## Success criteria

Helper behavior tests and the skill repository's portable gate pass. Every
available maintained consumer receives the same narrow guidance with resolving
local memory links. Scope and skipped consumers are recorded in task evidence.

## Sources and limits

- [Referenced image](https://x.com/undefinedKi/status/2095942506433089832/photo/1)
- [Referenced article](https://x.com/undefinedKi/status/2095876609689498067)
- [Spotify's original account](https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90)

The 350-line starting point comes from the Spotify example. Its reported savings
are not a benchmark of this helper or this fleet. The local byte ceiling also
bounds minified or otherwise unusually long source lines.
