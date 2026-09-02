#!/usr/bin/env bash
set -u

mode=quick
output=

usage() { printf '%s\n' 'usage: collect-health.sh [quick|full] [--output PATH]'; }

while [ "$#" -gt 0 ]; do
  case "$1" in
    quick|full) mode=$1 ;;
    --output) shift; [ "$#" -gt 0 ] || { usage >&2; exit 2; }; output=$1 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
  shift
done

run() {
  label=$1
  shift
  printf '\n## %s\n' "$label"
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'UNAVAILABLE: %s is not installed\n' "$1"
    return 0
  fi
  "$@" 2>&1 || printf 'CHECK_FAILED: exit=%s\n' "$?"
}

session_environment() {
  printf '\n## Session environment\n'
  for name in XDG_CURRENT_DESKTOP XDG_SESSION_DESKTOP XDG_SESSION_TYPE WAYLAND_DISPLAY DISPLAY HYPRLAND_INSTANCE_SIGNATURE DBUS_SESSION_BUS_ADDRESS; do
    value=$(printenv "$name" 2>/dev/null || true)
    if [ -n "$value" ]; then
      printf '%s=%s\n' "$name" "$value"
    else
      printf '%s=UNSET\n' "$name"
    fi
  done
}

collect() {
  printf '# Workstation health snapshot\n'
  printf 'mode=%s\ncollected_at=%s\n' "$mode" "$(date --iso-8601=seconds 2>/dev/null || date)"
  run 'Kernel and host' uname -a
  run 'Uptime and load' uptime
  run 'Memory' free -h
  run 'Filesystem capacity' df -hT
  run 'Failed system units' systemctl --failed --no-pager --no-legend
  run 'Failed user units' systemctl --user --failed --no-pager --no-legend
  run 'Recent coredumps' coredumpctl --no-pager --since '-7 days'
  run 'Mount verification' findmnt --verify --verbose
  run 'Block devices' lsblk -o NAME,TYPE,FSTYPE,SIZE,FSUSE%,MOUNTPOINTS
  run 'Package database lock' stat /var/lib/pacman/db.lck
  session_environment

  [ "$mode" = full ] || return 0
  run 'Journal errors this boot' journalctl -b -p err --no-pager -n 200
  run 'Kernel warnings this boot' journalctl -k -b -p warning --no-pager -n 200
  run 'Pressure' vmstat 1 5
  run 'Top processes' ps -eo pid,ppid,stat,%cpu,%mem,comm --sort=-%cpu
  run 'Network links and addresses' ip -brief address
  run 'Routes' ip route
  run 'Sensors' sensors
  run 'PCI graphics' lspci -k
  run 'Hyprland version' hyprctl version
  run 'Hyprland config errors' hyprctl configerrors
  run 'Pending repository updates' checkupdates
  run 'Foreign packages' pacman -Qm
  run 'Orphan packages' pacman -Qdt
}

if [ -n "$output" ]; then
  umask 077
  collect >"$output"
  printf 'wrote %s\n' "$output"
else
  collect
fi
