---
name: responsive-web-capture
description: Capture and visually verify local or preview web frontends across reproducible responsive viewport matrices. Use for before/after UI evidence, orientation audits, breakpoint regression checks, and cross-size visual QA; do not use for general web research or production mutations.
---

# Responsive Web Capture

Use the bundled `scripts/capture-responsive.sh` to create dimension-checked PNG evidence and a machine-readable receipt. Prefer a repository-native preview server when routing, generated assets, authentication, or a production base path matters. Use `--directory` only for root-mounted static files.

## Choose the matrix

- Use `--matrix quick` while iterating on a known defect.
- Use `--matrix standard` for ordinary responsive verification.
- Use `--matrix comprehensive` for full-site audits, final validation, or broad device coverage. It covers small and modern phones, tablets, laptops, 1080p, 1440p, ultrawide, and 4K, with portrait counterparts.
- Use repeated `--viewport WIDTHxHEIGHT` arguments for a focused regression rerun.

The comprehensive matrix is intentionally expensive. Capture representative routes rather than multiplying every route by every viewport without evidence that the cost is useful.

## Workflow

1. Discover the repository's build, preview, base-path, and browser-test commands. Build generated sites before capture.
2. Capture the baseline before editing when visual comparison matters.
3. Inspect every contact sheet and open suspicious original PNGs. A successful browser exit is not visual proof.
4. After editing, recapture affected viewports during iteration, then run the appropriate final matrix.
5. Run repository-native functional, console/network, and link checks separately. Use `web-quality-audit` for measured performance and accessibility, with `accessibility` or `core-web-vitals` for focused diagnosis. This script proves rendering and dimensions; it does not replace interaction, accessibility, or performance testing.
6. Report the URL, matrix, screenshots, receipt, contact sheet availability, and any skipped browser/tool coverage.

For sites deployed below a path such as `/project/`, start the repository-native server and pass its exact URL with `--url`. A root-mounted fallback can make absolute assets appear broken even when production is correct.

Keep evidence task-scoped unless the repository defines a tracked visual-baseline location. Do not capture authenticated pages containing secrets or personal data without confirming the storage location and scope.

For animated pages, record whether motion is running, reduced, or frozen. A fixed capture delay is not a deterministic animation phase. Use `web-animation` and the repository's runtime-aware harness when scroll pinning, enter/exit states, or canvas assets need controlled capture. This script's viewport matrix does not prove those behaviors.

## Script examples

```bash
scripts/capture-responsive.sh --name docs --directory ./dist --phase before --matrix comprehensive

scripts/capture-responsive.sh --name app --url http://127.0.0.1:4173/project/ --phase after --matrix standard

scripts/capture-responsive.sh --name app --url http://127.0.0.1:4173/ --phase after \
  --viewport 844x390 --viewport 915x412
```
