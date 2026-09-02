---
name: tdd
description: Develop a feature or bug fix through a practical red-green-refactor loop using the repository's native test tooling. Use when the user requests test-first development, red-green-refactor, regression tests, integration tests, or wants behavior established before implementation.
---

# Test-Driven Development

Read the nearest `AGENTS.md`, contributor guidance, relevant specification, and existing tests. Match the repository's domain vocabulary and test conventions.

## Choose the test surface

Test observable behavior through the narrowest stable public interface that proves the requirement. For straightforward changes, infer the seam from existing tests and proceed. Ask the user only when choosing a seam would materially lock in an uncertain interface.

Read [tests.md](tests.md) for examples and [mocking.md](mocking.md) when a boundary may need a test double. Consult `codebase-design` only when the interface itself is the design problem.

## Loop

1. Write one focused test that fails for the intended reason.
2. Run it with the repository's canonical focused-test command and preserve the failure evidence.
3. Implement the smallest coherent behavior that makes it pass.
4. Run the focused test, then relevant neighboring checks.
5. Refactor while green when it improves clarity without expanding scope; rerun tests after each refactor.
6. Repeat in vertical slices until the requested behavior is covered.

Prefer literals or specification examples as independent expected values. Avoid testing private methods, mocking internal collaborators, tautological expectations, and broad snapshots with weak behavioral signal.

Do not install test frameworks, rewrite established test architecture, or expand coverage beyond the requested behavior without explaining why. If a useful regression test is impractical, state the constraint and use the strongest available verification.
