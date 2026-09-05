# Processes and lifecycle

Use native shell/service APIs when they provide the needed state. When a helper is necessary, pass executable and arguments separately through `Process.command`. Shell interpolation requires explicit justification and correct argument handling. Check working directory, environment, exit status, and structured output before accepting a result. [Quickshell Process API](https://quickshell.org/docs/v0.1.0/types/Quickshell.Io/Process/).

Give each process, timer, watcher, connection, and retry an owner and end condition. Coalesce or supersede redundant reads, bound retained work by count and bytes where input can grow, and give stalled work a timeout. A retry must have delay/backoff and a finite policy. Do not create an immediate restart loop on every process exit.

Track request generation or identity so an old completion cannot overwrite newer settings or state after reload, monitor removal, or another request. Define how malformed, oversized, partial, and failed output is handled. A collector buffering until EOF needs an output bound, not just a timeout. Preserve a usable last-known value only when its staleness is visible and acceptable.

Detached processes outlive Quickshell ownership and are not tracked by the ordinary `running` property. Use them only when independent lifetime is intentional and another component owns cleanup. Verify whether helper children survive termination; do not assume stopping the direct process cleans up its whole tree.

On disable or destruction, stop scheduling work, invalidate pending results, disconnect owned callbacks, and terminate owned activity according to the host contract. Hidden UI may retain services intentionally, so visibility and ownership are separate decisions. Test repeated lifecycle transitions for duplicate subscriptions, growing queues, leaked helpers, and stale state.

IPC methods should have explicit argument validation, target scope, and bounded work. A local IPC origin does not make arbitrary shell text or file paths trustworthy. Keep privileged actions behind the repository's existing reviewed helper boundary.
