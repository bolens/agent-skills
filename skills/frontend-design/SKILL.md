---
name: frontend-design
description: Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults.
license: Complete terms in LICENSE.txt
---

# Frontend design

Make the visual direction fit the product, content, audience, and existing identity. A new campaign can justify a distinct visual language. A settings panel inside an established application usually needs continuity and clear behavior.

## Ground the direction

Inspect the supplied references, existing screens, components, tokens, typography, icons, and real content before designing. Honor explicit visual choices. Do not invent a client's history, rejection of earlier proposals, or demand for an aesthetic risk.

When the brief leaves the subject open, choose and state a concrete subject, audience, and primary job. Ask only when missing information would materially change the result. Use existing user preferences as evidence, not permission to override the current brief.

For a new direction, form a compact plan for hierarchy, palette, typography, layout, and any signature element. Keep the amount of planning proportional to the change. A small UI repair does not need a new palette or type system. Use `design-system` when decisions belong in reusable tokens, variants, or component states.

## Compose with real content

Make the primary task and information hierarchy apparent before adding decoration. Choose page structure for the content. A marketing page may need a hero, while an editor or dashboard may need to open directly on the work.

Typography should support hierarchy, density, reading length, and brand character. Reuse existing type roles where they work. A single well-chosen family can be sufficient. Verify fallback metrics, font availability, and long headings rather than choosing fonts only from a large static mockup.

Use spacing, alignment, grouping, and contrast to explain relationships. Numbering should represent an actual sequence or reference system. Avoid decorative statistics, fabricated testimonials, and unnecessary cards or separators. Use representative content lengths and realistic data density.

Create a distinctive detail when it serves the brief, such as a typographic treatment, illustration, composition, or interaction. Do not require novelty in every control or reject a valid design because its palette resembles a common style. For reference-matching work, fidelity takes priority over unsolicited reinvention.

## Design behavior alongside appearance

Include relevant loading, empty, error, success, disabled, selected, and focus states. Ensure primary actions remain discoverable at narrow widths and with long content. Preserve the repository's semantic controls, form behavior, and component APIs while changing appearance.

Use `forms-and-data-state` when submission, autosave, optimistic updates, or request ordering determines those states. Visual feedback must reflect confirmed data and preserve unsaved edits.

Motion should clarify state, spatial relationships, or the visual idea. Use `web-animation` for GSAP, Motion, native transitions, or other runtime work. Use `svg-animation` for moving vector geometry and `animation-assets` for Lottie/dotLottie or Rive. Preserve the requested engine and avoid adding animation merely to make a static design feel more elaborate.

Use `svg-design` for editable icons, sprites, or vector illustration. Reuse an established icon family. Use raster generation only when the required asset should be a bitmap, preserving the user's requested deliverable format.

## Implement and inspect

Build from existing components and styling conventions. Keep selector ownership clear and avoid broad element selectors that unexpectedly override component variants. Use container and content constraints when they better express responsive behavior than device labels.

Inspect a working first version early. Compare it with the brief and real content, then fix specific weaknesses in hierarchy, density, alignment, states, or behavior. Do not delay implementation until a design has been declared unique in the abstract.

Use `cli-web-evidence` to drive the actual page and inspect narrow and desktop captures. Use `responsive-web-capture` for repeatable viewport coverage and `design-system` for shared component-state coverage. Use `accessibility` for focused semantic/keyboard checks and `performance` when runtime evidence indicates a cost. Apply Sites guidance when the project is hosted with Sites.

Use `web-standard` when a native control, navigation pattern, or newer browser feature needs platform/compatibility verification. Use `technical-seo` for requested discoverability work on public pages, not for every visual edit.

Verify reduced motion, focus visibility, overflow, and relevant themes. Review interactive states as well as the initial screen. A successful build is not visual proof, and a static screenshot is not interaction proof. Report what was inspected and any coverage gap.

## Interface writing

Write from the user's task and vocabulary. Name actions precisely and keep the same term throughout a flow. Explain an error with a recoverable next step when one exists. Empty states should explain what belongs there and how to proceed.

Use real claims and supplied facts. Mark temporary sample content honestly. Keep implementation details out of labels unless they help the user make a meaningful decision. Prefer clear, concise prose to slogans, filler, or promotional adjectives.
