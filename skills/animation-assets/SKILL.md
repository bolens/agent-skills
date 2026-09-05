---
name: animation-assets
description: Integrate, diagnose, and verify authored Lottie JSON, dotLottie, and Rive animations in web interfaces, including player lifecycle, state-machine wiring, asset handoff, accessibility, and loading performance. Use for Lottie/Bodymovin, .lottie, or .riv work, not ordinary DOM animation, static SVG editing, or video production.
---

# Animation assets

Treat an authored animation as an asset plus a runtime contract. Keep the editable source, exported file, player version, and application behavior distinct.

## Inspect the asset and host

Identify the supplied format, authoring source, export settings, dimensions, duration/frame rate, markers or state machines, embedded/external images and fonts, intended player, and license. Inspect the actual asset rather than inventing artboard, state, or marker names. Check installed packages and preserve their versions and wrapper conventions.

Read [Lottie and dotLottie](references/lottie.md) or [Rive](references/rive.md) as appropriate. Do not mix APIs from similarly named players or assume a `.lottie` container is plain JSON. A `.riv` binary requires an appropriate Rive runtime or authoring tool. Do not fabricate one or promise binary edits with a text editor.

For new authored content, establish what can be produced with available tools. If the source file or editor is missing, implement the player integration and fallback where possible, and identify the exact authoring/export work still needed. Do not replace a requested Lottie or Rive deliverable with a different format without agreement.

## Integration contract

- Give the player a stable container and reserved dimensions. Keep meaningful text and controls in semantic DOM, even if the artwork renders into canvas.
- Initialize once per owned asset/container after mounting. Wait for the relevant runtime/asset readiness event before selecting frames or sending inputs. Dispose listeners, player instances, and owned resources when changing assets or unmounting.
- Define loading, load-error, unsupported-renderer, and reduced-motion behavior. Use an authored poster or known meaningful frame. Do not assume frame zero contains visible artwork.
- Bind discrete inputs to application state. Animation completion can provide presentation feedback but must not be the only way to record a successful transaction or unlock essential controls.
- Preserve the user's pause preference across visibility changes. Suspend unnecessary rendering offscreen or when hidden, and resume only previously active playback.
- Inspect actual transfers: JSON/container size, image/font assets, runtime/WASM, and worker files. Configure asset paths and CSP through the application rather than silently relying on a third-party CDN. Use the deployed base path in verification.

Do not convert files, change renderers, rasterize vectors, or rewrite export JSON merely to reduce a byte count without checking the visual and interaction result. Preserve source material and document any lossy handoff.

## Verify

Use the motion evidence contract in `web-animation` and the project's browser harness. Check the loaded asset, non-equivalent phases or state transitions, looping/segments, interruption, resize/pixel ratio, reduced motion, load failure, and repeated teardown. For state machines, test input transitions rather than assuming a frame seek proves interactivity.

Compare the exported animation with the supplied reference when one exists. Report renderer, runtime version, asset source, markers/inputs used, tested states, accessibility fallback, transfer or trace evidence when measured, and any missing authoring capability. Use `performance` only for measured runtime concerns and `svg-animation` only for geometry you actually own.
