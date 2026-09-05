# Browser-native implementation

Use this reference for requests described as browser-native or standards-based. Choose a native primitive when it meets the product contract, not as a mandate to replace an established library.

## Forms and controls

Prefer native form submission and constraint-validation behavior where it fits. `requestSubmit()` follows submission behavior including validation and the submit event, while `submit()` bypasses those steps. Preserve the intended submitter and button type. Inspect what `FormData` actually contains, including disabled controls, unchecked inputs, and files. Use `forms-and-data-state` for server validation and async ordering. [requestSubmit](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/requestSubmit).

Use `details`/`summary` for disclosure when their semantics fit. Do not turn every custom widget into a native element whose interaction contract differs from the requested control.

## Dialogs and popovers

For a modal dialog, inspect `showModal()` behavior rather than treating an `open` attribute or visual overlay as equivalent. Preserve accessible naming, a deliberate initial focus target, close/cancel behavior, and focus return. New dialog features need their own support check. [Dialog](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog).

Use actual action buttons with deliberate types. For destructive confirmation, choose initial focus appropriate to the consequence, commonly the non-destructive action, and verify that opening or dismissing the dialog cannot accidentally invoke the destructive operation.

Popover handles a different class of interaction and is not automatically a modal dialog, menu, or tooltip. Verify the intended modality, light dismissal, focus, and semantic role. Keep the trigger relationship and closing paths usable. Do not duplicate a primitive's native dismissal with competing global click handlers. [Popover API](https://developer.mozilla.org/en-US/docs/Web/API/Popover_API).

## URL and navigation

Use `URL` and `URLSearchParams` rather than ad hoc string concatenation. Preserve repeated query values when they are meaningful. Encoding a URL does not authorize its destination or protocol.

Keep history state and rendered state aligned, including the initial entry, back/forward actions, and direct deep links. `pushState()` alone does not render a view or fetch a document. In a routed application, use the router's supported integration instead of adding a competing history listener. Verify scroll/focus restoration as part of navigation. [History API](https://developer.mozilla.org/en-US/docs/Web/API/History_API/Working_with_the_History_API).

## Events and observers

Scope listeners, `ResizeObserver`, `IntersectionObserver`, timers, and asynchronous callbacks to their owner. Remove listeners and disconnect owned observers on teardown. Use delegated events only where propagation and target matching are understood, including shadow-root boundaries when present.

Prevent observer feedback loops and per-frame layout thrashing. Do not make business correctness depend on an observer firing immediately. Preserve focus and pointer capture/cancellation behavior where relevant. Repeated mount or route entry must not accumulate handlers.
