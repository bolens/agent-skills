# Verification and limits

## Source walkthroughs

These are manual instruction traces, not independent model invocations or live
application migrations. Each scenario was checked against the final owning path.

| Scenario | Traced decision |
| --- | --- |
| Shell, mise profile, and application file define the same key | Trace the actual launch/loader order with synthetic collisions; record the winning source without secret values |
| Compose interpolation supplies a key without service environment wiring | Do not infer that the application received the key |
| Diagnostic task activates a hook that installs tools | Inspect that wrapper before calling it read-only; keep repairs explicit |
| Existing runtime file survives repeated setup | Bootstrap preserves values and committed pins; updates and reset remain separate |
| Two branches normalize to the same slug | Use a collision-resistant checkout identity, including resources outside Compose's namespace |
| A claimed free port is taken before startup | Bind through runtime allocation or fail/isolate; do not trust a preflight probe |
| Database PID exists but migrations are unfinished | Await the required query/schema behavior within a deadline |
| One of two checkouts fails readiness | Retain bounded logs and stop only its owned resources; the other checkout survives |
| Generator emits a new untracked file | Check the complete owned output set, not only tracked diff |
| Schema contains a default but loader leaves the key absent | Distinguish schema annotation from actual default application |
| CI and developer use different secret providers | Consider optional SecretSpec with one requirement owner and process-scoped runtime injection |
| Provider is unavailable offline | Exercise synthetic failures; do not claim real provider verification or provision accounts |
| User asks for a commit message versus committing changes | Message-only returns wording; parent commit task continues its authorized staging/commit flow |
| Authenticated or hydrated dashboard needs viewport captures | Existing capable harness retains session/readiness and supplies captures; no second helper for receipt format |
| Static unauthenticated page needs initial screenshots | Bundled responsive helper remains available with explicit limits |
| Healthy page, slow LCP image, and slow interaction | Healthy page gains no mandatory hints; other cases route to their measured metric owner |
| Offline ordinary diagram generation | No update-check or notice-cache prerequisite; artifact and browser acceptance remain intact |
| Explicit Archify update discovery | Conditional checker remains available; upstream candidate goes through complete fork review before import |
| Audit drift versus reconcile named files | Audit stays read-only; an already authorized repair proceeds after owner/direction verification |

## Primary sources

Checked for this implementation:
[Compose environment precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/),
[mise environments](https://mise.jdx.dev/environments/),
[devenv processes](https://devenv.sh/processes/),
[SecretSpec integration](https://devenv.sh/integrations/secretspec/),
[JSON Schema annotations](https://json-schema.org/understanding-json-schema/reference/annotations),
[LCP optimization](https://web.dev/articles/optimize-lcp), and
[Chrome prerendering](https://developer.chrome.com/docs/web-platform/prerender-pages).

The moved speculation reference preserves the maintained Chrome eagerness behavior
and conditional cost/side-effect checks. Framework recipes already have metric
references; the entrypoint now selects them by evidence instead of duplicating
unconditional snippets. The existing Archify metadata test follows the moved update reference and retains
all notification assertions. No executable helper or invocation-policy file changed.

## Executed checks

- Edited skill entrypoints passed the skill-creator quick validator.
- The portable gate passed all 95 tests, provenance/syntax checks, and ShellCheck.
- The serialized Archify browser gate passed seven tests and its WebM smoke checks.
- All 121 checked relative links and heading anchors resolved.
- The pinned shared source-lint driver passed JavaScript and Python correctness
  checks; the final run used CI's exact Ruff 0.15.20 and shared tooling revision
  `7603518f305fb76f7bb1b9979f2692521f633b82`.
- The first full Archify run had one metadata-test failure because notice
  instructions moved out of the entrypoint. Its six focused metadata tests pass
  after following the linked reference and preserving all existing assertions.
  The final full rerun passed 1,022 tests with zero failures and four skips:
  the external pinned MCO fixture, a non-Node-22 rejection lane, and two site
  cases covered by the separate serialized browser gate.
No application bootstrap, two-service deployment, real secret-provider setup,
NixOS VM activation, or live field performance measurement was performed. The
request changes skill guidance; those scenario outcomes are source review only.
