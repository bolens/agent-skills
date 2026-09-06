# Documentation

Maintained skill sources, fork provenance, and installation pointers.

## Start here

| Need | Owning document |
| --- | --- |
| Use the project | [README.md](../README.md) |
| Change the repository | [AGENTS.md](../AGENTS.md) |
| Deliver or recover | [RELEASING.md](../RELEASING.md) |
| Plan substantial changes | [.specify/memory/project-guide.md](../.specify/memory/project-guide.md) |
| Non-negotiable constraints | [.specify/memory/constitution.md](../.specify/memory/constitution.md) |

## Architecture

Each skill owns its invocation boundary and procedure. References carry conditional detail, and
scripts carry executable behavior. [CONTRIBUTING.md](../CONTRIBUTING.md) owns maintenance and
generation. [UPSTREAMS.json](../UPSTREAMS.json) records audited revisions and local changes, while
[PROVENANCE.json](../PROVENANCE.json) and per-skill upstream pointers are generated.

## Deployment and recovery

[RELEASING.md](../RELEASING.md) separates source delivery from installation. Installed directories
point into the canonical checkout. An isolated worktree can validate source but cannot prove that
those installed links target it. Do not repoint installations to make a worktree check pass.

## Database and state

There is no application database. Preserve provenance and local customizations during imports. Dated
[audits](audits) describe the revision they inspected, while active behavior belongs in the owning
skill and its tests.

## Documentation maintenance

Keep decisions, invariants, failure modes, and recovery requirements in the owning document. Link to
commands, defaults, schemas, and generated catalogs instead of copying them. Change the owner and
affected references together. Update this index when adding or moving a guide, and verify relative
links and heading anchors. Historical specs and audits describe their recorded revision, not current
runtime proof. A topic without an implementation stays explicitly unimplemented.

## Topic guides

- [Contributing](../CONTRIBUTING.md)
- [Security policy](../SECURITY.md)
- [Development environments](development-environments.md)

- [Editor setup](../.vscode/README.md)
