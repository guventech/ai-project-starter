# Project tasks

## Starter workflow enhancement (2026-11-09)

Owner: repository maintainer. Scope and acceptance criteria: docs/PRD.md, REQ-001–REQ-009.

- [x] Define measurable requirements and obtain plan approval.
- [x] Add four skills and strengthen planning, release checks and both reviewers.
- [x] Document optional upstream installation, review gates and runtime limits.
- [x] Verify required-skill removal detection through observed red/green results.
- [x] Run configured starter commands and record evidence in docs/QUALITY_GATES.md.

## Authorized setup follow-up (2026-11-09)

Owner: repository maintainer. Acceptance criteria: SETUP-001–SETUP-003 in docs/PRD.md. Evidence: docs/SETUP.md and docs/QUALITY_GATES.md.

- [x] Install the four optional packs outside the starter and record source revisions.
- [x] Configure and inspect required Windows/Linux CI checks on main.
- [x] Install the official Agent CLI and record the editor/CLI versions.
- [x] Complete bounded CLI attachment/path-loading and native reviewer probes after authentication; record write refusal, canary results, collisions and enforcement limits in SETUP.md.

## One-command project helper (approved)

Owner: repository maintainer. Acceptance criteria: CHAT-001–CHAT-006 in docs/PRD.md. Evidence: docs/SETUP.md and docs/QUALITY_GATES.md.

- [x] Add the two-mode project-helper entry point and a dependency-free first-install script.
- [x] Bundle the seven local workflows and two reviewers without duplicate skill discovery.
- [x] Test overwrite refusal, repeat installation and required-skill removal detection.
- [x] Install for the current Cursor user and test invocation from separate workspaces.
- [x] Apply the independent review's nonempty-target clarification.
- [x] Finish final CLI nonempty-target and concrete-plan probes; no fixture files changed.

Publication follows the protected branch/PR workflow after CI; the final delivery reports the actual merge result.

## CI Node.js 24 action upgrade (MAINT-001)

Owner: repository maintainer. Acceptance criteria: MAINT-001 in docs/PRD.md.

- [x] Bump `actions/checkout` to `@v5` and `actions/setup-python` to `@v6` (smallest Node.js 24 majors; avoid checkout `@v6` credential-persistence change).
- [x] Keep job names, OS matrix, Python 3.12 and workflow permissions unchanged.
- [x] Confirm Windows and Linux CI jobs pass on the maintenance PR; update QUALITY_GATES with run [42583862239](https://github.com/guventech/ai-project-starter/actions/runs/42583862239).
- [x] Merge through the protected-branch PR workflow after green checks ([PR #5](https://github.com/guventech/ai-project-starter/pull/5)).

MAINT-002 (tool-level write probe) and MAINT-003 (full design/security review target) remain queued.

## Prior-art research workflow (approved)

Owner: repository maintainer. Acceptance criteria: PRIOR-001–PRIOR-005 in docs/PRD.md.

- [x] Add `.cursor/skills/prior-art/SKILL.md` with capped search, fit-first ranking and adopt approval rules.
- [x] Wire hybrid invocation into project-helper and a planning pointer; bundle via installer/validator/tests.
- [x] Update README, AGENTS, PRD, DECISIONS, CONFIGURATION and quality-gate evidence rows.
- [x] Run local starter checks (validator + unittest); PR CI passed both OS jobs ([42586480260](https://github.com/guventech/ai-project-starter/actions/runs/42586480260)).
- [x] Independent read-only review of the skill/helper text (PRIOR IDs passed; isolation unverified); merge through protected PR workflow pending.
- [x] Document that existing `~/.cursor/skills/project-helper` installs must be removed/renamed before reinstall to receive `prior-art` (AGENTS.md).

## Application adoption checklist

- [ ] Define each requirement in the PRD table with a measurable check and a verification method.
- [ ] Review architecture and approve the implementation plan.
- [ ] Select stack and record actual commands in QUALITY_GATES.md.
- [ ] Implement one end-to-end user journey with tests.
- [ ] Add real application checks to CI.
- [ ] Verify behavior, failure paths and deployment rollback.

Track each task with owner, acceptance criteria, status and verification evidence.
