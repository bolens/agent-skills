# Motion evidence contract

Use the repository's browser harness and `cli-web-evidence`. A screenshot with animations disabled proves a static state. A recording proves appearance over time, but assertions are still needed for state, focus, and cleanup.

## Choose evidence for the failure surface

| Surface | Evidence |
|---|---|
| CSS or WAAPI timing | Owned animation instances paused and sampled at known times, plus one real trigger |
| GSAP timeline | Instance progress or time samples, plus actual scroll/gesture wiring |
| Motion/framework state | Real state transition, intermediate appearance, settled semantics, repeated interruption |
| SVG geometry | Static frame and multiple non-equivalent phases using `svg-animation` |
| Lottie/Rive | Asset loaded, representative frames or state-machine input transitions, renderer and fallback checked |
| Route/scroll motion | Deep link, restored scroll, reverse navigation, resize, and teardown |

Do not assume `document.getAnimations()` exposes JS timelines, SMIL, canvas players, or state machines. Use the runtime's instance controls when possible. In tests, prefer a local harness adapter to permanent production debugging globals. Wait for observable load/readiness and settling, not an arbitrary long sleep.

For a looping motion, sample phases that cannot accidentally look identical. For a stateful interaction, test mid-flight reversal or repeated activation and confirm the final product state. Seeking past completion callbacks can bypass behavior, so deterministic samples supplement the real interaction path.

## Required shared checks

- Initial content is usable, including the intended loading/error fallback.
- Narrow and desktop layouts, plus the breakpoints where choreography changes.
- Reduced motion before load and, where supported, a live preference change.
- Keyboard/focus and touch alternatives for pointer-driven behavior.
- Repeated mount/unmount or route entry, with no accumulating listeners, timelines, triggers, players, or render loops.
- Hidden/offscreen suspension where used, without overriding an intentional user pause.
- Console, network, layout/overflow, and relevant production/SSR build results.

Check only the relevant subset of triggers and states, but report omissions precisely. Use a performance trace for frame cost or jank claims. A deterministic screenshot run with motion frozen cannot supply that evidence.

Record the revision, URL, viewport, browser, runtime/version, trigger, sampled times or states, reduced-motion setting, and artifact paths. Keep captures in task-scoped temporary storage unless the repository specifies otherwise.
