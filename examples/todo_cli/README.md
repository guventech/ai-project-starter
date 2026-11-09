# Worked example: a local task CLI

This is an authored example of the starter workflow, not an agent trial or a
production application. Python 3.12+ and the standard library are enough.

```sh
python examples/todo_cli/todo.py --data tasks.json add "Review proposal"
python examples/todo_cli/todo.py --data tasks.json list
python examples/todo_cli/todo.py --data tasks.json done 1
python examples/todo_cli/todo.py --data tasks.json list --pending
python -m unittest discover -s tests -p test_todo_example.py -v
```

Use a disposable data path. The commands above create/update that file.

## Requirements

| ID | Shall requirement | Verification |
|----|-------------------|--------------|
| TODO-001 | Add shall trim nonblank text, append a pending task and allocate max existing ID + 1. | add/list test; existing-ID boundary check |
| TODO-002 | List shall print tasks in stored order as `ID [ ] text` or `ID [x] text`. | default-output assertions |
| TODO-003 | Done shall select the actual ID and reject unknown IDs with exit 2 and unchanged data bytes. | noncontiguous-ID and unknown-ID assertions |
| TODO-004 | List --pending shall exclude completed tasks and leave stored bytes unchanged. | pending/default preservation assertions |
| TODO-005 | Empty additions and malformed stored records shall return exit 2 without changing existing data. | rejection/preservation assertions |

Wording check: one observable requirement per row, one verification per row, no
vague performance or usability promises. Missing files represent an empty list.
Records require exactly id/text/done; IDs are positive integers excluding bool,
text is nonblank, done is bool, and IDs are unique.

## Approved scope and plan

The owner authorized F-02 and delegated routine implementation choices. This
reference uses that authorization; it does not claim a separate owner review of
each example requirement. Plan recorded before implementation: stdlib add/list,
then actual-ID completion, then pending filtering; boundary tests at the CLI;
fresh read-only verification; record release limits. No import feature, dependency,
network service or deployment belongs to the reference. Evaluation cases are
separate synthetic variants, not results of building this reference.

## Observed test-first slices (2026-11-09)

The command was `python -m unittest discover -s tests -p test_todo_example.py -v`
on Windows/Python 3.13.14. These are concise execution records, not invented raw
transcripts; the assertions are in [the executable tests](../../tests/test_todo_example.py).

1. Add/list: the initial executable stub returned 2, `Not implemented`, instead
   of expected 0. Implemented add/list; one test passed.
2. Completion: `done 19` returned 2 with `invalid choice: 'done'`. Implemented
   actual-ID lookup and unknown-ID rejection; two tests passed.
3. Pending: `list --pending` returned empty stdout rather than `19 [ ] Second`.
   Implemented filtering; four tests passed, including stored-data regression checks.

Malformed-record checks passed when first added; they are regression evidence,
not an additional observed red/green slice. No refactor was required.

## Independent verification and release check

Fresh read-only reviewer `f02_example_verifier` used no inherited conversation.
It inspected the app and tests, found no bugs in the stated scope, and requested
additional boundary checks. It did not run tests or certify deployment readiness.
The parent added the requested boundary checks: malformed JSON/UTF-8, invalid record
shapes/types, unsorted existing IDs and missing-file refusal behavior. All six
tests passed. Final results are in [the evidence report](../../docs/EVIDENCE.md).

Release scope: educational local single-user reference only. No concurrency,
transactional disk-failure recovery, hostile-filesystem defense, packaging or
application deployment is promised. Writes use the selected local file directly;
back up any data you care about. Rollback: remove this example's disposable data
file or revert the PR; do not delete another project's data. The repository's
initializer removes this example and its development evidence from new copies.
