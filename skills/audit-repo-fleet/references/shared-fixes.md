# Carry a supported fix across the fleet

Use during an active fleet-wide implementation request, or when the user explicitly asks to check maintained peers for the same issue. Keep the current coordinator. A local-only fix or read-only review does not silently become fleet implementation.

## Establish the search boundary

Use the user's maintained-repository inventory, workspace roots, and existing ownership records. Deduplicate linked worktrees and mirrors of the same repository. Distinguish maintained forks from vendored dependencies, archives, examples, and unrelated checkouts. Do not infer that every repository under a home directory is maintained or in scope. If the inventory is incomplete, inspect the known scope and report that limitation.

After confirming a defect or a useful improvement in one repository, record its transferable cause: the affected contract, configuration pattern, helper/template, dependency coupling, or missing validation. An improvement needs a concrete benefit and applicability condition, not merely a preferred style. Search tracked source in the other in-scope repositories for that cause and relevant variants. Avoid ignored runtime files, secrets, broad log dumps, and private endpoint inventories.

For example, a corrected shared workflow input warrants checking callers and copied workflows. A Compose environment fix warrants checking stacks using the same preparation or rendering contract. A runtime-specific dependency fix does not justify upgrading unrelated ecosystems.

## Confirm applicability before editing

Compare each match with its own repository instructions, versions, consumers, generated-file ownership, and tests. Matching text is a candidate, not proof of the same defect. Different versions or intentional local behavior may require a different fix or no change.

When a shared generator, template, library, or reusable workflow owns the issue, fix that source and identify its consumers. Regenerate or update consumers through their normal mechanism. Do not patch generated output or maintained forks indiscriminately. Preserve upstream provenance and declared local changes.

Keep a compact coverage record in the existing task notes:

| Repository or consumer | Evidence | Disposition | Verification |
|---|---|---|---|
| In-scope match | Cause and affected contract, without private values | Fixed, already correct, not applicable, blocked, or deferred with reason | Revision and relevant check, or missing evidence |

Track uninspected repositories separately. Never describe a search miss as verified absence when a layout, branch, missing checkout, or unavailable access prevented inspection. Keep private inventory details out of public PR bodies and commits.

## Implement matching fixes

Within the authorized fleet scope, carry the supported fix to every confirmed maintained match that can be completed safely. Do not stop after the first repository or turn actionable matches into suggestions merely to avoid the remaining work. Reuse evidence and the approach, but adapt the patch to each repository's contract.

Honor explicit exclusions and endpoints. Fleet implementation can authorize repository edits and their required commits across the selected set. It does not automatically authorize pushes, merges, publication, deployments, data migrations, or changes to live services. Carry authority already granted for those actions without asking again. Continue independent repositories when another is blocked.

Use [git-hygiene](../../git-hygiene/SKILL.md) for ownership and isolated writes. Assign one owner to shared sources and generated outputs. Integrate source changes before dependent consumer changes where necessary. Use each repository's focused validation and required gate. Record failures and optional-tool skips per repository rather than substituting one fleet-wide green result.

Use [babysit](../../babysit/SKILL.md) for each target whose requested endpoint includes PR or release delivery. Return its outcome to the fleet coordinator. Keep partial delivery visible and preserve active or unintegrated branches and worktrees.

## Close the batch

Recheck the original cause across the known scope after fixes and regeneration. Include variants discovered during implementation without recursively starting unrelated improvement campaigns. Stop when the selected issue is covered across that scope, with remaining matches explicitly blocked, deferred, excluded, or uninspected and explained.

Report repositories inspected, confirmed matches, completed fixes and revisions, validation, and remaining coverage. Do not claim everything maintained is fixed unless the maintained inventory and all applicable matches were actually covered.
