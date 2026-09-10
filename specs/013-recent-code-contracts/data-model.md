# Validation data

The checker reads JSON objects named speckit and codex. Each requires a matching integration string and nonempty files object. Keys are canonical relative paths without traversal or backslashes. Values are lowercase 64-character SHA-256 digests. Additional release metadata does not affect the verdict.

Core inventory covers `.specify/templates/*.md`, `.specify/scripts/bash/*.sh`, and `.agents/skills/speckit-*/SKILL.md`. Other recorded paths are still checked. No persistent validation state is created.

Setup reads script location, checkout access, Git root, command lookup results, and Node version. Its output is exit status and diagnostics. There is no installation or migration state.
