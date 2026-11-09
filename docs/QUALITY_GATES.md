# Quality gates

## Starter checks (configured)
- `python scripts/validate_starter.py`: required files and Cursor metadata.
- `python -m unittest discover -s tests -v`: validator failure detection and chat-command installation/overwrite protection.
CI runs both on Linux and Windows using Python 3.12.

## Review gates

- Requirements/planning: before nontrivial implementation, fill docs/PRD.md, check requirement wording and verification methods, resolve blocking questions with `/grill-me` when needed, and obtain approval of the concrete plan. Existing approval covers unchanged scope.
- Design: use `/design-review` for a new system or material design change. Record the design revision, at least two fresh reviewer contexts and scopes, finding dispositions and human approval. No inherited conversation is allowed for goldfish reviewers. If the host cannot provide fresh contexts, the gate is unverified. A bounded change under an approved design can record this gate as not applicable with a reason.
- Behavior: use `/tdd` for executable behavior changes. Record the intended red failure, green result and affected regression results for each slice. Documentation changes use inspection and template validation rather than artificial behavior tests.
- Security: use `/security-audit` for a requested audit or sensitive trust-boundary changes. Record reconnaissance, a coverage ledger, hunting evidence, independent candidate verification and a structured report. Every candidate needs a disposition. Missing verification remains needs-validation; missing coverage remains visible. Record non-applicability for changes without security-boundary effects.
- Release: `/release-check` requires current requirement evidence, applicable design/security results, configured check results, remaining risks and rollback readiness. Skipped or unavailable required gates block readiness. Passing starter checks alone does not authorize an application release, publication or deployment.

## Application checks (not configured)
After stack selection, record exact commands, prerequisites and owners for formatting,
linting, type checks if applicable, unit/integration tests, build, dependency scanning,
secrets scanning and critical user-flow tests. Wire them into CI before shipping an app.
For web projects include accessibility and browser checks; for data changes test migrations and rollback.
Missing checks are unconfigured, never implicitly passed. Require the relevant CI checks through repository settings.

## Requirements evidence

Fill this table before calling work done. One row per shall requirement.
The method is test, analysis, demonstration, or inspection.
Evidence is a test name, a screenshot, or a short note.

| Requirement | Verification method | Evidence |
|-------------|---------------------|----------|
| REQ-001 | test | `python scripts/validate_starter.py` passes with all four new skill files and their explicit invocation metadata. |
| REQ-002 | inspection | grill-me steps 2–6 require one question at a time, recorded decisions, zero implementation blockers and plan approval before code. |
| REQ-003 | inspection | tdd steps 2–5 require observed red for the intended reason, one behavior slice, green, refactor and regression checks. |
| REQ-004 | inspection | design-review defines elephant drafting, two isolated goldfish scopes, finding resolution and human approval; unavailable contexts keep review unverified. Skill attachment and two fresh Task probes were observed; the full design workflow was not executed. |
| REQ-005 | inspection | security-audit defines inputs/outputs for four phases, a coverage ledger, fresh verification, three candidate dispositions and report fields including gaps. Explicit local-path loading was observed; the full audit was not executed. |
| REQ-006 | inspection | project-planning links interviews/design review and slice exit criteria; release-check maps requirements to evidence and discloses missing, stale or skipped gates. |
| REQ-007 | inspection | Architect questions assumptions and routes user decisions through the parent; verifier defines goldfish, diff and security modes. Both retain readonly true; starter validation passes. |
| REQ-008 | inspection | README.md and AGENTS.md list seven skills and the four requested commands; CONFIGURATION.md records host/installation limits. All nine requirements have evidence rows here. |
| REQ-009 | test | `test_each_required_skill_removal_detected` checks each of seven skills. Observed red: four failures before validator update; green: all five test methods pass after the update. |
| SETUP-001 | inspection | GitHub branch-protection PUT response confirms both job names restricted to app 15368, strict checks, admin enforcement, pull requests, resolved conversations and blocked force pushes/deletion. |
| SETUP-002 | inspection | Four user-level checkouts and source SHAs are recorded in SETUP.md. Counts: Matt 27, Addy 25, Cloudflare 1, EGM 7 canonical skills. EGM standards and Addy shared references exist; the seven project skill files have no diff. |
| SETUP-003 | demonstration | Authenticated CLI smoke sessions recorded in SETUP.md show explicit attachment/path loading, native reviewer calls, write refusal and an absent parent canary. Three bare slash names selected upstream files; explicit local paths loaded the intended workflows. Tool-level write denial and general isolation remain unproven. |
| MAINT-001 | test | Queued maintenance scope; the CI action upgrade has not been implemented in the project-helper delivery. |
| MAINT-002 | demonstration | Queued maintenance scope; tool-level write denial remains unverified beyond the earlier voluntary-refusal probe. |
| MAINT-003 | inspection | Queued maintenance scope; the target repository for full design/security review still awaits selection. |
| CHAT-001 | demonstration | User-level `/project-helper` in an empty temporary workspace asked exactly the new/improve mode question. Explicit new/existing goals selected their modes without repeating it. Session IDs are in SETUP.md. |
| CHAT-002 | test | Installer tests verify one discoverable SKILL.md, all seven workflow references and both reviewer references, with rewritten internal paths and no environment files. A separate workspace loaded the installed planning/TDD/verifier references. |
| CHAT-003 | demonstration | New-project planning probe used the installed planning reference and wrote no application files; the nonempty-target guard was strengthened after independent review. Final probe evidence is recorded in SETUP.md. |
| CHAT-004 | demonstration | Existing-project fixture review read its own AGENTS.md, calculator source and tests, used bundled TDD/verifier references and returned findings/proposed checks without changing files. This is a bounded routing trial, not a full application audit. |
| CHAT-005 | demonstration | Existing-project routing loaded installed references/tdd.md despite an optional upstream tdd skill. Bundled references use direct paths; no second slash command or configuration copy was requested. Installer tests cover all seven reference files. |
| CHAT-006 | test | Installer tests preserve an occupied destination and a customized command on repeat install. The symlink case is skipped when the host cannot create links; Linux CI executes that case. |

## Project-helper verification

The approved command is installed under `~/.cursor/skills/project-helper`. Initial tests observed the absent installer and missing project-helper validator requirement before implementation. After implementation, the validator passes and the unittest suite runs nine test methods; on this Windows host eight pass and the symlink test is skipped because link creation is unavailable. PR CI provides the cross-platform result. `git diff --check` passes.

A fresh read-only reviewer inspected the entry skill, installer and tests. Its nonempty-target clarification was applied: disclose existing contents and wait for the user's decision before planning writes. The reviewer found no additional concrete installer bug. The final live fixture runs and their limits are recorded in SETUP.md. They exercise menu/routing/approval boundaries in CLI Ask mode, not autonomous application creation, editor UI behavior or OS-enforced write restrictions.

## Enhancement verification record (2026-11-09)

Scope: the approved starter workflow enhancement in docs/PRD.md. This record covers procedure content and starter validation, not a live application release or execution of the prescribed audits.

- `python scripts/validate_starter.py`: passed on Windows, Python 3.13.14.
- `python -m unittest discover -s tests -v`: passed, five test methods including seven skill-removal subcases. Initial sandbox run could not access Windows temporary directories; rerunning with permission reached the expected red failures, then passed after the validator change.
- `git diff --check`: passed.
- Independent procedure review: a read-only reviewer started with no inherited conversation inspected the six planning/review skills and both agents. It checked unavailable fresh contexts and unavailable security reproduction scenarios: the procedures retain unverified/needs-validation outcomes. Its one wording clarification was applied to project-planning's exit criterion to require both fresh reviews when the design gate applies. This is a document review, not live Cursor execution.
- Design gate for this change: not applicable; this extends existing Markdown procedures and required-skill validation within the approved stack-agnostic architecture. The added design-review procedure was inspected, not executed as a live Cursor workflow.
- Security audit gate for this change: not applicable; no application trust boundary, runtime dependency or publishing behavior changed. The audit procedure was inspected, not executed against a target.
- Original local validation did not run Linux/Python 3.12 checks. Subsequent GitHub run [42577848331](https://github.com/guventech/ai-project-starter/actions/runs/42577848331) passed both OS jobs on Python 3.12 for commit 8391565. The authorized setup follow-up installed the optional packs outside the repository and configured branch protection. Authenticated CLI smoke checks then exercised attachment/path loading and both native reviewers; SETUP.md records observations, collisions and limits. Application checks remain unconfigured.
