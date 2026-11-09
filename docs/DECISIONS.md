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

## ADR-003: Compose concise local review workflows

Date: 2026-11-09. Status: accepted; enhancement plan approved by the user.
Context: CURSOR_UPDATE_PROMPT.md requests interviews, TDD, fresh-context design review and a multi-phase security audit without growing a stack-specific framework.
Options: vendor full external packs; depend on user-installed packs; write concise local procedures and document optional upstream installation.
Decision: use the third option, retaining explicit skill invocation, inherited models and read-only review agents. Local procedures use original wording and link their inspirations. Keep the existing Python validator and extend its required-skill coverage without dependencies.
Consequences: seven local skills work as documented procedures without upstream installation, but do not include upstream harnesses, schemas or complete review coverage. Fresh-context reviews require host support and remain unverified when unavailable. Optional installations can collide with local names or omit shared references.
Rollback: revert the enhancement diff; no application, dependency, storage or deployment changes require migration. Preserve unrelated user changes.
Related paths: .cursor/skills/, .cursor/agents/, README.md, docs/CONFIGURATION.md, scripts/validate_starter.py, tests/test_starter.py.

## New decision template
ID/title, date, status, context, options, decision, consequences, rollback and related paths.
