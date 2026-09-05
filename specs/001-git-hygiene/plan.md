# Implementation Plan: Git hygiene

**Branch**: `feat/git-hygiene` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

## Summary

Add a local-original `git-hygiene` skill. Keep commit-message writing and conflict resolution in existing skills. Add a README discovery link and a conditional conflict-resolution handoff.

## Technical Context

Markdown instructions and JSON provenance. Git CLI examples use portable arguments. No runtime service, agent API, new dependency, or automated destructive command. Validate using existing Python repository checks and manual scenario evaluation.

## Constitution Check

Before and after design: canonical content stays under skills/, local origin is recorded in PROVENANCE.json and UPSTREAM.md, no upstream import occurs, existing external-fork tracking stays untouched, and validation uses existing Make targets. Installation is separate and remains out of scope.

## Project Structure

- skills/git-hygiene/SKILL.md: ownership, isolation, staging, integration, recovery.
- skills/git-hygiene/UPSTREAM.md and PROVENANCE.json: matching local origin and three client install targets.
- skills/resolving-merge-conflicts/SKILL.md: route concurrent conflicts to ownership guidance.
- skills/babysit/SKILL.md and skills/git-hygiene/references/branch-cleanup.md: verified post-merge cleanup.
- README.md and CHANGELOG.md: discovery and new behavior.
- specs/001-git-hygiene/: specification, design, tasks, and validation evidence.

## Implementation strategy

Two focused commits: the skill with related routing and documentation, then babysit post-merge cleanup. No new test suite that matches instruction wording. Evaluate realistic scenarios, run existing contract checks, inspect the diff, and commit task-owned files. No external delivery.
