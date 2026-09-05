# Lottie and dotLottie

## Choose the actual player

`lottie-web` consumes exported Lottie animation data and supports SVG, canvas, and HTML renderers. Its `loadAnimation` returns an instance. Supply either `path` or `animationData`. Use instance methods rather than global playback calls that affect other animations. `goToAndStop(frame, true)` uses frames; omitting the flag changes interpretation. Destroy the instance on teardown. Some repeater assets require a fresh/deep-cloned data object per load. [lottie-web API](https://github.com/airbnb/lottie-web).

dotLottie players support `.lottie` containers and Lottie JSON. Inspect the package and version, such as `@lottiefiles/dotlottie-web` or a framework wrapper, before choosing APIs. Multi-animation containers may require selecting the intended animation. Do not pass a container to an unrelated JSON-only player. [dotLottie JavaScript player](https://docs.lottiefiles.com/en/runtimes/distributions/js).

The React wrapper exposes a player reference and methods such as frame/segment selection and freeze/unfreeze. Use the installed wrapper's lifecycle and distinguish player readiness from asset load. A paused playhead and suspended rendering are different states. Use only documented events and methods for that version. [dotLottie React API](https://docs.lottiefiles.com/en/runtimes/distributions/react/v0.x/api-reference).

## Authoring and export handoff

Record the composition bounds, frame rate, intended loop/segment, marker names, external asset paths, font treatment, and player renderer used for approval. Bodymovin/After Effects features do not all render identically across players. Test masks, mattes, expressions, effects, text, and blend modes actually used by the asset. Ask for a corrected export only after localizing the incompatible feature. [Supported features](https://github.com/airbnb/lottie-web/wiki/Supported-Features).

Prefer authored markers for semantic segments when available, and verify their actual names. Do not scatter guessed frame numbers through application code. Maintain a small mapping at the integration boundary. [Markers](https://github.com/airbnb/lottie-web/wiki/Markers).

Use an SVG renderer's generated DOM only through supported player customization or a deliberate, tested integration. Direct edits can disappear on the next render. Check a meaningful stopped frame for reduced motion and a separate fallback for a failed asset load.
