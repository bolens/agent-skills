---
name: design-system
description: Build or improve reusable web design tokens, themes, component variants, and component-state coverage using the repository's CSS/Tailwind, headless UI, shadcn/ui, or Storybook conventions. Use for shared UI consistency and component-system work, not an isolated page restyle or a broad accessibility audit.
---

# Design system

Make shared visual and interaction decisions explicit without turning one page into an unnecessary framework. Inspect existing tokens, components, stories, theme providers, and representative consumers first.

## Find the source of truth

Identify the framework/version, styling system, component primitives, icon family, and token ownership. Preserve existing APIs and local component changes. A Figma library or screenshot can inform design, but repository behavior and implementation constraints still need inspection. Do not claim a design matches an unavailable reference.

Read [framework integration](references/frameworks.md) when Tailwind, shadcn/ui, headless primitives, or Storybook are involved. Use `frontend-design` for visual direction, `svg-design` for icon consistency, and `web-animation` for motion tokens and lifecycle.

## Tokens and component boundaries

- Distinguish raw palette/scale values from semantic roles such as surface, text, border, accent, danger, and focus. Add a token when multiple consumers share a decision, not merely to rename every literal.
- Define light/dark and interaction-state mappings together. Check actual foreground/background pairs and focus visibility. Avoid a global color substitution that erases state or brand meaning.
- Keep typography, spacing, radii, elevation, density, and motion scales coherent with the existing system. Derive fluid behavior from content and layout constraints rather than an arbitrary breakpoint catalog.
- Expose variants that represent real usage. Prefer a small composable API to a growing collection of booleans that permits invalid combinations.
- Preserve ref forwarding, event composition, semantic elements, controlled/uncontrolled behavior, and keyboard/focus contracts when wrapping a primitive. A styled replacement is not behavior-equivalent merely because it looks the same.
- Migrate representative consumers before claiming a shared fix is complete. Keep compatibility aliases only when they support an actual transition, with a clear removal condition.

## State coverage

Select relevant states from enabled, hover, focus-visible, pressed, selected, disabled, loading, empty, error, success, long content, and overflow. For overlays, include open/close, Escape, focus return, scroll locking, and portal stacking. Do not create snapshots for impossible combinations.

Verify narrow/wide containers, text zoom/reflow, themes, reduced motion, and right-to-left layout when supported. Distinguish component container width from the browser viewport. Use logical CSS properties when direction changes are in scope.

Build stories or examples in the existing harness so the next change can reproduce these states. Use semantic queries and user interactions for behavioral tests. A screenshot assertion cannot prove focus trapping or a callback contract.

Use `forms-and-data-state` for submission and async data lifecycles behind shared control states. Keep the component's visual API separate from ownership of server data and drafts.

Use `web-standard` when choosing native dialogs, popovers, forms, or other primitives with browser-owned behavior. Preserve the existing component's contract and verify the supported-browser fallback before replacing it.

## Verify and deliver

Run the repository's component tests, style/type checks, and visual comparisons for affected consumers. Inspect actual captures with `cli-web-evidence` or `responsive-web-capture`. Use `accessibility` for interaction/semantics findings. Automated accessibility results do not establish complete conformance.

Report token/API changes, migrated consumers, demonstrated states, and remaining compatibility gaps. Do not regenerate a component library, install Storybook, or adopt a new styling framework for a small consistency fix unless that change is needed and within scope.
