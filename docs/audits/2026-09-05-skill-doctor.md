# Claude Code Skill Doctor audit

Audited the feature identified by [Daniel Avila's post](https://x.com/dani_avila7/status/2096052993166544914)
on 2026-09-05. X returned HTTP 403; a public FxTwitter response recovered the
post text and timestamp. The post identifies a built-in Claude Code command,
not an installable skill from a similarly named third-party repository.

## Verified behavior and limits

The official [v2.1.261 release notes](https://github.com/anthropics/claude-code/releases/tag/v2.1.261)
announce `/skill-doctor` as a report of unused loaded skills and context cost.
The [current skills documentation](https://code.claude.com/docs/en/skills#find-unused-skills)
describes a terminal report, interactive plugin Stats view, and text output in
print mode. Bundled and enterprise skills are excluded. Documentation lists
v2.1.252 as the minimum, with feature-flag and Remote Control restrictions.
The release announcement and documented minimum differ; availability must be
checked on the actual host.

The same documentation distinguishes the host's budgeted skill listing from
full source descriptions and skill bodies. `/context` reports the effective
listing cost. This supports inspecting live discovery evidence before editing
source to reduce context use.

These are documentation findings. No command implementation was obtained or
audited. Third-party repositories sharing the name and extracted system-prompt
collections were not substituted for the announced feature. Inside the sandbox,
`claude --version` reached a mise launcher that failed on the read-only filesystem.
After the user identified the external installation, an escalated version check
confirmed Claude Code 2.1.261. CLI help confirmed print-mode options.

Automatic approval review rejected the subsequent `claude -p /skill-doctor`
invocation because it could transmit project and skill context to the external
model service without explicit approval for that transfer. The attempted command
disabled agent tools, hooks, session persistence, and configured MCP servers,
and capped API spending at USD 0.01. It did not execute. Live usage history,
report accuracy, and token savings remain unverified pending that approval.

## Adoption judgment

The post's suggestion that usage and cost reveal what to remove needs additional
evidence. A recovery skill can be useful before the first incident. A new skill
has little history. Missing or truncated discovery metadata can explain absent
invocations without establishing that the underlying procedure is redundant.
These are local assessment criteria, not claims about the command's internal
classification algorithm.

Retain separate evidence for installed sources, host-visible listings, and
observed use. Record the observation window and task coverage. Treat cost as
context occupancy unless billing evidence supports a savings claim. Evaluate
neighboring triggers with realistic requests, then check task outcomes separately.
Prefer a targeted description correction over hiding useful functionality.

The repository already validates metadata, syntax, provenance, licenses, and
installation links. Those checks do not measure runtime discovery or usage.
There is no demonstrated need for another installed auditor, telemetry hook,
transcript collector, automatic pruning job, or numeric context-budget gate.

## Implementation and provenance

Added a conditional usage-and-context reference to `find-skills` within its
existing installed-skill comparison remit. Linked it from the contributor
validation workflow. Invocation policy, skill count, client settings, and
installation targets remain unchanged. This is prose maintenance rather than
a new runtime capability.

Preserved the Vercel origin, audited revision, and MIT license for `find-skills`.
Recorded the new reference and local behavior in `UPSTREAMS.json`, then
regenerated `PROVENANCE.json` and `UPSTREAM.md`. No external code or skill prose
was imported, and no audited upstream reference was advanced.

## Validation

Manual walkthroughs covered an unused recovery skill, an overlapping addition
whose existing counterpart is hidden, a source shared by several client
symlinks, and a shorter description that loses its distinguishing trigger.
The guidance retains useful capabilities, investigates missing evidence, and
requires separate routing and outcome checks. An ordinary discovery request
still follows the existing source-review and installation workflow.

A YAML-parsed inventory found 61 canonical skills, 18,083 description characters,
and no exact duplicate descriptions. This excludes names and host formatting
and is not a token count or evidence against semantic overlap. An initial
line-only probe misread multiline YAML descriptions, so its totals and duplicate
candidates were discarded. Host reports should take precedence over such source
estimates.

`make check-fast` and `make check` passed, including all 30 tests, provenance,
portability with ShellCheck, and installed links. Skill Creator's quick validator
also passed. These checks cannot replace an executed Claude Code usage report
or routing trial.
