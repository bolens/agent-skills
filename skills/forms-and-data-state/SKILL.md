---
name: forms-and-data-state
description: Implement and debug web form submission, validation, async reads and mutations, autosave, optimistic updates, conflict recovery, and unsaved-work handling. Use when correctness depends on request ordering or draft/server state, not for a form's visual styling alone.
---

# Forms and data state

Keep the user's draft, the submitted snapshot, and the server-confirmed result distinct. A response arriving last is not necessarily the newest intent, and a stopped spinner does not prove a save succeeded.

## Inspect the contract

Read repository guidance, the existing form/data library and version, component state, server handlers, schemas, and relevant tests. Preserve the established framework, query cache, and mutation conventions. Do not install a form or state library to fix one submission bug.

Identify the resource/user scope, field representation, validation boundary, request identity, server success/error shape, concurrency policy, and persistence behavior. Trace what survives navigation, refresh, account changes, and unmounting. Treat server-side authorization and validation as authoritative even when the client mirrors them for feedback.

## Model the interaction

- Separate editing, validating, submitting, acknowledged, failed, and conflicted states where the workflow needs them. Keep field errors separate from network failures and access/session failures.
- Submit a stable snapshot. An acknowledgement for an older snapshot must not overwrite newer typing or mark it saved. Clear dirty state only for the revision actually acknowledged.
- Map server field errors to the matching submitted fields. Preserve editable values after failure. Show form-level errors when they cannot be associated with a field.
- Keep labels, instructions, error associations, focus, and success feedback coherent. Do not move focus or announce every keystroke unnecessarily. Use `accessibility` for those semantics and `design-system` for shared control states. [WAI form notifications](https://www.w3.org/WAI/tutorials/forms/notifications/).
- Preserve native submission behavior such as Enter, the intended submit button, and browser autofill. Inspect disabled controls and serialized values rather than assuming the visual form equals the request payload.

## Control requests and mutations

Read [concurrency and recovery](references/concurrency.md) for overlapping reads, writes, optimistic state, or autosave. Choose ordering and retry behavior from the actual server contract.

Use the repository's query/cache API for cancellation, invalidation, and mutation state when available. Scope keys to all inputs that change the result, including account/tenant and filters. Keep an older request from replacing newer data or clearing a newer loading/error state. Clear or isolate sensitive cache state when identity changes.

Prevent accidental duplicate interaction locally, but do not treat disabling a button as server-side deduplication. Confirm whether a failed or timed-out mutation may already have succeeded before retrying an irreversible action. Do not invent backend idempotency support by adding an arbitrary header.

For autosave, debounce according to the interaction, then serialize or version writes so the server cannot apply stale content last. Preserve newer edits while earlier work is in flight. Do not report an offline local draft as saved to the server.

Preserve unsaved work according to the product's policy. Use scoped navigation guards where needed, not unconditional prompts on every exit. Do not rely on unload-time network work as the only persistence mechanism. Never persist passwords, tokens, or sensitive drafts in browser storage merely to simplify recovery.

## Verify the failure paths

Use controllable promises or the existing network-mocking layer for deterministic tests. Exercise the relevant cases:

- success, field rejection, server failure, session expiry, and empty results
- responses completing out of order, account/resource switches, and unmount during a request
- duplicate submit and ambiguous network failure after a write
- editing during save, overlapping optimistic mutations, and server conflict
- navigation away/back, autofill, keyboard submission, and restoration of permitted drafts

Assert payloads, resulting server/cache state, preserved drafts, and user-visible feedback. A spinner or toast assertion alone is insufficient. Use `tdd` for requested test-first work and `cli-web-evidence` for the real browser flow. Distinguish local mocks from verified backend behavior.

Report the state/concurrency policy, request contract inspected, scenarios tested, and unresolved server or persistence assumptions. Use `web-security` when the defect crosses an authentication, authorization, or untrusted-input boundary.
