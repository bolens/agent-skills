# Semantic commits, PR titles, and versions

Default to Conventional Commits for commits and PR titles, and SemVer for
versioned software. Respect explicit repository policies, native ecosystem
constraints, and existing release automation. Do not introduce releases into
an unversioned repository or migrate its version scheme as incidental work.

## Commits and PR titles

Use `type(scope)!: summary`, with scope and `!` optional. Choose `feat` for
new functionality and `fix` for bug corrections. Use the repository's types
for other work, such as `docs`, `refactor`, `perf`, `test`, `build`, `ci`, and
`chore`. Describe the actual outcome, not a desired version bump.

Mark an incompatible change with `!` or a `BREAKING CHANGE:` footer. Preserve
migration details in the body. A breaking change can have any type.
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

Apply the same format to PR titles as this collection's naming default. Write
the title from the complete final diff and revise it when scope changes.
For example, `fix(parser): retain empty fields` or
`feat(config)!: require explicit profiles`. Keep PR descriptions readable prose.

Inspect what the merge strategy and release parser actually consume. Before
squash merge, verify the final commit subject and body retain the intended type,
scope, breaking marker, and migration footer. A valid PR title alone does not
prove the host will generate that message. For retained commits, inspect their
messages too. Do not rewrite published history just to normalize old subjects.

## Release versions

Identify the release unit, previous version, and public compatibility contract.
For stable SemVer, use major for incompatible changes, minor for compatible
features or public deprecations, and patch for compatible fixes. Reset lower
components after a major or minor increment. Evaluate all changes since the
prior release and select the highest required increment.

`feat` normally signals minor and `fix` patch. Other types have no implicit
increment. Breaking markers take precedence. Verify actual compatibility and
configured release rules instead of inferring safety from labels alone.

Follow the documented development policy for `0.y.z`; it is not a stable API
promise. Prereleases such as `2.0.0-rc.1` sort below their matching final release.
Build metadata such as `+sha.abc123` does not increase precedence. A `v` tag
prefix is separate from the version. Never replace published version contents.
[Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

Keep version sources, generated metadata, tags, and release notes synchronized
through existing tooling. In monorepos, honor independent or fixed release units.
Map upstream versions to native package revisions and ordering rules explicitly.
Packaging rebuilds do not automatically change the upstream software version.
Preparing messages or versions grants no authority to publish or merge.
