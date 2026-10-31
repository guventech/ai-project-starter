---
name: project-planning
description: Plans new projects and material changes. Use when defining requirements, architecture or an implementation plan.
disable-model-invocation: true
---

# Project Planning

1. Read relevant code and docs/PRD.md. Identify users, constraints and measurable acceptance criteria. Fill the requirements table and self-check it against the wording rules before asking for approval.
2. Separate known facts from assumptions; ask only questions blocking a sound plan.
3. Compare a small set of suitable approaches, including the simplest one. Recommend a stack only when required.
4. Ask the architect subagent to review a bounded design question when complexity warrants it.
5. Propose small steps, affected paths, dependencies, risks, rollback and verification commands.
6. Present the concrete plan for approval. Do not start building while a requirement uses a banned vague word or has no verification method. Existing explicit approval covers its unchanged scope.
7. After approval, record decisions and tasks, implement incrementally and verify acceptance criteria.

Example: For a new booking feature, identify timezone behavior and double-booking constraints before selecting storage.
Output: requirements, assumptions, recommendation, steps, risks, checks and approval status.
