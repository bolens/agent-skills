# Sentrux local runtime integration

Reviewed Sentrux 0.5.7 at source revision
`f36da08a53e7f06c5b6aec33eb05816b371000ea`. The installed Linux x86_64 binary and
grammar archive match the SHA-256 digests in GitHub release metadata. The exact
values, license hashes, and grammar sources are recorded in
[the runtime provenance](../../skills/audit-repo-fleet/references/sentrux-notices/provenance.json).

## Adopted scope

A locally authored snapshot runner supplies selected source to the existing
binary through Bubblewrap. It includes non-ignored new files without staging the
original index, disables networking, isolates application state, pins runtime
identity, rejects empty baselines, and retains private comparison evidence.
The native product checks remain authoritative. No required CI, daemon, GUI, or
persistent MCP configuration was added.

The private fleet inventory contains 42 non-archived entries. Twenty-six scopes
were tried. Both PowerShell profile copies and two QML products' small helper
scopes produced no import edges and were deferred. The 22 adopted scopes cover
Bash, Python, JavaScript/TypeScript, Go, and Rust. Configuration/documentation
repositories and unsupported Fish/QML/Astro products stay with native tooling.
Forks with distinct source were tested separately. Repository paths, identities,
source snapshots, and per-run logs remain in private local evidence.

The trial used local checkout revisions and detached views of locally available
bare sources. It did not refresh every remote or certify fleet branch freshness.
A passing baseline is a stored measurement, not a passing architectural policy.
Some CLI graph file counts differ from input counts. The CLI does not expose
complete per-file parse success. Dynamic imports, unresolved edges, aliases,
external registration, and generated-source exclusions remain review limits.

## License and distribution boundary

The public [Sentrux license](https://github.com/sentrux/sentrux/blob/f36da08a53e7f06c5b6aec33eb05816b371000ea/LICENSE)
is MIT. Its full notice is retained. However,
[the release workflow](https://github.com/sentrux/sentrux/blob/f36da08a53e7f06c5b6aec33eb05816b371000ea/.github/workflows/release.yml)
builds the official binary with a private `sentrux-pro` crate. The public source
license does not establish the complete binary's redistribution terms.

The [grammar workflow](https://github.com/sentrux/sentrux/blob/f36da08a53e7f06c5b6aec33eb05816b371000ea/.github/workflows/build-grammars.yml)
clones mutable refs, sometimes falls back to a default branch, and packages native
libraries without notices or a source-revision manifest. Seven current upstream
MIT notices were retrieved, retained byte-for-byte, and recorded by Git blob and
SHA-256. They do not prove the exact release build inputs. Redistribution of
binary/grammar assets is excluded pending exact-build attribution and Pro-term
review. This integration uses the owner's installed binary without changing
license state. No activation or license bypass was attempted.

Only the locally authored runner, guidance, prospective feature contract, and
retained license notices enter the skill repository. No upstream implementation,
native library, application binary, grammar archive, or private source is bundled.
Existing skill origins and generated provenance remain unchanged. The runtime's
separate provenance is validated with its retained notices, as applicable to this
external dependency rather than relabeling the entire skill as an imported fork.

## Executed validation

- Eight runner unit tests passed, including invalid archive and missing/modified
  runtime notice/grammar rejection.
- Six real runtime scenarios passed: allowed import, baseline save, unchanged
  comparison, existing-output refusal, forbidden untracked import, and scope mismatch.
- Twenty-two scoped fleet baselines and unchanged comparisons succeeded.
- `make check-fast test portability` passed with socket access needed by existing
  browser fixture tests. Restricted execution first failed those socket fixtures.
- Ruff passed for the new Python code. No workflow or Archify code changed, so
  their separate runtime/workflow suites were not selected.

Use [the runner contract](../../skills/audit-repo-fleet/references/sentrux.md) for
setup, invocation, update review, and coverage limits. The earlier source audit
remains historical evidence and is not rewritten as a current runtime result.
