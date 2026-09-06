# Netviz and Sentrux assessment

Reviewed on 2026-09-05 for selective additions alongside Archify.

| Source | Audited revision | Decision |
| --- | --- | --- |
| [ShadowArcanist/netviz](https://github.com/ShadowArcanist/netviz/tree/0da6124b8093d4d5cd75a191fea1303b3c010b2f), branch `v2` | `0da6124b8093d4d5cd75a191fea1303b3c010b2f` | Keep Archify for diagram generation. Adopt custom-clock guidance in `web-animation`. Defer the editor. |
| [sentrux/sentrux](https://github.com/sentrux/sentrux/tree/6f8ff3c14b0423e4b58f42d1813d4d5f7fdc1d11), branch `main` | `6f8ff3c14b0423e4b58f42d1813d4d5f7fdc1d11` | Adopt structural-evidence guidance in `improve-codebase-architecture`. Defer binary, GUI, and MCP installation. |

## Netviz

The React/Vite application provides manual canvas editing, stored projects,
request-flow animation, and export. Archify already owns agent-authored diagrams,
exploration, motion, and image/video exports. Manual editing is a distinct benefit,
but this task establishes no recurring need for a separate editor and project
format. Vendoring the application would add a second frontend toolchain to maintain.
Reconsider when editable canvas handoff is a concrete requirement that Archify
cannot meet.

Inspected `package.json`, the MIT license, animation clock code, storage,
share UI, and clock tests. This is a focused adoption audit, not a complete
application security review.

- `src/animation/clock.ts` injects a frame scheduler, uses monotonic/timeline
  anchors, samples before rate and direction changes, and cancels pending frames.
  `tests/animation-clock.test.ts` exercises these behaviors. This adds useful
  detail to the existing animation skill's lifecycle and deterministic evidence
  guidance without importing another engine.
- `src/lib/storage.ts` persists snapshots and encodes compressed project data
  into a share URL fragment. The share dialog explains that recipients receive
  an editable copy. Such links carry project content, even though fragment-based
  sharing does not itself require an upload API. No sharing integration was added.
- `package.json` pins a React 18, React Flow, Vite, TypeScript, and Vitest stack.
  The repository supplies an Aube lockfile. No dependency install or full build
  was needed for the adopted guidance.

## Sentrux

Source dependency analysis is distinct from Archify's authored diagrams. Sentrux's
baseline/compare and architectural rules are useful ideas, but its current runtime
needs more work before it fits a predictable local analysis workflow.

| Finding | Source evidence at the audited revision | Consequence |
| --- | --- | --- |
| Startup has side effects before command parsing. | `sentrux-bin/src/main_impl.rs::run` initializes licensing, ensures grammars, syncs plugin files, and starts the update check before `Cli::parse`. | Even a help or analytics command is not a reliable first-launch isolation boundary. |
| Downloaded grammars are native executable libraries without effective declared-checksum verification. | `ensure_grammars_installed` invokes curl and tar. `sentrux-core/src/analysis/plugin/loader.rs::verify_checksum` reads the expected hash and bytes but returns success without comparing them; `load_grammar_dynamic` uses `libloading`. | Do not describe the supplied checksum field as verified integrity. A future integration needs pinned, verified artifacts before loading. |
| Update checks include aggregate usage data by default. | `sentrux-core/src/app/update_check.rs` sends platform, tier, plugin count, scan/MCP/gate counts, file count, and quality score to `https://api.sentrux.dev/version`. An existing `~/.sentrux/telemetry_opt_out` prevents the check. | No source-content upload was observed in this request path, but startup is not offline. No upstream executable was launched in this audit. |
| MCP can check only part of the configured policy. | `sentrux-core/src/app/mcp_server/handlers.rs::handle_check_rules` truncates layers/boundaries when unlimited rules are unavailable and reports `truncated`. CLI `run_check` follows a different path. | A passing MCP response cannot stand for complete configured-rule coverage. Verify the selected interface. |
| A baseline lacks comparison identity. | `sentrux-core/src/metrics/arch/mod.rs::ArchBaseline` stores time and metrics, without repository revision, parser version, or exclusions. Scanner code also applies file/parse limits. | Record identity and coverage separately. Reanalyze both revisions after a tool or scope change. |

The inspected surface also included scanner enumeration, baseline comparison,
the Cargo workspace manifest, build script, and license. The Rust app,
language grammars, Pro library, GUI, and MCP were not built or executed. No claim
of complete vulnerability coverage or measured analysis accuracy is made.

Reconsider runtime integration when a concrete repository needs its dependency
analysis and an isolated trial can prove parser coverage, complete rule execution,
artifact integrity, and controlled startup networking. A headline score is not
sufficient evidence to add a required CI gate or an always-on MCP server.

## Implemented changes and provenance

- `improve-codebase-architecture` now routes dependency/regression questions to
  a structural-evidence reference: comparable baselines, confirmed import sites,
  missing-parser/truncation limits, executable rule fixtures, and a bounded
  handoff to the existing refactor workflow.
- `web-animation` now routes custom transport controls to a playback-clock
  reference: shared playhead, continuity, loop semantics, and scheduler tests.

These are prose refinements within existing capabilities and triggers, using the
normal maintenance workflow. No application, skill, source code, or asset was
copied from either repository. Both root licenses are MIT, copyright 2026
ShadowArcanist and Sentrux respectively. The new prose is locally authored.
Existing `UPSTREAMS.json`, generated provenance, per-skill origins, and install
targets remain accurate and unchanged. Both edited skills already resolve through
managed symlinks, so the guidance reaches the installed collection immediately.

## Validation

- Compiled Netviz's isolated `clock.ts` with the available TypeScript compiler
  and ran a temporary Node assertion harness without installing its dependencies.
  Passed: one scheduled callback, pause/resume excluding paused time, seek/rate/
  direction continuity, a jump across multiple loop periods, and teardown.
  This is clock behavior evidence, not a browser or full application test.
- Manual instruction walkthrough: a scan with missing grammars is inconclusive;
  a higher score with a new forbidden import still fails its contract; changed
  parser versions require compatible rescans. An audit authorizes no refactor.
  A simple hover stays in the existing runtime and does not acquire a custom clock.
- `make check-fast` and `make check` passed: 61 registered skills, 39 tests,
  portability checks, generated provenance, and installed links. The full gate
  ran with local socket access for the existing capture fixtures.
- Skill Creator's `quick_validate.py` passed for both edited skills.
- Full Netviz/Sentrux suites, browser interaction, and Sentrux analysis accuracy
  were not tested. Archify runtime and provenance were unchanged, so its separate
  full runtime suite was not run for these prose changes.
