---
name: svg-animation
description: Design, implement, diagnose, and verify animated SVG graphics for websites and interfaces. Use when motion changes SVG geometry, transforms, paths, masks, strokes, icons, diagrams, or illustrations; do not use for animation that contains no SVG.
---

# SVG Animation

Build motion that preserves the drawing's meaning at every frame, including when animation is unavailable.

## Start with the static drawing

Inspect the rendered SVG and its `viewBox` before changing motion. Confirm that recognizable objects share the right geometry and attachment points. A basket belongs on its pole; a wheel rotates around its axle; liquid follows the glass silhouette. Fix those relationships before tuning timing.

Use `svg-design` when the task also requires constructing or repairing static paths, icon families, IDs, symbols, or export geometry. Preserve an existing icon system rather than drawing a competing one for a small motion change.

Separate static structure from moving parts with named groups or elements. Animate the smallest meaningful part. Do not rotate or translate a whole icon when only a crank, wheel, indicator, or particle should move.

## Choose the motion mechanism

- Prefer CSS transforms and opacity for short, independent icon motion. They are easy to pause, query, and disable.
- Use SVG presentation properties for stroke drawing or color changes when the property must follow SVG geometry.
- Use native SVG motion paths when an object must follow an authored path and a static fallback remains complete.
- Use the requested or existing GSAP, Motion, or other runtime when its sequencing, input, or lifecycle support fits the task. Use `web-animation` for runtime-specific integration and verification. Do not replace a selected library merely because a native alternative exists.

Read [references/geometry-and-motion.md](references/geometry-and-motion.md) when transforms, path motion, clipping, masks, or responsive scaling are involved.

## Accessibility and motion safety

Keep decorative SVGs out of the accessibility tree with `aria-hidden="true"`. Give meaningful standalone graphics an accessible name and description. Never put essential meaning only in motion.

Honor `prefers-reduced-motion: reduce`. Stop continuous travel, parallax, spinning, pulsing, and simulated physical movement. Show the complete static state instead of hiding meaningful geometry. Pause motion when the page is hidden when a long-running script or animation controller exists.

Avoid rapid flashes, large unexpected movement, and motion triggered solely by hover. Pointer-triggered animation must also work from keyboard focus when it communicates interaction state.

## Performance

Prefer `transform` and `opacity`. Keep animated filters, masks, gradients, large blurs, and path morphs small and justified. Reuse geometry with `<symbol>` and `<use>` only when it does not complicate styling or accessible names. Keep `viewBox`, explicit aspect ratio, or reserved layout dimensions stable so the SVG cannot cause layout shift.

Avoid adding a library solely for a trivial effect, but account for the user's choice and existing dependencies. Give each transform or path property one animation owner. For JavaScript motion, batch layout reads before writes and run frame callbacks only while needed. Do not drive per-frame values through framework rerenders when the runtime can update them directly.

## Diagnose

Trace a visual defect to geometry, coordinate space, paint order, clipping, or timing before editing. Check:

- the element's computed transform and `transform-origin`;
- whether `transform-box` is `view-box`, `fill-box`, or `stroke-box` as intended;
- whether the pivot matches the actual axle or joint in viewBox coordinates;
- whether moving elements are grouped too broadly;
- whether the static first frame is correct;
- whether clipping, overflow, or paint order hides the intended shape.

State the supported cause before changing code. Make one geometry or motion correction at a time.

## Verify

Read [references/browser-verification.md](references/browser-verification.md) for animated web output. At minimum, run the repository's checks, inspect narrow and desktop renders, verify reduced motion, and examine more than one animation phase. A single screenshot proves layout, not movement.

Use `responsive-web-capture` when the SVG participates in responsive page layout, `cli-web-evidence` for deterministic phase or interaction capture, `accessibility` for semantic and reduced-motion review, and `performance` only when runtime evidence identifies animation cost.

Report the mechanism used, the reduced-motion result, tested viewports, and any browser coverage gap.
