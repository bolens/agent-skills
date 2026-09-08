## Font optimization

Choose font behavior from measured text-render delay and layout shifts. `swap`
can expose fallback-metric shifts; compare fallback metrics and the supported
font-display choices. Preserve all supported scripts when subsetting; the Latin
range below is illustrative, not a default for multilingual applications.

### Loading strategy
```css
/* System font stack as fallback */
body {
  font-family: 'Custom Font', -apple-system, BlinkMacSystemFont,
               'Segoe UI', Roboto, sans-serif;
}

/* Prevent invisible text */
@font-face {
  font-family: 'Custom Font';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* or optional for non-critical */
  font-weight: 400;
  font-style: normal;
  unicode-range: U+0000-00FF; /* Subset to Latin */
}
```

### Preloading critical fonts

Preload only a face needed by the initial viewport when discovery delay is
measured. Match URL, format, and fetch mode; verify reuse rather than a second
download, and check that fonts do not delay the LCP image.
```html
<link rel="preload" href="/fonts/heading.woff2" as="font" type="font/woff2" crossorigin>
```

### Variable fonts
```css
/* One file instead of multiple weights */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2-variations');
  font-weight: 100 900;
  font-display: swap;
}
```
