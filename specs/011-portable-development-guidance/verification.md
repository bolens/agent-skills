# Evidence and scenario review

Primary sources checked on 2026-09-07:
[mise CI](https://mise.jdx.dev/continuous-integration.html),
[mise lockfiles](https://mise.jdx.dev/dev-tools/mise-lock.html),
[devenv tests](https://devenv.sh/tests/),
[Dev Container prebuilds](https://containers.dev/guide/prebuild), and
[NixOS VM integration testing](https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html).
The rendered Dev Container metadata page exposed no useful body. Its
[authoritative specification source](https://github.com/devcontainers/spec/blob/main/docs/specs/devcontainerjson-reference.md)
was checked instead. [devenv pinning](https://devenv.sh/pinning/) was also checked.

Manual source walkthroughs:

| Scenario | Expected and traced outcome |
| --- | --- |
| New repository needs Node and linters | Prefer repository mise pins/lock and native commands shared with CI |
| Working devenv project with native dependencies | Retain its Nix inputs and entrypoint; do not add competing runtime ownership |
| Devcontainer Dockerfile changes | Build that image, exercise lifecycle/setup in disposable state, and run the native gate; a separate Nix image is insufficient |
| Untrusted PR changes setup hooks | Inspect executable configuration and preserve CI token/cache/host boundaries |
| Editor invokes pre-commit without shell activation | Use an explicit environment path and verify noninteractive execution without installing on every commit |
| Dependency bot updates an action only | Do not infer mise/devenv lockfile update coverage from action monitoring |
| Single local bug unrelated to setup | Keep the diagnosis scoped; no environment migration |
| Service behavior depends on systemd/network topology | Select a pinned NixOS VM/test with runtime assertions and disposable guest state |
| Pure compiler/toolchain dependency setup | Use the shell/environment; no unnecessary full OS guest |

Host mise tools were installed and version-checked. The repository portable gate
passed through `mise exec -- make check-fast test portability`: 95 tests, no skips,
and host ShellCheck coverage. PR 43's actual devcontainer built and passed smoke
and portable checks using a disposable writable checkout. Its 95-test run skipped
one environment-specific test; this was not represented as full host coverage.

No CI workflow was migrated by this instruction change. No new Nix/devenv or
NixOS VM execution, editor attachment, macOS/Windows, or offline bootstrap test
ran. Review is a local source/scenario walkthrough, not measured invocation
quality or an independent agent evaluation.

Environment-contract source: [Runme implementation](https://runme.dev/blog/substitute-yaml-with-nouns-verbs). Manual walkthroughs cover a new `.env.spec`, an existing consumer requiring `.env.example`, a description-bearing annotated spec that cannot safely become runtime defaults, and schema-backed API/config examples. Guidance selects explicit syntax/validation and coordinated migration while preserving runtime values. No application environment files were migrated in this skills repository.

The full Archify harness passed: 1,022 passing, zero failing, four intentional
skips (external pinned MCO fixture, non-Node-22 rejection lane, and two serialized
site/browser cases). The separate serialized browser gate passed all seven tests
and produced a verified WebM artifact. These are helper regression checks, not
evidence of live NixOS or platform skill execution.
