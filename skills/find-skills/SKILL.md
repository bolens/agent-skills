---
name: find-skills
description: Discover installable agent skills for a concrete capability, verify their source and contents, compare them with already installed skills, and recommend only additions that materially improve the current skill set. Use when the user asks whether a skill exists, wants skill recommendations, or wants to extend Codex.
---

# Find skills

Find the smallest trustworthy addition that solves the user's recurring need. Do not recommend a skill merely because its title matches the query.

## Discover

1. Identify the task, target environment, and behavior the user lacks.
2. Inventory installed skills before searching. Treat overlapping triggers and conflicting instructions as costs.
3. Search first-party repositories, reputable ecosystem indexes such as [skills.sh](https://skills.sh/), and the source repository named by the user.
4. Inspect the actual `SKILL.md` and any scripts, references, hooks, agents, or manifests that affect behavior.

Use current web sources for repository contents, popularity, maintenance status, and compatibility claims. Install counts and stars are weak signals, not proof of quality.

## Evaluate

Recommend a skill only when it adds non-obvious procedures, maintained domain knowledge, deterministic tooling, or reusable assets. Check:

- source ownership and recent maintenance
- license and bundled executable code
- trigger precision and overlap with installed skills
- assumptions about Claude Code, Codex, or another host
- destructive actions, network access, credentials, and external side effects
- whether a small rewrite is required for the target environment

Reject generic prompt collections, stale migrations, duplicate workflows, and host-specific skills that would misroute Codex.

## Report

Give a short verdict for each serious candidate: what it adds, what overlaps, compatibility risks, and the source link. Say plainly when nothing is worth installing.

## Install

Do not install until the user asks. In Codex, use the native `skill-installer` workflow for GitHub paths or curated skills. Preserve the complete skill directory, not only `SKILL.md`, and validate the installed result. Use another package manager only when the user requests it or the source requires it.

After installation, state the destination and that the skill becomes available on the next turn.
