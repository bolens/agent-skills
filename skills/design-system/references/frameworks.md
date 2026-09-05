# Framework integration

Check the installed major version and repository conventions before using current examples. This guide routes recurring decisions, not framework upgrades.

## Tailwind CSS

Tailwind v4 uses CSS theme variables through `@theme` to define utility-generating tokens. Ordinary custom properties need not become theme tokens. Inspect existing aliases, dark-mode selectors, and source scanning before adding a parallel configuration. Preserve a v3 configuration when no migration is requested. Do not copy v4 syntax into a v3 project. [Theme variables](https://tailwindcss.com/docs/theme).

Avoid constructing utility class names from arbitrary runtime fragments. Use explicit variant mappings or CSS variables when appropriate so the installed build can discover the required styles. Check the production build, not just a development screenshot. [Detecting classes](https://tailwindcss.com/docs/detecting-classes-in-source-files).

## shadcn/ui and headless primitives

shadcn/ui provides component source that the project owns. Inspect its local modifications and chosen primitive backend before running generators or replacing files. Preserve that ownership rather than assuming a package update updates copied components. [shadcn/ui](https://ui.shadcn.com/docs).

For Radix, Base UI, React Aria, Headless UI, or another existing primitive, preserve its state, focus, and event contracts. Check the actual library/version when composing children, refs, portals, and controlled state. Do not assume APIs are interchangeable because the components have similar names.

Radix supports CSS enter/exit animation and imperative animation integration, with `forceMount` where the animation library must own unmount timing. Use it only with a complete presence/focus plan, not as a blanket fix that leaves closed content active. [Radix animation](https://www.radix-ui.com/primitives/docs/guides/animation).

## Storybook and component evidence

Reuse the existing stories, decorators, theme setup, mocks, and test integration. Keep state examples deterministic. Storybook interaction tests use a `play` function to exercise rendered behavior. Use the installed version's test imports and runner rather than copying old `@storybook/testing-library` or new imports indiscriminately. [Interaction testing](https://storybook.js.org/docs/writing-tests/interaction-testing).

Use accessibility checks in stories to catch repeatable component violations, then test keyboard/focus behavior manually or through interactions. Visual regression covers appearance separately. Do not add a hosted visual testing service or upload proprietary stories merely to run local comparisons. [Accessibility testing](https://storybook.js.org/docs/writing-tests/accessibility-testing).

For applications without Storybook, use an existing component test harness or a small local state gallery. Installing a documentation platform is not a prerequisite for testing a button.
