# Motion for React

Motion for React was formerly Framer Motion. Current standalone documentation uses the `motion` package with imports from `motion/react`. Preserve an existing `framer-motion` installation unless a migration is requested or necessary. Framer Code Components and Overrides use `framer-motion`, so do not mechanically rewrite those imports. [React setup](https://motion.dev/docs/react), [upgrade guide](https://motion.dev/docs/react-upgrade-guide), [Framer integration](https://motion.dev/docs/framer).

## State and presence

Use declarative animation props and variants for state-driven components. Keep stable keys tied to item identity. An `AnimatePresence` boundary must remain mounted to observe a child's removal. Choose exit sequencing for the actual layout, and preserve focus when an exiting element stays in the DOM. Do not let a disappearing overlay continue blocking input. [AnimatePresence](https://motion.dev/docs/react-animate-presence).

Use `layout` or shared `layoutId` for actual layout changes. Do not combine competing CSS transforms with Motion's transform ownership on the same element. Keep semantic DOM order correct even when visual interpolation bridges positions. Inspect clipping, scroll containers, text scale distortion, and interrupted transitions. [Layout animation](https://motion.dev/docs/react-layout-animations).

Use motion values and derived values for continuous pointer or scroll motion instead of triggering a React state update on every frame. Use component state for discrete product state. Do not render a new motion component type inside every render. [Motion values](https://motion.dev/docs/react-motion-value), [motion component](https://motion.dev/docs/react-motion-component).

## Accessibility and rendering

Set `MotionConfig reducedMotion="user"` when appropriate for the application and use `useReducedMotion` to implement specific alternatives. The global setting does not mean every effect is disabled: review opacity loops, custom motion values, scroll effects, and other engines separately. [Accessibility](https://motion.dev/docs/react-accessibility).

Keep hooks and browser reads in the correct client boundary. Match the server and initial client markup. `initial={false}` can suppress an unwanted first transition, but is not a hydration-error fix. Preserve content if an enhancement cannot load. Consult the installed version's integration guidance for React Server Components. [Installation](https://motion.dev/docs/react-installation).

Check rapid enter/exit, reordered keys, route changes, keyboard activation, touch input, and development remounts. Motion durations commonly use seconds, while browser timer APIs use milliseconds. Test the actual timing boundary rather than copying one number between APIs.
