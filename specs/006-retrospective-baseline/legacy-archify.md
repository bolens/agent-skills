# Archify legacy capability contracts

Dated extension: 2026-09-06. This expands W-005 into the shipped CLI and viewer
capabilities. The authored JSON remains the source of diagram meaning; generated
HTML, browser receipts, image exports, and perceptual judgments are separate
artifacts. The [entrypoint](../../skills/archify/SKILL.md),
[CLI](../../skills/archify/bin/archify.mjs), and
[delivery contract](../../skills/archify/references/delivery-contract.md) own these
interfaces. None of these retrospective mappings changes the imported schema or
claims every internal branch has been executed in this audit.

## LA-001: Five diagram families and authored meaning

| Family | Required observable contract | Implementation |
| --- | --- | --- |
| Architecture | Stable authored nodes, groups and relationships; inspectable compiled layout and optional repository evidence tied to explicit revision/path references. Geometry must not invent topology. | [Renderer](../../skills/archify/renderers/architecture/render-architecture.mjs), [schema](../../skills/archify/schemas/architecture.schema.json) |
| Workflow | Authored workflow semantics compiled into layout; retain supported v1 compatibility, enforce v2 hard contracts and expose diagnosed repair rather than silently changing meaning. | [Renderer](../../skills/archify/renderers/workflow/render-workflow.mjs), [schema](../../skills/archify/schemas/workflow.schema.json) |
| Sequence | Ordered authored actors/messages and readable columns; fit labels and preserve message endpoints/order. | [Renderer](../../skills/archify/renderers/sequence/render-sequence.mjs), [schema](../../skills/archify/schemas/sequence.schema.json) |
| Dataflow | Authored sources, transforms, stores and directed relationships; rendering cannot imply additional causal links. | [Renderer](../../skills/archify/renderers/dataflow/render-dataflow.mjs), [schema](../../skills/archify/schemas/dataflow.schema.json) |
| Lifecycle | Authored states and transitions remain identifiable and retain their meaning in static and trace views. | [Renderer](../../skills/archify/renderers/lifecycle/render-lifecycle.mjs), [schema](../../skills/archify/schemas/lifecycle.schema.json) |

Acceptance includes schema/type failures, stable relationship identity, workflow
compatibility, endpoint/layout failures, and preservation of the authored model.
Fixtures include [workflow hard contracts](../../skills/archify/test/workflow-compiler-hard-contract.test.mjs),
[semantic workflow](../../skills/archify/test/workflow-semantic-contract.test.mjs),
[v1 compatibility](../../skills/archify/test/v1-compatibility.test.mjs),
[sequence fit](../../skills/archify/test/sequence-column-fit.test.mjs), and
[repository evidence](../../skills/archify/test/repository-evidence.test.mjs).

## LA-002: All CLI commands

The CLI accepts the five named types, standard/showcase quality profiles, and
architecture-only repository evidence roots. Unknown command/type/unsupported
options return nonzero. Command-specific output is not a universal validation
receipt; preserve the distinctions below.

| Command | Contract and negative acceptance |
| --- | --- |
| `render` | Invoke the selected renderer and propagate failure; requested output or authored/default path follows the renderer's output policy. This does not independently claim final artifact or visual review. |
| `validate` | Render into disposable storage and run the artifact checker; delete private output after success/failure. JSON includes checks/composition or stage diagnostics. `--layout-json` is architecture/workflow only. |
| `inspect` | Architecture-only alias for validation's layout JSON. Reject other types. |
| `check` | Check the supplied existing HTML through the packaged artifact checker without regenerating it. A nonzero checker remains nonzero. |
| `deliver` | Read specification bytes once, freeze a private same-directory snapshot, render/check those bytes, build specification/artifact SHA-256 and byte-count receipt, then rename the verified candidate. Failure before commit preserves an existing trusted artifact. Recheck output aliases before commit. Optional opening occurs only after success and does not change validation status. |
| `visual-check` | Inspect the exact existing artifact through Chrome's DevTools pipe. Record four desktop containment measurements, light/dark endpoint captures, four PNG sidecars, contact sheet and hash-bound JSON. Exit 0 passed, 1 failed/incomplete, 2 browser unavailable. Always leave perceptual `visualReview: pending`; remove stale image sidecars on failed/skipped capture. |
| `preview` | Explicit opt-in loopback live authoring, watching one input and publishing only stable verified revisions. Invalid/partial/deleted/superseded bytes retain last-good output; identical bytes do not rebuild. No default unattended invocation or remote sharing. Stop owned server/watchers on exit. |
| `compare architecture` | Validate both authored snapshots, canonicalize collection ordering for deterministic geometry, compare stable semantics, and commit HTML plus same-directory sidecar receipt through the paired-output helper. Separate raw hashes/byte counts from semantic hashes and canonical artifact. Reject aliases, invalid inputs, incompatible identities or output/receipt paths. Comparison proof is bounded to authored snapshots and explicitly verified source references. |
| `migrate workflow` | Require distinct source/destination and `--to-schema 2`; compile/validate migrated candidate under the document's durable quality profile, check the artifact, recheck aliases and unchanged source bytes, then replace destination. Failure preserves source and previous destination. |
| `guide` | List scenario recipes or recommend from supplied query; text/JSON and English/Chinese options. Reject unknown options/languages. Recommendations do not change a diagram. |
| `brands` | Query built-in marks by name/alias/domain/category. `capture URL` obtains a digest-pinned brand reference with source/content evidence through the brand module; it is an explicit network operation. Missing built-in matches explain the capture seam. |
| `examples` | Run the packaged examples renderer in the skill root and propagate failure. It writes example outputs and is not a read-only listing command. |
| `doctor` | Check Node >=18, required runtime/references/examples/schemas and callable standalone validators. Report missing/invalid components with nonzero status; readiness does not prove Chrome availability or browser review. |
| `demo` | Render the packaged architecture example into the requested directory as archify-demo.html. Report the path; reject extra arguments or unwritable destination. No automatic publication/opening. |

Argument-array OS opening is separately bounded by five seconds. Unsupported or
failed opening must not invalidate an already committed artifact. Preview state,
local paths/ports, error text and reload tokens must never enter generated HTML or
exports. Delivery validation, browser evidence and perceptual inspection remain
three independent claims.

Acceptance fixtures: [output path](../../skills/archify/test/output-path.test.mjs),
[artifact checks](../../skills/archify/test/render-output-checks.test.mjs),
[repair receipts](../../skills/archify/test/repair-receipt.test.mjs),
[visual checks](../../skills/archify/test/visual-check.test.mjs),
[preview](../../skills/archify/test/preview.test.mjs),
[migration](../../skills/archify/test/workflow-migration.test.mjs), and
[opener](../../skills/archify/test/open-artifact.test.mjs). These cover failed
candidates and preservation, not merely successful rendering.

## LA-003: Viewer exploration and authored relationships

The [viewer runtime reference](../../skills/archify/references/viewer-runtime.md)
contracts these reader-visible operations:

- Guide lists current actions/shortcuts. Reading Depth defaults to READ at 100%,
  reveals FULL at 175%, and uses MAP below 100%; explicit focus/semantic actions
  reveal their exact facts independently of zoom.
- Semantic Lens filters/summarizes kinds without changing authored geometry.
  Intent Trace previews fine-pointer/keyboard targets; Node Finder searches
  labels and stable IDs. Focus opens Semantic Passport with authored facts,
  copyable deep links, explicit close, true outside activation and Escape.
- Semantic Radar mirrors the current viewport and authored graph. Direct
  Relationship Pin requires unique consistent source/target/label/ID metadata.
  Route Probe follows authored directed edges between exactly two endpoints,
  failing closed for conflicts or unreachable routes. Authored reachability is
  not a runtime impact or breakage prediction.

Acceptance: [semantic zoom](../../skills/archify/test/semantic-zoom.test.mjs),
[lens](../../skills/archify/test/semantic-lens.test.mjs),
[intent](../../skills/archify/test/intent-trace.test.mjs),
[passport](../../skills/archify/test/semantic-passport.test.mjs),
[radar](../../skills/archify/test/semantic-radar.test.mjs),
[direct relationships](../../skills/archify/test/relationship-direct-explorer.test.mjs),
and [route probe](../../skills/archify/test/route-probe.test.mjs). Stale reader state
cannot replace authored topology or leak into canonical exports.

## LA-004: Chapters, story, motion and presentation

At most five authored `meta.views` chapters with stable node IDs drive the chapter
rail, delta preview, beat navigator, follow camera, director strip, horizon and
shareable story moments. These controls share that source array. Transitions may
classify only exact adjacent-stop forward/reverse/multiple/grouped relationships;
proximity or order cannot invent a transitive edge or causal verb.

Story playback is reader-started, bounded and stale-safe. Static meaning is the
default; `meta.animation: trace` permits finite Live/Still trace. Still, reduced
motion, page hiding, print and export retain complete static meaning.
Presentation changes chrome/framing, not geometry. Narrow-screen containment is
supported without promising a mobile authoring/presentation product.

Acceptance: [story carrier](../../skills/archify/test/story-carrier.test.mjs),
[beat navigation](../../skills/archify/test/story-beat-navigator.test.mjs),
[follow camera](../../skills/archify/test/story-follow-camera.test.mjs),
[story links](../../skills/archify/test/story-moment-link.test.mjs),
[motion governor](../../skills/archify/test/motion-governor.test.mjs), and
[presentation](../../skills/archify/test/presentation.test.mjs).

## LA-005: Exports and sharing

Canonical export offers full-diagram PNG copy/download, JPEG/WebP download,
dual-theme SVG and trace-enabled WebM. Strip transient Guide, Lens, finder, focus,
route/story/camera/radar/presentation, motion ownership and temporary overlays.
The resulting asset preserves the complete authored diagram.

Optional Share Card produces a 1200×630 PNG in the current theme/preset without
cropping the canonical diagram; clipboard copying uses the same PNG when supported.
Route Share Card consumes a current exact ordered Route Probe snapshot and permits
only static route decoration in its isolated clone. Reach Share Card consumes the
already resolved authored upstream/downstream set without rerunning traversal.
Both specialized cards are download-only and fail closed on stale/conflicting or
empty/unreachable input. Neither becomes the canonical artifact or a validation
receipt. Exports do not create a hosted storage/service boundary.

Acceptance: [share card](../../skills/archify/test/share-card-export.test.mjs),
[route share card](../../skills/archify/test/route-share-card.test.mjs),
[reach share card](../../skills/archify/test/reach-share-card.test.mjs), and
[WebM decode smoke](../../skills/archify/test/webm-artifact.smoke.mjs).

## LA-006: Fork verification and delivery boundary

The [native harness](../../scripts/test_archify.py) fetches the exact audited
upstream revision into disposable storage, overlays the entire local fork,
installs its locked dependencies and runs tests against that overlay. It adapts
only the documented upstream/local release-notice fixture difference, not runtime
behavior. Shard 1 includes generated-source and golden checks; both shards run
selected Node tests with bounded concurrency. Browser mode runs WebM and site
integration serially with Chrome and FFmpeg. Tests must exercise local fork bytes,
not pass against the untouched upstream copy. See
[test_archify_runner.py](../../tests/test_archify_runner.py).

CI selects both shards and browser integration for Archify, runner, provenance,
Makefile or CI changes, and on main/scheduled runs. Its final validation job must
require success for selected jobs and actual skipped status for unselected jobs.
The portable collection gate alone cannot substitute for this suite. Installed
client links must remain untouched by the harness. A release package or upstream
publication is not created by this retrofit.
