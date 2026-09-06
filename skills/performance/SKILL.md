---
name: performance
description: Optimize web performance for faster loading and better user experience. Use when asked to "speed up my site", "optimize performance", "reduce load time", "fix slow loading", "improve page speed", or "performance audit".
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
---

# Performance optimization

Evidence-led performance optimization using real-user signals for prioritization and browser traces for diagnosis. Focuses on loading speed, runtime responsiveness, and resource delivery.

Use [modern web targets](../web-standard/references/modern-targets.md): prefer latest stable platform features and maintained tool versions, with legacy compatibility only when explicitly required. Measure current cross-engine behavior before adding polyfills, old syntax targets, or duplicate asset encodings.

## How it works

1. If a page can run, read [the measurement workflow](references/MEASUREMENT.md) and establish a field-plus-lab baseline before editing.
2. Prioritize poor real-user Core Web Vitals. Use a DevTools performance trace and its focused insights to find the cause.
3. Inspect and change only the code or assets connected to measured bottlenecks.
4. Re-run equivalent lab measurements and report before/after values, conditions, and uncertainty. Field verification remains pending until enough new user data arrives.

When no runnable page exists, perform static inspection but call findings **hypotheses**, not measured regressions. Include the command or browser workflow that can verify each high-impact hypothesis.

Use `responsive-web-capture` when a performance change can alter layout across device classes, and `cli-web-evidence` when the affected journey needs functional browser proof. A faster initial render is not sufficient evidence that responsive behavior or interaction still works.

Use `svg-animation` when a measured rendering or main-thread cost comes from animated SVG geometry, filters, masks, path morphs, or per-frame DOM work.

Use `web-animation` to repair measured timeline, scroll, gesture, or lifecycle costs, and `animation-assets` for Lottie/Rive loading, renderer, or player costs. Measure active motion and repeated route entry, not only a static initial frame. A library choice or transform-only implementation is not proof of smooth rendering.

Prefer a browser tool that records a performance trace and exposes focused insights. With Chrome DevTools MCP, use `performance_start_trace` and `performance_analyze_insight`; do not route performance through `lighthouse_audit`, which covers non-performance Lighthouse categories.

## Read the reference for the observed issue

Read only the relevant references for a narrow fix. For a full audit, cover
each requested category and report any unverified checks.

| Issue or task | Reference |
| --- | --- |
| Calibrate product budgets | [Starting performance budget](references/budgets.md) |
| Server latency, resource discovery, and JavaScript delivery | [Critical rendering path](references/loading.md) |
| Image size, format, and loading priority | [Image optimization](references/images.md) |
| Font loading, subsets, and preload | [Font optimization](references/fonts.md) |
| HTTP and service-worker caching | [Caching strategy](references/caching.md) |
| Rendering, handlers, lists, and navigation | [Runtime performance](references/runtime.md) |
| Third-party loading and facades | [Third-party scripts](references/third-party.md) |

## Measurement

Use [the measurement workflow](references/MEASUREMENT.md) whenever a URL is runnable. It defines Chrome DevTools MCP routing, CrUX and fallback sources, repeatable lab conditions, and a compact evidence format.

| Metric | Kind | Interpretation |
|--------|------|----------------|
| LCP, INP, CLS at p75 | Field | User-outcome Core Web Vitals; use for pass/fail prioritization |
| LCP, CLS in a trace | Lab | Reproducible diagnostic values for one navigation |
| TBT | Lab | Main-thread blocking diagnostic and a rough INP proxy, not field INP |
| FCP, Speed Index | Lab | Loading diagnostics, not Core Web Vitals |

Raw `PerformanceObserver` snippets are useful for the current browser session but are not real-user data by themselves. When the user wants production telemetry, read [the first-party RUM reference](references/RUM.md) and prefer `web-vitals` over a hand-rolled metric implementation.

## References

For Core Web Vitals specific optimizations, see [Core Web Vitals](../core-web-vitals/SKILL.md).
