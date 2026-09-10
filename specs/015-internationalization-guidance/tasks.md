# Tasks and evidence

- [x] Add internationalization workflow and focused references.
- [x] Add source-authority, content, privacy, and recovery guidance and handoffs.
- [x] Regenerate provenance and verify installations.
- [x] Run final repository gates and record outcomes.

## Source walkthroughs, 2026-09-09

These are coordinator source reviews, not live agent or browser evaluations.

| Request | Reviewed decision path |
| --- | --- |
| Switch to Arabic while editing an unsaved form | Keep explicit locale choice, retain the draft, reject stale-language responses, set language/direction separately, and verify mixed user text through the existing browser coordinator |
| Format a birthday and a recurring meeting | Keep the date-only value separate from instant conversion; preserve the meeting's named zone and recurrence intent; test daylight-saving boundaries |
| Recover after connection loss during save | Reconcile possible server acceptance before retry; preserve edits and distinguish local draft from server confirmation |
| Add session replay to diagnose an error | Inspect purpose and existing telemetry authority; use synthetic/redacted evidence and avoid exporting user text by default |
| Translate one paragraph, repair only hreflang, or recolor a button | Keep the task in ordinary translation, technical-seo, or design-system work; do not start a full internationalization audit |
| Claim conformance from a draft or a scanner score | Select the actual specification/version and scope; distinguish maturity, support, advisory checks, and missing evidence |

Skill quick validation passed. All 195 relative links in changed Markdown
resolved. Native Pi and Hermes loaders passed with 66 and 59 skills respectively.
The new skill links resolve in all five configured catalogs. No new runtime or
helper was added. Primary sources were checked where accessible; the Open Group
source was verified through its indexed official page after direct access returned
403. No claim depends on inaccessible ISO/IEC clauses.

`make check` passed: 180 tests passed and one filesystem-specific test skipped.
The final `make check-fast` also passed after wording and routing corrections.
No browser application, native-speaker review, or live model routing was exercised.
