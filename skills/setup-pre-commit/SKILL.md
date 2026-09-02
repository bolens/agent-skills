---
name: setup-pre-commit
description: Set up or improve repository pre-commit checks using the project's existing language, package manager, formatter, linter, type checker, and tests. Use when the user asks for pre-commit hooks, staged-file checks, commit-time validation, Husky, pre-commit, Lefthook, or similar tooling in Node, Python, Go, Rust, shell, or mixed repositories.
---

# Set Up Pre-Commit Checks

Build on the repository's existing tooling. Prefer a small, fast hook developers will keep enabled.

## Inspect

1. Read `AGENTS.md`, contributor docs, manifests, lockfiles, existing hooks, CI, and Make/task targets.
2. Identify the repository ecosystems and canonical commands. Examples include:
   - Node: package-manager scripts, lint-staged, Husky
   - Python: `pre-commit`, Ruff, Black, mypy, pytest
   - Go: gofmt, go vet, golangci-lint, go test
   - Rust: cargo fmt, Clippy, cargo test
   - Shell/config: shfmt, ShellCheck, repository validation targets
3. Preserve existing formatter and linter configuration. Do not introduce competing tools or style defaults.

## Design

- Reuse an existing hook framework. If none exists, choose the least invasive fit for the repo and explain the choice.
- Run formatting and linting on staged files when supported.
- Keep expensive full-suite tests in CI unless the suite is demonstrably fast or the user explicitly wants it locally.
- Never rewrite unrelated staged files. Warn before a formatter may modify files.
- Pin or lock new dependencies using the repository's normal conventions.

## Implement

Treat a request to set up hooks as authorization to edit repository configuration. Dependency downloads, changes outside the repository, and replacement of existing hooks still require the normal approvals.

Add only the files and scripts needed for the selected framework. Keep commands usable outside the hook, preferably through existing package scripts or Make/task targets.

Do not stage or commit changes unless the user explicitly asks. Do not replace an existing hook without describing what will be preserved.

## Verify

1. Validate configuration syntax.
2. Run each underlying command directly.
3. Exercise the hook against representative staged files when this can be done without disturbing the user's index; otherwise explain the limitation.
4. Report runtime, files changed, and any checks intentionally left to CI.
