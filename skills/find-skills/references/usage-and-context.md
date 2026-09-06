# Usage and context evidence

Use when assessing whether an overlapping addition earns its context cost or
whether an existing skill needs a narrower description. Record the host,
project, session, skill identity and source, and observation window. Resolve
installed symlinks to their canonical source before counting copies or editing.
The same source installed for multiple clients is not automatically redundant.

Prefer the host's actual listing and usage report when available. Distinguish
discovery metadata from a loaded skill body and subsequently read references.
File size is not an observed context-token count. Label estimates and retain
their method; do not equate context occupancy with billed tokens or savings.

For Claude Code, consult the current [unused-skill documentation](https://code.claude.com/docs/en/skills#find-unused-skills)
before using `/skill-doctor` in the local terminal. Its report excludes bundled
and enterprise skills. Availability depends on version, feature flags, and
connection type. Pair it with `/context` for the effective listing cost. Do not
assume these commands or their visibility settings apply to Codex.

Treat an unobserved invocation as a question. The task may not have occurred in
the available history, the skill may be new, or discovery may be broken. Check
whether the skill appears with a useful description, whether its identity was
shadowed, and whether history covers representative work. Keep unknown coverage
explicit. Rare recovery workflows can be valuable despite low frequency.

Compare neighboring skills with a realistic request for each and a request that
should select neither. Shared words alone do not establish a collision. Prefer
a focused description edit when responsibilities are distinct. Keep the main
trigger early and move conditional procedures into linked references, preserving
the boundaries that distinguish the skill. Reading fewer instructions is useful
only if the task still gets done correctly.

When evaluation is warranted, compare routing and task results separately in
fresh sessions before and after the change. Hold host, model, project, and test
inputs steady, and retain the original source for rollback. A lower context
count does not prove better routing or successful task completion. Manual
walkthroughs provide weaker evidence than executed host evaluations; label them.

Recommend retain, narrow, investigate, or remove with the supporting evidence.
Do not disable automatic invocation or delete a skill merely to improve a usage
metric. Invocation-policy changes need explicit user intent and the correct
host-specific control. In this collection, edit canonical `skills/` content and
preserve upstream metadata and install targets. Never prune through client
symlinks or import another host's settings into shared frontmatter.
