# Product requirements

Status: approved starter enhancement implemented; requirement evidence is recorded in docs/QUALITY_GATES.md. Live Cursor execution remains untested.

- Problem and target users: Cursor users need planning, test-first development and review workflows beyond the three starter skills.
- Primary user journey: clarify requirements, draft and review a design, approve implementation, build in tested slices, then verify release evidence.
- Goals and measurable success: seven local skills, two read-only reviewers and documented review gates, with both starter check commands passing.
- Constraints: retain a stack-agnostic template, existing Cursor metadata conventions and dependency-free validation. Keep secrets out of review inputs and reports.
- Functional requirements and acceptance criteria: see the table below.
- Out of scope: application code, stack selection, note-taking integration, installing external packs, publishing and deployment.
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

## To be resolved (TBR)

Mark an unknown value as TBR with a best estimate, an owner, and a due date. Use that instead of a blank TBD.

| ID | Value | Best estimate | Owner | Due date |
|----|-------|---------------|-------|----------|
| None | No unresolved values for the proposed scope. | Not applicable | Maintainer | Not applicable |

## Risks

| Risk | Worst case if ignored |
|------|------------------------|
| A host reuses author context for a goldfish review. | Missing assumptions escape review; require fresh-context setup and disclose unavailable isolation. |
| External pack names overlap local skills or need shared resources. | Installation replaces local workflows or leaves broken references; document selection and upstream setup limits. |
| Static validation is mistaken for workflow execution. | Release claims exceed evidence; report metadata checks apart from live Cursor checks. |
