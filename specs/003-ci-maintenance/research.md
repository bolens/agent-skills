# CI coverage audit

The local top-level inventory found 25 repositories with committed GitHub workflows, covering multiple language and configuration ecosystems. Structural inspection covered 141 workflow files. Presence counts are not compliance or maintenance-status findings. No credential values, private runner inventories, or ignored configuration were read.

## Evidence and decisions

| Evidence | Decision |
|---|---|
| Shared community constitution requires small reusable interfaces, immutable actions, least privilege, and caller compatibility | Make baseline and consumer discovery part of CI implementation |
| Current shared reusable-actionlint.yml provides optional blocking offline security audit with explicit inputs and scoped permissions | Inspect the workflow at the selected ref, including policy switches; do not assume calling lint enables security checks |
| Homelab repository-validation.yml calls native Make targets, with change-based validation and full global invariants | Keep one repository validation contract and test selection for shared changes |
| Homelab workflow-security.yml pins a reusable workflow and enables its security audit | Treat caller input and pin changes as one tested contract |
| Homelab CI separates browser checks and bounded failure artifacts from core validation | Match checks and evidence to the repository rather than imposing one job roster |
| This collection uses make check-fast test portability remotely and installed-symlink checks locally | Document real environment differences instead of weakening gates |
| setup-pre-commit owns local staged checks; babysit owns PR readiness and delivery; systematic-debugging owns cause tracing | Add ci-maintenance for pipeline design and implementation with conditional handoffs |

Shared workflow inspected remotely at community-repository main commit `2e99e898d79a0921d59447073418d9dcd36320e3`. This is audit evidence, not a recommended permanent pin. Local consumer snapshots were inspected as committed implementation examples, not assumed current remote policy. Tool versions must be resolved again for future changes.

Primary platform documentation: [secure use](https://docs.github.com/en/actions/reference/security/secure-use), [workflow reuse](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows). Reusable workflow callers, event trust, and required-check coverage need separate verification. No open question requires a universal scaffold or automatic settings change.
