# Codex Security source audit

Audited [Codex Security](https://github.com/openai/codex-security/tree/c8296885fbbf593edc1b405dc49859496b2bd8e4)
at `c8296885fbbf593edc1b405dc49859496b2bd8e4` on 2026-09-05.
Decision: refine finding assessment, remediation verification, and patch-risk
reasoning in existing skills. The full scanning service has dependencies and
operational scope that these prose improvements do not require.

## Findings that affect adoption

1. **Artifact integrity and narrative accuracy need separate checks.** The
   [contract validator](https://github.com/openai/codex-security/blob/c8296885fbbf593edc1b405dc49859496b2bd8e4/plugins/codex-security/scripts/validate_scan_contract.py)
   checks canonical documents, coverage, receipts, and the manifest seal. The
   [seal implementation](https://github.com/openai/codex-security/blob/c8296885fbbf593edc1b405dc49859496b2bd8e4/plugins/codex-security/scripts/finalize_scan_contract.py#L2346)
   verifies listed artifact paths and digests. In the supplied completed-scan
   example, the sealed artifacts are `findings.json` and `coverage.json`;
   `report.md` must exist but its prose is outside that artifact list. A
   disposable probe accepted replaced report prose and rejected a newline
   appended to canonical findings. This demonstrates a validation boundary,
   not an independently established exploitable vulnerability. Consumers need
   to compare narrative claims with canonical evidence and understand which
   files are sealed. Digests alone also do not establish trusted authorship.

2. **Triage must preserve the supplied claim.** The
   [static assessment reference](https://github.com/openai/codex-security/blob/c8296885fbbf593edc1b405dc49859496b2bd8e4/plugins/codex-security/references/static-finding-assessment.md)
   and inspected [triage guidance](https://github.com/openai/codex-security/blob/c8296885fbbf593edc1b405dc49859496b2bd8e4/plugins/codex-security/skills/triage-finding/SKILL.md)
   distinguish exact claims, deployment prerequisites, counterevidence, and
   gaps in proof. A neighboring vulnerable route cannot confirm a protected
   reported route. Missing runtime setup cannot refute source evidence. Local
   guidance now preserves source identifiers and records supported,
   contradicted, or unresolved outcomes without inventing missing intake data.

3. **Fix verification is a separate evidentiary step.** The
   [validation](https://github.com/openai/codex-security/blob/c8296885fbbf593edc1b405dc49859496b2bd8e4/plugins/codex-security/skills/validation/SKILL.md)
   and [verify-fix](https://github.com/openai/codex-security/blob/c8296885fbbf593edc1b405dc49859496b2bd8e4/plugins/codex-security/skills/verify-fix/SKILL.md)
   workflows inform checks of the original attack path, alternate consumers,
   and legitimate behavior at the patched revision. Moved code, a closed
   ticket, or a clean rescan cannot substitute for that evidence. Local
   verification retains an inconclusive outcome when material proof is missing.

4. **Patch risk has several independent dimensions.** The
   [risk rubric](https://github.com/openai/codex-security/blob/c8296885fbbf593edc1b405dc49859496b2bd8e4/plugins/codex-security/skills/assess-patch-risk/references/risk-rubric.md)
   separates impact, regression likelihood, test protection, recoverability,
   and confidence. Local code review adopts those distinctions for consequential
   changes. Test strength does not reduce the consequence of a failure, and
   a patch-risk assessment is distinct from vulnerability severity or merge
   authorization. Upstream automation policy is not adopted as local authority.

## Scope and implementation

Updated `web-security` with a conditional finding-assessment reference and
claim-preservation guidance. Updated `code-review` with proportionate patch-risk
reasoning. These are prose refinements within existing review and verification
remits, not a new security capability or runtime behavior. They add no mandatory
report schema, persistent findings store, scan service, provider connection,
credential setup, publication mechanism, or invocation mode.

The upstream contains 15 skills alongside an SDK, CLI, MCP/workbench, artifact
contracts, and publishing code. Importing that system would require a separate
task with operational requirements and validation. This audit does not establish
a need for the complete stack in this collection.

Both affected skills remain local originals. No upstream code, skill passages,
assets, or license-bearing subtrees were imported. Upstream declares Apache-2.0;
this pinned audit records the conceptual source without relabeling the skills'
origins. Existing provenance, upstream metadata, and installed symlink targets
remain synchronized.

## Audit coverage and limits

Inspected the README, manifests, SDK package metadata, skill inventory, full
static assessment, validation, and verify-fix instructions; selected triage and
patch-risk instructions; the contract validator and seal-validation functions;
completed-scan canonical examples; report-projection excerpts; and SDK excerpts
covering configuration, scan sandbox setup, and publication entry points.
Review of the SDK and the other skill bodies was partial. The audit does not
certify the whole project or every execution, credential, or publishing path.

Ran the upstream `test_validate_scan_contract.py` unittest module: all eight
tests passed. Also used the original validator against a disposable copy of
the completed-scan example: the original passed, replaced unsealed report prose
passed, and modified sealed findings failed. The probe performed no provider
calls and did not alter the upstream checkout. No dependencies were installed,
and no full scan, service launch, or report publication was performed. The full
upstream suite was not run, and there was no independent reviewer.

## Local validation

Manual walkthroughs checked a protected reported route with a vulnerable sibling,
missing runtime prerequisites, grouped findings with separate source identifiers,
a moved implementation after repair, stale report prose, and a well-tested patch
with severe failure consequences. Each retains its own claim and evidence;
ordinary reviews do not acquire a mandatory scan report or new execution scope.

`make check-fast` and `make check` passed: all 30 repository tests, provenance,
portability with ShellCheck, and installed symlink checks. Both edited skills
passed Skill Creator's quick validator. These checks establish collection
consistency, not the effectiveness of an unexecuted full security scan.
