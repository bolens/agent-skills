# Settings and tuning

Read the installed files and current [CachyOS settings documentation](https://wiki.cachyos.org/features/cachyos_settings/)
before changing defaults. Check package ownership and the effective configuration,
including sysctl, udev rules, systemd drop-ins, power management, and user overrides.
Use each subsystem's precedence rules. Prefer a minimal supported local override
to copying the whole packaged settings file, which obscures later updates.

Do not copy a fixed scheduler, governor, swappiness, or GPU environment variable
from an old guide. Identify the measured symptom and installed defaults first.
Separate CPU frequency policy, CPU scheduling, block-device I/O scheduling, and
application launch options. Changing one does not establish the others changed.

For sched-ext, consult the current [sched-ext tutorial](https://wiki.cachyos.org/configuration/sched-ext/)
and installed service/manager help. Verify kernel support, the loaded scheduler,
its flags, and who starts or selects it. Avoid competing managers or simultaneous
manual and service-owned instances. Preserve the previous manager configuration
and verify fallback after stopping a trial scheduler.

For a benchmark, record kernel and scheduler versions, power mode, thermal state,
workload, and baseline. Compare repeated equivalent runs and relevant regressions,
not one favorable score. A desktop responsiveness complaint may originate in a
driver or overloaded application rather than kernel policy.

The settings package includes reporting and paste helpers. Inspect their current
implementation and output path before collecting a report. Keep collection and
upload separate, sanitize the exact artifact to be shared, and preserve the user's
sharing scope. Do not assume an automatic redaction message proves privacy.
