# Hermes and Pi compatibility

Support this collection in Hermes Agent and Pi without changing existing Codex,
shared, or Claude installation behavior. Client runtimes and model credentials
are outside scope. The source checkout remains canonical.

## Acceptance

- Optional client selection installs only the requested Hermes or Pi targets and
  honors HERMES_HOME and PI_CODING_AGENT_DIR. Default installation stays unchanged.
- Pi receives all registered skills. Existing explicit-only skills carry Pi's
  disable-model-invocation flag as well as unchanged Codex policy.
- Hermes receives only automatically invocable skills because the inspected
  loader does not implement that flag. Documentation supplies explicit file
  loading for excluded skills and explains reference/tool limitations.
- Check mode never creates directories. Apply is repeatable, preserves existing
  independent files by default, and reports mismatches or collisions.
- Tests use temporary homes and verify references through installed links.
  Real client sessions are reported separately from installer and source evidence.

## Follow-through amendment: 2026-09-08

- Run pinned native loader functions in temporary profiles without model sessions.
  Verify catalog identity, explicit-only policy where supported, symlink aliases,
  and same-skill/sibling resource reads. Record permission-boundary limitations.
- Report obsolete links owned by this checkout and excluded Hermes skills found
  in its native catalog. Bound traversal and never delete independent entries.
- Installation planning must expose conflicts before writes and be usable from
  automation. Default checks remain offline and require no agent packages.
- Remove Codex-only assumptions from discovery guidance. Document optional helper
  backends and shared-home support in OpenCode, Gemini CLI, and Copilot CLI.
