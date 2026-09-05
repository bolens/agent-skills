---
name: web-animation
description: Design, implement, debug, and verify interface motion, timelines, scroll choreography, gestures, and page transitions using CSS, WAAPI, GSAP, Motion for React (formerly Framer Motion), Anime.js, or framework-native transitions. Use for web animation work, not static visual design or video rendering. Route Lottie and Rive assets to animation-assets and SVG geometry to svg-animation.
---

# Web animation

Make motion explain a state change, spatial relationship, or deliberate visual idea. Preserve usable content before initialization, during interruption, and when motion is reduced.

## Establish the motion contract

Inspect the framework, installed packages and versions, existing motion utilities, rendering model, and target browsers. Preserve the user's chosen library and the repository's conventions. Do not migrate `framer-motion`, add a second engine, replace the router, or add smooth scrolling merely to implement an effect.

For each effect define its trigger, moving properties, timing or spring behavior, interruption policy, final state, reduced-motion alternative, and owner responsible for cleanup. Scale this to the task. A button transition needs no storyboard, while a pinned scroll narrative benefits from a short sequence of states.

Use the smallest suitable implementation, accounting for an existing library's lifecycle and test support rather than bundle size alone. Read only the relevant reference:

| Work | Route |
|---|---|
| Timeline orchestration, ScrollTrigger, Flip, SVG plugins | [GSAP](references/gsap.md) |
| React layout, enter/exit, gestures, scroll-linked values | [Motion for React](references/motion.md) |
| CSS/WAAPI, View Transitions, native scroll timelines | [Browser-native motion](references/native.md) |
| Anime.js, React Spring, Vue, Svelte, Three.js/R3F boundaries | [Other runtimes](references/other-runtimes.md) |
| Lottie/dotLottie or Rive playback and asset handoff | `animation-assets` |

Use `svg-animation` alongside this skill when moving paths, pivots, masks, or SVG coordinate systems matter. Let the chosen runtime own timing and SVG guidance own geometry. Use `frontend-design` for the visual direction and `design-system` when motion tokens or shared components must be consistent.

## Implement ownership and lifecycle

- Give each animated property one owner. Separate layout placement and animated transforms into nested wrappers when CSS, a component primitive, and an animation engine would otherwise overwrite each other.
- Initialize DOM-dependent work after mounting in the framework's appropriate lifecycle. Keep browser globals out of server evaluation and the initial render deterministic. Preserve the smallest necessary client boundary in SSR applications.
- Cancel or reverse obsolete work on rapid input. Avoid queued hover effects, stale completion callbacks, and delayed removal that leaves hidden controls focusable. Product state must not depend solely on an animation completing.
- Scope selectors, timelines, observers, listeners, timers, and render loops to the component or route. Teardown must remove both animation objects and callbacks that could recreate them. Test repeated mount/unmount and development remount behavior.
- Separate playback control from construction. A visibility change or pause toggle should normally pause/resume the existing instance, not rebuild it and reset its position. Rebuild when asset or geometry inputs require it, with an explicit restart or progress-preservation policy.
- Treat font loading, image decode, container resize, and changing content as possible geometry invalidation. Re-measure only when needed. Do not alternate layout reads and writes every frame.

## Accessibility and runtime cost

Implement reduced motion in the selected runtime as well as CSS. Preserve status, focus, and the final content. A tiny duration alone does not remove large translation, parallax, camera movement, or loops. Handle changes to the preference during the session when the component remains mounted.

Keep scroll navigation, anchors, keyboard access, and pointer alternatives usable. Do not trap scrolling to force a narrative. Provide pause/stop controls where required for persistent moving content, using `accessibility` for the applicable requirements. Retain logical focus through exits and route changes.

Prefer transform and opacity when they express the effect. They are not a guarantee of compositor-only rendering. Measure expensive filters, layout animation, canvas resolution, and many simultaneous effects. Suspend unnecessary hidden/offscreen work and resume only what was playing before suspension. Do not restart a manually paused animation automatically.

## Verification and delivery

Use [the motion evidence contract](references/verification.md) and the existing browser harness. Verify behavior in the real integration, not only a playground. Run the proportionate build and tests, including a production/SSR check when the change affects hydration or loading.

Report the runtime and version inspected, triggers and states tested, reduced-motion behavior, cleanup evidence, browser/viewport coverage, and remaining gaps. Do not claim smoothness from screenshots or library marketing. Use `performance` when a trace is needed to substantiate runtime cost.
