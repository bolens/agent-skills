# Browser-native motion

Use CSS transitions/keyframes for bounded visual states. Target explicit properties instead of `transition: all`. Use WAAPI when imperative playback, cancellation, or deterministic seeking adds value. Retain only the animation instances this component owns.

WAAPI cancellation can reject an outstanding `finished` promise. Treat expected cancellation as interruption and avoid running stale completion work. Cancel owned instances on teardown and remove listeners separately. Persist the intended final style through application state or a deliberate style update rather than relying on a discarded animation. [Animation.cancel](https://developer.mozilla.org/en-US/docs/Web/API/Animation/cancel).

## View Transitions

Feature-detect the required same-document or cross-document capability. Preserve a direct DOM/router update when unavailable or motion is reduced. Keep navigation, history, loading, focus, and error handling with the router. Do not add a second navigation implementation to animate it.

Use unique transition names for concurrently rendered participants and clear temporary names when the transition is over. Snapshot animation is a visual layer, not proof that the underlying page's focus and interaction behavior is correct. Verify back/forward navigation and interruption. [View Transition API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API).

## Scroll-driven motion

Prefer native scroll/view timelines when they meet the target browser requirements and effect. Feature-detect the actual features used and keep content visible without them. Avoid a default `opacity: 0` reveal that only a supported timeline can undo. Use JavaScript orchestration when the requested choreography needs it rather than growing a brittle CSS workaround. [Scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations).

Native motion still needs reduced-motion handling, cancellation, resize checks, and performance evidence. Browser support varies by feature: verify against the project's browser matrix when implementing instead of storing a universal support percentage in the skill.
