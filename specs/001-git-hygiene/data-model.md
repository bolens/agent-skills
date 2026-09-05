# Coordination records

A task assignment records repository root, worktree, branch, base SHA, owner, allowed files, shared files, dependencies, checks, and integration owner.

A handoff records that assignment plus final SHA or patch identity, changed paths, check results, remaining work, and cleanup status.

Ownership moves from assigned to active to handed off to integrated. Failed or interrupted work stays recoverable. These records live in the available task channel or repository convention, not a required new database.
