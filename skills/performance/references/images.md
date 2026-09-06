## Image optimization

### Format selection
| Format | Candidate use |
|--------|---------------|
| AVIF | Photographic content when measured quality/size is favorable |
| WebP | Photographic or raster content where its encoding tradeoff fits |
| PNG | Lossless raster graphics when required |
| SVG | Code-native icons and vector illustrations |

Verify current target-engine decoding support and compare actual quality/size. Do not choose formats from static browser-share percentages or generate fallback encodings solely for hypothetical legacy users.

### Responsive images

The multi-format example below is for an explicitly required fallback matrix. When one encoding covers current targets, use that encoding with appropriate `srcset`/`sizes` instead of producing every format.

```html
<picture>
  <!-- AVIF for modern browsers -->
  <source
    type="image/avif"
    srcset="hero-400.avif 400w,
            hero-800.avif 800w,
            hero-1200.avif 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">

  <!-- WebP fallback -->
  <source
    type="image/webp"
    srcset="hero-400.webp 400w,
            hero-800.webp 800w,
            hero-1200.webp 1200w"
    sizes="(max-width: 600px) 100vw, 50vw">

  <!-- JPEG fallback -->
  <img
    src="hero-800.jpg"
    srcset="hero-400.jpg 400w,
            hero-800.jpg 800w,
            hero-1200.jpg 1200w"
    sizes="(max-width: 600px) 100vw, 50vw"
    width="1200"
    height="600"
    alt="Hero image"
    loading="lazy"
    decoding="async">
</picture>
```

### LCP image priority
```html
<!-- Above-fold LCP image: eager loading, high priority -->
<img
  src="hero.webp"
  fetchpriority="high"
  loading="eager"
  decoding="sync"
  alt="Hero">

<!-- Below-fold images: lazy loading -->
<img
  src="product.webp"
  loading="lazy"
  decoding="async"
  alt="Product">
```
