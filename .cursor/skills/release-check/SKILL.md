---
name: release-check
description: Reviews release readiness and reports evidence. Use before proposing publication or deployment.
disable-model-invocation: true
---

# Release Check

1. Inspect the actual diff and candidate revision, docs/PRD.md, applicable decisions and docs/QUALITY_GATES.md. Link every in-scope shall requirement to evidence; a plan to run a check is not evidence.
2. Run the relevant configured checks against that revision. Record commands, environment and results, including failures, skipped checks and missing application gates. Recheck affected evidence after code changes; do not reuse stale green results.
3. Check the applicable design-review gate (../design-review/SKILL.md): reviewed design, finding dispositions and human approval. Identify drift between design and implementation. For sensitive trust-boundary changes or an audit request, check ../trust-boundary-audit/SKILL.md results, coverage gaps and independent verification. Document why a gate is not applicable; missing execution is unverified, not passed.
4. Inspect migrations, compatibility, configuration, dependency/lockfile changes, secrets handling, rollout and rollback. Check recovery for destructive data changes; report unknown recovery behavior as a blocker.
5. Ask the verifier subagent for an independent, bounded diff review when useful. Keep its read-only constraints and provide the diff, requirement IDs and check evidence; disclose unavailable independence. Resolve findings or record user acceptance of remaining risks.
6. Report ready/blocked for the stated scope with requirement evidence, review dispositions, command results, limitations and rollback readiness. Blocking findings or unverified required gates mean blocked. Do not publish or deploy without user authorization; readiness is not authorization.
Example: For a database change, verify compatibility with both old and new application versions before rollout.
Output: ready/blocked, findings with paths, actual results, limitations and rollback readiness.
Exit: every applicable required gate has current evidence, no release blockers remain, and accepted residual risks have an owner. Template validation alone cannot establish application release readiness.

Lifecycle inspiration: [Addy Osmani's agent skills](https://github.com/addyosmani/agent-skills). Independently written reduced workflow; see THIRD_PARTY.md.
