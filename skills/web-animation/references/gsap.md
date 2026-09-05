# GSAP

Check the installed GSAP and plugin versions before using current APIs. Register only the plugins needed by the task. Check current official distribution and licensing instructions if adding a plugin, rather than assuming old Club/private-registry arrangements still apply.

## Framework lifecycle

In React, use the existing `@gsap/react` integration when present. `useGSAP` scopes selector text through its `scope` option and reverts collected GSAP objects on teardown. Use `revertOnUpdate` when dependency changes require rebuilding those objects. Delayed callbacks and event handlers that create animations need `contextSafe`; ordinary DOM listeners still need explicit removal. In other frameworks, own a `gsap.context()` and call `revert()` from teardown. Keep DOM work in the client lifecycle. [React integration](https://gsap.com/resources/React/).

Never call `gsap.globalTimeline.clear()` or kill every ScrollTrigger to clean up one component. Give each effect a local timeline or context. Scope text splitting and restore the original text structure on teardown. Preserve the accessible reading order.

## Timelines and responsive motion

Use timeline labels and relative positions for coordinated sequences. Distinguish reversing a sequence from constructing a new one on every event. GSAP duration values use seconds. Inspect `from`/`fromTo` initial rendering when elements jump before their intended start. [Timeline](https://gsap.com/docs/v3/GSAP/Timeline/).

Use `gsap.matchMedia()` for breakpoint and reduced-motion branches. Revert the match-media context on teardown. Reduced motion should leave content visible and remove unnecessary pinning or travel, not merely speed up the full effect. [matchMedia](https://gsap.com/docs/v3/GSAP/gsap.matchMedia()/).

## ScrollTrigger and layout

Use one scroll owner for a scrubbed timeline. Avoid attaching independent ScrollTriggers to children whose playheads the parent timeline already controls. Animate an inner element when transforming the trigger or pinned element would invalidate its measurements. Keep normal reading order and a usable unpinned layout.

After layout-affecting assets or content settle, refresh trigger geometry when needed. Use function-based measurements and `invalidateOnRefresh` where values depend on changing layout. Do not call `refresh()` on every scroll frame. Test deep links, restored scroll positions, resize, reverse scrolling, and route re-entry. [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/).

Use Flip for a measured layout transition when it fits the existing implementation. Capture the old state before changing layout. Do not assume a screenshot transform proves the final DOM layout or focus order is correct. [Flip](https://gsap.com/docs/v3/Plugins/Flip/).

For tests, retain the instance and sample a paused timeline at known progress values. Also run the real scroll/input path: seeking a timeline alone bypasses ScrollTrigger and interaction wiring.
