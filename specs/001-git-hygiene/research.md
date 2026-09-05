# Research decisions

The collection has conflict resolution, commit-message writing, read-only review, and fleet inventory skills. Search found no shared index ownership or concurrent writer protocol. Add a dedicated skill rather than broaden those descriptions.

Use distinct branches and worktrees for independent writers. Git documents separate HEAD and index state while other repository data is shared. Worktree locking protects against pruning, not agent edits. [Git worktree documentation](https://git-scm.com/docs/git-worktree).

Inspect the entire staged diff before committing. Adding selected paths does not clear previously staged changes. [Git add documentation](https://git-scm.com/docs/git-add).

Use an explicit single Git writer when agents share a checkout. File ownership alone cannot protect a shared index or a changing working tree during tests. A custom lock service would add maintenance and cannot coordinate agents that ignore it. Keep this as a cooperative protocol and state its limits.

No unresolved design questions. Existing repository checks cover metadata and links. Manual scenarios cover instruction decisions.

Keep branch cleanup in git-hygiene because its invariants are Git ownership and integration. Babysit invokes that reference after a verified merge. A broader repo-hygiene skill would overlap fleet inventory without adding a distinct workflow.
