---
name: tdd
description: Builds behavior through red-green-refactor cycles. Use for approved features or bug fixes with executable behavior checks.
disable-model-invocation: true
---

# TDD

1. Read the approved requirements, existing tests and docs/QUALITY_GATES.md. Choose one observable behavior and the smallest end-to-end slice through its public boundary. Reuse the current test runner; if none exists, propose its setup within the approved scope before adding dependencies.
2. Red: write one test expressing that behavior, including a boundary or failure case when relevant. Run it and observe failure for the intended missing behavior. Fix setup, import or syntax failures before treating the test as red. A passing test does not demonstrate a missing behavior.
3. Green: implement only what this slice needs. Run the focused test until it passes. Do not weaken the assertion to fit the implementation or mock away the boundary under test.
4. Refactor after green: remove duplication or improve structure while preserving behavior. Rerun the focused and affected regression tests. If a refactor fails, restore green before taking another slice.
5. Repeat red-green-refactor one slice at a time; do not write an entire test suite before implementation. Exercise failure paths through observable outcomes, not private call order. Use isolated fixtures rather than production services or secrets.
6. Run the relevant configured gates and link each completed requirement to evidence. For prose or metadata-only changes, use inspection or existing validation rather than artificial behavior tests; disclose anything not executed.

Output: requirement/slice, observed red failure, green result, refactor result and remaining checks.
Exit: each implemented slice has observed red/green evidence and affected regressions pass; missing checks remain explicit.

Inspiration: [Matt Pocock's skills](https://github.com/mattpocock/skills). Independently written reduced workflow; see THIRD_PARTY.md.
