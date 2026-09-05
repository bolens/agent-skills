---
name: web-standard
description: Implement and verify standards-based web behavior, browser-native controls and APIs, progressive enhancement, cross-browser compatibility, semantic HTML, navigation, and HTTP correctness. Use for web standards or browser-native implementation requests and platform-behavior defects, not every visual edit, SEO audit, or animation task.
---

# Web standard

Use platform behavior deliberately and verify it in the project's supported browsers. Prefer native capabilities when they meet the task, while preserving a chosen framework or established component contract.

## Establish the platform contract

Inspect target browsers/devices, embedded webviews when relevant, rendering/hosting model, framework/router, existing primitives, compatibility tooling, and the failing behavior. Separate normative semantics, browser support, and actual integration behavior.

Use WHATWG/W3C specifications for disputed semantics, MDN and browser compatibility data for implementation support, and the framework's own documentation for its integration. Check current sources when choosing a newer API. Baseline status is useful context, not proof for every webview, assistive technology, or browser in the product's matrix. [HTML Standard](https://html.spec.whatwg.org/multipage/semantics.html), [Baseline](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility).

Read only the reference needed:

- [Browser-native implementation](references/browser-native.md): forms, dialogs/popovers, events, observers, URL/history, and ownership.
- [Compatibility and HTTP](references/compatibility-and-http.md): progressive enhancement, feature detection, caching, fetch, and response behavior.

Native animation and View Transitions belong to `web-animation`. Data mutation state belongs to `forms-and-data-state`. Use `design-system` when replacing or wrapping a shared primitive changes its public contract.

## Implement the intended semantics

- Use links for navigation, buttons for actions, forms for submission, and appropriate landmarks/content structure. Preserve keyboard behavior, submit semantics, and real destinations.
- Inspect browser-parsed DOM as well as source markup. Invalid nesting can be repaired by the parser and lead to a different layout or hydration mismatch. Correct the source rather than hiding the warning.
- Treat ARIA as semantics, not a replacement for missing behavior. Check naming, focus, and interaction with `accessibility` when those are in scope.
- Feature-detect the actual capability, provide an appropriate fallback, and keep baseline content usable if an enhancement fails. Do not use user-agent sniffing or a blanket polyfill package when a scoped solution works.
- Preserve existing routing, lifecycle, and data ownership. Do not build a second router or remove a framework merely because the platform offers an equivalent primitive.

## Verify and report

Use the repository's validators and browser harness. Verify the specific feature in representative supported engines and the fallback path, using browser tooling that is actually available. Viewport emulation is not testing another browser engine.

Test direct load, enhanced interaction, keyboard behavior, relevant history navigation, and repeated initialization/teardown. Exercise partial initialization or unavailable feature paths when they affect essential content. A full no-JavaScript workflow is required only when the product contract calls for it, not as an automatic rewrite of every application.

Use `cli-web-evidence` for reproducible browser/HTTP proof. Label unavailable engine, device, assistive-technology, or deployment coverage. Use `web-security` for security boundaries and `technical-seo` for crawl/indexing requirements.

Report the behavior fixed, native/framework ownership, sources consulted, tested support/fallback conditions, and remaining compatibility limits. Do not equate a valid document, a Baseline label, or a successful build with complete standards conformance.
