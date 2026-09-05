# Source audit and decisions

Scope: committed homelab source only. No ignored runtime configuration, secret values, host inventories, environment dumps, or Docker daemon queries were read. Structural inventory found 215 Compose definitions and 217 stack metadata records. Counts describe source coverage, not deployed services.

| Evidence in the audited repository | Existing coverage | Decision |
|---|---|---|
| AGENTS.md, CONTRIBUTING.md, documents/STACK-METADATA.md require Compose, examples, preparation, metadata, and ingress to change together | Triage diagnoses outages, but excludes repository-only work | Add homelab-stack-maintenance |
| documents/PREPARATION-STANDARDS.md and scripts/prepare-stack-lib.sh define config copying, environment synchronization, and external resource creation | Triage mentions preparation but does not classify it as a mutation | Inspect helpers before execution, preserve config and shared resources |
| scripts/validate-compose-config.py stages public examples, rewrites env-file paths, and skips generated bundles | No skill explains what that rendering proves or omits | Add focused example-validation guidance and require accurate skip/normalization reporting |
| Makefile and scripts/validate-monitoring-config.sh contain container-based validators, private-path branches, reloads, and combined iterate targets | Generic read-only advice can misclassify compound helpers | Trace helper commands and separate validation from operational effects |
| AGENTS.md prohibits reading ignored runtime config and masking missing remote mounts | Triage requests resolved config without a collection boundary | Respect local prohibitions before collection, filter permitted evidence, preserve mount failures |
| CONTRIBUTING.md and generator scripts assign separate catalog, topology, diagram, and Pages sources | No stack-maintenance owner | Regenerate only affected outputs from their own source and inspect the diff |
| Existing backup recovery reference checks shared Compose resources and outbound effects | Already covered | Reuse backup-restore-verification, add no duplicate recovery skill |
| Existing network and dependency skills cover allow/deny probes, image candidates, digest alignment, and release authority | Already covered | Route selected changes, add no broad replacement skill |

Use repository contract names as examples rather than hardcoding a user's filesystem, domains, addresses, or deployment topology. A new monitoring skill is not justified by this audit alone. There was no live outage or runtime effectiveness test.

Docker documents shell and env-file interpolation and Compose rendering. Keep secrets out of both success output and error output. Sources: [interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/), [config](https://docs.docker.com/reference/cli/docker/compose/config/).

Interconnection decision: maintenance routes to triage, dependency updates, exposure, backups/migration, drift, sensitive audit, Git hygiene, and delivery only at the named boundary. Triage, exposure repair, and dependency transitions route back when committed stack contracts change. Keep the current coordinator and evidence across handoffs.
