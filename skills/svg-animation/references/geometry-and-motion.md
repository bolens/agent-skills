# Geometry and motion

## Coordinate systems

An SVG transform can resolve against different boxes. Choose deliberately:

- `transform-box: view-box` makes `transform-origin` coordinates align with the SVG `viewBox`. Use it for a known axle such as `12px 34px`.
- `transform-box: fill-box` resolves the origin against the element's painted bounds. Pair it with relative origins such as `center`.
- `transform-box: stroke-box` includes stroke extents when the visible outline defines the pivot.

Do not combine `fill-box` with viewBox-coordinate origins. Browser interpolation can pivot around a surprising point, especially for groups with uneven bounds.

## Construction rules

- Put fixed contours and moving details in separate groups.
- Draw connected objects around shared coordinates rather than aligning them by eye after animation.
- Keep path endpoints, axle centers, poles, stems, and baselines explicit in the path data.
- Test the icon with animation disabled. Recognition must not depend on a transient frame.
- Keep strokes legible under responsive scaling with a consistent authored stroke width; use `vector-effect="non-scaling-stroke"` only when scaling would otherwise harm the composition.

## Motion patterns

### Rotation around an authored pivot

```css
.wheel {
  transform-box: view-box;
  transform-origin: 12px 34px;
  animation: wheel-turn 4s linear infinite;
}
```

Keep the rotating spokes in `.wheel`; keep the tire and frame outside it when only the spokes should turn.

### Floating or thrown object

Translate and rotate around the object's own bounds:

```css
.disc {
  transform-box: fill-box;
  transform-origin: center;
}
```

Use a small closed motion range. The static position should remain plausible.

### Path travel

Native `<animateMotion>` is appropriate for decorative path travel. Retain the path as static context and hide only the traveler under reduced motion. If path position carries meaning, replace the animation with a visible final-state marker.

## Paint and containment

SVG paints in document order. Put background paths first, structural shapes next, and moving accents last unless deliberate overlap requires another order. Check `overflow`, masks, filters, and clip paths at the SVG boundary and every nested viewport.
