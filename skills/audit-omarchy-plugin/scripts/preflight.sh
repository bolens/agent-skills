#!/usr/bin/env bash
set -uo pipefail

repo=${1:-.}
if [[ ! -d $repo ]]; then
  printf 'ERROR repository not found: %s\n' "$repo" >&2
  exit 2
fi
repo=$(cd -- "$repo" && pwd)
errors=0
warnings=0

error() { printf 'ERROR %s\n' "$*"; errors=$((errors + 1)); }
warn() { printf 'REVIEW %s\n' "$*"; warnings=$((warnings + 1)); }
fact() { printf 'INFO %s\n' "$*"; }

printf 'Omarchy plugin preflight: %s\n' "$repo"

git -C "$repo" rev-parse --is-inside-work-tree >/dev/null 2>&1 || error 'repository root is not a Git worktree'
if [[ ! -f $repo/manifest.json ]]; then
  error 'root manifest.json is missing'
elif ! jq -e 'type == "object" and (.id | type == "string" and length > 0) and (.version | type == "string" and test("^[0-9]+\\.[0-9]+\\.[0-9]+")) and (.entryPoints | type == "object" and length > 0)' "$repo/manifest.json" >/dev/null 2>&1; then
  error 'manifest.json is invalid or missing id, stable version, or entryPoints'
else
  plugin_id=$(jq -r .id "$repo/manifest.json")
  fact "plugin id: $plugin_id"
  [[ $plugin_id == omarchy.* ]] && error 'plugin ID uses the reserved omarchy.* namespace'
  while IFS= read -r entry; do
    [[ -f $repo/$entry ]] || error "manifest entry point is missing: $entry"
  done < <(jq -r '.entryPoints[] | select(type == "string")' "$repo/manifest.json")
fi

readme=''
for candidate in "$repo"/README "$repo"/README.*; do
  [[ -f $candidate ]] && { readme=$candidate; break; }
done
[[ -n $readme ]] || error 'root README is missing'
if [[ -n $readme ]]; then
  rg -qi 'install' "$readme" || error 'README does not describe installation'
  rg -qi 'uninstall|remov' "$readme" || error 'README does not describe removal'
  rg -qi 'dependenc|requirement|package' "$readme" || warn 'README may not document external dependencies'
fi

license=''
for candidate in "$repo"/LICENSE "$repo"/LICENSE.* "$repo"/COPYING "$repo"/COPYING.*; do
  [[ -f $candidate ]] && { license=$candidate; break; }
done
[[ -n $license ]] || error 'root license file is missing'

if git -C "$repo" rev-parse --verify HEAD >/dev/null 2>&1; then
  fact "candidate SHA: $(git -C "$repo" rev-parse HEAD)"
  [[ -z $(git -C "$repo" status --porcelain) ]] || warn 'worktree is dirty; uncommitted files are outside exact-commit review'
else
  error 'HEAD commit is unavailable'
fi

scan_files=()
discovered=$(mktemp) || exit 2
trap 'rm -f -- "$discovered"' EXIT
if ! find "$repo" \
    \( -path "$repo/.git" -o -path "$repo/.github" -o -path "$repo/node_modules" \
       -o -path "$repo/docs" -o -path "$repo/test" -o -path "$repo/tests" \
       -o -path "$repo/fixtures" \) -prune -o -type f \
    \( -name '*.qml' -o -name '*.js' -o -name '*.mjs' -o -name '*.sh' -o -name '*.bash' \
       -o -name '*.py' -o -name '*.rb' -o -name '*.pl' -o -name '*.lua' -o -name '*.fish' \
       -o -name '*.zsh' -o -name '*.desktop' -o -name '*.service' -o -name '*.sudoers' \
       -o -name '*.toml' -o -name '*.yaml' -o -name '*.yml' \) -print0 >"$discovered"; then
  error 'source file discovery failed; preflight is incomplete'
  exit 2
fi
while IFS= read -r -d '' file; do scan_files+=("$file"); done <"$discovered"

probe() {
  local message=$1 pattern=$2 matches=''
  if ((${#scan_files[@]})); then matches=$(rg -n -i -- "$pattern" "${scan_files[@]}" 2>/dev/null || true); fi
  if [[ -n $matches ]]; then
    sed -n '1,20p' <<<"$matches"
    [[ $(wc -l <<<"$matches") -le 20 ]] || printf '... additional matches omitted\n'
    warn "$message"
  fi
}

probe 'download-to-shell pattern needs remediation' 'curl[^|\n]*\|[[:space:]]*(ba)?sh|wget[^|\n]*\|[[:space:]]*(ba)?sh'
probe 'remote Git use needs full-SHA pin and detached-checkout review' '--git[=[:space:]]|git[[:space:]]+clone|git[[:space:]]+fetch'
probe 'privilege, package, sudoers, or service-management capability needs review' 'sudo|pkexec|NOPASSWD|/etc/sudoers|pacman|yay|paru|systemctl|loginctl'
probe 'temporary state or process identity needs ownership and path review' '/tmp/|mktemp|XDG_RUNTIME_DIR|kill[[:space:]]|pkill|pidfile|pid_file'
probe 'subprocess lifetime, timeout, output, and recovery need review' 'Process[[:space:]]*\{|execDetached|StdioCollector|SplitParser'
probe 'retained collection needs count/byte bounds and stalled-worker tests' '(queue|backlog|pending).*(concat|push|append)|\.(push|append)\('
probe 'filesystem mutation needs path, symlink, consent, and rollback review' 'rm[[:space:]]+-|unlink|removeRecursively|writeFile|chmod|chown'

if command -v omarchy >/dev/null 2>&1; then
  if omarchy plugin validate "$repo" >/dev/null; then fact 'omarchy plugin validate: passed'; else error 'omarchy plugin validate failed'; fi
else
  warn 'omarchy command unavailable; plugin validation not run'
fi

printf 'Summary: %d error(s), %d review item(s)\n' "$errors" "$warnings"
((errors == 0))
