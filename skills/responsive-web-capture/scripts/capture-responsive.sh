#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    'Usage: capture-responsive.sh --name NAME (--url URL | --directory DIR) [options]' \
    '  --output DIR       Evidence root (default: ./visual-evidence)' \
    '  --phase NAME       Evidence phase (default: capture)' \
    '  --matrix NAME      quick, standard, or comprehensive (default: standard)' \
    '  --viewport WxH     Explicit viewport; repeatable and overrides --matrix' \
    '  --port PORT        Port for --directory mode (default: 4173)' \
    '  --browser PATH     Chrome/Chromium executable override'
}

name=''; url=''; directory=''; output='./visual-evidence'; phase='capture'
matrix='standard'; port='4173'; browser=''; explicit_viewports=()
while (($#)); do
  case "$1" in
    --name) name=${2-}; shift 2 ;;
    --url) url=${2-}; shift 2 ;;
    --directory) directory=${2-}; shift 2 ;;
    --output) output=${2-}; shift 2 ;;
    --phase) phase=${2-}; shift 2 ;;
    --matrix) matrix=${2-}; shift 2 ;;
    --viewport) explicit_viewports+=("${2-}"); shift 2 ;;
    --port) port=${2-}; shift 2 ;;
    --browser) browser=${2-}; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done

[[ -n "$name" ]] || { printf '%s\n' '--name is required' >&2; exit 2; }
if [[ -n "$url" && -n "$directory" ]] || [[ -z "$url" && -z "$directory" ]]; then
  printf '%s\n' 'Provide exactly one of --url or --directory' >&2; exit 2
fi
[[ "$name" =~ ^[A-Za-z0-9._-]+$ ]] || { printf '%s\n' 'Invalid --name' >&2; exit 2; }
[[ "$phase" =~ ^[A-Za-z0-9._-]+$ ]] || { printf '%s\n' 'Invalid --phase' >&2; exit 2; }
if [[ ! "$port" =~ ^[0-9]+$ ]] || ((port < 1024 || port > 65535)); then
  printf '%s\n' 'Invalid --port' >&2
  exit 2
fi

if [[ -z "$browser" ]]; then
  for candidate in chromium chromium-browser google-chrome-stable google-chrome chrome; do
    if command -v "$candidate" >/dev/null 2>&1; then browser=$(command -v "$candidate"); break; fi
  done
  [[ -n "$browser" ]] || [[ ! -x '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' ]] || browser='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  [[ -n "$browser" ]] || [[ ! -x '/Applications/Chromium.app/Contents/MacOS/Chromium' ]] || browser='/Applications/Chromium.app/Contents/MacOS/Chromium'
fi
[[ -x "$browser" ]] || { printf '%s\n' 'Chrome or Chromium was not found; pass --browser PATH' >&2; exit 1; }

quick=(390x844 844x390 1440x900 2560x1440)
standard=(390x844 844x390 820x1180 1180x820 1440x1000 1000x1440 2560x1440 1440x2560 2560x1080 1080x2560)
comprehensive=(
  320x568 568x320 360x800 800x360 390x844 844x390 412x915 915x412
  768x1024 1024x768 820x1180 1180x820 1024x1366 1366x1024
  1280x720 720x1280 1366x768 768x1366 1440x900 900x1440
  1920x1080 1080x1920 2560x1440 1440x2560 3440x1440 1440x3440
  3840x2160 2160x3840
)
if ((${#explicit_viewports[@]})); then
  viewports=("${explicit_viewports[@]}")
else
  case "$matrix" in
    quick) viewports=("${quick[@]}") ;;
    standard) viewports=("${standard[@]}") ;;
    comprehensive) viewports=("${comprehensive[@]}") ;;
    *) printf 'Unknown matrix: %s\n' "$matrix" >&2; exit 2 ;;
  esac
fi
for viewport in "${viewports[@]}"; do
  [[ "$viewport" =~ ^[1-9][0-9]{2,4}x[1-9][0-9]{2,4}$ ]] || { printf 'Invalid viewport: %s\n' "$viewport" >&2; exit 2; }
done

evidence_dir=$output/$phase/$name
mkdir -p "$evidence_dir"
server_pid=''
cleanup() { [[ -z "$server_pid" ]] || kill "$server_pid" 2>/dev/null || true; }
trap cleanup EXIT INT TERM
if [[ -n "$directory" ]]; then
  [[ -d "$directory" ]] || { printf 'Directory not found: %s\n' "$directory" >&2; exit 1; }
  command -v python3 >/dev/null 2>&1 || { printf '%s\n' 'python3 is required for --directory mode' >&2; exit 1; }
  python3 -m http.server "$port" --bind 127.0.0.1 --directory "$directory" >"$evidence_dir/server.log" 2>&1 &
  server_pid=$!
  url="http://127.0.0.1:$port/"
fi

ready=0
for _ in {1..40}; do
  if command -v curl >/dev/null 2>&1; then
    curl -fsS "$url" >/dev/null 2>&1 && ready=1 && break
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c 'import sys,urllib.request; urllib.request.urlopen(sys.argv[1],timeout=2).read(1)' "$url" >/dev/null 2>&1 && ready=1 && break
  else
    printf '%s\n' 'curl or python3 is required for readiness checks' >&2; exit 1
  fi
  sleep .25
done
((ready == 1)) || { printf 'URL did not become ready: %s\n' "$url" >&2; exit 1; }

receipt=$evidence_dir/receipt.tsv
printf 'viewport\twidth\theight\tbytes\tsha256\turl\n' >"$receipt"
images=()
for viewport in "${viewports[@]}"; do
  width=${viewport%x*}; height=${viewport#*x}
  screenshot=$evidence_dir/$viewport.png; log=$evidence_dir/$viewport.browser.log
  "$browser" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --force-prefers-reduced-motion --font-render-hinting=none \
    --window-size="$width,$height" --screenshot="$screenshot" "$url" >"$log" 2>&1
  [[ -s "$screenshot" ]] || { printf 'Browser did not create %s\n' "$screenshot" >&2; exit 1; }
  if command -v python3 >/dev/null 2>&1; then
    actual=$(python3 -c 'import struct,sys; d=open(sys.argv[1],"rb").read(24); w,h=struct.unpack(">II",d[16:24]); print(f"{w}x{h}")' "$screenshot")
  elif command -v magick >/dev/null 2>&1; then actual=$(magick identify -format '%wx%h' "$screenshot")
  else printf '%s\n' 'python3 or ImageMagick is required to validate PNG dimensions' >&2; exit 1
  fi
  [[ "$actual" == "$viewport" ]] || { printf '%s rendered as %s\n' "$viewport" "$actual" >&2; exit 1; }
  bytes=$(wc -c <"$screenshot" | tr -d ' ')
  if command -v sha256sum >/dev/null 2>&1; then digest=$(sha256sum "$screenshot" | awk '{print $1}')
  elif command -v shasum >/dev/null 2>&1; then digest=$(shasum -a 256 "$screenshot" | awk '{print $1}')
  else digest='unavailable'; fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$viewport" "$width" "$height" "$bytes" "$digest" "$url" >>"$receipt"
  images+=("$screenshot")
done

contact_sheet=$evidence_dir/contact-sheet.png
if command -v magick >/dev/null 2>&1; then
  magick montage "${images[@]}" -thumbnail '520x520>' -tile 2x -geometry '+16+24' -background '#20242b' "$contact_sheet"
elif command -v montage >/dev/null 2>&1; then
  montage "${images[@]}" -thumbnail '520x520>' -tile 2x -geometry '+16+24' -background '#20242b' "$contact_sheet"
else
  printf '%s\n' 'ImageMagick not found; screenshots and receipt were created without a contact sheet.'
fi

printf 'Captured %s viewport(s) from %s\nEvidence: %s\nReceipt: %s\n' "${#viewports[@]}" "$url" "$evidence_dir" "$receipt"
[[ -s "$contact_sheet" ]] && printf 'Contact sheet: %s\n' "$contact_sheet"
