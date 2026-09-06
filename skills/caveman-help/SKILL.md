---
name: caveman-help
description: >
  Quick-reference card for caveman modes, skills and commands.
  Trigger: /caveman-help or "caveman help".
---

# Caveman Help

Display this reference card when invoked. One-shot — do NOT change mode, write flag files, or persist anything. Output in caveman style.

## Modes

| Mode | Trigger | What change |
|------|---------|-------------|
| **Lite** | `/caveman lite` | Drop filler. Keep sentence structure. |
| **Full** | `/caveman` | Drop articles, filler, pleasantries, hedging. Fragments OK. Default. |
| **Ultra** | `/caveman ultra` | Extreme compression. Bare fragments. Tables over prose. |
| **Wenyan-Lite** | `/caveman wenyan-lite` | Classical Chinese style, light compression. |
| **Wenyan-Full** | `/caveman wenyan` | Full 文言文. Maximum classical terseness. |
| **Wenyan-Ultra** | `/caveman wenyan-ultra` | Extreme. Ancient scholar on a budget. |

Mode stick until changed or session end.

## Skills

| Skill | Trigger | What it do |
|-------|---------|-----------|
| **caveman-commit** | `/caveman-commit` | Conventional Commit messages. Aim for 50 characters, maximum 72. |
| **caveman-review** | `/caveman-review` | Terse findings: `file:line: [P2] trigger and consequence. Fix.` |
| **caveman-compress** | `/caveman-compress <file>` | Compress supported prose files with a preserved backup. Savings depend on the input. |
| **caveman-help** | `/caveman-help` | This card. |

## Deactivate

Say "stop caveman" or "normal mode". Resume anytime with `/caveman`.

## Language

Keep user's language by default. User write Portuguese → reply Portuguese caveman. Compress the style, not the language. Technical terms, code, commands, commit types, and exact error strings stay verbatim unless user ask for translation.

## Select a mode in this collection

The packaged skill defaults to `full`. Select another mode explicitly with the
commands above. This collection does not include automatic session-activation
hooks or a configuration reader. Setting `CAVEMAN_DEFAULT_MODE` or editing an
upstream config file does not configure these packaged skills.

## More

Full docs: https://github.com/JuliusBrussee/caveman
