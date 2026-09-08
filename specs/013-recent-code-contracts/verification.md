# Acceptance evidence

**Assessment date**: 2026-09-08
**Assessed source**: `72ec45220597b16a38e2ee842821f4af96b36518`
**Comparison**: `fbf0826..72ec452`, the retained legacy extension through current main.

## Inventory and ownership

The complete Git name-status diff was reviewed, including hidden configuration directories. These are the added executable surfaces and supporting runtime definitions:

| Surface | Prior coverage | Current contract and evidence |
| --- | --- | --- |
| [Spec Kit checker](../../scripts/check-speckit.py) | Project guide and nine regressions, no feature spec | US1, FR-001 through FR-004; [test_speckit.py](../../tests/test_speckit.py) |
| [Smoke script](../../.devcontainer/smoke.sh) | Source and historical build evidence, no acceptance contract | US2, FR-005 through FR-007; [test_devcontainer_setup.py](../../tests/test_devcontainer_setup.py) |
| [Post-create wrapper](../../.devcontainer/post-create.sh) | Source only | Same US2 contract; both entrypoints exercised for success, repeatability, missing tools, and runtime failure |
| [Dockerfile](../../.devcontainer/Dockerfile), [editor configuration](../../.devcontainer/devcontainer.json), and [.dockerignore](../../.devcontainer/.dockerignore) | Historical build/smoke recorded under 011 | Actual declared image build, non-root runtime, source-free image, and portable gate below |

The changed CI path filter and runtime pins retain the 003/006 validation contracts. Changes to Archify metadata and update-notifier tests retain the 006/012 contracts. New Arch, CachyOS, and NixOS instructions belong to 010. Portable-development instructions belong to 011/012. None adds an uncovered executable helper. Specs 007 and 009 continue to own the existing container adapter and Sentrux helpers. Tests added by this task are verification infrastructure for the two new contracts.

The original historical short ref `8e51a4f` is unavailable in this checkout. This assessment uses the available retained legacy-extension commit and does not change historical evidence or claim a fresh audit of unchanged code.

## Requirement-to-test map

Names below identify unittest methods in the linked suites. The map describes executed behavior, not source-string checks.

| Requirement | Executable evidence |
| --- | --- |
| FR-001 | `test_changed_and_deleted_files_fail_for_every_managed_surface`, `test_missing_and_invalid_manifests_fail_cleanly`, `test_manifest_identity_encoding_and_field_types_are_rejected`, and `test_invalid_paths_and_digests_fail` |
| FR-002 | `test_removed_manifest_entries_leave_no_existing_surface_unchecked`, `test_unrelated_skills_and_unrecorded_core_additions`, and `test_intact_files_and_project_owned_memory_pass_without_writes` |
| FR-003 | `test_named_pipe_manifests_and_managed_files_fail_without_blocking`, both symlink tests, `test_directories_and_dangling_symlinks_fail`, and `test_read_errors_are_diagnostics_and_other_integrations_are_checked` |
| FR-004 | `test_cli_reports_success_and_drift_with_exit_status`, `test_multiple_failures_are_aggregated_without_repair`, and success/preservation and read-error cases above |
| FR-005 | `test_both_entrypoints_are_repeatable_and_preserve_checkout`, `test_non_repository_and_parent_repository_are_rejected`, `test_git_failure_is_reported`, and `test_read_only_checkout_is_rejected` |
| FR-006 | `test_each_missing_tool_fails_and_wrapper_propagates_failure`, `test_wrong_node_major_is_reported`, and `test_node_version_predicate_accepts_only_supported_major` |
| FR-007 | Repeated setup snapshots all fixture files, including Git metadata and synthetic private runtime values; controlled PATH excludes installers and service tools |
| FR-008 | Dated inventory above, focused fixtures, full host gate, and actual image execution below |

## Reproduced defects and repairs

Before editing setup, the six initial setup tests produced five failures. Missing Make and a nested directory inside another repository incorrectly reported readiness. Read-only checkout, failed Git, and failed Node checks exited without a useful diagnostic. Setup now checks Make, compares the physical workspace path to the Git root, and explains each failure. Post-create documentation now says it verifies installed tools rather than claiming to install lockfile dependencies.

Checker tests previously accepted any finding for invalid paths/digests. Since a separate inventory error could satisfy that assertion, these cases now require the intended diagnostic. Additional cases cover invalid encoding/identity/types, directories and dangling links, unrecorded additions, unrelated local skills, multiple failures, preserved failure-state bytes, and injected read errors while still checking the other integration. No checker implementation change was needed.

## Executed checks

- Host `make check` passed: 116 tests, provenance, integrity, syntax, portability/ShellCheck, and installed-link verification.
- Container `make check-fast test portability` passed: all 116 tests, with no skips.
- Final focused suites also pass after strengthening the multi-error assertion and adding the Node-major boundary cases.

- All 35 checked local documentation links resolve.
- Focused suites: 14 Spec Kit tests and seven setup tests pass.
- Ruff passes for both changed Python test files. ShellCheck passes for both setup scripts.
- The declared Dockerfile builds successfully with `.devcontainer` as context, using cached layers. Local image tag: `agent-skills-013-check`; image ID `sha256:b08b2f8ac508cf4c77f34cb6a2757224490d41292e23540c3540a0705bd9724c`.
- Image-only execution confirms `/workspace` is empty before a bind mount. Runtime is `vscode`, Python 3.13.5, Node v26.8.1, and GNU Make 4.4.1.
- A disposable Git checkout containing the task changes was mounted at `/workspace`. The container ran as `vscode` with `--network none --cap-drop ALL --security-opt no-new-privileges`. No host credentials or Docker socket were mounted. Both post-create runs succeeded before the portable gate.

Reproduction commands:

```sh
docker build --tag agent-skills-013-check --file .devcontainer/Dockerfile .devcontainer
# task_checkout is a disposable Git checkout containing the candidate changes.
docker run --rm --network none --cap-drop ALL --security-opt no-new-privileges \
  --user vscode --env PYTHONDONTWRITEBYTECODE=1 \
  --mount "type=bind,src=${task_checkout},dst=/workspace" --workdir /workspace \
  agent-skills-013-check bash -c \
  'bash .devcontainer/post-create.sh && bash .devcontainer/post-create.sh && make check-fast test portability'
```

## Limits

This is acceptance coverage for the inventoried surfaces, not a whole-repository coverage percentage. Permission-error injection exercises checker error handling; setup permissions use actual non-root filesystem access. The Node boundary fixture runs the actual expression with controlled version metadata, not separate Node 25/27 installations. The image supplies real Node 26 evidence.

VS Code UI attachment, UID remapping for other users, other CPU architectures, Docker-compatible engines, and the unchanged Archify browser suite were not rerun. Hosted Source lint was not run; local Ruff and ShellCheck were executed. Cached image build success does not establish fresh remote registry availability. Manifest checks do not authenticate upstream releases, recover files, or guard against concurrent hostile filesystem replacement.
