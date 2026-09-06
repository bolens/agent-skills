# Research and decisions

Baseline inspection: 2026-09-05 at `8e51a4f`.

| Question | Evidence | Decision |
| --- | --- | --- |
| Is backfilling allowed? | The user explicitly requested retrofit specs after the Netviz/Sentrux audit. AGENTS.md normally prohibits backfill. | Honor the explicit request, label retrospective material, and preserve original history. |
| Is every deferred app incomplete? | All nine source audits distinguish guidance adoption from runtime installation. | Assess accepted behaviors; do not reverse source-audit decisions just to clear a task list. |
| How broad is coverage? | PROVENANCE.json registers 61 skills; specs 001-004 cover selected features. | Use four domain contracts plus one inventory, preserving more detailed existing specs. |
| Is more validation tooling needed? | The repository already checks metadata, provenance, syntax, installed links, and selected helper behavior. | Use an explicit repeatable inventory check and existing gates, avoiding a second registry or permanent prose-test suite. |
| Should network and system diagrams use different tools? | Archify's entrypoint covers infrastructure and network topology; Netviz adds manual canvas editing. | Route by authored output versus manual editing. Keep Netviz deferred until that editing need is concrete. |
| What is still unverified? | Skill Doctor audit records a rejected external-model call; other audits state runtime and deployment limits. | Preserve those limits. This request does not authorize a new context transfer or live operation. |

No unresolved design questions require external research or installation.
This task reviews local source and dated audits, not fresh upstream revisions.
