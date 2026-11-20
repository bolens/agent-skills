# Implementation plan

Add a locally authored skill under `skills/evaluate-agent-workflows` with a
conditional Codex reference. Use generated install and provenance records.
The workflow is client-independent. Codex live runs require an authenticated
CLI and fixture permissions. Benchmarks run separately from CI and installation.

Use a synthetic read-only fixture and a frozen copy of the full skill catalog.
Keep the answer key and runner outside the fixture. Use fresh Codex CLI
sessions with both requested model IDs, identical reasoning effort, and
network disabled for tools. Record successful skill reads and grade plans
against observable requirements. Preserve the existing installed checkout.
