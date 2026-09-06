---
name: accessibility
description: Audit and improve web accessibility following WCAG 2.2 guidelines. Use when asked to "improve accessibility", "a11y audit", "WCAG compliance", "screen reader support", "keyboard navigation", or "make accessible".
license: MIT
metadata:
  author: web-quality-skills
  version: "2.0"
---

# Accessibility (a11y)

Comprehensive accessibility guidelines based on WCAG 2.2 and Lighthouse accessibility audits. Goal: make content usable by everyone, including people with disabilities.

## Evidence-led audit workflow

When a rendered page is available:

1. Run a live Lighthouse Accessibility audit when that capability is available; with Chrome DevTools MCP, use `lighthouse_audit`. Use mobile navigation mode for a general public page or snapshot mode when reloading would lose authenticated or user-created state.
2. Use failed audit nodes to localize the relevant component or template instead of searching the whole repository for generic patterns.
3. Inspect a rendered accessibility-tree snapshot for names, roles, states, landmarks, and heading structure; with Chrome DevTools MCP, use `take_snapshot`. Exercise the affected flow with the keyboard.
4. Fix the source, then re-run the same audit and manual interaction.

If the live tools are unavailable, use Lighthouse CLI or axe for automated coverage and complete the same manual checks. Automated tools detect only a subset of accessibility barriers: a score of 100 is not WCAG conformance, and a low score does not replace issue-level evidence.

Use `responsive-web-capture` to verify orientation, reflow, zoom-adjacent narrow layouts, focus visibility, and target spacing across the requested matrix. Use `cli-web-evidence` to record keyboard and interaction flows. Screenshots cannot prove accessible names, focus order, announcements, or keyboard operability.

Use `svg-animation` when an accessibility defect depends on animated SVG geometry or motion; retain this skill's ownership of semantics, keyboard access, and WCAG evaluation.

Use `web-animation` for GSAP, Motion, or other runtime-specific reduced-motion and focus/exit fixes. Use `animation-assets` for Lottie/Rive playback and semantic fallback. Use `design-system` when the defect belongs to shared component states or tokens rather than one page.

## Read the reference for the observed issue

Read only the relevant references for a narrow fix. For a full audit, cover
each requested category and report any unverified checks.

| Issue or task | Reference |
| --- | --- |
| Conformance scope and principles | [WCAG Principles: POUR](references/principles.md) |
| Names, text alternatives, contrast, and media | [Perceivable](references/perceivable.md) |
| Keyboard access, focus, targets, timing, and motion | [Operable](references/operable.md) |
| Language, navigation, forms, and authentication | [Understandable](references/understandable.md) |
| ARIA roles, states, and live announcements | [Robust](references/robust.md) |
| Audit tools, manual checks, and issue prioritization | [Testing checklist](references/testing.md) |
