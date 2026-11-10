# Project tasks

## Model-cost guidance (approved Lite docs slice, 2026-11-10)

Owner: repository maintainer. Acceptance criteria: COST-001–COST-004 in docs/PRD.md. Decision: ADR-029. Evidence: docs/QUALITY_GATES.md.

- [x] Add model-cost recommendations and escalation triggers beside process weights in the helper and generated guide.
- [x] Document dated optional OpenRouter/llm-router references, free vs Auto and upstream-claimed Cursor compatibility.
- [x] Record the agreement and scope limits; leave deferred work unchanged.
- [x] Regenerate the guide/baseline and record configured check results (90 tests; six host symlink skips).
- [x] Open a docs PR after green local checks ([PR #39](https://github.com/guventech/ai-project-starter/pull/39)); merge remains outside this slice.

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
- [x] Bundle the local workflows and two reviewers without duplicate skill discovery (eight workflows after prior-art).
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

## MAINT-002 tool-level write probe (Phase C)

Owner: repository maintainer. Acceptance criteria: MAINT-002 in docs/PRD.md. Evidence: docs/SETUP.md and docs/QUALITY_GATES.md.

- [x] Matched-pair probe in isolated temp fixture (writable `generalPurpose` control + fresh `verifier` probe).
- [x] Classify from tool trace + marker state; label `host-denied` (permission/read-only denial; control present; probe absent).
- [x] Record evidence in SETUP/QUALITY_GATES; update PRD status; add ADR-010.
- [ ] Commit/PR only when requested.

MAINT-003 (full design/security review target) remains queued.

## Prior-art research workflow (approved)

Owner: repository maintainer. Acceptance criteria: PRIOR-001–PRIOR-005 in docs/PRD.md.

- [x] Add `.cursor/skills/prior-art/SKILL.md` with capped search, fit-first ranking and adopt approval rules.
- [x] Wire hybrid invocation into project-helper and a planning pointer; bundle via installer/validator/tests.
- [x] Update README, AGENTS, PRD, DECISIONS, CONFIGURATION and quality-gate evidence rows.
- [x] Run local starter checks (validator + unittest); PR CI passed both OS jobs ([42586480260](https://github.com/guventech/ai-project-starter/actions/runs/42586480260)).
- [x] Independent read-only review of the skill/helper text (PRIOR IDs passed; isolation unverified); merged via [PR #7](https://github.com/guventech/ai-project-starter/pull/7).
- [x] Document that existing `~/.cursor/skills/project-helper` installs must be removed/renamed before reinstall to receive `prior-art` (AGENTS.md).

## Phase B installer upgrade (approved)

Owner: repository maintainer. Acceptance criteria: UPGR-001–UPGR-004 in docs/PRD.md.

- [x] Add manifest write, `--upgrade`, `--force` (with upgrade only), and pre-force managed-file backups.
- [x] Cover refuse/upgrade/force/backup behaviors in installer tests.
- [x] Update README/AGENTS/CONFIGURATION and quality-gate evidence; run starter gates locally (validator + 18 unittests, 2 symlink skips).
- [x] Merge through protected-branch PR workflow after green checks ([PR #11](https://github.com/guventech/ai-project-starter/pull/11); CI [42592357225](https://github.com/guventech/ai-project-starter/actions/runs/42592357225)).
- [x] Refresh the maintainer global install with `--upgrade --force` and confirm the installer manifest is present.

## Phase A skill-inventory integrity (approved)

Owner: repository maintainer. Scope: align docs/evidence with the nine-skill / eight-workflow inventory; add drift regression coverage.

- [x] Introduce `scripts/skill_inventory.py` as the shared WORKFLOWS / REQUIRED_SKILLS source for validator, installer and tests.
- [x] Align PRD, QUALITY_GATES, CONFIGURATION, SETUP and TASKS skill counts and install fingerprint evidence.
- [x] Add `test_skill_inventory_sources_agree` with observed red (CONFIGURATION omitted prior-art) then green.
- [x] Run both starter gates locally (validator + 10 unittests, 1 symlink skip) and record results; open PR after CI.
- [x] Merge through protected-branch PR workflow after green checks ([PR #9](https://github.com/guventech/ai-project-starter/pull/9); CI [42589919473](https://github.com/guventech/ai-project-starter/actions/runs/42589919473)).

## Inventory and upgrade hardening (HARD-001 / HARD-002)

Owner: repository maintainer. Acceptance criteria: HARD-001–HARD-002 in docs/PRD.md. Agreed with Codex CLI brainstorm; items 3–5 deferred/blocked.

- [x] Refuse non-forced upgrades when the installer manifest is incomplete or has invalid digests; add regression tests.
- [x] Reject unregistered `.cursor/skills` directories; assert required skill names in AGENTS.md.
- [x] Run both starter gates and record evidence (PR when requested).

## Transactional fresh install (HARD-003)

Owner: repository maintainer. Acceptance criteria: HARD-003 in docs/PRD.md. Agreed with Codex CLI as the next step after PR #14.

- [x] Stage fresh packages beside the destination; promote only after validation.
- [x] Failure-injection tests for mid-write and manifest failures; upgrade-absent path uses the same fresh install.
- [x] Run both starter gates locally; open PR when requested.

## Review F-08 privacy hygiene

Owner: repository maintainer. Acceptance criteria: PRIV-001 in docs/PRD.md.

- [x] Redact personal home paths, session/agent UUIDs and reconstruction chatter from public docs.
- [x] Add home-path validator coverage and regression tests.
- [x] Merge through protected-branch PR after CI ([PR #16](https://github.com/guventech/ai-project-starter/pull/16)).

## Review F-04 attribution

Owner: repository maintainer. Acceptance criteria: ATTR-001 in docs/PRD.md.

- [x] Compare overlapping local skills to upstream revisions; write THIRD_PARTY.md and ADR-012.
- [x] Package THIRD_PARTY.md in the installer; align README and skill footers.
- [x] Merge through protected-branch PR after CI ([PR #17](https://github.com/guventech/ai-project-starter/pull/17)).

## Review F-01 skill rename

Owner: repository maintainer. Acceptance criteria: COLLIDE-001 in docs/PRD.md. Codex + Cursor: keep repo name; rename four colliding skills.

- [x] Rename local skill directories and update inventory, docs, agents and workflows.
- [x] Add colliding-name validator denylist and obsolete reference cleanup on upgrade.
- [x] Merge through protected-branch PR after CI ([PR #19](https://github.com/guventech/ai-project-starter/pull/19)); refresh global install with `--upgrade --force` when authorized.

## Review F-03 skill decision guide

Owner: repository maintainer. Acceptance criteria: GUIDE-001 in docs/PRD.md.

- [x] Add skills-meta blocks, generator, docs/SKILLS.md, and stale-guide validation.
- [x] Replace competing skill inventories with links to the guide.
- [x] Merge through protected-branch PR after CI ([PR #20](https://github.com/guventech/ai-project-starter/pull/20)).

## Review F-05 consumer AGENTS split

Owner: repository maintainer. Acceptance criteria: CONSUME-001 in docs/PRD.md. Codex + Cursor: keep brand; finish F-03 then F-05.

- [x] Move maintainer process to MAINTAINING.md and install/upgrade to docs/INSTALL.md.
- [x] Keep AGENTS.md under 50 lines with consumer rules and links only; reject maintainer markers in validation.
- [x] Merge through protected-branch PR after CI ([PR #21](https://github.com/guventech/ai-project-starter/pull/21)).

## Review F-16 prior-art search hygiene (approved)

Owner: repository maintainer. Acceptance criteria: SEARCH-001–SEARCH-004 in docs/PRD.md.

- [x] Record the approved scope and check requirement wording and verification methods.
- [x] Require query redaction and confidentiality skip; retain untrusted-result, candidate-cap and adoption rules.
- [x] Add one synthetic scenario and extend the existing installer packaging check.
- [x] Run starter gates, inspect the diff and record actual evidence; runtime scenario remains not run.
- [x] Submit [PR #23](https://github.com/guventech/ai-project-starter/pull/23); both protected-branch CI jobs must pass before merge.

## Review F-13 read-only installer check (approved slice)

Owner: repository maintainer. Acceptance criteria: CHECK-001–CHECK-003 in docs/PRD.md. Versioning, diff and first-prerelease continuations are recorded below.

- [x] Record requirements, exit-code decisions and wording self-check.
- [x] Observe focused red/green checks for status reporting and manifest validation.
- [x] Add --check, no-write fixture assertions and install documentation.
- [x] Run starter gates and record actual evidence.
- [x] Submit [PR #24](https://github.com/guventech/ai-project-starter/pull/24); require both OS CI jobs before merge.

## Review F-10 rule-trigger coverage (approved)

Owner: repository maintainer. Acceptance criteria: RULE-001–RULE-003 in docs/PRD.md.

- [x] Record scope, measurable requirements and wording self-check.
- [x] Observe red/green layout coverage; extend scoped source and Go test globs.
- [x] Add docs/RULES.md with inventory, adaptation examples and attachment procedure; link README/CONFIGURATION.
- [x] Record Go positive/README control CLI marker observations and limits; Node/Python remain static coverage.
- [x] Run starter gates and submit [PR #25](https://github.com/guventech/ai-project-starter/pull/25); both OS CI jobs are required before merge.

## Review F-14 contribution basics (approved slice)

Owner: repository maintainer. Acceptance criteria: CONTRIB-001–CONTRIB-003 in docs/PRD.md. Remaining community policy, settings and discoverability work stays deferred.

- [x] Record measurable requirements and wording self-check.
- [x] Add CONTRIBUTING.md, two Markdown issue templates and README entry link.
- [x] Inspect metadata, relative links and public-report privacy guidance.
- [x] Run existing starter checks and submit [PR #26](https://github.com/guventech/ai-project-starter/pull/26); both OS CI jobs are required before merge.

## Review F-06 project initialization (approved)

Owner: repository maintainer. Acceptance criteria: INIT-001–INIT-005 in docs/PRD.md.

- [x] Assess alternatives; record exact content policy and requirement wording.
- [x] Complete two fresh design reviews and affected-section rereviews; resolve line-ending, cache, backup, path-alias and Git-monitor findings.
- [x] Observe preview/apply, refusal and recovery behavior on disposable copies; preview and Git-filter red/green recorded.
- [x] Verify clean output and all four configuration invariants under explicit --project mode.
- [x] Run source checks, record security/review limits and submit [PR #27](https://github.com/guventech/ai-project-starter/pull/27); both OS jobs passed on the implementation commit and remain required on the PR head before merge.

## Review F-07 README positioning (authorized continuation)

Owner: repository maintainer. Acceptance criteria: READ-001–READ-004 in docs/PRD.md.

- [x] Define measurable scope and check requirement wording.
- [x] Lead README with purpose, audience and two quickstart paths; retain brand and canonical skill guide.
- [x] Add a sourced bounded example/comparison, verification overview and optional-pack guide; move migration/publishing detail to its dedicated home.
- [x] Verify initialization removes the new evidence overview; inspect relative links, anchors and claims; resolve upgrade-guidance review finding.
- [x] Regenerate baseline, run existing checks and submit [PR #28](https://github.com/guventech/ai-project-starter/pull/28); both OS jobs passed on the implementation commit and remain required on its head before merge.

## Review F-02 worked reference and controlled evidence (authorized continuation)

Owner: repository maintainer. Acceptance criteria: EVAL-001–EVAL-005 in docs/PRD.md.

- [x] Define measurable requirements, frozen cases/protocol/rubric and execution limits.
- [x] Complete two fresh design reviews and affected-section reviews; resolve grading authority, publication, parser and transport findings.
- [x] Build the stdlib reference with observed red/green and fresh read-only verification; six CLI checks pass.
- [x] Verify native read/shell denial, JSON transport, isolated public-test execution and rejection of forged grade records in unscored readiness.
- [x] Attempt four paired trials once each; retain seven failures and one accepted finish; inspect final artifacts and frozen-input hashes.
- [x] Block further live trials because complete native isolation and useful protocol compatibility were not established; no outcome-based reruns.
- [ ] Establish an isolated/disabled-native-tool runner under a new reviewed method before claiming useful comparative outcomes (remaining F-02).
- [x] Publish bounded conclusions, classify 90 individual removals and pass local source gates (71 tests; six host symlink skips).
- [x] Submit [PR #29](https://github.com/guventech/ai-project-starter/pull/29) for this partial evidence slice; both protected CI jobs are required before merge. Useful comparative outcomes remain open above.

## Review F-15 changelog consistency (authorized continuation)

Owner: repository maintainer. Acceptance criteria: LOG-001–LOG-003 in docs/PRD.md. Cursor + Codex: reversible follow-up to VERSION/CHANGELOG; defer PR scraping and Releases.

- [x] Record measurable requirements and wording self-check.
- [x] Add `scripts/changelog_release.py` with `--check`/notes extraction and failure cases.
- [x] Wire the check into starter validation; document implementation-PR changelog updates.
- [x] Run starter gates and merge protected-branch PR after both OS CI jobs ([PR #34](https://github.com/guventech/ai-project-starter/pull/34)).

## Review F-13 version metadata (authorized continuation)

Owner: repository maintainer. Acceptance criteria: VER-001–VER-003 in docs/PRD.md. Cursor + Codex: diff and first-prerelease continuations are recorded below; remaining F-02/F-11/F-12 stay deferred.

- [x] Record measurable requirements and wording self-check.
- [x] Add VERSION `0.1.0`, CHANGELOG.md and installer `--version` / package-version printing.
- [x] Package VERSION in the installer; remove VERSION/CHANGELOG on initialization.
- [x] Run starter gates and merge protected-branch PR after both OS CI jobs ([PR #32](https://github.com/guventech/ai-project-starter/pull/32)).

## Review F-09 process weights (authorized continuation)

Owner: repository maintainer. Acceptance criteria: WEIGHT-001–WEIGHT-003 in docs/PRD.md. Cursor + Codex: implement after F-02 partial merge; defer remaining F-02 runner.

- [x] Record measurable requirements and wording self-check.
- [x] Define Lite/Standard/Strict in the generated skill guide; update project-helper selection rules.
- [x] Add `scripts/process_weight.py` with typo/rename → Lite and payment → Strict checks.
- [x] Run starter gates and merge protected-branch PR after both OS CI jobs ([PR #30](https://github.com/guventech/ai-project-starter/pull/30)).

## Review F-13 installer diff (authorized continuation)

Owner: repository maintainer. Acceptance criteria: DIFF-001–DIFF-003 in docs/PRD.md.

- [x] Record measurable requirements, plan, wording check and ADR-027.
- [x] Observe red/green for managed-text preview; verify missing-final-newline rendering.
- [x] Cover drift summaries, extra-content exclusion, inspection errors, conflicting flags and no-write snapshots.
- [x] Complete diff review, resolve output-encoding finding, run source checks (90 tests; six host symlink skips) and regenerate the initialization baseline.
- [x] Submit [PR #36](https://github.com/guventech/ai-project-starter/pull/36); implementation commit passed both OS jobs in [run 42783168886](https://github.com/guventech/ai-project-starter/actions/runs/42783168886). Both jobs remain required on the PR head before merge.

## First tagged prerelease (Cursor + Codex agreement)

Owner: repository maintainer. Acceptance criteria: REL-001–REL-003 in docs/PRD.md.

- [x] Obtain Cursor's read-only decision review and Codex agreement; record conditional owner authorization, scope and ADR-028.
- [x] Align current publication wording and changelog date; retain evidence limitations and deferred scope.
- [x] Run configured gates (90 tests; six host symlink skips), review notes/installation evidence and regenerate baseline; fresh read-only review reported no concrete findings.
- [x] Merge [PR #37](https://github.com/guventech/ai-project-starter/pull/37); both required jobs passed on merged main in [run 42785224680](https://github.com/guventech/ai-project-starter/actions/runs/42785224680).
- [x] Publish annotated `v0.1.0` and GitHub prerelease at `413ae453193c0c069850a4da08a1ca73e76da1a0`; verify draft false, prerelease true, notes and exact commit on [release metadata](https://github.com/guventech/ai-project-starter/releases/tag/v0.1.0).

Publication was recorded on the release and in follow-up docs after the tagged preparation revision, so the tag target itself did not need to change.

## Application adoption checklist

- [ ] Define each requirement in the PRD table with a measurable check and a verification method.
- [ ] Review architecture and approve the implementation plan.
- [ ] Select stack and record actual commands in QUALITY_GATES.md.
- [ ] Implement one end-to-end user journey with tests.
- [ ] Add real application checks to CI.
- [ ] Verify behavior, failure paths and deployment rollback.

Track each task with owner, acceptance criteria, status and verification evidence.
