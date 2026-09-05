---
name: verify-and-stop
description: Prove existing work meets acceptance conditions without expanding scope. Use for validation-only tasks, completion checks, focused gate runs, and last-mile proof.
---

# Verify and stop

Translate acceptance conditions into smallest sufficient proof set.

- Reuse results only when the checked files, dependencies, configuration, and relevant runtime conditions still match. Record the command and scope so a previous pass is not mistaken for proof of later changes.
- Run focused checks before wider gates.
- Distinguish pass, fail, unavailable, and blocked exactly.
- Do not edit product code unless verification request includes fixes.
- Do not add polish, cleanup, or unrelated tests after criteria pass.

Once acceptance proof is complete, end verification. Complete any remaining delivery steps already required by the user or repository instructions, such as a focused commit or requested artifact. Do not infer permission to push or publish from passing checks. Report results and any verification gaps without starting another improvement pass.
