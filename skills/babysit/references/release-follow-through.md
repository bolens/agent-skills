# Release follow-through

Use the repository's release playbook as the source of truth. Read its referenced workflows and version files before changing them. Do not invent a parallel manual release process.

## Establish what is needed

For an existing or partially published version, reconcile the published artifacts, tag, workflow attempt, and intended source commit before selecting a candidate. Newer default-branch code does not automatically belong to that version.

- Determine whether the PR changes shipped behavior, compatibility, configuration, runtime requirements, or security exposure. Check whether those changes are already included in an unpublished release entry.
- Identify the release unit in a monorepo. Follow its versioning policy rather than bumping every package.
- Determine whether release preparation belongs in this PR, a dedicated release PR, or automation after merge. Check for an existing release PR, tag, or package version to avoid duplicate work.
- Read the required order of version updates, lockfiles, generated files, changelog entries, tests, builds, signing, merge, tag, publication, and deployment. Record which steps are automatic and what triggers them.

Use `changelog-maintainer` for reader-facing release notes. Use `migration` when upgrade or rollback compatibility requires it. A release note should explain observable effects and any required user action, not list internal commits.

## Prepare and execute

Prepare the repository-prescribed release edits, run its release gates, and include the changes in the audit. Inspect the actual package or artifact when the playbook requires packaging checks. Audit publication content with `sensitive-info-audit` before exposure.

Before a merge or release mutation, verify that the reviewed head, required checks, approvals, mergeability, and release target are still current. Carry out already-authorized steps without asking again. When authorization is missing, present the concrete PR, commit, version, destination, and command or workflow that is ready to execute. Complete all independent preparation first.

If the playbook releases automatically after merge, watch that workflow instead of also invoking a manual publisher. If a release job fails, inspect the failure and whether any artifacts were already published before retrying. Do not overwrite an immutable package version, move a public tag, or repeat deployment blindly.

## Verify the outcome

Confirm the tag resolves to the intended release commit. That commit may differ from the PR head after a squash merge or automated version commit. Trace the relationship using the merged PR and release workflow evidence.

Check the release workflow result and the expected publication destination for the exact version and artifacts. Verify signatures, checksums, or installation smoke tests when required by the playbook. Distinguish package publication from deployment and verify each only when it is in scope.

Report what was actually published, its commit and version, verification results, and remaining rollout or approval steps. A successful workflow trigger is not proof of publication.
