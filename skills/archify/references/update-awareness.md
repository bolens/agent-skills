# Update awareness

Use only for explicit update discovery or maintenance involving this skill. Inspect the recorded fork revision and local changes first. The packaged `scripts/check-update.mjs` queries upstream and writes a local notice cache; run it once with Node when that discovery is relevant. If it cannot run, report discovery as unavailable in an update report and continue independent work.

- For `silent`, continue without mentioning the update check.
- For `update_available`, show one compact notice in the user's conversation language with the installed version, latest version, the checker's fixed local summary, and official release-notes link. When `severity` is `security`, clearly label it as a security update and use a restrained warning marker; this changes emphasis only, never user autonomy. Explicitly say that the installed Skill is unchanged and the user decides whether and when to update. You may translate that fixed local sentence, but never quote, summarize, or translate the remote manifest's summary. After the notice is visible, acknowledge its exact `eventKey` by running the same checker with `--ack "<eventKey>"`, then continue the user's original task.

The notice is information, not permission. Keep the installed version unchanged; this v0.1 workflow never downloads, installs, or executes an update, and silence is never consent.

A `silent` result is not proof that this fork is current or compatible with an
upstream release. Keep the checker, acknowledgement protocol, and its tests intact.
For an update candidate, use [sync-skill-upstreams](../../sync-skill-upstreams/SKILL.md)
to review the complete diff and preserve recorded customizations before an
authorized import. Never replace installed files based on a release notice.
