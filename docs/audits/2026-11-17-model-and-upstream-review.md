# Skill review for GPT-6.2 and upstream updates

Reviewed on 2026-11-17 against `origin/main` at `fd3126d`. The local
installed checkout started twelve commits behind that revision. The feature
branch uses a separate worktree, so its changes are available for review before
they reach installed clients.

## Skill discovery and instructions

OpenAI lists GPT-6.2 Astra and Sol for Codex. Its skill guidance favors concise
discovery descriptions and conditional references. Its GPT-6.2 guidance
recommends carrying out the authorized task with reasonable assumptions and
stating project-specific conventions where they affect the result.
[Model release](https://openai.com/index/introducing-gpt-6-2-astra-sol/)
· [Skill guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
· [GPT-6.2 prompting guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices)

Reviewed discovery metadata across 66 skill entrypoints and traced selected
overlapping workflows into their instructions and references. Thirteen revised
descriptions went from 4,611 to 1,917 characters combined (58% shorter).
Across all descriptions, the count went from 18,062 to 15,368 (15% shorter).
These are source character counts. Client selection, token use, latency, and
task quality require model runs to measure.

CI guidance starts with the affected workflow, caller, and command. It routes
toolchain and environment work to existing references. Git guidance calls for
ownership coordination when writers overlap and uses a short handoff record
for shared work. Skill names, invocation settings, and provenance pins retain
their existing contracts.

Source walkthroughs checked these routing boundaries:

| Request | Expected workflow |
| --- | --- |
| Change a required CI check, set up a local staged-file hook, or monitor an existing PR | `ci-maintenance`, `setup-pre-commit`, or `babysit`, respectively |
| Review a diff, rank architecture issues across a codebase, or compare two designs for one interface | `code-review`, `improve-codebase-architecture`, or `codebase-design`, respectively |
| Integrate a Rive machine, animate an SVG path, or implement a CSS page transition | `animation-assets`, `svg-animation`, or `web-animation`, respectively |
| Diagnose broad desktop instability, an application core dump, or a dangling config symlink | `workstation-health-triage`, `diagnose-crash`, or `managed-config-drift`, respectively |

Run these prompts without explicit skill names on GPT-6.2 Sol and Astra for
a live comparison. Record which entrypoints the client actually loads, whether
it preserves the requested endpoint, and which checks it completes.

## Tracked remotes

The branch-tip audit resolved all seven remotes for 18 external forks. It
flagged 14 different tips. Comparing each recorded path and license at the
exact revisions found eight changed skill subtrees, five Caveman entries with
license changes alone, and one unchanged subtree and license at a newer tip.

| Upstream tip | Decision |
| --- | --- |
| [Omarchy `4d64235`](https://github.com/omacom/omarchy/commit/4d64235cd8bbe2dac37b4a6fd77b5d77f22f9316) | First import to consider. The crash reporting update targets the new repository owner and calls `omarchy-debug --no-sudo --print` directly for package installs. Review monitor state precedence, `o.rebind`, and plugin safety/localization separately. Keep discovery limited to Omarchy-owned configuration. |
| [Archify `4478129`](https://github.com/tt-a1i/archify/commit/44781293f38728baf04dbad33ce1a0cef8c39cca) | Evaluate 3.2.0 in a dedicated upgrade. Atomic output and recovery, new diagram types, and a combined validation command are worth testing. The subtree diff spans 312 files and adds Apache-2.0 and third-party notices. Verify the monorepo test layout, local icon assets, and the fork's policy of checking for updates only during maintenance or on request. |
| [Caveman `a192894`](https://github.com/JuliusBrussee/caveman/commit/a192894723a8f47e7f504c7b5041967ff1f18e55) | Defer a wholesale import. The root license changes from MIT to Apache-2.0. Voice modes move to new sibling skills and the compressor adds provider routing and out-of-tree backups. Review how credentials, whole-file transmission, validation, and recovery work before considering the compressor changes. |
| [Anthropic skills `e4bb5d9`](https://github.com/anthropics/skills/commit/e4bb5d960d87126ff3b3a8af1a104b7db67560ba) | Keep the local frontend-design workflow. It already covers scoped typography, deliberate motion, interface writing, and real visual checks. Upstream's confirmation step for underspecified briefs and larger process checklist give less room to proceed on reversible assumptions. |
| [Cursor plugins `93b916d`](https://github.com/cursor/plugins/commit/93b916d4a1e806507e22f4716b352fa91f2b227e) | Keep the local blast-radius workflow. Upstream simplifies some wording but retains the arena dependency. The fork already uses direct history inspection, scoped execution evidence, and explicit evidence gaps. |
| [Vercel skills `57217cf`](https://github.com/vercel-labs/skills/commit/57217cf86ba38148a57af9e90d14a4c049558330) | The find-skills subtree and license match their audited versions. |
| [Web quality skills `afa8da9`](https://github.com/addyosmani/web-quality-skills/commit/afa8da942115f2961fdbfa80807ea0b232ff6c00) | All four skills are at their audited branch tip. |

Spec Kit is maintained separately from those forks. The base holds v1.3.3,
and the remote automation branch proposes v1.4.1. Upstream v1.4.2 adds version
provenance to generated skills and improves task field and drift guidance.
Compare its generated output using the existing integration update workflow.
[Spec Kit v1.4.2](https://github.com/github/spec-kit/releases/tag/v1.4.2)

## Theo Browne's tstack

Read all nine entrypoints, the included PR watcher, and the MIT license at
[11e37a7](https://github.com/t3dotgg/tstack/tree/11e37a74d0a6868c121cd0910ab2b3bd9873b92a).
The two adaptations are original local guidance in existing references.

| tstack skills | Decision |
| --- | --- |
| `modernize`, `takeover` | Adopt the supersession check before an old PR is rebased, use range-diff to verify the rebased series, and preserve verified contributor credit across a takeover or squash. Existing Git and delivery rules govern remote updates. |
| `file-pr`, `leaving-pr-comments` | Adopt a problem-first PR description with a short account of the behavioral change and its proof. A fixed attribution callout and an automatic preference for non-draft PRs would cut across repository conventions and user choices. |
| `council`, `sol-loop` | Keep the existing independent, evidence-based reviews. A bounded same-model loop is useful for targeted rechecks, which the existing reference already scopes to changed behavior. A three-provider scoring loop adds provider access, code-sharing decisions, and potentially repeated review rounds. |
| `full-send`, `full-stop`, `babysit-pr` | Retain the existing delivery coordinator and user-selected endpoint. The phrase triggers can be ordinary prose, and the flows can change auto-merge or rewrite a remote branch. The optional watcher assumes specific bots for readiness, caches required-check names during a run, and has no subprocess deadline for `gh` calls. |

## Verification

The portable gate passed with 208 tests passing and one case-insensitive-filesystem
test skipped on Linux. Shell portability checks passed. The canonical link
check found missing links for `arch-linux`, `cachyos`, `internationalization`,
and `nixos` in all three default homes. Those four installation targets are
outside the installed checkout's present link set. No model invocation
benchmark, new upstream runtime test, or live PR workflow was run.
