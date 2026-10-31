# Product requirements

Status: awaiting project definition.

- Problem and target users:
- Primary user journey:
- Goals and measurable success:
- Privacy, accessibility, reliability and performance constraints:
- Functional requirements and acceptance criteria: use the table below.
- Out of scope:
- Open questions and assumptions:

## Requirement wording

shall means a requirement, will means a fact, and should means a goal.

Each requirement is one thought. It says what the product must do and leaves the design out.

Avoid these vague words: fast, easy, user-friendly, robust, adequate, minimize, maximize, flexible, sufficient, safe, portable, and other vague words ending in ly or ize.

Filled rows below are examples. Replace them.

## Requirements

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| REQ-001 | The system shall confirm a saved record within 2 seconds. | The person needs proof the save worked before leaving the page. Assumes an ordinary home network. | Confirmation appears in 2 seconds or less. A failed save shows an error and keeps the entered text. | test |

The acceptance criterion needs a measurable value or a tolerance. The verification method is test, analysis, demonstration, or inspection.

## To be resolved (TBR)

Mark an unknown value as TBR with a best estimate, an owner, and a due date. Use that instead of a blank TBD.

| ID | Value | Best estimate | Owner | Due date |
|----|-------|---------------|-------|----------|
| TBR-001 | Maximum save confirmation time | 2 seconds | product owner | YYYY-MM-DD |

## Risks

| Risk | Worst case if ignored |
|------|------------------------|
| A failed save drops the text the person typed. | They must start over and may leave. |
