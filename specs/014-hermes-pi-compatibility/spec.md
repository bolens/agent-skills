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
