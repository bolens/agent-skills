---
name: cli-web-evidence
description: Verify websites and web applications from the command line using repository-native checks, Chrome or Chromium automation, screenshots, and inspectable evidence. Use for visual QA, responsive checks, browser-flow verification, or proof that a web change works. Do not use for general web research or when the user explicitly asks to control the in-app browser.
---

# CLI Web Evidence

Verify the real website through command-line tooling and leave evidence another person can inspect.

## Tool choice

Prefer, in order:

1. The repository's existing browser tests, screenshot scripts, or visual-regression harness.
2. Its installed Playwright, Puppeteer, Cypress, or Chrome DevTools Protocol tooling.
3. A small Puppeteer script run with the repository's package manager, using an installed Chrome or Chromium executable.
4. Direct Chrome/Chromium headless commands when a scripted interaction is unnecessary.

Do not use the in-app browser-control capability merely because a task involves a website. Use it only when the user explicitly requests it, when an existing authenticated in-app session is essential, or when CLI-driven Chrome cannot reach the required state. Explain that exception when it occurs.

Reuse installed dependencies and browser binaries. Do not add packages, download a browser, or change project configuration unless the task requires it and the user has authorized that change.

## Local evidence tools

This machine has a CLI-first capture and inspection toolchain. Confirm availability with `command -v` before use because packages can change.

- `chromium` and `google-chrome-stable`: headless page rendering, screenshots, print-to-PDF, and CDP targets.
- ImageMagick 7: use `magick` as the primary entry point. `identify`, `compare`, `montage`, `convert`, and `mogrify` are also installed for metadata, visual diffs, contact sheets, conversion, and batch processing.
- GraphicsMagick: use the `gm` entry point when its behavior or performance better fits the task. Do not confuse `gm compare` output with ImageMagick's `compare` command.
- `vhs`: script or record deterministic terminal demonstrations. Keep the `.tape` source beside the generated GIF, WebM, or MP4 when reproducibility matters. Do not use `vhs publish` unless the user asks to upload the recording.
- `wf-recorder`: record a Wayland output or selected geometry when motion, focus, drag-and-drop, or compositor behavior cannot be shown by screenshots.
- `gpu-screen-recorder`: an alternative screen recorder when GPU capture is useful. It may require access to GPU and user configuration outside the sandbox.
- `grim` and `slurp`: capture a Wayland screen or interactively select a region when compositor-level evidence is required.
- `ffmpeg`: inspect, trim, transcode, extract frames, or create a contact sheet from recordings.
- `pw-record`: capture PipeWire audio only when audio behavior is part of the requested proof.

Choose the smallest artifact that proves the behavior. Prefer a screenshot for static layout, a before/after pair plus an image diff for visual changes, a `vhs` recording for terminal flows, and a short screen recording for motion or interaction that still images cannot establish.

## Verification workflow

- Discover the project's start, build, and test commands before inventing a harness.
- Start local servers with the repository's normal command and capture their logs. Keep long-running processes in a managed terminal session and stop only processes started for this task.
- Drive the user-visible path: load the page, perform relevant interactions, and wait for observable readiness rather than arbitrary sleeps.
- Check console errors, failed requests, page errors, target URLs, and important DOM state alongside visual output.
- Exercise the viewport sizes relevant to the task. For general responsive QA, include at least one narrow mobile and one desktop viewport.
- When `responsive-web-capture` is installed, use its reusable script for standard or comprehensive multi-viewport audits. Prefer focused `--viewport` reruns while iterating, then use the requested final matrix. Pass the exact repository-native preview URL when the deployed site uses a non-root base path.
- When quality scores, Core Web Vitals, accessibility, or performance regressions are in scope, use `web-quality-audit` for the measurement plan and this skill for the executable browser evidence. Do not substitute screenshots for those measurements.
- Capture screenshots after the state under review is fully rendered. Use full-page captures for layout review and focused captures when they make a defect easier to see.
- For whole-page visual analysis, capture the page from top to bottom rather than relying on only the initial and final viewport. Prefer the browser tool's native full-page screenshot when it faithfully captures the document. Before capture, scroll incrementally from the top to the bottom to trigger lazy-loaded content, waiting for visible loading and layout shifts to settle, then return to the top.
- When native full-page capture is unreliable, take an ordered series of viewport screenshots from top to bottom. Common causes include sticky or fixed elements, nested scroll containers, virtualized content, canvas-heavy pages, and browser height limits. Use consistent viewport dimensions and 10-20% vertical overlap so no content falls between frames. Capture independently scrollable regions separately when they are in scope.
- Preserve the ordered top-to-bottom frames and create a labeled contact sheet for analysis. Record the page's measured scroll height, viewport height, scroll positions, and frame count so coverage can be checked. Do not stitch overlapping frames into a purported pixel-accurate full-page image when fixed elements, animations, or layout changes would duplicate or distort content; use the contact sheet instead and note the limitation.
- When SVG animation is under review, use the `svg-animation` skill's browser-verification contract. Inspect multiple animation phases and reduced motion; a single screenshot proves only one frame.
- Inspect screenshots visually before claiming success. A successful automation exit code does not prove that the page looks correct.
- Use `identify` to verify screenshot dimensions and format. Use `compare` or `magick compare` only when a reference image and a meaningful tolerance exist. Report the metric and tolerance with the diff artifact.
- Use `montage` to make a labeled contact sheet when several viewports or states must be reviewed together. Preserve the original captures.
- Record with `vhs`, `wf-recorder`, or `gpu-screen-recorder` only when the requested behavior depends on time or interaction. Trim dead time and retain the source tape or exact recording command.
- When visual comparison matters, preserve clearly named before/after images under a temporary evidence directory unless the repository defines an artifact location.

## Evidence standard

Report concise, reproducible evidence:

- exact command or existing test invoked;
- URL and viewport used;
- interaction or state verified;
- screenshot paths;
- whole-page coverage details when applicable: native full-page capture or ordered scroll frames, measured page and viewport heights, scroll positions, overlap, and contact-sheet path;
- diff, contact-sheet, or recording paths when those artifacts add proof;
- relevant console, network, assertion, and exit-code results.

Prefer a small JSON or text receipt next to screenshots when several pages or viewports are checked. Do not claim pixel-perfect or cross-browser coverage unless it was actually measured. Distinguish a rendering check from a functional assertion and note any skipped state that required unavailable credentials, services, or browser binaries.

## Safety and scope

Treat website interaction as an external action: do not submit purchases, publish content, send messages, alter production data, or bypass authentication without explicit authorization. Prefer local, preview, staging, test, or read-only paths. Screenshots may contain secrets or personal data; keep them in task-scoped temporary storage unless the user asks to retain them.
