# Security policy

[Documentation](docs/README.md)

Use [GitHub private vulnerability reporting](https://github.com/bolens/agent-skills/security/advisories/new)
for sensitive findings in this collection. Private reporting is enabled for this
repository. Do not put credentials, private configuration, or an exploit that
exposes another user's data into a public issue or pull request.

## What to report

A skill can direct an agent to read files, run commands, invoke tools, or change
external systems. Report instructions or helpers that cross an authorization
boundary, expose private data, destroy unrelated work, or treat untrusted content
as authority. Include dependency and supply-chain findings affecting bundled code.

A useful report includes:

- The affected skill or helper and exact repository revision.
- The triggering request and a minimal reproduction using synthetic data.
- The expected behavior and what actually happened.
- Required tools, permissions, operating system, and runtime.
- The affected trust boundary and likely impact.

Redact tokens, private endpoints, personal paths, and identifying log content.
Describe an exposed credential by type and location rather than including its
value. If a credential was exposed, revoke or rotate it through its provider.
Removing it from the latest file does not remove copies in history or artifacts.

## Upstream and fork ownership

Use the affected skill's `UPSTREAM.md` and [PROVENANCE.json](PROVENANCE.json) to
identify its original project. A local instruction or adaptation may be the
source of a problem even when the skill was imported.

For a vulnerability that also affects upstream, coordinate a report through
that project's private security channel. Preserve the distinction between the
upstream defect and this fork's changes. Do not disclose an unresolved sensitive
report publicly as part of normal upstream synchronization.

## Before sharing changes

Use [sensitive-info-audit](skills/sensitive-info-audit/SKILL.md) on the actual
publication boundary: changed files, generated output, diagnostic attachments,
and the commit history being pushed. Use a history-aware scanner for commits.
A clean working-tree scan does not cover earlier versions.

Keep real environment files, runtime state, private fleet inventories, and
credentials out of examples and reports. Review tool output before attaching it.
Record what was scanned, which checks ran, and any coverage limits without
copying sensitive findings into the public validation receipt.

A passing repository check is not a security audit. Syntax and metadata checks
do not establish that a skill respects permissions or handles untrusted input.
Verify those behaviors when the change affects them.
