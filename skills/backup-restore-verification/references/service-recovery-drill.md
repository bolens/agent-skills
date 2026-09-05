# Isolated service recovery drill

Choose a representative service and a recovery point whose application data, database, configuration, and encryption dependencies can be restored together. Record the expected recovery point and the user operation that will prove usability. Reuse the repository's restore playbook and compatible image/database versions. Do not attach recovered data to a live application.

## Establish isolation before starting anything

Use a disposable destination, project identity, data volumes, and network. Inspect the fully resolved deployment privately before starting it. A different Compose project name does not isolate explicit `container_name`, host bind mounts, external volumes/networks, host networking, or production URLs/credentials. Override each shared resource and verify the resulting mount and endpoint identities.

Prevent outbound effects before application startup: production databases, replication, mail, webhooks, scheduled jobs, queues, cloud storage writes, and external identity callbacks. Use test substitutes or an isolated network with only the required test dependencies. Do not rely solely on a feature toggle that may be applied after startup. Restore sensitive data with restrictive permissions and avoid exposing a drill port beyond its intended client.

If needed credentials or dependencies cannot be isolated, perform the remaining offline validation and mark service recovery unproven. Do not use live endpoints just to obtain a green health check.

## Restore and prove usability

Restore database and application state in the documented order. Run native integrity checks, then start compatible isolated dependencies and the application. Record migrations triggered during startup against the disposable copy. A migration on recovered data is not evidence that rollback to an earlier binary remains possible.

Verify connectivity between restored components and perform the chosen representative operation, such as opening a known document, reading an attachment, or a test write/read round trip confined to the drill. Check expected records/files and permissions. A process being healthy or an HTTP 200 login page is insufficient.

Record the selected backup timestamp, usable recovered state, measured restore/startup/verification durations, dependencies or keys still needed, and any expected data gap. Separate the backup's recovery point from the time taken to recover it. Describe sample scope rather than claiming full disaster-recovery coverage.

## Teardown

Inventory resources actually created by the drill. Stop and remove only those disposable resources after recording evidence and within the task's authorized cleanup scope. Never run blanket pruning or volume removal based only on a project name. Confirm production resources were not attached and dispose of recovered personal data according to the agreed retention policy. Preserve concise redacted evidence, not a second uncontrolled backup.
