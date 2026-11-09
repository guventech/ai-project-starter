---
name: hypothesis-debugging
description: Diagnoses reproducible failures and verifies minimal fixes. Use for a failing test, runtime error or unexpected behavior.
disable-model-invocation: true
---

<!-- skills-meta
use_when: A reproducible failure, failing test, or unexpected runtime behavior
do_not_use_when: No reproduction exists yet and cannot be obtained
needs_first: Expected vs actual behavior and smallest reproduction
produces: Root cause, fix, verification commands/results
done_when: Reproduction passes and temporary diagnostics removed
typical_next: test-first-change regression or release-check
weight: standard
-->


# Hypothesis Debugging

1. Capture the expected and actual behavior, exact error and smallest reproduction; redact secrets.
2. Inspect relevant changes and the failing boundary. Form one testable hypothesis at a time.
3. Gather evidence with the least intrusive check. Avoid speculative rewrites.
4. Apply the smallest fix within the approved scope; add a regression test when useful.
5. Run the reproduction and adjacent checks. Remove temporary diagnostics.
Output: root cause, evidence, fix, commands/results and any unresolved uncertainty.
Example: Reproduce a timezone offset error with a fixed timestamp before changing date conversion.

Inspiration: [obra/superpowers](https://github.com/obra/superpowers) systematic-debugging. Independently written reduced workflow; see THIRD_PARTY.md.
