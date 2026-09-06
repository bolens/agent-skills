# Local Sentrux runner

Use this optional runner for selected-source dependency measurements and session
comparisons. It requires Linux x86_64, Python 3.10+, Git, Bubblewrap, and the
reviewed Sentrux 0.5.7 binary. It does not belong in required CI, package runtime
dependencies, or a persistent MCP server by default.

## Setup and license boundary

The [provenance record](sentrux-notices/provenance.json) pins the binary and grammar
archive hashes. Download the `grammars-linux-x86_64.tar.gz` asset from the
[v0.5.7 release](https://github.com/sentrux/sentrux/releases/tag/v0.5.7), then run:

```sh
python3 scripts/prepare-sentrux.py --archive /path/to/grammars-linux-x86_64.tar.gz --runtime /path/to/private-runtime
```

Paths here are relative to this skill. Setup verifies the complete archive before
copying only the seven reviewed grammar files and retained notices. It makes no
network requests and refuses an existing destination. Scans verify the installed
binary and grammar bytes. Startup synchronizes embedded plugin configurations
from that binary. Never regenerate the grammar manifest to accept unexplained
changes. An upgrade needs a new source, license, parser, and fixture review.

Public Sentrux source is MIT, with the full notice retained in
[sentrux-notices/SENTRUX-LICENSE](sentrux-notices/SENTRUX-LICENSE). The official
release workflow also builds a private Pro crate. The public source license alone
does not establish redistribution rights for that binary. Use the owner's
existing installation. Do not bypass licensing or copy it into images, packages,
Git commits, or releases.

Grammar notices are retained separately. The upstream bundle was built from
mutable grammar refs, without an exact source-revision manifest or license files.
The recorded current-source notices are supporting evidence, not proof of the
exact release inputs. Redistribution of the runtime remains outside this
integration until those source and notice gaps are resolved. No runtime binary,
archive, grammar library, or imported implementation is committed here. This
runner is locally authored and keeps the skill's existing local provenance.

## Select a scope

Create private JSON with explicit include patterns and extension-to-plugin names:

```json
{
  "include": ["src/*", "tests/*"],
  "exclude": ["*/fixtures/*", "*/vendor/*"],
  "extensions": {".py": "python"},
  "context": [],
  "rules": "[constraints]\nmax_cycles = 0\n"
}
```

Patterns use Python `fnmatchcase`, where `*` also matches directory separators.
Use `context` patterns for resolver inputs such as `go.mod`, `package.json`, and
`tsconfig.json`. They are copied separately from the selected source extensions.
Every selected file must be regular, inside the repository, and at most 512 KiB.
The runner includes tracked working changes and non-ignored untracked files,
without changing the real Git index. Ignored new files, symlinks, generated code,
external dependencies, and files outside the selected patterns are not coverage.
Select submodule repositories separately.

The runner creates a temporary Git snapshot so Sentrux's tracked-file enumeration
sees new source. Application code is parsed, never executed. The process has an
isolated application home and disabled networking. Logs, file hashes, revision,
working status, parser identity, and metrics stay in the chosen private output.
Concurrent commands must use separate runtimes or run serially.

```sh
python3 scripts/sentrux.py baseline /path/to/repo --scope scope.json --runtime /path/to/private-runtime --output /path/to/session-before
python3 scripts/sentrux.py compare /path/to/repo --scope scope.json --runtime /path/to/private-runtime --baseline /path/to/session-before --output /path/to/session-after
python3 scripts/sentrux.py check /path/to/repo --scope scope.json --runtime /path/to/private-runtime --output /path/to/rules-check
```

Outputs must be new directories outside the scanned source. Baselines are never
automatically replaced. Comparisons refuse changed repository paths, scopes,
runners, binaries, grammars, or altered baseline metrics. Rebaseline deliberately
after a tooling/scope change. Exit 0 means the requested analyzer operation
succeeded, 1 means a rule or regression finding, and 2 means evidence unavailable.
Saving a baseline accepts existing metrics for comparison. It does not certify
architecture health. `check` is separate and uses configured rules, defaulting
to a diagnostic zero-cycle rule. Trace its reported edges before proposing fixes.

## Coverage limits

The 0.5.7 trial found useful import graphs in Bash, Python, JavaScript, TypeScript,
Go, and Rust scopes. PowerShell loaded but produced zero dependency edges in both
profile copies. QML, Fish, and Astro have no matching parser. Markdown and Vlang
plugins failed in the full bundle. Do not substitute helpers' scores for these
products' architecture. Configuration-only repositories stay on native checks.

CLI output provides graph counts, not complete per-file parse-success evidence.
Unresolved dynamic imports, aliases, and external registrations require source
inspection. Empty graphs are inconclusive and cannot create accepted baselines. Whole-repository native tests and
language-specific lint remain authoritative. Before a new rule becomes required,
prove allowed and forbidden fixtures with its actual language and path patterns.
