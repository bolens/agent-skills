---
name: changelog-maintainer
description: Audit, write, and maintain project changelogs and release history. Use when creating release entries, cleaning historical changelogs, deciding whether a change belongs in a changelog, or adding checks that keep changelog prose concise and reader-facing.
---

# Changelog Maintainer

Preserve release facts while rewriting the changelog for people deciding whether to install, upgrade, or change configuration. Read repository guidance, release automation, version sources, and the existing changelog convention before editing.

## Decide what belongs

- Include user-visible features, behavior changes, fixes, removals, compatibility changes, migrations, and security changes.
- Include maintainer or dependency work only when it changes compatibility, supported platforms, release integrity, security, or an operator workflow.
- Omit raw commit scopes, PR numbers, release commits, formatting churn, test-only changes, and routine dependency bumps. Git and GitHub release notes retain that detail.
- Never invent dates, versions, impact, or migration guidance. Resolve them from tags, manifests, release workflows, and the actual diff.

Use [semantic conventions](../git-hygiene/references/semantic-conventions.md) when release numbering is in scope. Check that the proposed version reflects compatibility changes and matches the release unit. Translate semantic commit metadata into reader-facing outcomes without copying type prefixes into bullets. Keep unreleased work under Unreleased until the release process assigns its version and date.

## Write entries

Follow the repository convention when it is coherent. Otherwise use Keep a Changelog categories: Added, Changed, Deprecated, Removed, Fixed, and Security.

Write each bullet as one reader-facing outcome. Name the affected command, setting, platform, or behavior. Prefer present tense for maintained history. Combine implementation details that serve the same outcome. Split unrelated outcomes. Keep breaking changes and required action explicit.

Read [references/style.md](references/style.md) before a broad historical rewrite or when setting repository policy.

## Audit history

Check released sections against tags and release metadata. Preserve factual coverage, but collapse commit inventories into outcomes. Keep old compatibility and migration facts even when their implementation is obsolete. Do not silently reclassify a breaking or security change.

Rank findings by reader impact: misleading or missing upgrade guidance, omitted security or breaking changes, generated commit noise, oversized sections, then minor style drift.

## Keep it maintained

Prefer a small repository-local check that enforces objective structure and residue rules. Do not encode subjective word choices as a brittle linter. A useful check can require the Unreleased section, allowed categories, bounded bullet length and count, HTTPS comparison links, and absence of PR numbers, Conventional Commit markup, emoji headings, and release-automation commits.

Use `scripts/check-changelog.py` as a starting point when its limits fit the repository. Adjust limits to the project instead of deleting important history merely to satisfy the script. Add the check to existing CI and release validation when possible.

For generated changelogs, fix the generator or template first, regenerate, then review the result. Do not hand-edit output that the next release will overwrite.

## Validate and hand off

Run the changelog check, Markdown lint, version-sync check, and release-note extraction relevant to the touched repository. Report rewritten releases, facts intentionally retained, automation added, and any release metadata that could not be verified. Editing a changelog does not authorize tagging, publishing, or rewriting Git history.

When changelog work belongs to requested PR follow-through or release preparation or publication, automatically use [babysit](../babysit/SKILL.md) to coordinate the remaining work, including releases without a PR. Return changelog evidence to an already active workflow. An isolated changelog edit does not start follow-through.
