# Wide-event logging guidance

Reviewed Boris Tane's [Observability wide events 101](https://boristane.com/blog/observability-wide-events-101/)
on 2026-09-05, including its sample event, implementation, and tracing discussion.
The useful idea is a correlated, context-rich event per operation/service hop,
with business state alongside timing and outcome. That can make a nominally
successful but incorrect operation easier to investigate.

The example directly assigns request headers, `process.env`, user and application
objects, dependency results, and an exception message. A comment about excluding
secrets does not enforce that exclusion. Its synchronous logger call in `finally`
also needs failure isolation in a production implementation. These are limits
of illustrative code, not a finding about a deployed service. No article code
was copied or executed.

Consulted the [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
for sensitive-data exclusion, interaction identifiers, log-injection defenses,
logging-failure testing, access control, and retention. Its guidance supports
checking actual outputs and failure behavior rather than relying solely on a
redaction promise or secret scanner.

## Local implementation

Extended `systematic-debugging` with a conditional reference for wide events and
error handling. The adaptation uses explicit fields and operation-local state,
preserves errors and cancellation, distinguishes attempts from terminal results,
and ties events to the executing build. It keeps useful successful examples so
debugging is not limited to operations already classified as failures.

Sensitive-data controls apply before values enter event buffers or exporters.
Raw object dumps, arbitrary exception serialization, predictable identifier
hashes, and collector-only redaction are insufficient. The reference calls for
synthetic leak fixtures across enabled outputs, including tracing and fallback
logging, alongside tests that preserve the application's original behavior.

The workflow keeps existing logger/tracing contracts and does not introduce a
vendor, backend, schema migration, or live collection. This is documentation
within the existing debugging remit. No application instrumentation or redaction
implementation was changed, so no runtime privacy guarantee or speedup is claimed.
Original provenance and installed targets remain unchanged.

## Validation

Manual walkthroughs checked concurrent request isolation, a retry followed by
success, an HTTP success with a wrong business result, a secret in a nested
exception, a failing exporter, and cancellation before normal handler return.
The instructions require usable diagnostic evidence without changing the
original outcome, and treat unavailable telemetry as a gap rather than success.
These are instruction reviews, not executed leak tests or model evaluations.

`make check-fast` and `make check` passed, including all 30 tests, provenance,
portability with ShellCheck, and installed links. Skill Creator's quick validator
also passed. Application-level leak and lifecycle tests remain requirements for
future instrumentation changes, not evidence produced by this documentation edit.
