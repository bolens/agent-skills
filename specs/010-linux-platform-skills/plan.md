# Implementation plan

Create concise `arch-linux`, `cachyos`, and `nixos` entrypoints with conditional
references only where substantial platform procedure warrants them. Verify
current facts against primary project documentation. Write original guidance,
linking sources instead of importing their text or tools.

Narrow `omarchy`, gate related desktop handoffs on the installed platform, and
route Arch upgrade preparation through CachyOS guidance only for its specific
repositories, profiles, or kernel policy. Preserve upstream refs and record the
Omarchy customization in `UPSTREAMS.json`. Regenerate provenance, update README
and changelog, and record the feature in the spec index.

Constitution: canonical source stays in `skills/`; local origins and existing
licenses remain intact; no upstream import, executable wrapper, or installed-link
mutation. Validate with quick skill checks, `make check-fast test portability`,
and manual positive/negative routing and authority scenarios. Live activation,
boot, hardware, and Nix evaluation remain unverified unless actually exercised.
