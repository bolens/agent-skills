# LCP optimization reference

## What is LCP?

Largest Contentful Paint (LCP) measures when the largest content element in the viewport becomes visible. This is typically:

- An `<img>` element
- An `<image>` element inside `<svg>`
- A `<video>` element with poster image
- An element with a background image via `url()`
- A block-level element containing text nodes

## LCP timeline

```
[  Server Response  ][  Resource Load  ][  Render  ]
       TTFB              Download         Paint
       └─────────────────────────────────────┘
                         LCP Time
```

## Detailed optimizations

Select only remedies supported by the measured LCP subpart. A missing CDN or
edge runtime is not itself a defect; preserve cache privacy and the application
rendering contract when considering the examples below.

### 1. Server response time (TTFB)

Target: < 800ms

**Causes:**
- Slow server/database queries
- No CDN/edge caching
- Inefficient backend code
- Cold starts (serverless)

**Solutions:**
```javascript
// Use edge functions for dynamic content
// Vercel example
export const config = { runtime: 'edge' };

// Use stale-while-revalidate caching
// Cache-Control header
res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');
```

### 2. Resource load time

**For images:**
```html
<!-- Discoverable responsive LCP image; choose sizes for the actual layout -->
<img src="/hero-800.webp"
     srcset="/hero-400.webp 400w, /hero-800.webp 800w"
     sizes="100vw" width="1200" height="600"
     fetchpriority="high" alt="Hero">
```

Only add a preload when the trace still shows late discovery. Match the image's
actual `srcset`, `sizes`, format, URL, and fetch mode so the request is reused.
A WebP preload paired with an AVIF-selected `<picture>` can download both formats;
preloading unrelated responsive candidates also wastes bandwidth. Inspect
`currentSrc` and the network trace at the relevant viewports. See
[responsive image preloads](https://web.dev/articles/preload-responsive-images).

**For text (web fonts):**
```css
@font-face {
  font-family: 'Heading';
  src: url('/fonts/heading.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately */
}
```

### 3. Render blocking resources

Prefer the framework's supported CSS splitting/delivery mechanism when a trace
identifies blocking styles. Inline only measured critical rules under the existing
CSP, accounting for cache reuse and HTML growth; 14KB is not a universal budget.
Do not copy an inline `onload` stylesheet switch into a strict-CSP application.
If deferring CSS, verify it still loads with script failure/disabled scripting and
that late styles do not break first paint or cause shifts. Preserve a working
stylesheet path rather than weakening CSP. See [CSP guidance](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP).

**Defer JavaScript:**
```html
<!-- ❌ Blocks parsing -->
<script src="/app.js"></script>

<!-- ✅ Deferred (runs after HTML parsed) -->
<script defer src="/app.js"></script>

<!-- ✅ Module (deferred by default) -->
<script type="module" src="/app.mjs"></script>
```

### 4. Client-side rendering

**Problem:** Content not in initial HTML.

**Solutions:**

**Server-side rendering (SSR):**
```javascript
// Next.js
export async function getServerSideProps() {
  const data = await fetchHeroContent();
  return { props: { hero: data } };
}
```

**Static site generation (SSG):**
```javascript
// Next.js
export async function getStaticProps() {
  const data = await fetchHeroContent();
  return { props: { hero: data }, revalidate: 3600 };
}
```

**Streaming SSR:**
```jsx
// React 18+
import { Suspense } from 'react';

function Page() {
  return (
    <Suspense fallback={<HeroSkeleton />}>
      <Hero />
    </Suspense>
  );
}
```

## Framework-specific choices

Use the installed framework and router's documented image/rendering APIs. Inspect
the emitted HTML and requests; prop names alone do not prove early discovery.

- Next.js: `priority` is deprecated starting in version 16. Choose `loading`,
  `fetchPriority`, or `preload` for the measured cause; do not combine them blindly.
  A `fill` image also needs a sized containing block to reserve layout space.
  See the [Image API](https://nextjs.org/docs/app/api-reference/components/image).
- Nuxt: use its image sizing and loading controls for the actual LCP candidate;
  add `preload` only if discovery is late and verify the selected resource is reused.
- Astro: retain intrinsic dimensions from its image pipeline and prioritize the
  measured LCP resource. Do not force synchronous decoding as a general fix.

The SSR examples above use the Next.js Pages Router API. Match the existing
router; a Suspense boundary alone does not establish that content streams from
the server. Verify the response HTML and loading timeline before claiming SSR
removed the delay.

## Debugging LCP

```javascript
// Identify LCP element
new PerformanceObserver((entryList) => {
  const entries = entryList.getEntries();
  const lastEntry = entries[entries.length - 1];

  console.log('LCP:', {
    element: lastEntry.element,
    time: lastEntry.startTime,
    size: lastEntry.size,
    url: lastEntry.url,
    renderTime: lastEntry.renderTime,
    loadTime: lastEntry.loadTime
  });
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

## Common issues

| Issue | Evidence to confirm | Typical fix |
|-------|---------------------|-------------|
| LCP resource discovered late | Large resource load delay in `LCPBreakdown` or `LCPDiscovery` | Put it in initial HTML, add priority, and preload only when still necessary |
| Large image transfer | Resource load duration and response bytes dominate | Resize/compress and choose an appropriate format |
| Render-blocking CSS | `RenderBlocking` insight and long render delay | Remove unused rules, split non-critical CSS, or inline only proven critical CSS |
| Slow TTFB | `DocumentLatency` insight or LCP TTFB subpart dominates | Cache, reduce redirects, or optimize server work |
| Client-rendered LCP | LCP element absent from initial HTML and render delay dominates | SSR, static rendering, or earlier rendering |

Do not attach generic millisecond savings to these fixes. Measure the relevant LCP subpart before and after under equivalent conditions.
