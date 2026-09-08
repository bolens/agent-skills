## Critical rendering path

### Server response
* **TTFB < 800ms.** Time to First Byte should be fast. Use CDN, caching, and efficient backends.
* **Enable compression.** Gzip or Brotli for text assets. Brotli preferred (15-20% smaller).
* **HTTP/2 or HTTP/3.** Multiplexing reduces connection overhead.
* **Edge caching.** Cache HTML at CDN edge when possible.
* **Consider Early Hints (HTTP 103) for measured document latency.** If a trace shows slow HTML generation and stable critical subresources, send an interim `103` with `Link` headers before the normal final response from the same request. Use HTTP/2 or later. A CDN may synthesize the `103` from `Link` headers on an earlier `200`, or the origin/edge handler can emit it directly. Unsupported clients continue to the final response, but confirm current browser and infrastructure support. Limit hints to proven critical preloads or preconnects: inaccurate hints waste bandwidth. Cloudflare reported a 20–30% LCP improvement in an artificial, image-heavy test; treat that as a vendor case study, not an expected saving, and measure your result. See [MDN's 103 implementation example](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/103) and [the Cloudflare study](https://blog.cloudflare.com/early-hints-performance/).

### Resource loading

**Preconnect where a critical connection delay is measured:**

Use only origins needed early by the tested route. Verify the request uses that
connection and that speculative connections do not crowd out critical work.
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com" crossorigin>
```

**Preload critical resources:**

Preload only resources whose late discovery is visible in the trace. Each preload competes for bandwidth and an unnecessary high-priority request can delay LCP.

```html
<!-- LCP image -->
<link rel="preload" href="/hero.webp" as="image" fetchpriority="high">

<!-- Critical font -->
<link rel="preload" href="/font.woff2" as="font" type="font/woff2" crossorigin>
```

**Prerender likely-next navigations** with the [Speculation Rules API](https://developer.chrome.com/docs/web-platform/prerender-pages):
```html
<script type="speculationrules">
{
  "prerender": [{
    "where": { "href_matches": "/*" },
    "eagerness": "moderate"
  }]
}
</script>
```
`moderate` waits for a stronger intent signal than eager modes. Measure prediction hit rate, transferred bytes, and server cost; a wrong prerender is roughly an unused navigation. See [measured navigation speculation](../../core-web-vitals/references/navigation-speculation.md) for the tradeoffs and the `prerenderingchange` gating needed for analytics.

**Defer CSS only for an observed blocking cost:**

Use the framework's supported delivery path and preserve its CSP. See
[render-blocking resource guidance](../../core-web-vitals/references/LCP.md#3-render-blocking-resources)
for first-paint, cache, script-failure, and layout checks. An inline `onload`
stylesheet-switch recipe can be blocked by strict CSP; do not relax policy to
make a performance example work.

### JavaScript optimization

**Defer non-essential scripts:**
```html
<!-- Parser-blocking (avoid) -->
<script src="/critical.js"></script>

<!-- Deferred (preferred) -->
<script defer src="/app.js"></script>

<!-- Async (for independent scripts) -->
<script async src="/analytics.js"></script>

<!-- Module (deferred by default) -->
<script type="module" src="/app.mjs"></script>
```

**Code splitting patterns:**
```javascript
// Route-based splitting
const Dashboard = lazy(() => import('./Dashboard'));

// Component-based splitting
const HeavyChart = lazy(() => import('./HeavyChart'));

// Feature-based splitting
if (user.isPremium) {
  const PremiumFeatures = await import('./PremiumFeatures');
}
```

**Tree shaking best practices:**
```javascript
// ❌ Imports entire library
import _ from 'lodash';
_.debounce(fn, 300);

// ✅ Imports only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 300);
```
