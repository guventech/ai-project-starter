---
name: release-check
description: Reviews release readiness and reports evidence. Use before proposing publication or deployment.
disable-model-invocation: true
---

# Release Check

1. Inspect the diff, acceptance criteria and docs/QUALITY_GATES.md.
2. Run relevant configured checks; identify missing gates rather than treating them as passed.
3. Inspect migrations, configuration, dependency changes, secrets handling and rollback.
4. Ask the verifier subagent for an independent, bounded review when useful.
5. Report blockers, evidence and skipped checks. Do not publish or deploy without user authorization.
Example: For a database change, verify compatibility with both old and new application versions before rollout.
Output: ready/blocked, findings with paths, actual results, limitations and rollback readiness.
