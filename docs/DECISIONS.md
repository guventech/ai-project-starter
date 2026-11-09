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

## ADR-004: Select overlapping local skills by file path

Date: 2026-11-09. Status: accepted within the authorized setup verification scope.
Context: authenticated Cursor CLI slash attachment selected optional upstream grill-me, tdd and security-audit instead of the project files. The local bodies and installed packs are both intentional.
Options: rename local skills; rewrite upstream names; remove overlapping upstream files; select local workflows by explicit source path.
Decision: document explicit `.cursor/skills/<name>/SKILL.md` selection for these three workflows. Keep the requested local names and complete upstream files intact. The explicit-path loading route was tested.
Consequences: bare slash names remain available for the upstream variants; tasks using this starter's acceptance criteria must select its local paths. Runtime behavior can change with host updates, so record the loaded source when retesting.
Rollback: retire the workaround only after retesting name resolution on the installed host; no package or application migration is needed.
Related paths: AGENTS.md, README.md, docs/CONFIGURATION.md, docs/SETUP.md.

## New decision template

ID/title, date, status, context, options, decision, consequences, rollback and related paths.
