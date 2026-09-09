# Implementation plan

The coordinator owns all edits and Git writes. Add `skills/internationalization`
with message/locale and layout/testing references. `web-standard` owns standards
source selection; `accessibility` owns content clarity; `web-security` owns the
privacy reference; `forms-and-data-state` owns recovery behavior. Link consumers
to these owners rather than copying the guidance.

Preserve imported accessibility and web-quality-audit provenance by recording
local additions in `UPSTREAMS.json`. Generate registry and origin pointers.
Update discovery, changelog, and this specification index. Run skill validation,
repository gates, installed-catalog checks, and source walkthroughs. These prove
structure and reviewed routing, not live model selection or user comprehension.

Constitution: canonical source, hard-fork notices, immutable imported revisions,
portable guidance, and existing validation contracts remain intact.
