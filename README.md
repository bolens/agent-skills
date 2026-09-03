# Agent Skills

Canonical maintenance repository for the personal Codex and agent skills used by
`bolens`.

Every directory under [`skills/`](skills/) is maintained as a **hard fork**.
[`PROVENANCE.json`](PROVENANCE.json) records its original source, source path,
import target, and fork status. Each skill also contains an `UPSTREAM.md` pointer.

## Maintenance

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
- `scripts/validate.py`: skill, provenance, syntax, and portability checks
- `scripts/link-installed.py`: idempotent installation symlinks
- `tests/`: repository contract tests
- `.specify/memory/constitution.md`: maintenance rules

Public releases should pass `sensitive-info-audit`, including a history-aware
scanner, before they are pushed.

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing a skill and
[SECURITY.md](SECURITY.md) before reporting sensitive behavior.
