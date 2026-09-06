# Required older-browser support

Use this reference when the user or repository explicitly requires older browsers, embedded webviews, or enterprise-managed browser versions. Keep [modern targets](modern-targets.md) as the default elsewhere. Compatibility work must deliver the required user journeys, not merely make a build accept an older target string.

## Turn requirements into a support contract

Record browser engine and minimum version, OS/device or webview constraints, required journeys, and support level: full functionality, functional fallback, or an explicitly agreed limited experience. Separate essential behavior from optional visual enhancement. Use existing product requirements and relevant usage evidence; analytics can inform the decision but cannot silently remove a named requirement. Ask only when an unresolved support level changes the implementation materially.

Identify the framework and dependency support floors before promising compatibility. A polyfill cannot generally make a framework support an engine it explicitly excludes. Where the requested matrix conflicts with the stack, present concrete options such as an alternate supported implementation, a bounded compatibility build, or a revised requirement. Keep security and functionality costs explicit rather than silently downgrading the stack or dropping the browser.

Make one authoritative browser matrix drive the applicable JavaScript compiler, CSS processor, bundler runtime, tests, and delivery configuration. Inspect which tools actually consume Browserslist and which require separate targets. Resolve the configured query with the repository's installed tooling and inspect the resulting versions for the production environment. Do not assume `defaults`, a usage threshold, `not dead`, or `last N versions` includes an explicitly required old version. Pinning a minimum version is different from a moving release query. See [Browserslist configuration and queries](https://github.com/browserslist/browserslist#queries).

## Choose the right compatibility mechanism

| Gap | Appropriate response | What does not solve it |
| --- | --- | --- |
| Unsupported JavaScript syntax | Build-time syntax transformation covering entrypoints, dependencies, lazy chunks, workers, and generated runtime code | A runtime polyfill or a feature check in a file the browser cannot parse |
| Missing JavaScript built-in | Targeted maintained polyfill or compatible local helper, including needed dependencies | Syntax transpilation alone |
| Missing DOM/browser API | Verify a maintained API-specific polyfill's semantics or use a supported alternative | Assuming an ECMAScript polyfill bundle supplies every web API |
| Unsupported CSS feature | Supported declarations/layout first, then enhancement; use build transforms only where semantics can be preserved | Assuming vendor prefixes implement a missing layout engine or `@supports` repairs a feature |
| Missing codec or asset format | Encode a supported alternative only for the required matrix; verify selection and delivered content | A JavaScript shim that cannot provide the required decoder or platform integration |
| Missing platform/security capability | Redesign the affected flow or document an explicit unsupported boundary | Claiming a polyfill can reproduce permissions, hardware APIs, TLS support, or browser security guarantees |

Feature-detect the exact capability or known faulty subfeature, not just an API name. Ensure the detector and loader themselves use syntax and APIs supported by the minimum browser. Parsing happens before runtime branches: wrapping optional chaining in an `if` does not make it safe for an engine that cannot parse optional chaining. Avoid user-agent routing unless a documented engine defect cannot be identified more reliably; keep any such exception narrow and tested.

## Keep polyfills bounded and correctly loaded

Inventory existing framework/bundler polyfills first. Add only implementations needed for actual target gaps, with maintenance, license, semantics, bundle cost, and dependency verification. Prefer bundled or self-hosted reviewed artifacts with locked versions and update monitoring. Do not introduce an unpinned third-party polyfill service as a prerequisite for application execution.

With Babel, inspect the installed preset/plugin versions, targets, injection mode, and configured core-js version. `@babel/preset-env` can select transforms and supported built-in polyfills from targets, but it does not supply every browser API. Choose one deliberate entry-based or usage-based strategy and inspect emitted output for missing or duplicate coverage. Match configuration to the installed core-js release; do not copy a stale major/minor from an example. See [preset-env](https://babeljs.io/docs/babel-preset-env/).

Load required polyfills before the code that uses them, including framework bootstrap and route chunks. Test cold entry and direct deep links. A dynamic polyfill loader may itself require Promise, module loading, or syntax unavailable in the target; solve that bootstrap dependency first. Keep browser-only patches out of server execution, and account separately for worker globals and isolated execution contexts. Libraries should avoid silently patching their consumers' globals; prefer a scoped implementation or an explicit consumer requirement when feasible.

Use the existing bundler's supported compatibility mechanism. Differential modern/legacy delivery is useful only when its runtime and loader cover the required browsers and the cost is justified. Module support alone does not mean every modern syntax feature or API is present. Verify that a browser gets the correct entry and does not execute both builds, and that legacy lazy chunks are also compatible. If selection affects responses, check caching and content negotiation. Retain CSP and integrity requirements for the actual delivered assets.

Keep a functional baseline for required journeys. A fallback for a dialog, popover, or form must preserve keyboard/focus behavior, validation, submission, and error recovery, not just its appearance. Preserve deterministic SSR/hydration, reduced motion, and loading/network-failure recovery independently of browser age. A full no-JavaScript implementation is required only when the product contract says so.

## Verify and retire support deliberately

Test production artifacts in the actual required browser versions or a trustworthy matching remote environment. Modern Chromium with a changed user agent or a deleted API is not old-browser validation. Use such simulations only as supplemental fallback-path checks. Record unavailable engines as unverified; do not declare the requirement met from a successful transpile or lint run.

Verify initial parsing/bootstrap, direct navigation, lazy loading, required interactions, API behavior, CSS layout, assets, and accessibility on both the minimum supported version and current engines. Include failed/delayed polyfill loading where applicable. Check final network requests, cache behavior, CSP, duplicate bundles, transferred bytes, and execution cost. Re-test after dependency or build-tool updates that can emit newer syntax or change polyfill injection.

Record each compatibility layer's covered requirement, owner, verification, and removal condition. Remove it only after the support contract changes and current-target tests pass. Browser-data updates and moving queries can change output without source changes, so review the resolved matrix and bundle diff during updates. Do not let a temporary exception become an undocumented permanent runtime pin.
