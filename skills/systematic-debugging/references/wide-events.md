# Wide events and safe error handling

Use when adding or improving request, job, command, or service-hop diagnostics.
Work within the application's existing logger, tracing system, and error
contract. A short local failure may need only its error and exit status.

## Build an event that answers a debugging question

Accumulate explicitly selected fields in an operation-local context and emit
one completion event at the owning boundary. Reuse an existing span when it
already captures that boundary. Avoid duplicate catch-and-log messages at every
layer and shared mutable contexts that mix concurrent requests.

Include operation/route template, service, environment label, build revision,
start time, duration with units, outcome, and an opaque correlation ID. Add the
decision flags, dependency name/status, attempt count, and timings that explain
this operation. Distinguish transport success from the intended business result.
Keep field names, types, outcome values, and error codes stable enough to query.

Use existing trace propagation across services. Give retries their own attempt
identity under the same operation, and distinguish a failed attempt from terminal
failure. Validate externally supplied identifiers and do not derive correlation
IDs from credentials or personal data. Do not put request IDs into metric labels
or propagate sensitive attributes through tracing baggage.

## Handle the failure without changing its meaning

Classify expected rejection, dependency failure, timeout, cancellation, and
unexpected defect under the application's existing contract. Capture a stable
error code/type, failing stage, retryability where known, and a sanitized cause.
Preserve the original exception or exit status when propagating the failure.
Logging must not turn failure into success, invent retryability, or retry a
non-idempotent operation merely because an error was transient.

Return the appropriate public error and an opaque support ID when useful.
Keep internal stack traces, provider responses, and diagnostic details out of
public responses. Exception messages and nested causes are untrusted data too;
map them to safe fields instead of serializing arbitrary error objects.

Finalize through the framework's real completion/error hooks, including early
returns and cancellation. Streaming responses finish later than handler return.
A `finally` block cannot guarantee delivery after process termination. Isolate
serialization/export failures so they do not mask the original outcome or block
requests indefinitely. Report dropped telemetry through a bounded safe counter
or fallback. Preserve any separate mandatory audit-log contract.

## Exclude sensitive data before collection

Define an allowlist of fields and safe value sources at instrumentation sites.
Do not attach whole requests, headers, cookies, environment maps, user objects,
database rows, query parameters, SQL bind values, cache contents, or payloads.
Prefer a route template over a raw URL, an operation name over query text, and
a safe decision flag over the input that produced it.

Remove or transform sensitive values before event construction, buffers, spans,
console output, and exporters. Collector-side redaction is only a second layer.
Check nested causes, stack messages, auto-instrumentation, and fallback loggers
for bypasses. Truncation does not redact a secret. Hashing a predictable email
or identifier does not anonymize it; use a scoped pseudonym only when needed
and permitted, with access and retention appropriate to its linkability.

Use structured serialization with bounded field lengths, collection sizes,
nesting, and total event size. Prevent untrusted values from injecting extra log
records or overriding trusted fields. Limit retention and reader/export access.
Review the exact diagnostic bundle before sharing through `sensitive-info-audit`.

## Keep enough evidence and verify it

Keep a useful successful baseline as well as errors, since incorrect business
outcomes may return success. Apply sampling only after the relevant outcome is
known when supported. Preserve error/slow-path evidence within explicit volume
bounds, record the sampling policy, and do not infer total failure rates from a
biased sample. Wide events complement metrics and required audit records.

When implementing logging, test success, rejection, exception, timeout,
cancellation, concurrent operations, retries, and exporter failure as relevant.
Inject synthetic secret and personal-data sentinels into headers, payloads,
URLs, nested errors, and metadata. Assert they are absent from every enabled
output, including console/fallback and trace exports, while useful correlation,
failure classification, and original application behavior remain intact.
Verify that a query can locate the failing operation and a comparable success.
Never use real credentials as leak-test fixtures or claim zero exposure from a
generic secret scanner alone.
