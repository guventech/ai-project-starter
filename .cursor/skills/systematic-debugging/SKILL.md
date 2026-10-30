---
name: systematic-debugging
description: Diagnoses reproducible failures and verifies minimal fixes. Use for a failing test, runtime error or unexpected behavior.
disable-model-invocation: true
---

# Systematic Debugging

1. Capture the expected and actual behavior, exact error and smallest reproduction; redact secrets.
2. Inspect relevant changes and the failing boundary. Form one testable hypothesis at a time.
3. Gather evidence with the least intrusive check. Avoid speculative rewrites.
4. Apply the smallest fix within the approved scope; add a regression test when useful.
5. Run the reproduction and adjacent checks. Remove temporary diagnostics.
Output: root cause, evidence, fix, commands/results and any unresolved uncertainty.
Example: Reproduce a timezone offset error with a fixed timestamp before changing date conversion.
