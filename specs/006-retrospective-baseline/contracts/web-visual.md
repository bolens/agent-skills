# Web and visual workflow contract

Retrospective at `8e51a4f`, recorded 2026-09-05. See [scope](../spec.md).
The [coverage map](../coverage.md) assigns primary owners.

## W-001: Usable interfaces and data state

Preserve intentional visual direction, reusable design tokens, semantic controls,
keyboard/focus behavior, responsive layouts, and progressive enhancement. Forms
and async mutations preserve drafts, submission outcomes, ordering, conflict
recovery, and applicable unsaved-work handling.

Acceptance: a stale response cannot silently overwrite newer intent; validation
errors remain usable by keyboard; a failed mutation preserves recoverable input.

Source: frontend-design, design-system, accessibility, forms-and-data-state,
web-standard.

## W-002: Performance and search evidence

Audit relevant performance, accessibility, SEO, and browser-quality evidence.
Separate field metrics from lab diagnostics and static source from rendered state.
Crawlability, metadata, canonicals, redirects, sitemaps, and indexing policy reflect
the target environment. Optimize measured bottlenecks without losing semantics.

Acceptance: a lab score is not presented as field performance; a preview site does
not inherit a production indexing assumption without inspection.

Source: web-quality-audit, performance, core-web-vitals, technical-seo.

## W-003: Browser and responsive evidence

Record URL, revision, browser, viewport, state, trigger, assertions, and artifacts.
Check actual backend capabilities and rendered outcomes. Capture failures, timeouts,
missing screenshots, and skipped matrix cells remain visible. Isolate owned
servers and processes, preserving requested deliverables during cleanup.

Acceptance: protocol success alone does not prove a screenshot; a wrong-size image
or occupied server port cannot pass the capture helper; interruption cleans owned
processes without deleting another task's evidence.

Source: cli-web-evidence, responsive-web-capture, tests/test_responsive_capture.py.

## W-004: Artwork and animation lifecycle

Keep static SVG geometry, runtime timing, and authored Lottie/Rive asset playback
with their appropriate owners. Define interruption, reduced motion, cleanup, and
geometry invalidation. Custom transport players preserve playhead continuity,
exclude paused time, and bound frame ownership. Prefer an existing suitable engine.

Acceptance: seek/rate/reverse changes avoid discontinuity; repeated mounting leaves
no callbacks; reduced motion preserves usable state; a frozen screenshot proves
appearance at that time but not smoothness or interactive behavior.

Source: svg-design, svg-animation, web-animation and references/playback-clocks.md,
animation-assets.

## W-005: Generated technical diagrams

Archify generates validated standalone explorable HTML with inline SVG for
architecture, workflow, sequence, dataflow, and lifecycle diagrams. It retains
supported themes, trace motion, export formats, geometry validation, and explicit
visual evidence. Real-code claims need source inspection; authored topology alone
is not dependency analysis. Retain bundled third-party notices and source identity.

Acceptance: route a request lifecycle to an appropriate diagram type; invalid
input reports diagnostics; deliver the checked artifact and truthful visual status.
The native suite and browser export checks remain separate from metadata checks.

Source: skills/archify/SKILL.md, its bundled CLI/renderers, scripts/test_archify.py,
tests/test_archify_runner.py, RELEASING.md.

Network versus systems architecture is not a tool split. Archify covers both.
Netviz is a deferred manual canvas/editor option for editable project handoff,
not an installed network-specific skill. Reconsider when that editing requirement
is concrete. Sentrux analyzes source structure and is not a diagram replacement.
