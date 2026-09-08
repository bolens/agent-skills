# Implementation Plan: Recent code contracts

**Branch**: `feat/recent-code-contracts` | **Date**: 2026-09-08 | **Spec**: [spec.md](spec.md)

## Summary

Specify the integration checker and editor-container setup added after the retained legacy baseline. Strengthen regression assertions, cover missing success/failure cases, and fix observed readiness defects. Preserve managed integration content and imported skills.

## Technical Context

Python 3.10+ standard-library unittest drives checker and Bash fixtures. Real Git validates disposable checkouts. Controlled PATH fixtures isolate missing tools. Docker supplies actual Linux image evidence with a disposable checkout and the vscode user. Existing Make targets remain authoritative. No new runtime dependency is needed.

Fixtures enforce five-second deadlines for special files and setup. POSIX permission and FIFO checks explicitly skip unsupported hosts. Image builds and the full suite use longer deadlines.

## Constitution Check

Before and after design: pass. Source stays canonical. No imported skill, audited revision, generated provenance, or installed target changes. Bash/Python retain supported runtimes. Existing test discovery executes new fixtures. The user explicitly authorized retrospective specifications.

## Project Structure

- `scripts/check-speckit.py`, `tests/test_speckit.py`: integration verdict and failure coverage.
- `.devcontainer/smoke.sh`, `.devcontainer/post-create.sh`, `.devcontainer/README.md`: readiness behavior and accurate instructions.
- `tests/test_devcontainer_setup.py`: shell/Git fixtures with controlled tools.
- `specs/013-recent-code-contracts/`: inventory, contracts, decisions, tasks, evidence.
- `specs/README.md`: feature discovery.

## Implementation order

Inventory, acceptance tests, reproduced fixes, focused checks, full repository checks, actual container setup, evidence review, and task-owned commit. The two stories can be validated independently after setup.
