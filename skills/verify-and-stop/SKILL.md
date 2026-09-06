---
name: verify-and-stop
description: Prove existing work meets acceptance conditions without expanding scope. Use for validation-only tasks, completion checks, focused gate runs, and last-mile proof.
---

# Verify and stop

Translate acceptance conditions into smallest sufficient proof set.

For each material condition, identify the observable result, the candidate it
applies to, and a check capable of rejecting a violating result. Check that the
command actually selects the relevant tests or assertions. A zero exit status,
empty findings list, or model confidence alone does not establish correctness.
When a new or suspect check might pass vacuously, exercise a known failing case
in disposable state without weakening the gate or mutating the delivery candidate.

- Reuse results only when the checked files, dependencies, configuration, and relevant runtime conditions still match. Record the command and scope so a previous pass is not mistaken for proof of later changes.
- Run focused checks before wider gates.
- Distinguish pass, fail, unavailable, and blocked exactly.
- Do not edit product code unless verification request includes fixes.
- Do not add polish, cleanup, or unrelated tests after criteria pass.

For failed conditions, report the affected unit, expected and observed result,
evidence, and the narrow correction or missing prerequisite. Return that receipt
to an existing coordinator. Preserve valid proof for unaffected inputs, but
invalidate it when a changed dependency or assumption alters what was checked.
Verification-only authority does not include performing the correction.

Once acceptance proof is complete, end verification. Complete any remaining delivery steps already required by the user or repository instructions, such as a focused commit or requested artifact. Do not infer permission to push or publish from passing checks. Report results and any verification gaps without starting another improvement pass.

If the broader task already includes PR follow-through or release preparation or publication, automatically use [babysit](../babysit/SKILL.md) for that remaining endpoint after verification. Return proof to an already active workflow without restarting it. A validation-only request ends with its results and does not start PR monitoring or release work.
