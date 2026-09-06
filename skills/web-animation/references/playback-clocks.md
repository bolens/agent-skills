# Playback clocks

Use this guidance for custom timeline players and synchronized scenes. Prefer
the existing runtime's timeline controls when they satisfy the motion contract.
A hover transition does not need a custom clock.

Keep the serializable scene and timing data separate from playback state and
rendered effects. Drive synchronized tracks from one logical playhead. Evaluate
their visual state at a supplied time so seeking does not depend on having
rendered every earlier frame. Keep business side effects outside this evaluation.

For a custom clock, calculate progress from elapsed monotonic time and a timeline
anchor rather than counting frames. On a rate or direction change, sample the
old trajectory first, then anchor the new trajectory at the same position. Pause
must exclude paused wall time, and a seek must establish the next playback anchor.
Define whether returning from a hidden tab catches up or resumes from suspension.

Specify endpoint and loop behavior, including reverse playback, loop subranges,
zero duration, invalid rates, and jumps spanning several loop periods. Avoid
letting a zero-length loop create division by zero. Maintain one scheduled frame
callback per player and cancel it on teardown.

Inject a frame scheduler or use the existing runtime's test clock. Check these
observable cases where supported:

- Repeated play calls leave one pending frame callback.
- Pause, advance wall time, then resume without a playhead jump.
- Seek during playback, then change rate or direction without discontinuity.
- Advance across multiple loop periods and verify the expected position.
- Destroy while playing and verify that callbacks cannot recreate the loop.

Pair deterministic timing checks with actual user controls and the
[motion evidence contract](verification.md). These checks prove timing and
lifecycle behavior, not smooth rendering or correct keyboard interaction.

The approach was informed by Netviz's injectable scenario clock and tests at the
revision recorded in the [source audit](../../../docs/audits/2026-09-05-netviz-sentrux.md).
No Netviz runtime or source code is bundled here.
