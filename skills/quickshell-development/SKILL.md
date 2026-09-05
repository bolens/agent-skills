---
name: quickshell-development
description: Implement and debug Quickshell/QML shell components and Omarchy plugins, including reactive state, process ownership, IPC, monitor lifecycle, and graphical behavior. Use for shell code development, not ordinary desktop configuration or a read-only marketplace audit.
---

# Quickshell development

Fit the component into the existing shell's ownership and lifecycle. Read repository instructions, plugin entry points, host integration, settings schema, and supported Quickshell/Qt versions before choosing APIs. Check installed types and version-matched official documentation rather than copying examples from another release.

## Model ownership and state

Identify which objects live once per shell, once per screen, or once per transient view. Keep shared services mounted independently of a panel's visibility. Use the repository's stable screen identity and define removal/reconnection behavior. Do not use a transient array index as persistent monitor identity. When changing persisted identity keys, migrate known mappings and preserve ambiguous legacy settings without assigning them to an unrelated monitor.

Keep a clear source of truth for settings, runtime state, and derived presentation. Preserve bindings when updating state. Imperative assignment can remove a QML property binding, so fix the owning state or deliberately establish a new binding instead of repeatedly synchronizing copies. Avoid binding loops and side effects in expressions. [Qt property bindings](https://doc.qt.io/qt-6/qtqml-syntax-propertybinding.html).

Read [processes and lifecycle](references/processes-and-lifecycle.md) for helpers, watchers, IPC, asynchronous work, or reload behavior. Keep visual delegates separate from shared command execution so adding a monitor does not multiply background jobs.

## Implement and verify

Reuse the shell's public integration, settings, and IPC contracts. Validate external values before applying them. Preserve unknown settings when the repository's schema requires forward compatibility. Write configuration through its established persistence path, with failure handling and without truncating the user's source on parse errors.

Use existing component tokens, keyboard/focus conventions, accessible names, and motion controls. Test interrupted transitions and hidden/unmounted states. Browser CSS/GSAP guidance does not establish QML animation behavior. Do not replace the stock bar or launch another shell instance merely to insert a component into an existing host.

Run the repository's QML lint/type checks with its import paths and versions, then behavior tests for changed state/lifecycle logic. Exercise relevant show/hide, enable/disable, reload, monitor add/remove, failed helper, and stale response cases. Use the repository's isolated graphical harness or an authorized test session. Real Wayland focus, layering, scale, and input behavior needs graphical evidence; offscreen tests or source-pattern checks cannot prove it.

Use [omarchy](../omarchy/SKILL.md) when the requested change edits live desktop configuration. Use [audit-omarchy-plugin](../audit-omarchy-plugin/SKILL.md) for a separate publication/readiness audit and [babysit](../babysit/SKILL.md) for PR or release follow-through. Do not install or reload a live plugin merely to complete a source-only change.

Report implementation, ownership/lifecycle decisions, regression checks, graphical observations, and environmental skips. Keep runtime proof distinct from marketplace policy validation.
