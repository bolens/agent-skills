# Contributing

See [the delivery playbook](RELEASING.md) for pushing, merging, installation
verification, and recovery.

Edit the canonical copy under `skills/<name>/`. Read its `UPSTREAM.md` before
changing behavior.

## Checks

```bash
make check-fast
make check
```

`make check-fast` validates skill metadata, provenance, and script syntax.
`make check` also runs contract tests, ShellCheck when installed, and verifies
installed symlinks on the maintainer machine.

## Upstream updates

Treat upstream updates as manual merges:

1. Read the upstream release and diff.
2. Import only the intended files.
3. Preserve local instructions and invocation policy.
4. Update `PROVENANCE.json` when the source path or reference changes.
5. Run the full check and describe behavior changes in `CHANGELOG.md`.

Do not present these forks as upstream releases.
