# Decision log

## ADR-001: Keep the starter stack-agnostic
Status: accepted for the template.
Context: projects have different runtime, UI and storage needs.
Decision: ship agent configuration and starter validation; choose the stack during planning.
Consequence: starter CI is not an application readiness signal.

## ADR-002: Keep requirement writing short
Status: accepted for the template.
Context: the starter should teach clear requirements and stay small.
Decision: keep a small requirements table, TBR rows and risks in docs/PRD.md, and link each shall to evidence in docs/QUALITY_GATES.md.
Consequence: a glossary, a concept of operations, and a full verification matrix wait until a real project needs them.

## New decision template
ID/title, date, status, context, options, decision, consequences, rollback and related paths.
