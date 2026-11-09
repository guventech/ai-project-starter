# Product requirements

Status: approved starter enhancement implemented; requirement evidence is recorded in docs/QUALITY_GATES.md. Bounded authenticated Cursor CLI smoke checks are complete; full workflow execution and tool-level permission enforcement remain outside that evidence.

- Problem and target users: Cursor users need planning, test-first development and review workflows beyond the three starter skills.
- Primary user journey: clarify requirements, draft and review a design, approve implementation, build in tested slices, then verify release evidence.
- Goals and measurable success: eight local skills, two read-only reviewers and documented review gates, with both starter check commands passing.
- Constraints: retain a stack-agnostic template, existing Cursor metadata conventions and dependency-free validation. Keep secrets out of review inputs and reports.
- Functional requirements and acceptance criteria: see the table below.
- Out of scope: application code, stack selection, note-taking integration and application deployment. Follow-up authorization covers optional pack installation, repository protection and documentation commits.
- Assumptions: local workflows are concise original instructions informed by the linked packs, not vendored copies. Fresh-context reviews require host support; unavailable review execution must be reported as unverified.

## Requirement wording

shall means a requirement, will means a fact, and should means a goal.

Each requirement is one thought. It says what the product must do and leaves the design out.

Avoid these vague words: fast, easy, user-friendly, robust, adequate, minimize, maximize, flexible, sufficient, safe, portable, and other vague words ending in ly or ize.

These rows cover the starter enhancement requested in CURSOR_UPDATE_PROMPT.md. Replace them when adopting the template for an application.

## Requirements

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| REQ-001 | The starter shall include grill-me, tdd, design-review and security-audit skills. | Add the four workflows named in the update prompt. | All four folders contain a SKILL.md with matching name, description and explicit invocation metadata. | test |
| REQ-002 | The grill-me skill shall require resolution of implementation-blocking questions before coding. | Turn assumptions into decisions and measurable criteria. | Instructions cover one-question-at-a-time interviews, decision recording and an exit condition with zero unresolved implementation blockers. | inspection |
| REQ-003 | The tdd skill shall prescribe a red-green-refactor cycle for each behavior slice. | Verify behavior before expanding implementation. | Instructions require observing a failing test for the intended reason, implementing one slice, rerunning tests and refactoring after green. | inspection |
| REQ-004 | The design-review skill shall require design drafting, fresh-context review and human approval before implementation. | Expose assumptions absent from the design document. | Instructions define both phases, at least two bounded fresh reviewers, finding resolution and an unverified outcome when fresh contexts are unavailable. | inspection |
| REQ-005 | The security-audit skill shall define four audit phases with finding verification. | Distinguish supported findings from suspicions. | Reconnaissance, coverage-led hunting, fresh-agent verification and reporting each have inputs and outputs; reports include coverage gaps and finding dispositions. | inspection |
| REQ-006 | The planning and release skills shall reference the new review workflows and their exit criteria. | Connect the lifecycle without imposing application tooling. | Planning references grill-me and design-review; release-check requires requirement evidence, applicable review results and disclosure of skipped or missing gates. | inspection |
| REQ-007 | Both review agents shall define read-only responsibilities for their review modes. | Preserve the author/reviewer boundary. | Architect includes requirements questioning and design review; verifier includes fresh-context design, diff and finding review with evidence and limitations; both retain readonly true. | inspection |
| REQ-008 | The documentation shall describe the seven skills, review gates and four external pack installation commands. | Make local workflows and optional external installations discoverable. | AGENTS.md and README.md contain all four requested commands; QUALITY_GATES.md maps all nine requirements to evidence; configuration docs state runtime verification limits. | inspection |
| REQ-009 | The validator shall detect removal of any required local skill. | Prevent future updates from dropping the requested workflows. | Tests remove each of the seven required skills in turn and assert a missing-skill error; both configured starter check commands pass. | test |

The acceptance criterion needs a measurable value or a tolerance. The verification method is test, analysis, demonstration, or inspection.

## Authorized setup follow-up

The user requested all remaining checks and optional installations after the enhancement was pushed. Keep external packages in user-level Cursor directories to preserve the template's seven local skills and stack-agnostic scope. Do not configure application tooling before a stack is selected.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| SETUP-001 | The main branch shall require the Windows and Linux starter CI checks before merging changes. | Both Python 3.12 jobs passed for commit 8391565. | GitHub settings show both exact job names as required, strict status checks, and no force pushes or branch deletion. | inspection |
| SETUP-002 | The setup shall install the four optional upstream packs outside this repository. | Keep shared resources intact and preserve the seven local skills. | Each pack has a recorded source revision and installed path; EGM retains agents and document standards; no local skill is overwritten. | inspection |
| SETUP-003 | The verification record shall distinguish observed Cursor execution from unavailable checks. | CLI authentication and host capabilities can block runtime evidence. | Record installed editor/CLI versions, login status and results for skill discovery, read-only agents and fresh-context review; any missing result stays unverified. | demonstration |

Setup risks: upstream names can overlap project skills; full-package resources must remain beside their skills; live execution requires Cursor authentication. Rollback removes only the added user-level package directories and the new branch-protection configuration after checking current state. Existing user configuration remains untouched.

## Proposed maintenance follow-up

Status: MAINT-001 approved and implementing (`checkout@v5` + `setup-python@v6`); MAINT-002 and MAINT-003 remain queued. The target for the full reviews is pending user selection.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| MAINT-001 | The starter CI shall use Node.js 24 action releases. | Current checkout/setup-python actions produce Node.js 20 deprecation annotations. | Both actions use upstream-supported Node.js 24 releases; Windows and Linux jobs pass with the existing job names and Python 3.12. | test |
| MAINT-002 | The permission probe shall distinguish behavioral refusal from host-denied writes. | Earlier reviewers refused before attempting a tool call. | An isolated fixture records the invoked read-only agent, attempted benign write or refusal, host result and marker-file state; missing denial evidence remains unverified. | demonstration |
| MAINT-003 | The full review report shall identify the selected repository and reviewed revision. | No application audit target was provided. | Design review records two fresh reviewers and finding dispositions; security review records surface coverage and candidate verification; exclusions and unresolved findings are listed. | inspection |

Plan: update checkout/setup-python to their current Node.js 24 major releases; keep the matrix, job names and permissions; run both starter commands and PR CI; run the permission probe in a temporary workspace with no repository credentials; perform full reviews after the user selects the target. Risks: upstream action changes, target scope ambiguity and confusing voluntary refusal with enforced denial. Rollback: revert the CI/documentation commit; discard only the probe's named temporary directory after checking its path.

## Proposed one-command project assistant

Status: approved entry point and installer implemented; local tests and isolated authenticated CLI probes are recorded in docs/QUALITY_GATES.md and docs/SETUP.md. This is the user's current priority; the earlier maintenance follow-up remains queued.

User experience: open a folder in Cursor and type `/project-helper`. The assistant asks whether to start a new project or improve the open project, asks one relevant question at a time, then selects the required planning, review, debugging, testing and release procedures. After the initial command, the user continues in plain language.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| CHAT-001 | The project-helper command shall offer new-project and existing-project modes. | One entry point serves both use cases. | Invoking the command without a goal asks one mode question with two choices; an explicit goal selects its matching mode without repeating the question. | demonstration |
| CHAT-002 | The installed command shall include the local procedures and reviewer instructions it needs. | Other projects should not need manual file copying or this repository's absolute path. | A dependency-free installer packages seven workflow files and two reviewer definitions with the entry skill; the installed command loads these files from another workspace. | test |
| CHAT-003 | New-project mode shall obtain an approved plan before implementation. | Project goals and target directory must be resolved before building. | The assistant gathers the idea and target folder, records measurable criteria, presents a plan, and writes no application code before approval; nonempty target folders require an explicit decision to use them. | demonstration |
| CHAT-004 | Existing-project mode shall inspect the open project's instructions and checks before proposing edits. | Existing conventions and user changes must be preserved. | Initial review reports findings and evidence without changing application files; implementation follows approval of a bounded plan. | demonstration |
| CHAT-005 | The command shall select bundled workflows by file path. | Upstream slash names have known collisions. | Installed-mode probes load the bundled paths for overlapping names and require no second slash command from the user. | demonstration |
| CHAT-006 | The installer shall refuse to replace an existing destination. | Global user skills must not be overwritten by setup. | Tests show an occupied or linked destination is rejected without changing its contents; install output identifies the command location and reload step. | test |

Implementation plan: add the project-helper entry skill; add a one-time Python installer that bundles the existing workflows and reviewers without dependencies or machine-specific paths; extend starter validation and installer tests; simplify README/AGENTS guidance; install into the user's Cursor skill directory; run isolated new/existing-mode CLI probes and both starter gates; commit through a pull request after CI. No standalone website, desktop window, application framework, automatic deployment or upstream skill rename is part of this change.

Risks and verification: the host must discover user-level skills after a reload; test invocation outside this repository. Keep new-project probes in temporary folders and existing-project probes read-only. Missing subagent capabilities or checks remain explicit limitations. Rollback removes only the added command package after checking for user edits, and reverts its repository diff.

## To be resolved (TBR)

Mark an unknown value as TBR with a best estimate, an owner, and a due date. Use that instead of a blank TBD.

| ID | Value | Best estimate | Owner | Due date |
|----|-------|---------------|-------|----------|
| TBR-001 | Target repository for full design/security review | This starter, pending user selection | Repository maintainer | 2026-11-09 |

## Risks

| Risk | Worst case if ignored |
|------|------------------------|
| A host reuses author context for a goldfish review. | Missing assumptions escape review; require fresh-context setup and disclose unavailable isolation. |
| External pack names overlap local skills or need shared resources. | Installation replaces local workflows or leaves broken references; document selection and upstream setup limits. |
| Static validation is mistaken for workflow execution. | Release claims exceed evidence; report metadata checks apart from live Cursor checks. |
