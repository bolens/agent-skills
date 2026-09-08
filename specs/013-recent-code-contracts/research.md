# Source decisions

- Compare `fbf0826` to `72ec452` because the former contains the retained legacy executable-contract extension. The original short baseline `8e51a4f` does not resolve in this checkout. Preserve its historical reference.
- The complete diff adds `scripts/check-speckit.py`, `.devcontainer/post-create.sh`, and `.devcontainer/smoke.sh`. Dockerfile/editor configuration supplies setup runtime. Changed Archify files are tests for behavior contracted under 006 and 012.
- Specs 007 and 011 cover devenv/container adapters and reusable instructions. Neither defines these VS Code setup scripts' verdict. Add a dated contract rather than rewrite completed history.
- Existing invalid-path/digest tests assert only that some problem exists. Core inventory failures can now satisfy those assertions independently. Require the intended diagnostic.
- Use standard-library fixtures and real shell/Git. Map contract conditions to tests rather than add a coverage dependency solely to claim a percentage. Separate actual-container evidence.
