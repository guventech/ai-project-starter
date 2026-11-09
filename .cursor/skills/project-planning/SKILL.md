---
name: project-planning
description: Plans new projects and material changes. Use when defining requirements, architecture or an implementation plan.
disable-model-invocation: true
---

# Project Planning

1. Read relevant code and docs/PRD.md. Identify users, constraints and measurable acceptance criteria. Fill the requirements table and self-check it against the wording rules before asking for approval.
2. Separate known facts from assumptions. For unresolved requirements, use the interview procedure in ../grill-me/SKILL.md: ask one decision at a time and record answers until no implementation blockers remain. Do not repeat an interview when the requirements are settled.
3. Compare a small set of suitable approaches, including the simplest one. When prior-art research applies, follow ../prior-art/SKILL.md first or reuse its memo; rank fit before popularity. Do not clone or copy a candidate into the target without explicit approval of that candidate. Recommend a stack only when required.
4. Ask the architect subagent to review a bounded design question when complexity warrants it. For a new system or material design change, use ../design-review/SKILL.md: draft with context, review with at least two fresh agents, resolve findings and record approval. Keep the gate unverified if fresh contexts are unavailable. For a bounded change within an approved design, record why another design review is not applicable.
5. Propose small steps, affected paths, dependencies, risks, rollback and verification commands. Give each step observable exit criteria and link it to requirement IDs. Use ../tdd/SKILL.md for behavior changes and ../security-audit/SKILL.md for audit work or changes to sensitive trust boundaries; scope these checks to the change.
6. Present the concrete plan for approval. Do not start building while a requirement uses a banned vague word or has no verification method. Existing explicit approval covers its unchanged scope.
7. After approval, record decisions and tasks, implement incrementally and verify acceptance criteria.

Example: For a new booking feature, identify timezone behavior and double-booking constraints before selecting storage.
Output: requirements, assumptions, recommendation, steps, risks, checks and approval status.
Exit: requirements pass the wording check, no implementation blockers remain, the applicable design-review gate is completed with both fresh reviews and finding dispositions, and the user has approved the concrete plan. Record a reason when the design gate is not applicable. Existing approval covers routine fixes within that scope.
