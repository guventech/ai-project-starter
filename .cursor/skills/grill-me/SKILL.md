---
name: grill-me
description: Interviews the user to resolve requirements and design decisions before implementation. Use for an underspecified plan or an explicit grilling session.
disable-model-invocation: true
---

# Grill Me

1. Read relevant code, docs/PRD.md and existing decisions first. Separate facts, assumptions and unanswered decisions; do not ask the user for facts the repository supplies.
2. Ask one question at a time, starting with the decision that blocks the most others. Give concrete alternatives, a recommendation and the consequence of each choice. Wait for the answer before following its branch.
3. Challenge the answer with a failure case or boundary: users and permissions, inputs and outputs, data lifetime, integrations, recovery and measurable success. Cover only branches relevant to this change; do not reopen settled decisions without new evidence.
4. Record answers as requirements and acceptance criteria in docs/PRD.md, material tradeoffs in docs/DECISIONS.md, and remaining questions with an owner and due date. Deferred questions cannot hide an implementation blocker.
5. Summarize the resolved plan, assumptions, exclusions and checks. Exit the interview when every in-scope branch has a decision and there are zero unresolved implementation blockers. If the user stops early, report what remains unresolved and stop dependent work.
6. Return to project-planning for the implementation plan and approval. An interview answer is not implementation approval; existing approval covers unchanged scope. Write no application code during the interview.

Output: decisions, requirement IDs, explicit exclusions, remaining blockers and approval status.
Example: For a booking flow, resolve timezone ownership and competing reservations before discussing storage.

Inspiration: [Matt Pocock's skills](https://github.com/mattpocock/skills). This is an original, reduced workflow for this starter.
