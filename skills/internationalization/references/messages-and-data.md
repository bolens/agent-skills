# Messages and locale data

## Catalog and negotiation contract

Use valid language tags and the product's supported-locale matching policy.
Preserve explicit route/account/user choices and make fallback deterministic.
Avoid redirect loops and keep language switching available without discarding
the current task. BCP 47 tags describe languages, not a currency or time zone.
Consult [RFC 5646](https://www.rfc-editor.org/rfc/rfc5646.html),
[RFC 4647](https://www.rfc-editor.org/rfc/rfc4647.html), and the
[IANA registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry).

Keep complete translatable messages with named placeholders, translator context,
and the catalog's plural/select constructs. Avoid sentence-fragment concatenation
and English-only singular/plural logic. Use the existing message syntax and its
supported version; ICU MessageFormat, MessageFormat 2, and framework formats are
not interchangeable. Check placeholder parity and missing keys with native tools.
See [ICU message formatting](https://unicode-org.github.io/icu/userguide/format_parse/messages/)
and [CLDR plural rules](https://cldr.unicode.org/index/cldr-spec/plural-rules).

Keep trusted component interpolation separate from raw translated HTML and
untrusted user values. Preserve escaping and allowlisted rich-text handling.
Define whether missing translations fail a build, emit diagnostics, or fall back
at runtime. Avoid silently exposing message keys as successful localized output.

## Formatting and storage

Use locale-aware number, currency, unit, date, list, plural, and collation APIs
where supported. Pass the intended locale and options explicitly when output
must be reproducible. Do not derive a payment currency from UI language or assume
all currencies have two decimal places. Formatting does not define arithmetic,
rounding, validation, or parsing of arbitrary localized input.

For JavaScript, check the runtime's supported
[ECMA-402 APIs](https://tc39.es/ecma402/); use
[Unicode locale data](https://www.unicode.org/reports/tr35/) rather than embedding
hand-maintained locale rules. Keep display formatting separate from serialized
API values and calculation types.

Distinguish an instant, a date-only value, and a wall-clock appointment in a named
zone. Do not route a date-only birthday through UTC conversion. A recurring local
meeting needs zone and recurrence intent, not just a fixed UTC offset. Verify
daylight-saving gaps/overlaps according to the product's policy. Use
[IANA time-zone data](https://www.iana.org/time-zones) and the runtime's maintained
time facilities; record relevant data-version differences before changing tests.

## Rendering and state

Make server and client agree on locale, time zone, messages, and initial values
to avoid hydration differences or flashes of the wrong language. Scope localized
query/cache entries by every representation input that varies. For HTTP caching,
verify the route or negotiated response's cache policy and relevant `Vary` headers
without turning every response into an uncacheable resource.

Switching locale must not let an older request restore previous-language content
or discard an unsaved draft. Preserve the user's underlying value when changing
its display format. Use the existing router and data layer; read
[forms and data state](../../forms-and-data-state/SKILL.md) when requests overlap.
