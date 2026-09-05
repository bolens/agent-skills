# Other runtimes and workflows

Preserve an existing stack. These are integration routes, not reasons to install every library. Verify APIs against the installed major version and official documentation when implementing.

## Anime.js

Use for imperative timelines and SVG/DOM animation when selected by the user or repository. Current v4 APIs differ from common v3 examples. Do not mix a v3 `anime({...})` recipe with v4 imports. A scoped v4 integration can use `createScope` and `revert()` for owned animation cleanup. Explicitly remove event listeners in cleanup too. [Scope cleanup](https://animejs.com/documentation/scope/scope-methods/revert/).

## React Spring

Use for spring-driven React values and interactive continuity when it is already the chosen engine. Keep spring state distinct from application state. Verify the package target, controller lifecycle, reduced-motion support, and interruption behavior in the installed version. Do not copy damping/stiffness or timing values directly from another engine and assume equivalent motion. [React Spring docs](https://www.react-spring.dev/docs).

## Vue and Svelte

Vue's `Transition` handles entering/leaving content, while `TransitionGroup` covers keyed lists and reordering. Preserve stable keys and settle JavaScript hooks correctly on completion or cancellation. Avoid simultaneous CSS and JS ownership of the same transition. [Vue Transition](https://vuejs.org/guide/built-ins/transition.html), [TransitionGroup](https://vuejs.org/guide/built-ins/transition-group.html).

In Svelte, first inspect built-in transition and animate facilities plus the project's version conventions. Prefer declarative transitions over an unnecessary React-oriented dependency. Scope imperative additions to component lifecycle, and verify keyed reorders and overlapping intros/outros. [Svelte transitions](https://svelte.dev/docs/svelte/transition), [animate](https://svelte.dev/docs/svelte/animate).

Motion also documents JavaScript and Vue integrations. Use their actual APIs rather than substituting React imports. [Motion documentation](https://motion.dev/docs).

## Three.js and React Three Fiber

Use only when the requested effect needs a 3D scene, shader, or existing canvas integration. Do not replace an ordinary DOM interaction with WebGL for novelty. Keep accessible controls and content in the DOM.

In R3F, avoid React state updates inside `useFrame` for continuous animation. Mutate owned render values, use frame delta for time-based movement, and consider demand rendering for mostly static scenes. Coordinate invalidation when external animation changes scene values. Bound pixel ratio and inspect GPU/resource cleanup according to ownership. These rules do not substitute for a scene-specific rendering or asset pipeline review. [R3F performance](https://r3f.docs.pmnd.rs/advanced/scaling-performance).

For an offline rendered video, use the project's video workflow instead of pretending browser interaction evidence proves export timing or encoding. Lottie and Rive authoring/runtime handoffs belong to `animation-assets`.
