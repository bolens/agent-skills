# Inputs and evaluation

Resolve the project's existing configuration command and selected host. For a
flake repository, inspect input URLs, follows relationships, lock revisions,
supported systems, and local source inclusion. Git-backed flakes omit untracked
files; when a newly imported module appears missing, check tracking before
changing module paths. Follow repository staging policy and preserve unrelated
index entries. See [flake source semantics](https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-flake.html).

Do not update inputs just to evaluate a local edit. Use the installed CLI's
lockfile-preserving options where appropriate, check the resulting diff, and
report when the locked source cannot be fetched. Do not accept new substituters,
trusted keys, impure evaluation, or relaxed sandboxing merely to get a build green.

When the task explicitly updates a flake input, current Nix supports
`nix flake update INPUT` from the flake directory. Check installed help and the
[update command](https://nix.dev/manual/nix/stable/command-ref/new-cli/nix3-flake-update.html)
before using it. Shared dependencies or follows relationships may widen the lock
diff. Review those changes rather than assuming a named input isolates every node.
For channel-based configurations, use that project's channel ownership and update
workflow. Root and user channels can differ.

Use the repository's checks and evaluate/build the actual NixOS host output.
`nix flake check` is useful when configured, but does not by itself establish that
every host's system closure was built. Review the derivation and builders selected
by a wrapper. Builds may fetch sources and execute build scripts, even though they
do not activate the host. An unavailable builder or cache is a verification gap,
not a reason to rewrite the target platform or its dependencies.
