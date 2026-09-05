---
name: sensitive-info-audit
description: Audit a repository, patch, diagnostic bundle, or publication candidate for secrets and privacy-sensitive information before sharing, pushing, publishing, or making it public. Use when public exposure is planned or the user asks for a secret, credential, PII, privacy, or sensitive-data review. Report and redact findings safely; do not print secret values or rewrite history without explicit authorization.
---

# Sensitive information audit

Audit the exact publication boundary, including committed history when Git is involved. Do not treat a clean current tree as proof that history is clean.

## Procedure

1. Establish scope: tracked files, untracked files, ignored files intended for packaging, Git history, generated artifacts, archives, logs, screenshots, and metadata.
2. Run `scripts/audit-sensitive.py PATH` for a file or directory. In a Git directory it scans tracked working-tree files. Add `--include-untracked` when untracked content could be published. It scans symlink text without following the target. If packaging dereferences links, audit the resulting package separately.
3. If available, run two independent history-aware scanners such as `gitleaks git PATH --redact` and `trufflehog git file://PATH --only-verified --no-update`. Record unavailable tools as coverage gaps.
4. Review privacy indicators manually: names, email addresses, usernames, home paths, internal domains, private addresses, device IDs, UUIDs, screenshots, location data, and repository remotes. Context determines whether they are sensitive.
5. Inspect suspicious files without echoing credential values. Report file, line, detector class, confidence, exposure boundary, and remediation.

The bundled scanner redacts match contents. Exit 0 means no supported secret detector matched and no files were skipped, 1 means secret material was detected, and 2 means invalid input or an incomplete scan. Secret findings take precedence over skipped files in the exit status. Review the scanned count and every skip. An empty scan is not publication proof. Privacy indicators are warnings because public identity and infrastructure details may be intentional.

For an incremental push, resolve the destination tip and local head to commit hashes before starting a history scanner. Pass those hashes using the installed scanner's range options and verify its reported range and scanned count. A scanner that clones the repository can resolve `origin/main` differently inside its clone. An empty range or zero scanned content does not prove pending commits are clean. For a first publication, audit all reachable history being published.

## Remediation boundaries

Removing a secret from the current file does not remove it from Git history. Before rewriting history, rotating credentials, deleting artifacts, changing repository visibility, or force-pushing, explain the exposure and obtain explicit authorization. Rotation normally comes before history cleanup for a live credential.

Re-run every applicable scanner after remediation. For a public repository, verify remote visibility and the pushed commit after publication.
