# GitHub Actions event and trust contracts

Inspect the repository's actual triggers, rulesets, runners, and reusable workflow chain. Platform behavior and action runtimes change; verify current documentation for the affected feature.

## Event coverage

Map each enabled event to the source revision, trust level, needed checks, token permissions, secrets, and allowed side effects. Keep PR validation separate from privileged labeling, publishing, or deployment.

`pull_request_target` and privileged `workflow_run` jobs must not check out or execute untrusted PR content. A trusted workflow definition does not make downloaded artifacts or invoked repository scripts trusted. Pass untrusted metadata through quoted arguments or environment variables rather than interpolating it directly into generated shell source. Scope token permissions per job and avoid retaining checkout credentials for validation. See [GitHub secure use](https://docs.github.com/en/actions/reference/security/secure-use).

Review fork and dependency-bot execution separately from same-repository pushes. Missing secrets or token privileges are not a reason to expose them to untrusted code. Do not send public PR code to a persistent self-hosted runner with access to the homelab, Docker socket, credentials, or private network. An ephemeral runner still needs an appropriate network and credential boundary.

Publishing jobs must validate the triggering repository, ref, and artifact provenance. OIDC requires a narrowly scoped identity/trust policy, not just `id-token: write`. Do not execute or publish outputs from an untrusted run merely because a privileged job can download them. Establish the authorized release source and trusted build provenance before promoting an artifact; otherwise rebuild it through the trusted release path. Verify workflow/run identity and commit before using an artifact in a privileged context. Keep evidence uploads bounded, short-lived, and free of env files or credential-bearing logs.

## Required checks and change selection

Inspect required-check names and expected source applications in current settings when available. Preserve them or prepare their explicit migration.

A workflow skipped by path/branch filtering can leave a required check pending. A conditionally skipped job can report success without executing its intended check. If using a required aggregate job, make it run after its prerequisites and explicitly reject their failures or cancellations while distinguishing intentional skips. Do not add an unconditional green job to conceal missing coverage. When merge queues are enabled, required Actions checks need the applicable `merge_group` trigger. See [required-check troubleshooting](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

Test changed-file selection against shared helpers, workflow files, lockfiles, generated inputs, renames, and global configuration. Ensure the comparison revision exists in the fetched history. Do not use an empty or failed diff to skip all work. Avoid event-dependent assumptions about base refs in manual, scheduled, or merge-group runs.

Check the revision actually tested: PR head, test merge commit, and merge-group commit can differ. Do not reuse green status from an older head or interpret cancellation as success. Keep stable, unambiguous check names across matrices and reusable jobs.

## Reusable workflow compatibility

Inspect the called workflow at the exact selected ref, not merely its current default branch. Validate input types and defaults, required inputs, outputs, job dependencies, explicit secrets mapping, and the complete nested call chain. Confirm that the caller grants the permissions the callee needs; nested reusable workflows cannot elevate token permissions beyond the caller. Prefer explicit secret contracts over broad inheritance when practical. See [workflow reuse](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

A local reusable call and an external SHA-pinned call can resolve different revisions during a PR. Confirm which source the representative caller exercises. Test optional policy switches both enabled and disabled where their behavior matters. For a fleet security-audit switch, verify that enabled means a blocking audit actually runs and produces the expected status.

Resolve shared changes at their owning source. Stage compatible consumer updates after the source is available, preserve each repository's gates, and report callers still pinned to old behavior. Do not silently migrate another CI provider or remove repository-specific checks to match a shared example.
