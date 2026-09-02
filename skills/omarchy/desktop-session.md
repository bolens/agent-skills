# Desktop session diagnostics

Use this guide for a broken or degraded Hyprland desktop session. Start with `workstation-health-triage` when the failing subsystem is unclear.

## Establish session access

Check `XDG_CURRENT_DESKTOP`, `XDG_SESSION_TYPE`, `WAYLAND_DISPLAY`, `HYPRLAND_INSTANCE_SIGNATURE`, and `DBUS_SESSION_BUS_ADDRESS`. A command run from a sandbox, SSH session, service, or terminal outside UWSM may not inherit the graphical session. Report that limitation instead of treating missing IPC as a desktop failure.

## Narrow by subsystem

- Hyprland: `hyprctl version`, `hyprctl configerrors`, monitors, clients, and relevant user journal entries.
- UWSM and environment: inspect the user unit state and activation environment without importing or changing variables.
- Portals: inspect `xdg-desktop-portal*` user units and logs when screen sharing, file pickers, or application launch integration fails.
- Audio and video: inspect PipeWire, WirePlumber, and session-manager units and logs.
- Omarchy shell: inspect Quickshell processes, user units, and logs before restarting the shell.
- Lock and idle: inspect processes, units, and config; do not unlock, kill, or restart them without a direct request.
- Graphics: correlate compositor logs, kernel DRM/GPU messages, renderer identity, and recent driver/package changes.

Keep logs bounded by boot, time, priority, or unit. Correlate timestamps across components. Do not use `omarchy refresh`, restart the session, replace configuration, or modify packaged files as a diagnostic shortcut.

Use `managed-config-drift` when live configuration may differ from its repository or packaged default. Use `sensitive-info-audit` before sharing debug output or screenshots.
