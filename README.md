# Agent Skills

Canonical maintenance repository for the personal Codex and agent skills used by
`bolens`.

Every directory under [`skills/`](skills/) is maintained as a **hard fork**.
[`PROVENANCE.json`](PROVENANCE.json) records its original source, source path,
import target, and fork status. Each skill also contains an `UPSTREAM.md` pointer.

## Maintenance

Repository maintenance scripts require Python 3.9 or newer. Node.js 18 or newer
is required to validate the bundled Archify fork. Bash is required only by
skills whose runtime workflows use Bash.

```bash
make check-fast
make check
python3 scripts/link-installed.py --check
python3 scripts/audit-upstreams.py
```

Run `python3 scripts/link-installed.py --apply` to replace configured installed
copies with symlinks to this checkout. The command refuses unexpected targets
unless `--replace` is also supplied.

The managed global roots cover these clients:

- `~/.codex/skills`: Codex
- `~/.agents/skills`: Cursor, Gemini CLI, GitHub Copilot CLI and app, OpenCode,
  Windsurf, and other Agent Skills compatible clients
- `~/.claude/skills`: Claude Code and the Claude Agent SDK

Set `CODEX_HOME`, `AGENTS_HOME`, or `CLAUDE_HOME` to override a root. The shared
Agent Skills root avoids duplicate client-specific trees such as
`~/.cursor/skills`, `~/.gemini/skills`, and `~/.config/opencode/skills`.

Changes to third-party skills do not track upstream automatically. Review and
merge upstream changes manually so local behavior is never overwritten.
Exact audited commits and local overlays live in [`UPSTREAMS.json`](UPSTREAMS.json).
A weekly read-only workflow reports when a tracked branch advances; it never
merges upstream content.

## Repository map

- `skills/`: canonical hard-forked skills
- `PROVENANCE.json`: machine-readable origin and install-target registry
- `UPSTREAMS.json`: tracked branches, audited commits, and local changes to retain
- `scripts/validate.py`: skill, provenance, and syntax checks
- `scripts/check-portability.py`: portable-path, shebang, line-ending, and
  ShellCheck validation
- `scripts/link-installed.py`: idempotent installation symlinks
- `tests/`: repository contract tests
- `.specify/memory/constitution.md`: maintenance rules

Contract tests check that inline local links in skill entrypoints resolve. They
do not verify remote URLs or section anchors.

## Concurrent repository work

Use [git-hygiene](skills/git-hygiene/SKILL.md) alongside implementation skills when
multiple agents write across repository surfaces. It covers worktree isolation,
file ownership, a single Git writer for shared checkouts, focused staging, and
validation after integration. Shared lockfiles and generated outputs need explicit
owners even when agents edit different packages. Post-merge branch cleanup lives
in this skill alongside local worktree cleanup.

## Review workflows

Use [code-review](skills/code-review/SKILL.md) to trace a diff through affected
callers, contracts, failure paths, tests, and delivery boundaries. Its review
receipt identifies the actual revisions, evidence, and remaining coverage gaps.
Substantive PRs use independent agents with distinct relevant focuses when
available and permitted.
[caveman-review](skills/caveman-review/SKILL.md) compresses the findings while
preserving that review depth. [babysit](skills/babysit/SKILL.md) carries findings
and coverage through authorized PR or release follow-through, addressing nits
from every independent review and recording each disposition.

## Web and design workflows

| Task | Skill |
|---|---|
| Page composition and visual direction | [frontend-design](skills/frontend-design/SKILL.md) |
| Shared tokens, themes, variants, and component states | [design-system](skills/design-system/SKILL.md) |
| Form submission, autosave, optimistic state, and data races | [forms-and-data-state](skills/forms-and-data-state/SKILL.md) |
| Native controls, platform semantics, HTTP, and browser compatibility | [web-standard](skills/web-standard/SKILL.md), including its browser-native reference |
| Authentication, authorization, sessions, and untrusted input | [web-security](skills/web-security/SKILL.md) |
| Crawlability, metadata, canonicals, and optional agent discovery | [technical-seo](skills/technical-seo/SKILL.md) |
| Static vector artwork and reusable icons | [svg-design](skills/svg-design/SKILL.md) |
| Moving SVG geometry, pivots, strokes, and morphs | [svg-animation](skills/svg-animation/SKILL.md) |
| GSAP, Motion, native transitions, and other interface motion | [web-animation](skills/web-animation/SKILL.md) |
| Lottie/dotLottie and Rive asset integration | [animation-assets](skills/animation-assets/SKILL.md) |
| Browser interaction and responsive visual evidence | [cli-web-evidence](skills/cli-web-evidence/SKILL.md), [responsive-web-capture](skills/responsive-web-capture/SKILL.md) |

Runtime-specific references are loaded only for the selected stack. Existing
packages, component conventions, and requested formats take precedence over
adding or migrating frameworks.

## Media, packages, and operations

| Task | Skill |
|---|---|
| Audio/image/video preservation, archive utilities, and batches | [media-preservation](skills/media-preservation/SKILL.md) |
| PKGBUILDs, local patches, clean builds, and pinned rebuilds | [arch-package-maintenance](skills/arch-package-maintenance/SKILL.md) |
| LAN/WAN/VPN reachability, firewalls, Docker, DNS, and TLS | [network-exposure-verification](skills/network-exposure-verification/SKILL.md) |
| Quickshell/QML component and plugin implementation | [quickshell-development](skills/quickshell-development/SKILL.md) |
| Backup validation and isolated application recovery drills | [backup-restore-verification](skills/backup-restore-verification/SKILL.md) |
| PR follow-through or standalone release preparation/publication | [babysit](skills/babysit/SKILL.md) |

Related review, repair, maintenance, and verification skills automatically use
`babysit` when the requested endpoint includes PR follow-through or release
preparation or publication. Local-only work and one-off audits keep their scope.
Automatic selection does not grant push, merge, or publication authority.

Public releases should pass `sensitive-info-audit`, including a history-aware
scanner, before they are pushed.

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing a skill and
[SECURITY.md](SECURITY.md) before reporting sensitive behavior.
