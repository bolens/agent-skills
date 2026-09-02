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
```

Run `python3 scripts/link-installed.py --apply` to replace configured installed
copies with symlinks to this checkout. The command refuses unexpected targets
unless `--replace` is also supplied.

Changes to third-party skills do not track upstream automatically. Review and
merge upstream changes manually so local behavior is never overwritten.

## Repository map

- `skills/`: canonical hard-forked skills
- `PROVENANCE.json`: machine-readable origin and install-target registry
- `scripts/validate.py`: skill, provenance, syntax, and portability checks
- `scripts/link-installed.py`: idempotent installation symlinks
- `tests/`: repository contract tests
- `.specify/memory/constitution.md`: maintenance rules

Public releases should pass `sensitive-info-audit`, including a history-aware
scanner, before they are pushed.

See [CONTRIBUTING.md](CONTRIBUTING.md) before changing a skill and
[SECURITY.md](SECURITY.md) before reporting sensitive behavior.
