# Concurrency and recovery

## Reads

Cancel obsolete work when supported and also guard state updates with request identity or the data layer's equivalent. Cancellation can race with resolution. A stale request's `finally` block must not clear the active request's loading state. Keep cancellation distinct from an error the user needs to act on.

`AbortController` can abort the client fetch or response consumption. It does not establish that a server-side mutation was cancelled or rolled back. [AbortController](https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort).

## Writes and autosave

Choose a policy deliberately: serialize writes, coalesce pending drafts, or use server-supported version/precondition checks. A client-side latest-response guard cannot prevent the server from applying writes out of order.

Serialization in one client does not coordinate other tabs, devices, or writers. For shared resources, use the server's supported concurrency control and apply its precondition atomically with the update. Preserve a conflicting local draft rather than silently retrying against the new server version.

Where the server supports ETags and conditional updates, `If-Match` can reject a write against an outdated representation. Handle the precondition failure as a conflict with a recoverable draft, not as permission to overwrite the remote value. Do not add the header without verifying the server contract. [If-Match](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/If-Match).

Record the submitted draft revision and returned server revision. A successful save of revision A while the user edits B confirms A only. Preserve B and save it according to the selected policy. Use a new logical-operation identity when the intended mutation changes; reuse a supported idempotency key only for retries of that same operation and payload.

## Optimistic updates

Associate each optimistic change with its operation and resource. On failure, remove or compensate that operation without restoring an old whole-cache snapshot over later successful work. Reconcile temporary IDs, server normalization, ordering, and query variants. Use the established data library's supported optimistic lifecycle.

Do not optimistically show irreversible completion when the server has not accepted it. Distinguish pending presentation from confirmed results. For an ambiguous timeout, reconcile with an authoritative status/read or the backend's idempotency mechanism before retrying.

## Retry and recovery

Retry only errors and operations that the contract makes retryable, with bounded backoff and cancellation. Authentication, validation, and version conflicts need their own recovery. Preserve enough redacted evidence to diagnose a failure without logging credentials or full sensitive payloads.

Browser reload/unload, offline storage, and a promise resolving are separate persistence boundaries. Define exactly which one the UI's "Saved" message represents.
