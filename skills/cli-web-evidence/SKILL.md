---
name: cli-web-evidence
description: Verify websites and web applications through CLI browser automation, screenshots, visual comparisons, and interaction evidence. Use for CLI web capture, visual QA, browser-flow verification, or proof that a web change works. Do not use for general web research or an explicit in-app browser request.
---

# CLI web evidence

Choose the smallest executable check that proves the requested behavior. Preserve inspectable artifacts and distinguish what was asserted, visually inspected, and left unverified.

## Choose the tool and scope

Discover the repository's build, preview, base path, browser tests, and visual baselines. Prefer its existing harness, then installed Playwright, Puppeteer, Cypress, or CDP tooling. Use direct headless Chrome only for simple rendering that needs no authenticated setup, interaction, or application-specific readiness. Reuse dependencies and browser binaries. Install missing tooling only when needed within the authorized task.

When considering another engine such as Obscura, or a remote CDP/MCP endpoint,
read [browser backend evidence](references/browser-backends.md). Protocol
connectivity does not prove rendering, emulation, or diagnostic support. Verify
the required effects and retain the product's supported browsers as acceptance
targets.

For viewport PNGs, use [responsive-web-capture](../responsive-web-capture/SKILL.md). Its helper captures the initial viewport, with reduced motion by default. It does not establish full-page coverage, actual CSS viewport dimensions, application readiness, or mobile-device behavior. Use a scripted harness for those requirements.

Use the in-app browser when explicitly requested, when its authenticated session is essential, or when CLI tools cannot reach the required state. Explain the reason for switching. Do not silently copy the user's browser profile into a test session.

Select representative routes and states before multiplying viewports. During iteration, rerun the affected state and sizes near the relevant breakpoint. Use the requested final matrix once the focused checks pass. Different window sizes in Chromium do not prove Safari, Firefox, touch, high-DPI, zoom, or mobile browser behavior. Exercise those separately when relevant.

## Establish reproducible state

Start the repository-native server in a managed session and retain its logs. Check the intended application identity and exact route/base path. HTTP readiness alone can point at a login page, error shell, stale build, or unrelated server. Stop only processes started for the task.

Install console, page-error, failed-request, and relevant HTTP-response observers before navigation. HTTP 4xx/5xx responses need explicit checks, since they may not appear as failed requests. Attribute failures to the tested path and distinguish expected cancellations from defects. Browser stderr alone is not a page-console or network audit.

Navigate and exercise the user-visible path. Wait with a deadline for the state that matters: hydrated control, loaded data, dismissed loader, decoded image, or completed transition. Check fonts and in-scope image readiness when layout depends on them. `load`, a sleep, or global `networkidle` alone does not prove application readiness. Assert the resulting URL and meaningful DOM state. [Playwright readiness API](https://playwright.dev/docs/api/class-page#page-wait-for-load-state).

For comparisons, hold browser/version, viewport, device scale, theme, locale, test data, scroll position, and motion policy constant. Record relevant differences instead of masking them. Use fresh contexts for independent states, or deliberately reuse a context when testing navigation/session continuity. Keep authenticated test state private and out of tracked artifacts.

With snapshot-based interaction tools, refresh the snapshot after navigation,
tab changes, or DOM-changing actions. Resolve the current target before acting
and assert the resulting state. A previous element reference is not a durable
selector or proof that a click reached the intended control.

## Capture and inspect

Read [capture and comparison](references/capture-and-comparison.md) for whole-page coverage, lazy loading, scroll frames, diffs, contact sheets, or recordings. Use an element or viewport capture when it proves the requested change. Inspect the actual images before declaring visual success. A successful process exit and matching PNG dimensions are insufficient.

Use [svg-animation](../svg-animation/SKILL.md), [web-animation](../web-animation/SKILL.md), or [animation-assets](../animation-assets/SKILL.md) for phase sampling, reduced motion, interruption, and teardown. Reduced-motion or animation-disabled screenshots prove their captured state, not playback or frame cost. Use [web-quality-audit](../web-quality-audit/SKILL.md) when measured accessibility or performance is requested.

Preserve the original baseline and capture each rerun separately. Use repository-defined artifact paths or task-scoped temporary storage. Avoid signed URLs, cookies, tokens, and personal data in receipts, traces, and screenshots. Use authorized test data where possible.

## Report evidence and stop

Report the exact command or test, URL, browser, viewport, relevant emulation/state, assertions, visual inspection result, and artifact paths. Include coverage limits and actionable console/network failures. For multiple captures, keep a receipt beside the originals with completed, failed, and skipped states. Do not infer clean coverage from missing output.

Separate rendering evidence from functional assertions and measured quality. An incomplete capture is not a passing check. Keep partial artifacts for diagnosis and state what remains unverified. Once the requested evidence passes, stop unless a new failure justifies another run.

Before the final handoff, apply [temporary evidence cleanup](../git-hygiene/references/evidence-cleanup.md). Retain requested captures and receipts as deliverables, and remove disposable task-owned runs once the feature is complete. If capture is an intermediate step, hand exact paths and retention needs to the feature owner. Report retained artifact paths rather than links to deleted scratch files.

Website interactions remain within the user's authorized scope. Purchases, publishing, messages, and production-data changes require authorization for that action. Prefer local, preview, test, or read-only paths.
