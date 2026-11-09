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
Consequences: the original seven local workflows (later expanded; see ADR-005 and ADR-007) work as documented procedures without upstream installation, but do not include upstream harnesses, schemas or complete review coverage. Fresh-context reviews require host support and remain unverified when unavailable. Optional installations can collide with local names or omit shared references.
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

## ADR-005: Bundle a single user-level project command

Date: 2026-11-09. Status: accepted; concrete plan approved by the user.
Context: manually copying skills and choosing workflows made both new-project setup and existing-project assessment too complicated for the user.
Options: build a separate desktop/web app; maintain instructions for manual adoption; add one user-level chat entry point that selects the existing procedures.
Decision: implement `/project-helper` with two modes and a dependency-free installer. Package the then-existing procedures and two reviewer roles as `.md` references beside the entry skill, rewriting their known internal paths (eight workflows after ADR-007). Keep only one discoverable SKILL.md in the global package.
Consequences: the command runs from other workspaces without installing upstream packs or retaining the source checkout path. Installed snapshots need a deliberate update and cannot silently overwrite customizations. Host permissions, fresh reviewers and project-specific checks remain external capabilities; the command cannot guarantee them.
Rollback: revert the entry point/installer diff; remove the installed package only after checking its resolved path and user edits. Other projects are not modified by installation.
Related paths: .cursor/skills/project-helper/, scripts/install_chat_command.py, tests/test_install_chat_command.py, README.md, docs/CONFIGURATION.md.

## ADR-006: Prefer checkout v5 for the Node.js 24 CI bump

Date: 2026-11-09. Status: accepted; maintenance plan approved by the user.
Context: MAINT-001 requires Node.js 24 action releases. Both `actions/checkout@v5` and `@v6` run on Node.js 24; `@v6` also changes credential persistence.
Options: bump only to the minimum Node.js 24 majors; jump checkout to `@v6` with setup-python `@v6`; pin exact patch tags.
Decision: use `actions/checkout@v5` and `actions/setup-python@v6`, keep floating major tags, and verify both OS jobs on a PR before merge.
Consequences: clears the Node.js 20 deprecation path with less behavioral change than checkout `@v6`. Future checkout `@v6` adoption stays a separate decision.
Rollback: revert the workflow/docs commit on the maintenance branch or close the PR.
Related paths: .github/workflows/ci.yml, docs/PRD.md, docs/QUALITY_GATES.md, docs/TASKS.md.

## ADR-007: Add hybrid prior-art research before planning

Date: 2026-11-09. Status: accepted; concrete plan approved by the user.
Context: Users want GitHub/web prior art for new projects and substantial improvements without burning tokens on tiny fixes or adopting a repo because it has many stars.
Options: always-on search; opt-in only; hybrid trigger with a dedicated skill invoked by project-helper.
Decision: add `/prior-art`, invoke it from `/project-helper` by path, run always for new projects and for non-tiny improve goals, rank fit then activity/license then stars, adopt only after explicit candidate approval, and persist docs only when a candidate is adopted or seriously considered.
Consequences: eight bundled workflows ship with the installer; global installs need a manual reinstall to receive the new reference; missing search tools leave the gate unverified and planning continues.
Rollback: revert the prior-art skill and helper/installer/docs changes; remove only a freshly installed package after checking for user edits.
Related paths: .cursor/skills/prior-art/, .cursor/skills/project-helper/, .cursor/skills/project-planning/, scripts/install_chat_command.py, scripts/validate_starter.py, tests/, README.md, AGENTS.md.

## ADR-008: Single skill-inventory source for docs and tools

Date: 2026-11-09. Status: accepted; Phase A integrity plan approved by the user.
Context: After prior-art landed, PRD/QUALITY_GATES/CONFIGURATION/SETUP still said seven skills or omitted prior-art while the validator required nine.
Options: edit docs once without tests; add inventory assertions without sharing constants; centralize WORKFLOWS/REQUIRED_SKILLS and test CONFIGURATION/README coverage.
Decision: add `scripts/skill_inventory.py`, import it from the validator and installer, and fail tests when CONFIGURATION or README omit a required skill name.
Consequences: skill-count drift is caught by CI; docs must list every required skill by exact name. Installer overwrite/upgrade behavior stays unchanged until Phase B.
Rollback: revert the inventory module and doc/test changes on the feature branch or PR.
Related paths: scripts/skill_inventory.py, scripts/validate_starter.py, scripts/install_chat_command.py, tests/test_starter.py, docs/CONFIGURATION.md, docs/PRD.md, docs/QUALITY_GATES.md, docs/SETUP.md.

## New decision template

ID/title, date, status, context, options, decision, consequences, rollback and related paths.
