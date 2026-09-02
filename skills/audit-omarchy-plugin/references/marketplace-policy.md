# Marketplace policy snapshot

Checked against `omacom/omarchy-plugin-marketplace` commit `656958dd158c225dbedc9c07ed10fe54be23689c` on 2026-09-01. Refresh before an approval request because policy, categories, tags, limits, and scanner behavior can change.

Authoritative sources:

- `SUBMISSION.md`
- `VERIFICATION.md`
- `SECURITY.md#automated-security-baseline`
- `scripts/security-baseline-policy.mjs`
- `scripts/security-baseline-scope.mjs`
- `scripts/security-baseline-analysis.mjs`

## Submission structure

A new listing currently requires a public, active, unarchived GitHub repository with one root `manifest.json`, a root README containing installation and removal instructions, a root license file, documented external dependencies, and a globally unique non-`omarchy.*` plugin ID. A root preview is optional and may be PNG, JPG/JPEG, WebP, or AVIF. Preview input is limited to 50 MB and 40 megapixels.

The issue format requires one exact category, one to three allowed tags, six ordered headings, and five checked ownership/safety statements. Read current `SUBMISSION.md` for the live category/tag lists and exact issue text.

## Exact-commit model

New listings use `approved-and-verified`. Existing listings use the verification form for either the recorded `listingValidatedCommit` or a newer full 40-character upstream SHA. Multi-plugin sources are handled source-wide. Mutable upstream installation is not bound to the verified snapshot.

## Automated Security Baseline

At this snapshot:

- baseline version: `3`
- enforcement mode: `selective`
- marker protocol: `4`
- outcomes: `passed`, `review-required`, `needs-fixes`

Finding rules:

- `curl-pipe-shell`
- `cargo-git-unpinned`
- `remote-git-execution-unpinned`
- `sudoers-dangerous-passwordless-command`
- `privileged-process-control-from-shared-temp`

The selectively blocking rules are `sudoers-dangerous-passwordless-command` and `privileged-process-control-from-shared-temp`. Other findings still require exact maintainer review for verified publication under the current selective policy.

Review capabilities:

- `installer`
- `package-manager`
- `privilege`
- `remote-build`
- `bundled-executable-binary`
- `service-management`
- `sudoers-modification`

Scan limits:

- 512 KiB per text file
- 8 MiB relevant snapshot text
- 1,000 relevant files
- 4 KiB probe for oversized executable files
- 256 setup-named binary asset candidates
- 1 MiB total setup-named asset probe budget

The scan includes the root README, recognized script/configuration extensions, executable and relevant extensionless files, setup-like paths, manifest entry points, and referenced sudoers policies. It normally excludes `.github`, coverage, docs, fixtures, node_modules, spec/specs, and test/tests unless an entry point forces inclusion. Manual audit must cover relevant excluded code and runtime behavior.

## Official scanner invocation

This section is for an explicitly requested submission simulation, not every ordinary audit. Prefer an existing current marketplace checkout. If none exists, fetch only the scanner's required source closure when practical; do not download the full repository archive or unrelated site assets solely to obtain the scanner.

The scanner CLI expects validation metadata rather than a local repository path:

```json
{
  "schemaVersion": 1,
  "context": "submission",
  "repoUrl": "https://github.com/owner/repository",
  "commitSha": "FULL_40_CHARACTER_SHA",
  "pluginIds": ["plugin.id"],
  "entryPoints": ["Service.qml"],
  "listedPlugins": [
    {"pluginId": "plugin.id", "manifestPathHint": "manifest.json"}
  ]
}
```

Run from the marketplace checkout:

```bash
node scripts/security-baseline.mjs \
  --metadata=/absolute/path/metadata.json \
  --json=/absolute/path/result.json
```

The command reads the exact public GitHub snapshot and does not execute community code. For a newer listed-plugin update set `context` to `update` and use the configured plugin ID set and manifest hints from the listing. Keep marketplace policy inspection separate from the list of repositories being audited.
