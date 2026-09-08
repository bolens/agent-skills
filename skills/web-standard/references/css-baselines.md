# CSS normalization and resets

Use when choosing or updating global base CSS, diagnosing browser-default
inconsistencies, or integrating a shared component system. Sources reviewed in
September 2026; recheck their maintained documentation and installed versions on
adoption. There is no universal "2026 reset" that every site should install.

## Choose one owner

Inspect the CSS entrypoint, framework imports, reset/normalize dependencies,
component-library baseline, layers, and generated CSS. Preserve a working baseline
unless a specific inconsistency or migration warrants a change. A reset replaces
selected browser defaults with design decisions; normalization primarily aims to
make defaults consistent. Neither replaces component styling or browser testing.

| Existing setup or need | Reference and decision |
| --- | --- |
| Tailwind project | Read [Preflight](https://tailwindcss.com/docs/preflight) for the installed major. Current Tailwind imports its baseline into the base layer; inspect the build before adding another reset or normalizer |
| Small current-browser normalization | Consider [modern-normalize](https://github.com/sindresorhus/modern-normalize), whose declared targets are current Chrome, Firefox, and Safari; inspect its actual rules and target fit |
| Existing Normalize.css integration | Preserve and assess [Normalize.css](https://github.com/necolas/normalize.css) against the actual support contract; an older release date alone does not justify replacement |
| Additional opinionated baseline modules | Assess [sanitize.css](https://csstools.github.io/sanitize.css/) and only its needed modules; check overlap with framework styles |
| Deliberate project-owned baseline | Use [Andy Bell's explanation](https://piccalil.li/blog/a-more-modern-css-reset/) or [Josh Comeau's explanation](https://www.joshwcomeau.com/css/custom-css-reset/) to evaluate individual decisions, not as mandatory full-file recipes |

Keep the selected dependency pinned through the project's package/lock workflow.
Use the existing build pipeline; do not load an unversioned remote reset stylesheet
on every page. If vendoring is justified, retain its source revision, license, and
local differences. Link to upstream rationale instead of copying its tutorial into
skills or maintaining independent snippets across projects.

## Respect the cascade and component boundaries

Use the existing cascade-layer order. For a new layered system, put normal baseline
rules in an early layer that component and utility rules can override. Inspect
emitted CSS: normal unlayered author declarations outrank normal layered ones, and
important declarations reverse layer priority. Moving a stylesheet into a layer
can change behavior even if its selectors are unchanged. Do not use `!important`
to patch a misunderstood order. See [MDN layers](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer).

Scope exceptions to the owning component or third-party integration. A reset of
all image dimensions/borders can break maps, editors, or widgets. Document-wide
resets do not automatically normalize an iframe or shadow tree; inspect inherited
properties, exposed parts, and the component's supported styling interface. Avoid
injecting a second document reset into every component package.

## Review decisions that affect usability

Review box sizing, pseudo-elements, margins, headings, lists, replaced elements,
and form controls against actual consumers. Preserve focus indication, keyboard
operation, native disabled/validation states, and discoverable links. Removing
list markers can affect list exposure in some browser/assistive-technology paths;
follow the framework's documented semantics and verify the resulting accessibility
tree rather than applying ARIA to every list.

Keep text zoom/reflow, forced colors, and user preferences usable. Do not globally
remove outlines, disable resizing or text adjustment, strip every control's native
appearance, or apply `all: unset` merely to get a blank canvas. Such decisions need
a scoped reason and an accessible replacement where needed. Treat typography,
heading balancing, smooth scrolling, and motion as product choices. A global
near-zero animation duration is not a complete reduced-motion implementation;
use the existing motion workflow for explicit states and event/lifecycle behavior.

## Verify the baseline change

Use the existing component/browser harness with representative headings, nested
lists, links, images/SVG, tables, and enabled/disabled/invalid form controls.
Exercise focus, keyboard navigation, zoom/reflow, long/localized text, themes,
forced colors, and relevant embedded widgets. Test current Chromium, Firefox,
and Safari as required by [modern targets](modern-targets.md); retain any explicit
older-browser support contract. Chromium viewport emulation is not Safari proof.

Compare before/after computed styles and rendered states at affected boundaries.
Confirm the built output loads the intended baseline once and that layer/import
ordering is stable. Report missing engines or assistive-technology coverage.
When only one component is broken, prefer repairing its rule over replacing the
entire project's reset. No new reset is needed when the existing baseline meets
the requested behavior.
