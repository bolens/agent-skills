# Choosing standards sources

Read this when selecting a protocol, schema, platform behavior, or conformance
claim. Choose the body that owns the affected contract; do not apply every row
to every project. This map is guidance for evidence selection, not a new source
of authority over the user's task or repository requirements.

| Contract | Primary source and when it applies |
| --- | --- |
| HTML, DOM, URL, Fetch | [WHATWG standards](https://spec.whatwg.org/): browser parsing and platform algorithms |
| CSS, accessibility, web internationalization | [W3C specifications](https://www.w3.org/TR/), [WAI](https://www.w3.org/WAI/), and [Internationalization](https://www.w3.org/International/): distinguish Recommendations, drafts, and non-normative tutorials |
| JavaScript and locale APIs | [Ecma TC39](https://tc39.es/): ECMA-262/402 and proposal status, checked against runtime support |
| Text and locale data | [Unicode standards](https://www.unicode.org/standard/standard.html) and [CLDR](https://cldr.unicode.org/): encoding, segmentation, bidi, normalization, and regional data |
| HTTP, TLS, OAuth, language tags | [IETF RFCs](https://www.ietf.org/process/rfcs/): inspect status, updates, obsoletions, and errata |
| Registered identifiers and time zones | [IANA registries](https://www.iana.org/protocols) and [tz database](https://www.iana.org/time-zones): authoritative assigned values and zone data, not implementation recipes |
| API descriptions and JSON validation | [OpenAPI Initiative](https://spec.openapis.org/oas/latest.html) and [JSON Schema](https://json-schema.org/specification): match the chosen version/dialect and actual validator/code-generator support |
| Federated identity | [OpenID Foundation](https://openid.net/specs/openid-connect-core-1_0.html): OIDC when that protocol is used; it is not interchangeable with OAuth authorization |
| Portable shell and OS interfaces | [The Open Group/IEEE POSIX](https://www.opengroup.org/austin/): declared shell/API portability, verified on the target operating systems |
| Security and privacy assessment | [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) and [NIST Privacy Framework](https://www.nist.gov/privacy-framework): select applicable controls and evidence; these do not establish legal compliance |
| Contractual or industry standards | [ISO](https://www.iso.org/standards.html) and [IEC](https://webstore.iec.ch/): use the named edition and actual clauses when the product contract requires them |

For other domains, use their actual specification owner, such as OASIS for an
adopted OASIS protocol, or OCI for an implemented container specification. Extend
this map only when an existing task needs that contract.

## Resolve authority and version

Record the document/edition or living-spec retrieval date, section, maturity,
applicable requirement, and implementation evidence. An RFC number does not mean
Internet Standard; a TC39 proposal or W3C draft does not mean deployed support.
Use the [IETF process guide](https://www.ietf.org/process/process/) for status.
Do not treat a mutable `latest` page as a pinned compatibility contract.

Separate normative requirements from informative examples, MDN explanations,
vendor docs, framework conventions, and scanner recommendations. Runtime docs
explain implemented behavior; they do not redefine a protocol. When behavior
differs, preserve the product's supported clients, document the difference, and
choose a tested adaptation rather than silently claiming conformance.

Use the smallest relevant primary section instead of copying a manual or a table
of locale rules into a skill. Keep decision criteria and task-specific evidence
locally. If a standard is inaccessible, say which clause could not be checked;
do not invent its requirements from a summary or claim certification. A standard
is not automatically a legal obligation. Resolve actual jurisdictional or
contractual obligations separately when that is part of the task.

Report conformance only for the named scope, version, and executed checks.
Schema validity does not prove API semantics, accessibility tooling does not
prove WCAG conformance, and a security checklist does not certify an application.
