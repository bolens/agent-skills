# Validate the packaging skill

From the canonical checkout, run `make check-fast` and `make check`. Run the
skill-creator validator for `skills/release-packaging`. Regenerate provenance
through `python3 scripts/update-provenance.py`; install missing links only through
the managed installer. No application or public package is produced by this guide.

Use the skill with bounded hypothetical repositories and record outputs in
`verification.md`:

- A portable Rust CLI with tagged sources/binaries and main builds: assess all
  targets, retain WinGet, avoid pretending Flathub accepts a CLI or nightly feed,
  and distinguish source recipes from binary caches.
- A Python library with native extensions: select PyPI/source recipes, qualify
  wheel ABI/libc targets, and exclude unsupported desktop installer targets.
- A Linux desktop application with a platform-only dependency: assess Flatpak and
  AppImage, keep Flathub nightlies in an owned remote, and mark Windows blocked
  until there is a supported port.
- A binary-only Windows application: use native installers/catalogs, mark source
  variants unavailable, and avoid source-building wrappers that install compilers.
- An artifact with build-tool references, newer glibc symbols, and a required
  dynamic plugin: detect the portability/closure defects and preserve the plugin.
- A changelog-only edit: retain the existing workflow without adding packaging.

These scenarios validate instructions and routing. They do not establish actual
build, install, signing, or store acceptance on any target operating system.
