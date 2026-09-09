# Content clarity and cognitive accessibility

Use this for labels, instructions, errors, navigation wording, and recovery flows.
Follow [WAI supplemental guidance](https://www.w3.org/WAI/WCAG2/supplemental/) for
cognitive accessibility. It extends practical usability guidance beyond WCAG
success criteria; do not label every recommendation a normative WCAG failure.

Name the action and its consequence in familiar terms. Keep instructions near
the affected control and explain required formats before submission. Use consistent
terms for the same object and distinguish actions such as saving a draft and
publishing it. Preserve necessary technical precision for the actual audience.

Errors should identify the problem, preserve valid work, and offer an available
next step. Do not blame the user or recommend retry when the operation may already
have succeeded. Pair visible messages with the appropriate accessible association
or announcement; repeated assertive messages can interrupt task completion.
Use [forms and data state](../../forms-and-data-state/SKILL.md) for recovery state.

Keep instructions independent of color, position, or an icon alone. Use descriptive
links and controls, progressive detail where it helps, and predictable help.
Do not simplify legal or domain meaning away. A reading score is a diagnostic,
not proof of comprehension; test the affected task with representative users when
available and report that coverage separately from automated checks.

Use [internationalization](../../internationalization/SKILL.md) when wording,
layout, or messages must work across locales. Keep translator context and test
translated labels/errors together with their controls, not as isolated strings.
