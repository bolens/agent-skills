---
name: core-web-vitals
description: Optimize Core Web Vitals (LCP, INP, CLS) for better page experience using field and lab evidence. Use when asked to "improve Core Web Vitals", "fix LCP", "reduce CLS", "optimize INP", "page experience optimization", or "fix layout shifts".
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
---

# Core Web Vitals optimization

Targeted optimization for the three Core Web Vitals using field data to identify user impact and browser traces to diagnose causes.

Use [modern web targets](../web-standard/references/modern-targets.md) for current stable feature/version choices and explicit legacy exceptions. Preserve measured behavior across current target engines; do not add old-browser compatibility work without a requirement.

## Measure before optimizing

When a runnable URL is available, read [the performance measurement workflow](../performance/references/MEASUREMENT.md). Prefer this sequence:

1. Check page-level CrUX p75 data, with a clearly labeled origin fallback when page data is unavailable.
2. Record a browser performance trace under stated conditions. With Chrome DevTools MCP, trace summaries can include CrUX alongside the observed lab metrics.
3. Analyze only the insights associated with the failing metric, then inspect the implicated code and resources.
4. Re-run equivalent lab measurements after the fix. Do not claim an immediate field improvement; CrUX and first-party RUM need new user visits.

If only source code is available, identify likely causes but do not claim that LCP, INP, or CLS is failing without runtime evidence.

Use `responsive-web-capture` to check viewport-specific layout after LCP or CLS fixes, and `cli-web-evidence` to replay INP-sensitive interactions. Keep those artifacts beside, but conceptually separate from, metric evidence.

## The three metrics

| Metric | Measures | Good | Needs work | Poor |
|--------|----------|------|------------|------|
| **LCP** | Loading | ≤ 2.5s | 2.5s – 4s | > 4s |
| **INP** | Interactivity | ≤ 200ms | 200ms – 500ms | > 500ms |
| **CLS** | Visual Stability | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |

Google measures at the **75th percentile** — 75% of page visits must meet "Good" thresholds.

---

## LCP: Largest Contentful Paint

Identify the actual LCP element and divide the trace into server response,
resource discovery delay, resource transfer, and render delay. Use
[the LCP reference](references/LCP.md) only for the implicated phase. A slow
image load, delayed text render, and client-only content need different remedies.

Treat recipes as candidates, not acceptance requirements. Add preload only for
observed late discovery; prioritize the actual critical resource and check for
competing downloads. Change CSS delivery, fonts, caching, or rendering architecture
only when the trace supports that change. Preserve correct first paint, layout,
and application behavior, then compare equivalent measurements.

Likely-next navigation optimization is a separate, optional task. Read
[navigation speculation](references/navigation-speculation.md) when that measured
journey warrants it; a healthy page does not need new resource hints or prerendering.

---

## INP: Interaction to Next Paint

INP measures responsiveness across clicks, taps, and key presses during a visit. Diagnose its input delay, processing time, and presentation delay separately; a slow interaction may involve main-thread contention before the handler, expensive application work, or delayed rendering after it.

When field INP is poor or a trace identifies a slow interaction, read [the INP reference](references/INP.md) for trace interpretation, yielding patterns, third-party and rendering causes, a single-session observer, and first-party attribution.

---

## CLS: Cumulative Layout Shift

CLS measures unexpected layout shifts across a page visit. Use field attribution or a trace to identify the shifted node and the trigger; do not assume the visible victim caused the shift.

When field CLS is poor or a trace reports shifts, read [the CLS reference](references/CLS.md) for reserved-space patterns, dynamic content, font and animation fixes, a debugging observer, and a verification checklist.

---

## Measurement sources

| Source | Use |
|--------|-----|
| Browser performance trace (Chrome DevTools MCP: `performance_start_trace`) | Observe one load or interaction and diagnose focused insights; use included CrUX context when available |
| CrUX or Search Console | Prioritize aggregated real-user outcomes at p75 |
| Lighthouse CLI or PageSpeed Insights | Controlled lab fallback when DevTools tools are unavailable |
| First-party RUM | Segment current production experience by route, device, release, and attribution |
| Raw `PerformanceObserver` | Inspect one page session during debugging |

Do not route performance through Chrome DevTools MCP's `lighthouse_audit`; that capability intentionally covers non-performance Lighthouse categories. Do not compare a single lab value directly with a field p75 as if they were equivalent samples.

When adding or reviewing production collection, read [the first-party RUM reference](../performance/references/RUM.md). Prefer the `web-vitals` library because raw browser APIs do not by themselves implement every Core Web Vital's lifecycle and reporting rules.

---

## Apply remedies through the framework's owner

Use the installed framework's documented image, loading, and scheduling APIs for
the measured cause. Read only the relevant metric reference. Verify generated
HTML, request priority, reserved layout space, and the affected interaction; an
image component, dynamic import, or transition API alone does not prove a fix.
Do not disable SSR or add memoization merely to satisfy a generic checklist.

## References

- [Detailed LCP optimization](references/LCP.md) — read when an LCP trace points to discovery, loading, or render delay
- [Detailed INP optimization](references/INP.md) — read when a trace or field attribution identifies a slow interaction
- [Detailed CLS optimization](references/CLS.md) — read when a trace or field attribution identifies unexpected shifts
- [web.dev LCP](https://web.dev/articles/lcp)
- [web.dev INP](https://web.dev/articles/inp)
- [web.dev CLS](https://web.dev/articles/cls)
- [Performance skill](../performance/SKILL.md)
