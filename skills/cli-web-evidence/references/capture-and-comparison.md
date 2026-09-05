# Capture and comparison

## Whole-page coverage

Use the browser harness's native full-page screenshot when it faithfully represents the document. Before capture, scroll incrementally through the in-scope page to trigger lazy content, wait for observable loading/layout completion, then return to the intended position. Bound both elapsed time and frame/scroll count. Infinite feeds need a stated item or section boundary, not an attempt to reach an ever-moving bottom. [Playwright screenshot modes](https://playwright.dev/docs/screenshots).

Record measured scroll height and viewport dimensions. Native full-page output does not prove lazy content loaded or virtualized items existed simultaneously. Verify sticky elements, nested scroll regions, and canvas content before treating one image as complete coverage.

When native capture distorts the page or hits browser height limits, capture ordered viewport frames with consistent dimensions and 10–20% vertical overlap. Record actual scroll positions, measured heights, frame count, and the stopping boundary. Capture in-scope nested scroll regions separately. Preserve the original frames and make a labeled contact sheet. Do not stitch repeated fixed elements or changing content into a purported pixel-accurate full-page image.

## Visual comparisons

Check tool availability with `command -v`. Prefer ImageMagick's `magick identify`, `magick compare`, and `magick montage`. Use GraphicsMagick's `gm` commands only with its own documented options and metrics.

Compare matching routes, states, dimensions, and rendering conditions. Keep originals beside the diff and record the metric, threshold, and differing region. Do not resize an image to force a passing comparison. Apply any approved masks consistently and report what they exclude. Font rasterization and platform differences can produce pixel noise that requires inspection rather than a larger unexplained tolerance.

For ImageMagick comparison, handle exit status deliberately: 0 means similar under the selected settings, 1 indicates a difference, and 2 indicates an error. A shell using `set -e` must still retain and inspect a difference result. Check the installed version's behavior and the repository's tolerance policy before interpreting a metric. [ImageMagick compare](https://imagemagick.org/script/compare.php).

A contact sheet is a navigation aid. Label each tile with its viewport/state, preserve originals, and open full-resolution images for small text, clipping, or suspicious regions. Report sheet generation failure separately from capture failure.

## Record only when time matters

Prefer browser-controlled traces or recordings for DOM interaction. Use `ffmpeg` for frame extraction, trimming, or transcoding. Use `wf-recorder`, `gpu-screen-recorder`, or `grim`/`slurp` only when Wayland/compositor behavior is part of the evidence. These tools require the relevant desktop session and are not portable browser automation.

Use `vhs` for terminal demonstrations and retain its source tape. Keep recordings short and scoped to the target window or region. Capture audio with `pw-record` only when audio is part of the requested proof. Do not publish recordings without authorization.
