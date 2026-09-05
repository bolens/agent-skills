---
name: create-verification-skill
description: "Create or update a reusable project-local skill for exercising an app and capturing behavior evidence. Use when the user requests a verification skill or control skill for a repository, not for a one-off test or ordinary bug fix."
---

# Create a verification skill

Generate instructions that let another agent launch the app, exercise a user path, capture evidence, and clean up without prior conversation context. Reuse an existing verification skill and harness when they cover the requested surface.

Use the user's requested destination first, then the repository's existing skill-directory convention. If neither exists, use `.agents/skills/verify-<app>/` for a shared Agent Skills project. Use a client-specific directory when the target client requires it. Refer to the selected directory as `<skill-dir>` below and keep all generated paths consistent. Preserve existing invocation policy when updating a skill.

## 1. Interview the repo, not the user

Answer these from the codebase and only ask the user what you cannot observe:

- **Surface:** what does a user actually touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library? A repo can have several; pick the primary one and note the rest.
- **Run:** how does the app start locally? Prefer the repo's own documented dev command (package scripts, Makefile, README quickstart). Note ports, env vars, seed data, auth.
- **Drive:** how can an agent interact with it programmatically? Existing harnesses first — Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port. Only then pick a generic recipe: browser/CDP for web and Electron, a tmux/PTY harness for CLI/TUI, plain HTTP for services.
- **Observe:** what evidence can be captured? Screenshots, terminal transcripts, response bodies, logs, exit codes, DB state.
- **Isolate:** can two instances run side by side (ports, data dirs, profiles)? If not, say so in the generated skill: refusing to double-drive a shared instance beats corrupting the user's session.

If the checkout does not build or start, distinguish a missing local prerequisite from a product failure. Use documented setup within the task's authority. Do not turn skill generation into unrelated product repair. If execution remains blocked, generate only instructions supported by inspected evidence, label the result an unverified draft, and report the blocked step. Any temporary verification files must be isolated, named, and removed during cleanup without replacing existing user files.

## 2. Generate the skill

Write `<skill-dir>/SKILL.md` with YAML frontmatter (`name: verify-<app>` and a `description` that names the app, surface, and trigger) and these sections, grounded in the inspected repository with no unfinished placeholders:

- **Launch:** the exact command that starts the app for verification, and how to tell it's ready (a log line, a port answering, a prompt). Include teardown. For a short-lived CLI or TUI there is no server to keep alive: launch means build the binary (or install deps) once, then start each drive in its own isolated PTY or tmux session.
- **Doctor:** one read-only check that answers "is this instance worth driving?" — process up, right version/build, port owned by us, auth valid. An agent runs this first whenever anything looks off.
- **Drive:** the harness recipe with real selectors/commands from this repo, not examples. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths) over coordinates and tab order.
- **Evidence:** what to capture for a proof and where it goes. State the proof standards: exercise the real user path, not internal setters or test-only endpoints; capture the action and the resulting state, not just the final screen; verify side effects (files written, rows inserted, messages sent) alongside what's visible; mocks only where a production boundary already isolates the external system. When the safe path is a dry-run or test mode, verify what it actually skips by observing (files, network, git refs) rather than trusting its name: some dry-runs still touch the network or open a browser.
- **Cleanup:** how to tear down instances the run created. Never kill by process name; kill what you started. Cleanup removes instances and scratch state, never the evidence: proof artifacts survive the teardown, in a location the skill names.
- **Helpers:** any script the skill ships is executable and its invocation is shown in the skill body. A helper the reader has to reverse-engineer is not a helper.

## 3. Seed the feature map

Create `<skill-dir>/features/README.md` and feature files for the requested scope. For a broad request, start with the main user journeys found in routes, commands, menus, or docs. Follow the shape in [`references/feature-map-example/`](references/feature-map-example/), with a README index and one file per feature. Each file answers, from the user's point of view: what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. Link the map from the generated `SKILL.md` and tell readers to load only the feature files relevant to their task. Record which paths each run covers. One passing path does not prove every mapped feature works.

## 4. Prove the generated skill before handing it over

Run its own instructions end to end once: launch, doctor, drive ONE mapped feature (one is enough; the map exists so later runs can cover the rest), capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location — a cleanup that eats the proof fails this step. Fix what fails, and run the generated cleanup after every failed iteration too, so broken attempts don't strand processes and ports. A generated skill that was never executed is a draft, not a deliverable.

## 5. Maintain the skill

For an update request, compare the existing launch commands, selectors, and mapped paths with the current app. Update the affected instructions and rerun the changed flow, preserving unrelated feature documentation. Report the skill path, exercised feature, evidence location, and any unverified paths. Do not recommend a maintenance command unless it is actually available.
