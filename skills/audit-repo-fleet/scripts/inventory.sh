#!/usr/bin/env bash
set -euo pipefail

export GIT_OPTIONAL_LOCKS=0

fleet_root=${1:-.}
max_depth=${2:-3}

if [[ ! -d $fleet_root ]]; then
  printf 'workspace root is not a directory: %s\n' "$fleet_root" >&2
  exit 2
fi
if ! [[ $max_depth =~ ^[1-9][0-9]*$ ]]; then
  printf 'max depth must be a positive integer: %s\n' "$max_depth" >&2
  exit 2
fi
fleet_root=$(cd -- "$fleet_root" && pwd -P)

printf 'repository\tbranch\tupstream\ttracked_changes\tuntracked\tahead\tbehind\tlast_commit\tagents\tconstitution\tworkflows\tupdates\tmanifests\n'

while IFS= read -r -d '' git_dir; do
  repo=${git_dir%/.git}
  name=${repo#"$fleet_root"/}
  [[ $name == "$repo" ]] && name=$(basename "$repo")

  branch=$(git -C "$repo" symbolic-ref --quiet --short HEAD 2>/dev/null || git -C "$repo" rev-parse --short HEAD 2>/dev/null || printf unknown)
  status=$(git -C "$repo" status --porcelain=v1 2>/dev/null || true)
  tracked=$(printf '%s\n' "$status" | awk 'NF && substr($0,1,2) != "??" { count++ } END { print count+0 }')
  untracked=$(printf '%s\n' "$status" | awk 'substr($0,1,2) == "??" { count++ } END { print count+0 }')

  ahead=-
  behind=-
  upstream=-
  if git -C "$repo" rev-parse --abbrev-ref '@{upstream}' >/dev/null 2>&1; then
    upstream=$(git -C "$repo" rev-parse --abbrev-ref '@{upstream}')
    counts=$(git -C "$repo" rev-list --left-right --count 'HEAD...@{upstream}' 2>/dev/null || printf '%s' '- -')
    read -r ahead behind <<<"$counts"
  fi

  last_commit=$(git -C "$repo" log -1 --format=%cs 2>/dev/null || printf unknown)
  [[ -f $repo/AGENTS.md ]] && agents=yes || agents=no
  [[ -f $repo/.specify/memory/constitution.md ]] && constitution=yes || constitution=no
  workflows=0
  if [[ -d $repo/.github/workflows ]]; then
    workflows=$(find "$repo/.github/workflows" -maxdepth 1 -type f \( -name '*.yml' -o -name '*.yaml' \) -print | wc -l)
  fi
  updates=none
  if [[ -f $repo/.github/dependabot.yml && -f $repo/renovate.json ]]; then
    updates=dependabot,renovate
  elif [[ -f $repo/.github/dependabot.yml ]]; then
    updates=dependabot
  elif [[ -f $repo/renovate.json ]]; then
    updates=renovate
  fi

  manifests=()
  for candidate in package.json pyproject.toml Cargo.toml go.mod requirements.txt \
    pnpm-workspace.yaml Dockerfile docker-compose.yml compose.yaml Makefile \
    Taskfile.yml justfile Gemfile flake.nix PKGBUILD; do
    [[ -f $repo/$candidate ]] && manifests+=("$candidate")
  done
  manifest_text=-
  if ((${#manifests[@]})); then
    manifest_text=$(IFS=,; printf '%s' "${manifests[*]}")
  fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$name" "$branch" "$upstream" "$tracked" "$untracked" "$ahead" \
    "$behind" "$last_commit" "$agents" "$constitution" "$workflows" \
    "$updates" "$manifest_text"
done < <(find "$fleet_root" -mindepth 1 -maxdepth "$max_depth" -name .git \( -type d -o -type f \) -print0 -prune)
