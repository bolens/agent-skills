# Plan

Use the existing provenance generator and symlink installer. Add optional target
metadata rather than making new client homes mandatory for make check. Keep the
current schema's required install_targets contract and add optional_install_targets.
Use native profile variables. Pi can also consume the existing shared home.

Mirror the seven existing explicit-only policies into SKILL.md frontmatter, retain
fork changes in UPSTREAMS.json, and regenerate provenance. Hermes optional targets
exclude those entries. Do not modify client configuration or install agent runtimes.

Constitution: canonical sources and licenses stay intact. Standard-library Python
and existing Make checks own validation. No upstream revision is advanced.

Source ownership: scripts/link-installed.py, scripts/update-provenance.py,
explicit-only skill metadata, tests/test_client_installation.py, README.md,
docs/client-compatibility.md, generated provenance and pointers.

Follow-through uses a separate opt-in loader harness with pinned dependencies.
No model credentials, persistent client runtime installation, or new native client
homes are needed. Installer auditing remains read-only with bounded catalog walks.
Extend the existing spec before implementation and preserve prior evidence.

The coordination amendment adds a shared PyYAML metadata reader and declares
that dependency in development environments and CI. POSIX directory locks avoid
persistent lockfiles and serialize catalog writers even across separate worktrees.
Check/plan remain read-only. One local owner edits scripts, metadata, CI, and
coordination references and validates their combined state before committing.

POSIX follow-through uses filesystem identities and atomic same-filesystem link
replacement. Keep the existing directory-lock protocol across versions. Add a
macOS CI job using existing pinned setup actions and the focused Make target;
document WSL2 Linux-side setup and filesystem constraints without changing mounts.
