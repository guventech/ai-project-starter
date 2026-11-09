# Controlled workflow comparison

**Post-run status:** live model trials are blocked. Seven of eight attempts failed
the protocol, and Read/Shell controls did not establish complete native-tool
isolation. `--run` now refuses before creating files or calling models/Docker.
The offline checks and container-only `--pilot` remain available. Exact historical
inputs are data in [inputs.json](results/2026-11-09-composer25/inputs.json), verified
against the original manifest hashes. The report records all failures; no arm was
retried. [Evidence and remaining work](../docs/EVIDENCE.md).

This opt-in experiment compares explicit starter guidance with a baseline task
under one shared typed-action protocol. It does not run the native IDE workflow.
Offline tests run in source CI; live calls require the authenticated Windows CLI
2026.11.05-86047df and the existing Docker runtime. No global package is upgraded.

```sh
python -m unittest discover -s tests -p test_workflow_eval.py -v
python evals/workflow_runner.py --pilot
```

Historical command (currently blocked):
`python evals/workflow_runner.py --run evals/results/2026-11-09-composer25`.

The live command uses paid/authenticated model access and creates only labeled,
disposable containers. It refuses an existing result directory. Do not rerun an
arm to replace a disappointing result. A new experiment needs a new directory and
an explanation. Raw CLI streams stay in ignored build/f02-quarantine for local
inspection; they contain reasoning and must not be committed.

## Frozen inputs and order

[workflow_cases.py](workflow_cases.py) contains exact task prompts, starting code,
public tests, clarification/approval strings and parent-owned oracle checks.
[workflow_runner.py](workflow_runner.py) defines the common protocol, treatment
source paths, fixed reviewer prompt, limits and execution adapter. Their hashes,
joined treatment hash and requested/reported versions are recorded before scoring.
Do not edit those files while a scored run is active.

Order: bug baseline/starter, feature starter/baseline, risky baseline/starter,
ambiguous starter/baseline. One attempt per arm. Readiness pilots are excluded:
native read/shell must be tool-denied, JSON-only transport must work, the container
public test must pass, and forged grading records must fail. A failed pilot blocks
all scored calls. The fixed image is identified by digest in the runner/design.

## Rubric, fixed before scored calls

Report each dimension separately, without weights or a combined score.

| Dimension | Rule and evidence |
|-----------|-------------------|
| Correctness | Parent-owned named CLI checks all pass; fixed existing-command test remains independent of candidate test edits. Missing/failed grading is unverified, never pass. |
| Requirements captured | Inspect plan requirements and PRD/PLAN artifacts. Explicit = every task clause is stated; partial = at least one but not all; absent = none. Quote action/file references. Code alone is not a requirements artifact. |
| Test first | A test_todo.py write precedes the first todo.py write. Report ordering only; inspect test changes separately for relevance. |
| Regression caught | A public run before the first app write returns a task-relevant assertion failure. Syntax/import/setup errors and unconditional failing tests do not count. Cite the actual test/action and inspection disposition. |
| Scope | Inspect final diff for added user-visible behavior outside the task and preserved commands. Record observed additions or none; do not infer absence from passing tests. |
| Cost | Actual wall seconds, author actions, total model calls and review calls; no token or monetary estimate when the CLI does not supply a verified measure. |
| Ambiguity | Asked-and-followed = duplicate-policy question received the fixed answer and import checks pass; guessed-matching = no question and checks pass; other-policy = checks fail. An unasked matching guess is not successful clarification. |

Case clauses: bug = actual-ID lookup, gaps, unknown-ID rejection/no mutation,
existing commands; feature = pending filter, stable order/default output/no writes,
existing commands; risky = full validation, exact record types/keys, duplicate
rejection within/across stores, no writes on any rejection, valid ordered append,
existing commands; ambiguous = ordered append, duplicate decision and existing
commands. A duplicate/collision/ID question matches the frozen predicate in the
runner. Other product questions end the arm as needs-clarification.

Every author call is a fresh process reconstructed from visible history. Optional
plans receive the same scoped scripted approval; this is delegated fixture
authorization, not independent human plan review. One optional fresh reviewer has
the same model/task/public files in either arm, without author history, treatment
or hidden expectations. It costs one extra model call and one author action.
The limit is 20 author actions including the review request, hence at most 21
model calls. On invalid-action failure, bounded known assistant text may be
published as visible_response after path redaction and manual inspection. Unknown
events, native tool payloads, reasoning and stderr remain quarantined. Timeouts
and overflow retain bounded partial raw streams there, together with failure status.

## Interpretation and boundaries

The baseline still receives the task, mechanics, scope authorization and the host's
ambient global configuration. This is not an empty-system prompt. Additional
guidance, requested review and model behavior are bundled treatment effects.
One pair per task, no random seed, an opaque provider model revision, reconstructed
sessions and a constrained tool interface prevent general benefit/causal claims.
The complete workflow's native tool execution and human approval are not measured.

Candidate Python runs only inside containers without mounts/network/credentials;
the host never imports it. A trusted parent grades application outputs/data rather
than trusting candidate-written tests or pass records. Docker and CLI defects are
outside the guarantee. Container flags are inspected before starting. Windows
process jobs clean up CLI descendants; owned container IDs/labels guard cleanup.
The initializer removes these maintainer artifacts individually from stock copies.
