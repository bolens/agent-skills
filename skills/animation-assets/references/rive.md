# Rive

Inspect the actual `.riv` file's artboards, state machines, animations, inputs or data bindings, and external assets with the available editor/runtime. Keep these names in one integration mapping. Do not infer them from a marketing preview.

## Runtime ownership

Select the installed web or framework runtime and renderer deliberately. Load the intended artboard and state machine, then wait for readiness before binding controls. Keep canvas dimensions, device pixel ratio, fit, and alignment consistent with the layout. At the low-level web integration, release an owned Rive instance with `cleanup()` when it is no longer needed. Do not separately destroy a resource managed by a framework wrapper without checking its lifecycle. [Web runtime](https://rive.app/docs/runtimes/web/web-js).

Distinguish pausing animation from stopping the rendering loop. Preserve the prior playback state when suspending for visibility. Check the current runtime API before managing renderer/GPU resources directly. [Runtime parameters and lifecycle](https://rive.app/docs/runtimes/web/rive-parameters).

## Application state

Use the state-machine or data-binding interface actually exported by the file. Do not invent a universal boolean/number/trigger interface for assets authored with a different binding model. When traditional state-machine inputs are used, verify their types and fire triggers deliberately rather than on every render. [State-machine playback](https://rive.app/docs/runtimes/web/state-machines).

Keep the application's semantic state and accessible controls outside the canvas. Test rapid input changes, completion/error paths, source replacement, and resizing. A timeline pose does not prove a state machine reached the intended state. For reduced motion, use a supported static state/poster and preserve the underlying action and feedback.

If a requested change requires editing the `.riv` source and no authoring capability is available, deliver supported integration work and a precise source-edit specification. Do not claim an exported binary was changed when only its host component was modified.
