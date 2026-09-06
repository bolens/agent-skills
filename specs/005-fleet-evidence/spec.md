# Durable fleet verification evidence

## Problem

Fleet maintenance crosses repositories, worktrees, and long-running checks. A
remembered successful command does not establish that the current candidate
passed. Lost context can also cause identical failures to be rerun without a
changed candidate or a diagnosed transient cause.

## Scope

Extend the existing fleet-audit skill with a portable, dependency-free command
runner and verification records. Keep each repository's native checks and its
existing permissions, Git ownership, PR review, and delivery requirements.
Repository applications do not acquire an agent framework or model dependency.

## Acceptance

- Execute an explicit command in the selected repository with a finite timeout.
- Record command, candidate fingerprint, HEAD, status, exit code, elapsed time,
  and paths to local stdout/stderr evidence, including failed and timed-out runs.
- A passing command that changes the candidate does not certify its new state.
- Report evidence as stale after tracked or nonignored source changes, including
  deletion and symlink changes; ignored runtime output does not invalidate it.
- Never persist source contents or tool-output caches in tracked configuration.
- Never retry commands automatically. Repeating an identical failed candidate
  requires an explanation and is bounded by an attempt limit.
- Distinct worktrees and concurrent invocations have independent records.
- Keep missing tools, failed checks, skipped checks, and unexecuted checks
  distinguishable from success. Do not claim independent review from self-review.

## Fleet adoption

Use each maintained repository's existing project guide to identify its native
checks and delivery conditions. Add only missing execution and evidence guidance;
record already-covered and inactive archive cases explicitly. Private metadata
and execution logs remain private. No release is implied for documentation or
agent-only maintenance.

## Source assessment

Inspired by [marfin's article](https://x.com/marfinxx/status/2081687570488954915).
The source links no implementation repository. Its snippets are illustrative and
its performance and zero-defect claims are not acceptance criteria. Returning
cached text still consumes context, and caching file contents can preserve
secrets. This implementation records hashes and execution evidence instead.
