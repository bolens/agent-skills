# Verification

## Manual instruction walkthroughs

These are source-based scenarios, not live agents or activated machines.

| Request and evidence | Result of tracing the instructions |
| --- | --- |
| Fix an Arch service with a packaged unit and an existing config repo | Inspect unit/drop-ins and package/symlink owner; edit managed source, validate, apply only authorized activation, then test service behavior |
| Build a PKGBUILD or recover a failed pacman transaction | Existing package-maintenance or update-recovery remains owner; no duplicated general workflow |
| Change a terminal theme on plain CachyOS with no Omarchy package | Omarchy applicability fails; use the terminal's owner, not Omarchy refresh/restart commands |
| Change CachyOS GPU profile after a kernel update | Query installed chwd interface, map kernel/header/module and boot state, retain known-working recovery and report missing reboot evidence |
| Tune a scheduler with no baseline measurement | Inspect effective policy and owner, measure equivalent workload before recommending a retained change |
| Review a NixOS service edit with pinned flake inputs | Resolve named host and module definitions; preserve lock and stateVersion; evaluation/build do not activate |
| User already requested a specific NixOS switch | Existing authority carries forward after candidate and target verification; no repeated approval ritual |
| Roll back after a service changed its database | Generation rollback and persistent data recovery remain separate, with no claim the database was restored |
| Test a NixOS service topology in a development VM | Reuse pinned modules and isolated guest fixtures; assert behavior after boot; no host switch |
| A Node development shell on macOS | NixOS system trigger does not apply; use existing portable environment guidance |
| Explicit request to reset Omarchy shell | Identify reset scope and backup; existing request supplies authority |

## Executed checks and limits

- New skill quick validators passed for arch-linux, cachyos, and nixos.
- Repository portable gate passed with host mise tools: 95 tests, no skips,
  provenance/metadata/syntax validation, and ShellCheck-backed portability.
- Current host identity was observed as CachyOS. Tool installation and a real
  devcontainer build/smoke/gate were exercised as separate authorized tasks.
- No NixOS evaluator, VM, boot, GPU/driver change, or scheduler trial ran. These
  remain unverified runtime paths. No host-visible invocation trial was run.
- Installed skill links were not repointed. This clone does not own installation.
- Review was a separate local source/scenario pass, not independent agent review.

The full Archify harness passed: 1,022 passing, zero failing, four intentional
skips (external pinned MCO fixture, non-Node-22 rejection lane, and two serialized
site/browser cases). The separate serialized browser gate passed all seven tests
and produced a verified WebM artifact. These are helper regression checks, not
evidence of live NixOS or platform skill execution.
