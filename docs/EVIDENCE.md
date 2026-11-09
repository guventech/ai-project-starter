# Workflow evidence

The [worked stdlib task CLI](../examples/todo_cli/README.md) is implemented and
tested. The first controlled comparison produced seven protocol failures and one
accepted completion. This does not establish that the starter improves outcomes.
F-02's useful comparative outcome evidence remains open; no failed arm was retried.

## Worked reference

The example records its requirements, delegated scope approval, plan, three
observed red/green slices, independent read-only verification and release limits.
Six CLI boundary tests passed locally on Windows/Python 3.13.14. This is authored
evidence of one local workflow, not an agent-scored trial or application release.

## Comparison method

Frozen task prompts, rubric and order: [eval guide](../evals/README.md).
Execution design and review dispositions: [design](designs/workflow-evidence.md).
Four paired cases cover an ID bug, pending filter, risky import and underspecified
import. Composer 2.5 proposes typed actions; a host controller executes candidate
Python only in restricted disposable containers. The baseline shares task, initial
code, mechanics, limits and the ambient host configuration; the starter arm adds
explicit workflow instruction texts. Plans receive scripted scope approval under
the owner's delegation. There is one attempt per arm and no outcome-based retry.

CLI 2026.11.05-86047df, Docker 29.7.2, Linux x86_64 execution image pinned by digest
in the runner/manifest. Native Windows CLI sandbox was unavailable. The Windows
wrapper dropped redirected stdin; the runner uses that installed version's Node
entry point directly. Matched cwd/workspace and deny-all project permissions
tool-denied synthetic outside Read and Shell. Earlier cwd-mismatch and incomplete
config pilots failed; they were feasibility controls and are excluded from scoring.
The JSON-only pilot and restricted-container public test passed; forged pass
records were rejected by host-owned grading. Raw thinking/native payloads stay
in ignored quarantine; only the declared visible schema is published after review.

## Observed results

Run: [manifest](../evals/results/2026-11-09-composer25/manifest.json),
[readiness](../evals/results/2026-11-09-composer25/readiness.json),
[completion time](../evals/results/2026-11-09-composer25/completed.txt).
The manifest hashes refer to the exact strings in
[archived inputs.json](../evals/results/2026-11-09-composer25/inputs.json), including
the historical runner, cases, rubric and treatment/protocol/reviewer text. The
current runner has a post-run guard; it is not the historical runner snapshot.
The source revision is the base commit; uncommitted experiment inputs were frozen
by those hashes. Model identity was requested as composer-2.5 and reported as
Composer 2.5; no immutable provider model revision was available.

| Case/arm (execution order) | Terminal observation | All named checks pass? | Calls | Seconds |
|---------------------------|----------------------|------------------------|-------|---------|
| [Bug baseline](../evals/results/2026-11-09-composer25/bug-baseline/result.json) | Native edit attempt; stopped | No | 1 | 32.569 |
| [Bug starter](../evals/results/2026-11-09-composer25/bug-starter/result.json) | Native read attempts; stopped | No | 1 | 32.992 |
| [Feature starter](../evals/results/2026-11-09-composer25/feature-starter/result.json) | Native search attempt; stopped | No | 1 | 32.323 |
| [Feature baseline](../evals/results/2026-11-09-composer25/feature-baseline/result.json) | Implemented filter; prose before finish JSON rejected | Yes, 3/3 | 3 | 79.804 |
| [Risky baseline](../evals/results/2026-11-09-composer25/risky-baseline/result.json) | Accepted finish | Yes, 13/13 | 3 | 95.370 |
| [Risky starter](../evals/results/2026-11-09-composer25/risky-starter/result.json) | Native edit attempt; stopped | No | 1 | 46.957 |
| [Ambiguous starter](../evals/results/2026-11-09-composer25/ambiguous-starter/result.json) | Native read/edit attempts; stopped | No | 1 | 55.139 |
| [Ambiguous baseline](../evals/results/2026-11-09-composer25/ambiguous-baseline/result.json) | Native edit attempt; stopped | No | 2 | 62.235 |

Every arm directory contains actions.jsonl, result.json, final files and changes.diff.
Diffs were rendered with zero context after the run so unchanged blank-line context
markers do not appear as trailing whitespace in Git checks; graded code and primary
records were unchanged. This is display formatting, not outcome repair.
Seven visible-failure.jsonl supplements extract only known assistant text and native
tool type names from quarantined streams. Tool arguments/results, thinking and IDs
are excluded. Proposed code in rejected responses was never applied or graded.
No outputs were repaired to improve a score. There were six accepted actions and
seven failed action attempts, hence 13 author/model calls and zero review calls.
437.389 seconds includes model calls and host/container grading, excludes readiness
and engineering time, and is not a measure of development productivity or cost.

## Rubric inspection

Fresh read-only review f02_results_review inspected all published trial artifacts
without executing candidate code. Parent inspection agreed with these dispositions:

- Requirements capture: absent in all arms under the frozen rubric; no plan
  actions or PRD/PLAN artifacts. Code or final summaries do not count.
- Tests first: no test writes. Only the two baseline feature/risky arms applied
  app writes; the other six never applied a code change through the controller.
- Regressions caught: none observed. The two public test runs followed app writes
  and passed the unchanged existing-command test. No task-relevant red occurred.
- Correctness: the feature baseline artifact passed all three named checks despite
  failed completion formatting; risky baseline passed 13 and completed the protocol.
  The other six retained initial app files and failed at least one task check.
  Existing-command checks passed everywhere, which does not establish task completion.
- Scope: feature baseline adds requested filtering. Risky baseline also strips
  imported text, an unsolicited normalization not exercised by the oracle. Other
  applied diffs are empty; rejected proposed edits do not count as delivered code.
- Ambiguity: neither arm asked the duplicate-policy question; neither implemented
  import. Negative checks passed incidentally because argparse rejected the missing
  command. Visible rejected responses proposed skipping/reassigning IDs, but those
  intentions are not implemented behavior or successful clarification.
- Review effectiveness and separate human approval: unmeasured. No reviewer was
  requested, and scope approval was scripted under owner delegation.

No private home paths, session IDs, reasoning blocks or native payload bodies were
observed in the inspected published tree. This describes publication inspection,
not a guarantee about quarantined content or complete CLI isolation.

## Live-run block and remaining work

Read/Shell denial does not prove complete native-tool isolation: the feature
starter's Grep returned success. A separate post-run synthetic outside search
also returned success without exposing its unknown sentinel; that does not prove
outside content access or tool-level denial. No private file was used in controls.
Complete native-search isolation remains unverified. Seven protocol failures also
prevent a useful paired outcome comparison.

The current runner therefore rejects live --run and direct trial calls before
creating result files or calling models/Docker. Offline tests and --pilot's
container-only check remain available. Historical source is archived as JSON data,
not an endorsed executable entry point. No further scored run occurred after this
finding. A future experiment needs demonstrated native-tool disabling or a CLI
host containing only synthetic inputs and its own authorized authentication;
it needs a new reviewed method and result directory. Existing account credentials
were not read, copied or changed. F-02 is partial; F-09 weights remain deferred.

## Limits

One pair per task cannot establish general benefit or significance. This tests
explicit guidance within an artificial action protocol, not the full native IDE,
human approval or an empty-system baseline. Fresh process reconstruction, optional
review, ambient global configuration and opaque provider model revisions limit
interpretation. CLI permission controls are not an OS sandbox; Docker/CLI defects
are outside the guarantee. Named oracle checks sample the task contracts rather
than proving all possible inputs. Local starter tests alone cannot release an app.

F-09 weights and new skills remain deferred until these observations are assessed.
