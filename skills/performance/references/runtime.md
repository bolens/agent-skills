## Runtime performance

### Avoid layout thrashing
```javascript
// ❌ Forces multiple reflows
elements.forEach(el => {
  const height = el.offsetHeight; // Read
  el.style.height = height + 10 + 'px'; // Write
});

// ✅ Batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight); // All reads
elements.forEach((el, i) => {
  el.style.height = heights[i] + 10 + 'px'; // All writes
});
```

### Debounce expensive operations
```javascript
function debounce(fn, delay) {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), delay);
  };
}

// Debounce scroll/resize handlers
window.addEventListener('scroll', debounce(handleScroll, 100));
```

### Use requestAnimationFrame
```javascript
// ❌ May cause jank
setInterval(animate, 16);

// ✅ Synced with display refresh
function animate() {
  // Animation logic
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### Virtualize long lists
```javascript
// For lists > 100 items, render only visible items
// Use libraries like react-window, vue-virtual-scroller, or native CSS:
.virtual-list {
  content-visibility: auto;
  contain-intrinsic-size: 0 50px; /* Estimated item height */
}
```

### Smooth navigations with View Transitions

The [View Transitions API](https://developer.chrome.com/docs/web-platform/view-transitions) lets the browser cross-fade (or custom-animate) between two DOM states using a single GPU-composited snapshot — no double-render, no layout thrash, and the snapshot doesn't count toward CLS.

**Same-document transitions:** Check current support for the actual features used.
```javascript
// Wrap the DOM mutation that swaps the view
function navigate(newView) {
  if (!document.startViewTransition) return swapDOM(newView);
  document.startViewTransition(() => swapDOM(newView));
}
```

**Cross-document transitions:** Verify current engine support separately from same-document transitions; retain ordinary navigation when the enhancement is unavailable.
```css
/* On both source and destination pages */
@view-transition { navigation: auto; }
```
That's the entire integration — same-origin navigations now fade automatically. To opt specific elements into shared-element transitions (e.g. a thumbnail expanding into a hero), give them a matching `view-transition-name`:
```css
.product-thumb[data-id="42"], .product-hero { view-transition-name: product-42; }
```

For predictive loading alongside transitions, see [Speculation Rules](loading.md#resource-loading).
