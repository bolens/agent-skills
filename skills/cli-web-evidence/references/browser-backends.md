# Browser backend evidence

Use when selecting an alternate engine or attaching to a browser control
endpoint. Keep the repository's harness and required browser matrix authoritative.
Evaluate another backend only for a concrete task benefit, such as constrained
resource use or an engine-specific reproduction.

## Probe effects before collecting evidence

Record the engine, version or audited revision, build capabilities, client, and
transport. A CDP connection through a client named `chromium` does not identify
the server as Chromium. Some implementations acknowledge unsupported methods
to keep clients connected.

Apply relevant emulation settings before navigation when the application reads
them at startup. Then measure their effects in the page. For example, use the
existing harness's evaluation tool to inspect:

```javascript
({
  width: innerWidth,
  height: innerHeight,
  scale: devicePixelRatio,
  reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches,
  dark: matchMedia('(prefers-color-scheme: dark)').matches,
  touchPoints: navigator.maxTouchPoints
})
```

Compare observed values with requested settings. Touch properties alone do not
prove touch interaction. Use the relevant interaction or diagnostic fixture to
establish that capability. Mark unsupported effects unavailable and use the
required browser for that proof. Do not silently relabel a setting as verified.

## Separate output validity from fidelity

For an engine comparison, first establish the same page identity, loaded
resources, application state, scroll boundary, and capture timing in both runs.
Keep viewport, scale, fonts, network fixtures, and motion settings comparable.
An unexpected blank page or login screen, missing required snapshot content,
or failed image makes the capture incomplete rather than a fidelity score.

Inspect structural differences such as box positions, line wrapping, clipping,
and sticky behavior before tuning pixel tolerances. Reduce a discrepancy to a
deterministic fixture and confirm it in the product's supported browsers before
changing application code. Avoid engine- or hostname-specific application fixes
that merely hide a backend limitation.

Validate the output contract separately. A screenshot proves no selectable text
or document structure. A PDF that opens may still lack tags, text, or required
print layout. Requested export options and successful responses are insufficient
when a backend reports ignored options or lacks those capabilities.

## Own the control session

Use a task-owned process or a deliberately assigned remote session. Prefer stdio
for a single local MCP client when supported. Keep local CDP/HTTP endpoints on
loopback. Before sharing an endpoint, establish authentication, session ownership,
and whether clients share tabs, cookies, or active-page state. An Origin allowlist
controls browser callers; it does not authenticate native clients.

Use authorized fixture data. Keep private-network and file-access exceptions
scoped to the test process and intended fixture. A broad private-network switch
does not restrict access to one fixture host. Retain OS isolation for untrusted
page execution and a bounded process deadline in addition to navigation/readiness
limits. Clean up only the owned process and state.

## Obscura assessment

The evaluated source is
[`a1e09de68c7617b8079fbb1661b0548c501971c1`](https://github.com/h4ckf0r0day/obscura/tree/a1e09de68c7617b8079fbb1661b0548c501971c1),
reviewed on 2026-09-05. Recheck changed capabilities before relying on a later
build. This reference does not install or configure Obscura.

At that revision, rendering is a source-build feature, while release archives
include separate rendering and stealth variants. CLI fetch distinguishes raw
response bytes from DOM/JavaScript processing. Its omitted wait uses bounded
adaptive settling, while an explicit wait is a fixed delay. Neither establishes
application readiness by itself.

CDP emulation and diagnostic coverage is partial. MCP element references are
snapshot-scoped, and the HTTP server shares browser state across clients. PDF
output is raster-based. Keep these limits in the evidence receipt. Stealth and
tracker blocking change the tested environment, so enable them only when they
are part of the requested conditions and disclose their effect on comparison.
