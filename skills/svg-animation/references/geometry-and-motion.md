# Geometry and motion

## Coordinate systems

An SVG transform can resolve against different boxes. Choose deliberately:

- `transform-box: view-box` uses the nearest SVG viewport as the reference box. Inspect nested viewports and transforms before treating an origin as a coordinate in the outer drawing.
- `transform-box: fill-box` uses the object's bounding box, excluding stroke. Pair it with relative origins such as `center`.
- `transform-box: stroke-box` includes stroke extents when the visible outline defines the pivot.

Do not combine `fill-box` with viewBox-coordinate origins. Browser interpolation can pivot around a surprising point, especially for groups with uneven bounds.

For an explicit SVG user-space pivot, a nested group with `transform="translate(cx cy)"`, an inner animated rotation, and artwork centered around the local origin can make ownership easier to inspect. Do not let CSS, a library, and an SVG transform attribute independently write the same transform.

Pointer coordinates are in screen/client space. Map them through the inverse `getScreenCTM()` of the relevant element before using them as local SVG coordinates. Account for a missing or non-invertible matrix. Do not subtract the container's pixel offset and assume that handles viewBox scaling, letterboxing, or nested transforms. [getScreenCTM](https://developer.mozilla.org/en-US/docs/Web/API/SVGGraphicsElement/getScreenCTM).

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

### Path drawing and morphing

For stroke reveals, derive dash lengths from the actual path or use a deliberate normalized `pathLength`. Verify closed paths, caps, joins, and dashed artwork instead of assuming a unit-length recipe fits every path.

Native path-data interpolation requires compatible path structure. Match commands, point order, winding, and subpaths, or use a morphing tool that explicitly handles normalization. A matching count of points alone does not guarantee a useful intermediate shape. Inspect intermediate frames for self-intersections and inverted holes. Keep the original authored geometry, and avoid destructive optimization that breaks morph correspondence. [SVG path data](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/d).

## Paint and containment

SVG paints in document order. Put background paths first, structural shapes next, and moving accents last unless deliberate overlap requires another order. Check `overflow`, masks, filters, and clip paths at the SVG boundary and every nested viewport.
