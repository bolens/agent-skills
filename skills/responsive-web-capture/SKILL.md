---
name: responsive-web-capture
description: Capture and visually verify local or preview web frontends across reproducible responsive viewport matrices. Use for before/after UI evidence, orientation audits, breakpoint regression checks, and cross-size visual QA; do not use for general web research or production mutations.
---

# Responsive Web Capture

Use the bundled `scripts/capture-responsive.sh` to create initial-viewport PNGs, a TSV inventory, and a JSON run receipt. The wrapper requires Bash, Python 3.9+, and installed Chrome/Chromium on Linux or macOS. ImageMagick is optional for labeled contact sheets. Prefer a repository-native preview server when routing, generated assets, authentication, or a production base path matters. Use `--directory` only for root-mounted static files.

## Choose the matrix

- Use `--matrix quick` while iterating on a known defect.
- Use `--matrix standard` for ordinary responsive verification.
- Use `--matrix comprehensive` when a broad viewport audit is requested. It covers small and modern phones, tablets, laptops, 1080p, 1440p, ultrawide, and 4K, with portrait counterparts.
- Use repeated `--viewport WIDTHxHEIGHT` arguments for a focused regression rerun.

The comprehensive matrix is intentionally expensive. Capture representative routes rather than multiplying every route by every viewport without evidence that the cost is useful.

## Workflow

1. Discover the repository's build, preview, base-path, and browser-test commands. Build generated sites before capture.
2. Capture the baseline before editing when visual comparison matters.
3. Inspect every contact sheet and open suspicious original PNGs. A successful browser exit is not visual proof.
4. After editing, recapture affected viewports during iteration, then run the appropriate final matrix.
5. Run repository-native functional, console/network, and link checks separately. Use `web-quality-audit` for measured performance and accessibility, with `accessibility` or `core-web-vitals` for focused diagnosis. This script proves rendering and dimensions; it does not replace interaction, accessibility, or performance testing.
6. Inspect `receipt.json`: `complete` means all requested PNGs passed dimension checks. A failed capture exits nonzero and retains an `incomplete` receipt plus partial artifacts. Contact-sheet failure is recorded separately and does not discard successful captures. Report the URL, matrix, screenshots, receipt, and skipped coverage.

For sites deployed below a path such as `/project/`, start the repository-native server and pass its exact URL with `--url`. A root-mounted fallback can make absolute assets appear broken even when production is correct.

Keep evidence task-scoped unless the repository defines a tracked visual-baseline location. Use authorized test data and keep sensitive artifacts out of tracked directories.

Record each run's exact path for [temporary evidence cleanup](../git-hygiene/references/evidence-cleanup.md) at feature completion. Preserve requested screenshots, receipts, and visual baselines, then remove disposable task-owned run directories. The helper retains output for inspection and cannot determine feature completion. If handing off before completion, pass the paths and retention needs to the feature owner. Do not delete the shared `visual-evidence` root or another task's runs.

The helper requests reduced motion by default and records that choice. Use `--motion browser-default` to omit the override. Neither mode freezes animations or verifies the actual media-query result. A fixed capture delay is not a deterministic animation phase. Use `web-animation` and the repository's runtime-aware harness when scroll pinning, enter/exit states, or canvas assets need controlled capture. This script's viewport matrix does not prove those behaviors.

## Capture limits and controls

Use the repository's existing harness first when available. This fallback starts a fresh browser profile for every viewport. It does not reuse authentication, drive interactions, wait for hydration/fonts/images, scroll lazy content, assert page identity, or collect page-console/network diagnostics. For those checks and full-page coverage, use [cli-web-evidence](../cli-web-evidence/SKILL.md).

PNG dimensions are output pixels. They do not establish `innerWidth`/`innerHeight`, device emulation, or coverage of another browser engine. The receipt records requested scale and motion settings, not measured application behavior. Keep baseline and comparison settings consistent.

Each run gets a unique directory under `--output/PHASE/NAME/`; the default root is the system temporary directory's `visual-evidence`. Reruns preserve earlier evidence. `--directory` binds a loopback-only server to an automatically assigned port. An explicit occupied `--port` fails rather than reusing another server. This static server has no framework routing or authentication middleware.

`--timeout SECONDS` bounds each browser/contact-sheet command, default 30. `--ready-timeout SECONDS` controls the HTTP probe, default 10. The probe establishes reachability only. Browser processes and the owned server are cleaned up on failure or interruption. `--no-contact-sheet` skips optional montage work. Read browser logs when capture fails. Do not weaken browser sandboxing to make a failed run appear successful.

## Script examples

```bash
scripts/capture-responsive.sh --name docs --directory ./dist --phase before --matrix standard

scripts/capture-responsive.sh --name app --url http://127.0.0.1:4173/project/ --phase after --matrix standard

scripts/capture-responsive.sh --name app --url http://127.0.0.1:4173/ --phase after \
  --viewport 844x390 --viewport 915x412
```
