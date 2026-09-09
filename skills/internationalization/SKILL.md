---
name: internationalization
description: Implement and verify locale-dependent application behavior, message catalogs, regional formatting, Unicode input, and right-to-left interfaces. Use for i18n/l10n implementation or defects, not translation-only copy requests or localized SEO alone.
---

# Internationalization

Preserve meaning and task completion across the product's supported locales.
Reuse the existing framework, catalog format, runtime locale APIs, and translator
workflow. A request to repair formatting does not authorize adding languages,
replacing the translation system, or sending private copy to a translation service.

## Establish the locale contract

Identify supported language/script/region tags, source language, fallback chain,
locale selection and persistence, rendering boundary, and translated surfaces.
Language, country, currency, and time zone are separate choices. Preserve an
explicit user selection instead of repeatedly overriding it with browser or IP
inference. Inspect server and client locale data and library versions together.

Read only the relevant reference:

- [Messages and locale data](references/messages-and-data.md): catalogs, plurals,
  formatting, dates, negotiation, and cache identity.
- [Layout, input, and verification](references/layout-and-testing.md): RTL,
  bidirectional content, Unicode, international forms, and deterministic evidence.

Use [standards sources](../web-standard/references/standards-sources.md) when
choosing normative references or resolving conflicting advice. Prefer native
locale facilities supported by the actual runtime; browser `Intl` availability
does not establish support in another client or server.

## Implement and verify

Trace one affected journey from input through storage, server output, translated
messages, and rendered or spoken feedback. Preserve machine identifiers and
canonical transport values while localizing presentation. Translate accessible
names, errors, and status messages alongside visible copy. Keep untrusted values
escaped even when they pass through a translation formatter.

Use `forms-and-data-state` for draft and request ownership, `design-system` for
shared direction/layout behavior, and `accessibility` for language semantics and
interaction. `technical-seo` owns localized URL annotations and indexing.
Use these handoffs only where the affected behavior needs them.

Verify the supported locale cases with the existing test harness before expanding
the matrix. Record locale, time zone, runtime/locale-data version, fallback, and
tested behavior. Use `cli-web-evidence` for actual browser proof within shared
browser capacity limits. Static catalog checks and pseudolocalization do not prove
translation quality; report missing native-speaker or assistive-technology review.
