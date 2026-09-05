---
name: svg-design
description: Create, refine, and integrate code-native SVG icons, symbols, sprites, logos, and illustrations with consistent geometry, accessible semantics, theming, and safe optimization. Use for static SVG drawing, icon families, SVG cleanup, or vector integration. Use svg-animation for motion and archify for technical architecture diagrams.
---

# SVG design

Build editable vector geometry that reads at the actual display size. Inspect the existing drawing or icon family before changing its style.

## Establish the visual contract

Identify intended sizes, viewBox, stroke/fill language, optical weight, corner treatment, palette, themes, and whether the asset is decorative or informative. Reuse an established icon package, sprite, or local components when adding an icon to an existing interface. Do not introduce a second visual language for one missing symbol.

For a new family, draw representative simple, dense, and asymmetric members first. Compare them at final size. Match perceived weight and alignment rather than imposing identical bounding boxes or blindly snapping all coordinates to integers. Keep the user's reference recognizable and explain only choices that affect the requested result.

## Construct and integrate

- Use explicit viewBox bounds and deliberate aspect-ratio behavior. Reserve layout space in the host. Include stroke, shadows, and intended overflow in clipping decisions. [viewBox](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/viewBox).
- Prefer basic shapes and readable groups while authoring. Convert to paths only when the toolchain or geometry needs it. Keep editable originals separate from optimized output when the project already has an export pipeline.
- For reusable monochrome icons, use `currentColor` where the host should own color. Preserve deliberately multicolor marks. Do not replace meaningful color distinctions with a blanket fill rule.
- Scope IDs for gradients, masks, clips, filters, symbols, and accessible titles. Include per-instance uniqueness when the same inline component can appear twice, with stable server/client IDs in SSR. File-level prefixes alone do not solve repeated instances of the same file.
- Rewrite all ID references together, including `url(#...)`, `href`, CSS selectors, and ARIA references. Use explicit coordinate units for masks/gradients/clips when the bounding-box default is not intended.
- Preserve the icon's hit target in its semantic button/link wrapper. Do not put a tiny clickable path in place of an accessible control.

## Semantics and optimization

Hide decorative inline SVG from assistive technology. For meaningful graphics, provide the required accessible name and surrounding explanation. An image embedded with `<img>` needs appropriate host `alt` text. Do not depend on text converted to outlines for searchable or accessible content. Use `accessibility` when semantics or interactive behavior are in scope.

Use the repository's optimizer configuration. Review before/after renders and IDs rather than running a maximum-compression preset blindly. Preserve viewBox, intentional precision, animation targets, and accessible labels. SVGO's `prefixIds` helps prevent file-level collisions, but reusable components still need instance-aware handling. [SVGO prefixIds](https://svgo.dev/docs/plugins/prefixIds/).

Do not paste untrusted SVG markup into an application without inspecting active content and external references. Use the repository's asset sanitization/import path when one exists.

## Verify and hand off

Render at smallest and largest intended sizes, light/dark backgrounds, and twice on the same page. Inspect clipping, strokes, alignment, color inheritance, ID references, and accessibility naming. Check responsive embedding and SSR/hydration when applicable. XML parsing or a screenshot of one large instance is insufficient visual proof.

Use `cli-web-evidence` for browser evidence and `svg-animation` if the vector will move. Prefer `archify` for technical diagrams and `imagegen` only when the requested deliverable should be a raster asset rather than editable vector code.

Report the edited asset/component, size/theme coverage, optimization performed, and evidence paths. Retain the established source/export ownership.
