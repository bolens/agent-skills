# Layout, input, and verification

## Direction and text

Set the actual document language and base direction independently. Use logical
CSS properties for direction-sensitive spacing and alignment. Preserve logical
DOM and focus order; reversing everything visually is not RTL support. Mirror
directional navigation where its meaning requires it, not logos, media controls,
or all icons indiscriminately. Consult
[W3C direction guidance](https://www.w3.org/International/questions/qa-html-dir).

Isolate inserted opposite-direction or unknown-direction text with suitable
markup such as `bdi` or `dir="auto"`. Test punctuation, numbers, identifiers, and
mixed-script user content in their real context. Do not strip direction controls
or normalize all stored text as a blanket repair. Identifier security and display
text have different contracts. See
[inline bidi markup](https://www.w3.org/International/articles/inline-bidi-markup/)
and [Unicode security considerations](https://www.unicode.org/reports/tr36/).

Allow translated text to wrap and expand without clipping controls. Verify glyph
coverage, shaping, line breaking, and fallback fonts for supported scripts before
subsetting. For truncation, cursor behavior, or character limits, distinguish bytes,
code units, code points, and grapheme clusters. Use runtime segmentation where
available and define the server's matching limit. Consult
[Unicode text segmentation](https://www.unicode.org/reports/tr29/).

## International input

Preserve Unicode across input, transport, and storage, using UTF-8 where that is
the protocol/storage encoding. Declare encodings consistently and test round trips
instead of treating escaped source text as proof.

Preserve IME composition while validating, submitting, and handling Enter. Test
paste, autofill, combining marks, and non-Latin input. Avoid ASCII-only names,
mandatory Western first/last-name splits, or one country's address/phone rules
unless the domain explicitly requires them. Ask only for fields the task needs.
Use locale-specific display with an explicit parsing and validation contract.
See [W3C personal names](https://www.w3.org/International/questions/qa-personal-names)
and [internationalization quick tips](https://www.w3.org/International/quicktips/).

## Bounded verification

Choose cases from supported behavior, rather than every locale times every viewport:

- Source locale, a supported contrasting locale, and missing/unsupported-locale fallback.
- Relevant plural categories, zero/fractional values, currency precision, and date boundaries.
- RTL with mixed user content, long translations, and supported-script font coverage.
- Locale switching during editing/loading, direct localized loads, and server/client agreement.
- Translated accessible names, validation errors, keyboard/IME input, and status feedback.

Pin locale, time zone, clock/test data, and relevant runtime/ICU versions in tests.
Avoid tests accidentally depending on the developer's machine defaults or assuming
punctuation and spacing stay identical across locale-data upgrades. Keep exact
strings where they are the contract; otherwise assert meaningful structured parts.
Pseudolocalization helps expose unextracted strings and space assumptions but
cannot validate translation meaning or every script's layout.

Use the existing browser harness with
[shared capacity ownership](../../ci-maintenance/references/setup-contracts.md#browser-workload-ownership).
Record executed locale/zone cases, assertions, inspected visuals, and human-review
gaps. Do not claim multilingual conformance from a single English screenshot.
