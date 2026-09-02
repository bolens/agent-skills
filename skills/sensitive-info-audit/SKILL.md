---
name: sensitive-info-audit
description: Audit a repository, patch, diagnostic bundle, or publication candidate for secrets and privacy-sensitive information before sharing, pushing, publishing, or making it public. Use when public exposure is planned or the user asks for a secret, credential, PII, privacy, or sensitive-data review. Report and redact findings safely; do not print secret values or rewrite history without explicit authorization.
---

# Sensitive information audit

Audit the exact publication boundary, including committed history when Git is involved. Do not treat a clean current tree as proof that history is clean.

## Procedure

1. Establish scope: tracked files, untracked files, ignored files intended for packaging, Git history, generated artifacts, archives, logs, screenshots, and metadata.
2. Run `scripts/audit-sensitive.py PATH`. Add `--include-untracked` when untracked content could be published.
3. If available, run two independent history-aware scanners such as `gitleaks git PATH --redact` and `trufflehog git file://PATH --only-verified --no-update`. Record unavailable tools as coverage gaps.
4. Review privacy indicators manually: names, email addresses, usernames, home paths, internal domains, private addresses, device IDs, UUIDs, screenshots, location data, and repository remotes. Context determines whether they are sensitive.
5. Inspect suspicious files without echoing credential values. Report file, line, detector class, confidence, exposure boundary, and remediation.

The bundled scanner redacts match contents and exits nonzero only for high-confidence secret material. Privacy indicators are warnings because public identity and infrastructure details may be intentional.

## Remediation boundaries

Removing a secret from the current file does not remove it from Git history. Before rewriting history, rotating credentials, deleting artifacts, changing repository visibility, or force-pushing, explain the exposure and obtain explicit authorization. Rotation normally comes before history cleanup for a live credential.

Re-run every applicable scanner after remediation. For a public repository, verify remote visibility and the pushed commit after publication.
