# Development environments

Provide a pinned devenv shell for the portable agent-skills validation gate and a source-free Linux development image usable with Docker, Podman, and Apple container. Existing Make targets remain authoritative.

Acceptance: devenv shell and test run `make check-fast test portability`; the image includes the same tools without copying checkout files; container commands preserve argument boundaries and exit status; writable mounts preserve host ownership; unsupported engines fail clearly. Apple execution requires a Mac and a matching Linux image architecture. Installed skill links and live host services are outside this feature.
