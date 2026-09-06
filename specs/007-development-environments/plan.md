# Implementation plan

Own root devenv configuration and lockfile, one container helper with process-level tests, ignored local artifacts, and development documentation. Keep skill provenance and generated Spec Kit integration unchanged.

Use Nix packages for Python, Git, Make, Bash, ShellCheck, and the portable check dependencies. Export a Linux image through devenv's pinned nix2container input. Docker receives a Docker archive; Podman and Apple receive OCI archives. Mount the checkout only at run time.

Validate native devenv evaluation and tests, helper success/failure behavior, actual Docker and Podman execution, and existing portable repository gates. Record Apple execution as unavailable on this Linux host. Follow RELEASING.md for current-head CI and protected merge; no versioned release applies.
