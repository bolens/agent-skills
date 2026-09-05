# Browser verification

Use the repository's browser harness first. Otherwise use CLI-driven Chrome or Chromium through CDP, Playwright, or Puppeteer.

For a page-wide viewport matrix, follow `responsive-web-capture`. For interaction recordings, console/network checks, and evidence receipts, follow `cli-web-evidence`. Apply `accessibility` when names, descriptions, keyboard behavior, forced colors, or reduced motion are in scope.

## Required evidence

1. Inspect a static render at one narrow and one desktop viewport.
2. Capture or inspect at least two animation phases. Use deterministic animation control when possible:
   - pause CSS animations with the Web Animations API and set `currentTime`;
   - for SMIL, use the SVG timeline controls when available, otherwise record the motion;
   - seek owned GSAP/library instances through their runtime controls rather than assuming the Web Animations API can see them;
   - do not infer correct rotation or path travel from one frame.
3. Emulate `prefers-reduced-motion: reduce` and confirm continuous motion stops while the graphic remains understandable.
4. Check console errors, failed requests, horizontal overflow, and layout dimensions.
5. Check dark mode and forced colors when the host interface supports them.

For rotation, compare the moving sub-element's computed transform at two times and confirm static siblings do not change. For path travel, inspect the traveler's screen position at two times. For opacity or particle motion, verify that the containing object does not shift.

Choose non-equivalent phases, including an intermediate shape for morphs. Test two instances on the same page to expose ID collisions, selector leakage, and shared timeline state. Re-enter the route or remount the component to detect duplicated animation work. Check the actual interaction as well as any programmatic seek. Use `web-animation` for interruption and runtime cleanup evidence, and `animation-assets` for generated Lottie/Rive players whose internal geometry is not owned by the component.

Keep screenshots and recordings in a task-scoped temporary directory unless the repository defines an evidence location. Record the URL, viewport, state, and command used.
