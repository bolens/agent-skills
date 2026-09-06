# Upstream

This skill is maintained here as a **hard fork**.

Original project: [https://github.com/cursor/plugins](https://github.com/cursor/plugins)

Tracked branch: `main`

Original path: `pstack/skills/blast-radius`

Last audited reference: `93b00b89ef425a9c1bac0d0b317dfc49c930ac99`

Upstream license: [MIT](LICENSE)

License source: [pstack/LICENSE](https://github.com/cursor/plugins/blob/93b00b89ef425a9c1bac0d0b317dfc49c930ac99/pstack/LICENSE)

Preserve during imports: `agents`

Local changes to retain:
- Keep current invocation policy and agents metadata; do not restore the Cursor-specific disable-model-invocation field.
- Replace unavailable how, why, and arena dependencies with direct history inspection, code-review routing, and a permitted local fallback.
- Preserve read-only assessment boundaries, isolated proof, explicit evidence gaps, and impact/likelihood/confidence separation.

Updates are audited and merged manually. This fork does not track or represent upstream releases.

See [`../../PROVENANCE.json`](../../PROVENANCE.json) for the machine-readable record.
