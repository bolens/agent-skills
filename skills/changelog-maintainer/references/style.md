# Reader-first changelog style

A changelog is an upgrade guide, not a commit log.

## Entry test

Keep an entry when a reader may need it to choose an upgrade, understand changed behavior, update configuration, assess risk, or find a fixed problem. Leave internal refactors, formatting, test changes, routine dependency bumps, PR numbers, and release commits in Git history.

## Shape

- Start with the affected behavior or surface.
- State the outcome before the mechanism.
- Use one logical outcome per bullet.
- Name required user action and breaking behavior directly.
- Group security changes under Security and removals under Removed.
- Keep implementation detail only when it explains impact or risk.

## Compression

Combine details that support one outcome. A large release may need several bullets, but category length should reflect distinct reader decisions, not commit count. Twelve bullets per release and 280 characters per bullet are useful defaults, not permission to erase important facts.

## Remove these artifacts

- Conventional Commit scopes such as `*(ci)*`
- PR numbers and bot wording
- emoji category headings
- `Miscellaneous Tasks` and `Other` buckets
- release commits and `[skip ci]`
- dependency version lists without compatibility or security impact
- vague verbs such as “improve” or “enhance” without the changed behavior

## Preserve these facts

- breaking changes and migration steps
- affected versions, platforms, commands, settings, and formats
- security boundaries and mitigated behavior
- removed compatibility or deprecated interfaces
- release dates and comparison links supported by repository evidence
