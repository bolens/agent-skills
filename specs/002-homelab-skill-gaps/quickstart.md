# Validation scenarios

1. Add a required key and external volume: update Compose, examples, preparation, metadata, and documentation. Confirm the example renderer cannot read a live env file.
2. Change only an image pin: use dependency triage and maintain affected stack contracts without starting deployment.
3. A preparation wrapper creates a directory and network: inspect it as a mutator, exercise only a temporary fixture with a stubbed runtime, and preserve existing config on repetition.
4. A validation alias also reloads monitoring: use its read-only subset or report a limitation.
5. A metadata lifecycle says externally generated: preserve that contract and report a skipped render, not a healthy service.
6. A mount directory is absent: do not create it to make health checks pass. Distinguish the expected remote filesystem from a local directory.
7. Local guidance prohibits reading ignored config: do not run default Compose rendering, inspect Env, or scan ignored files. Continue against public examples and report unavailable runtime evidence.
8. A backend port changes: align the container port, ingress upstream, metadata, health check, and docs. Do not publish the port just to make it reachable.
9. A shared helper changes: broaden validation to its consumers and regenerate affected outputs from their respective sources.
10. A reviewer wants ordinary application Docker development: do not select the homelab workflow solely because a Dockerfile exists.

Run skill quick validation, make check-fast, and make check. Scan new and changed artifacts with the sensitive-info audit and reviewed history with a redacting scanner. Keep test output aggregate or sanitized.

## Evidence, 2026-09-05

Manual source walkthrough covered all ten scenarios. An independent agent evaluated two compound scenarios covering a required environment key, bind-backed data, prohibited live env reads, environment mirror ownership, preparation effects, container-based validation, absent generated includes, an image-related incident, ingress changes, and a narrowed repository-readiness endpoint. It found no substantive defect. Its clarity nit was addressed by explicitly stopping live incident work when the endpoint becomes repository readiness.

Skill quick validation and make check-fast passed. Full make check passed all 26 tests, portability, provenance, and installed symlink verification. The new skill's three managed client links were installed. These checks verify the skill collection, not the homelab runtime. No operational helper was executed against the homelab.

Sensitive-info audit of the 16 changed/new artifacts reported zero secrets, zero privacy indicators, zero skips. Gitleaks scanned the same artifact fixture with no findings. Only committed homelab source and structural counts informed the audit. No ignored live files, environment values, private deployment inventory, or container data were collected.
