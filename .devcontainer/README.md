# agent-skills devcontainer

Open this repository in VS Code and run **Dev Containers: Reopen in
Container**. A local Docker-compatible engine and the Dev Containers extension
are required. The first build downloads the pinned tool images and distribution
packages. Post-create setup runs `smoke.sh` to verify the mounted checkout and
tools already installed in the image. It does not install checkout dependencies.
Rebuild after Dockerfile changes. Rerun `bash .devcontainer/post-create.sh` to
check readiness after changing the workspace or tool environment.

The portable gate works in a checkout. The installed-skill link check in
`make check` belongs to the canonical host checkout. Do not repoint host skill
links from the container.

Run from the workspace root:

```sh
make check-fast test portability
```

The editor runs as `vscode`, with its UID adjusted for the local workspace. The
source is bind-mounted at `/workspace` and is never copied into image layers.
Use a regular clone when the container cannot see a linked worktree's external
Git directory. Keep credentials in your local development environment.

`bash .devcontainer/smoke.sh` checks the writable Git root, required tool presence
including Make, and Node 26. Failures identify the missing prerequisite. It
does not run the application test suite. No application starts automatically.
Image references include immutable digests. Dependabot monitors the Dockerfiles
where supported. Distribution packages resolve from the configured Debian
repositories at build time. Update image pins and rerun setup and native checks
together. Existing native and Nix workflows remain available independently.
