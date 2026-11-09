# F-02: controlled workflow evidence

## Scope and authority

The owner approved F-02 after the README/initializer work. Deliver one focused PR
with a worked example, four paired scenarios, executable evaluation tooling and
honest raw visible results. Requirements: EVAL-001–EVAL-005 in docs/PRD.md. Do not
change skills, weights, global Cursor settings, account credentials or another
project. No public deployment or release is part of this experiment.

## Feasibility findings

The installed Cursor CLI is authenticated and lists `composer-2.5`. Readiness
controls first observed an unexpected successful edit with the process working
directory different from --workspace. Repeating with both directories equal and
deny-all Read/Write rules returned native readPermissionDenied for edits inside
and outside the fixture; neither marker was written. Explicit sandbox mode
exited before execution: it requires macOS/Linux and is unavailable on this Windows
host. Therefore do not use native writable CLI tools for candidate code. Existing
Docker Desktop server 29.7.2 is available; no new cloud service is required.
With cwd equal to --workspace and the deny-all policy below, native Read of an
existing synthetic outside file returned errorMessage "Permission denied"; its
sentinel never appeared in the stream. Native Shell returned permissionDenied.
These are readiness pilots, not scored trials. CLI version: 2026.11.05-86047df;
reported model: Composer 2.5. Pinned execution image:
`python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b`.

## Selected architecture

Use the CLI as a read-only proposal engine (`--print --mode ask --model
composer-2.5 --output-format stream-json`), not a native implementation agent.
Both arms emit one typed JSON action per response. A parent stdlib runner validates
and executes actions inside disposable Python 3.12 containers. This compares
explicit starter guidance with a baseline task prompt under a shared artificial
tool protocol; it does not claim full IDE execution or an empty-system baseline.

Actions: read a bounded list of fixture files; write an allowed app/test/doc file;
run the fixed public unittest command; propose a plan; ask a product question;
request a fresh read-only review; or finish. No arbitrary shell command is accepted.
The common protocol gives mechanics and allowed paths, not TDD/review advice.
The starter arm additionally receives the current AGENTS/project-helper and
relevant planning/test-first/verifier/release instruction text. The baseline arm
does not receive those instructions. Ambient global host configuration remains
unchanged and is a disclosed confound. Record the requested and reported model.

Containers: pinned Python 3.12 slim image digest, network none, no host mounts or
credentials, read-only root filesystem, unprivileged UID, dropped capabilities,
no-new-privileges, bounded memory/CPU/processes and tmpfs working directories.
Upload only synthetic fixture data through stdin to a fixed executor. Resolve
paths under /work; reject traversal, absolute/drive paths, symlinks and unknown
action fields. Candidate Python runs only in the container. Native CLI tool use
is a protocol failure; do not publish its unreviewed payload. Before scored calls,
read/shell controls must demonstrate denial with the exact per-call configuration:
process cwd equals --workspace, project .cursor/cli.json denies Read(*), Read(**),
Write(*), Write(**), Shell(*), Mcp(*:*), WebFetch(*), and mode ask. Native tools
remain exposed but are denied by this tested configuration; this is not an OS
sandbox or a guarantee against a CLI defect. No force/yolo flag.

Create only uniquely named/labeled containers. Before force-removing a timed-out
or completed container, inspect the exact ID/ownership label; never enumerate
and delete unrelated resources. Kill only the runner's own CLI process tree on
timeout; preserve its failure record. Verify named host-temp boundaries before
cleanup. The image may be pulled if absent; do not install project dependencies.

## Fixtures and preregistered scenarios

Implement a small stdlib JSON task CLI as a separate worked reference with add,
list and done operations. The reference is authored/tested with the local workflow
and is not scored as an agent trial. Store its requirements, plan, actual slice
evidence, independent verifier report and release limitations beside the example.

Each trial starts from identical per-scenario code and existing tests in both arms:

1. Bug: completing a task must use its ID, not a list position; noncontiguous IDs
   and unknown IDs must preserve other records.
2. Feature: list only pending tasks when requested, preserving default order,
   existing default output and stored data.
3. Risky/security-sensitive import: validate the whole input before mutation;
   reject malformed types/duplicate IDs and preserve existing data on rejection.
4. Ambiguous import: an underspecified merge request omits the duplicate policy.
   A question about that decision receives the same predeclared append-and-reject
   policy in either arm; unasked assumptions are not corrected after grading.

Freeze exact prompts, fixture variants, public tests, withheld-oracle checks and
rubric before any scored model call. Alternate arm order per scenario. One scored
attempt per arm; no discarding failures or retrying to improve a result. Permission/
network/model errors are host/protocol outcomes, not automatic quality failures.
Hidden checks are not supplied to the model or used for repair. Grade final files
in a separate fresh container after interaction ends.

## Interaction and measurements

At most 20 author actions and 180 seconds per model response; at most one review
request among those actions. Its reviewer response costs one extra model call,
so the maximum is 21 model calls. A plan within the predefined scope receives the same
scripted approval text; this is protocol approval under the owner's delegated
fixture scope, not a claim of separate human plan review. The ambiguous task has
one fixed clarification answer. Other unresolved product questions end the run
as needs-clarification; never invent an adaptive answer to help an arm pass.

Each action uses a new CLI process with a reconstructed visible transcript; no
session resume or hidden reasoning is carried forward. Both arms receive the same
task authorization to act within the listed fixture paths. A plan is optional in
the common protocol: do not enforce a plan-before-write gate or count its absence
as a baseline protocol failure. Record first plan/test/app writes as observations.
Plans contain requirements, steps and allowed paths; approve only that frozen
scope. Invalid JSON, duplicate keys, unknown fields/actions or native tool use
end the arm as protocol-error, without a repair retry. One optional reviewer call
uses Composer 2.5, the same fixed correctness/regression prompt, current public
files and task only (no author transcript, treatment text or hidden checks).
It counts as an extra model call and one of the 20 actions. Review findings are
read-only; the author may repair within its remaining budget.

Freeze a per-case checklist of required behavior, preservation checks and scope
limits. Report requirements as explicitly captured/partial/absent with quoted
action references; test-first as test write before app write; regression detection
as an observed failing behavioral test before repair; scope as added behavior
outside the task. Ambiguous outcomes distinguish asked-and-followed-policy,
guessed-matching-policy and other-policy. Do not interpret a matching guess as
successful clarification. Record syntax/import failures separately from red.
Final grading is a trusted parent supervisor: it invokes the candidate CLI in
fresh containers and compares its untrusted stdout, exit status and exported data
with frozen expectations. It never imports candidate code or parses candidate
output as authoritative grading records. A candidate printing forged pass or
completion records must fail. Parent-owned check results alone determine scores;
missing, exception, timeout or truncated responses fail grading. Candidate public
tests are never the correctness oracle. Hidden expectations remain on the host
and are never uploaded to candidate execution containers.

Manifest: source revision; SHA-256 for treatment, protocol, review prompt, cases,
fixtures, grader and runner; CLI requested/reported model and version; image
digest; platform; action/call/time limits; arm order and UTC start/end. Pilots are
listed apart and excluded from scored results. The model has no immutable provider
revision identifier, so exact future reruns are not promised.

Record actual wall time, model/action/review/controller-response counts and final
file changes. Objective outcomes: hidden check pass/fail, public-test executions,
whether a test write preceded the first app write, and whether an actual behavioral
red result was returned to the model before implementation. Distinguish behavioral
red from syntax/import/setup failure; retain reviewer evidence for that disposition.
Record requirement capture, regression detection and scope-creep assessment with
the exact action/artifact evidence and an explicit inspection method. No weighted
total or statistical significance claim. Both arms may succeed or fail.

## Artifacts and privacy

Store case specifications and runner in evals/, the reference app/evidence in
examples/todo_cli/, and one immutable result directory with sanitized visible
JSONL actions/responses, test outputs, final files/diffs and metadata per arm.
Publish only a positive event schema: known assistant text converted to validated
actions, controller observations, model name and normalized failure status. A
failed action may additionally retain bounded known-assistant text as
visible_response, without native payloads or unknown event contents; redact it
and manually inspect it before publication. Omit
thinking, user echoes, IDs, tool payloads, unknown event shapes and stderr. Unknown,
malformed or truncated streams terminate the trial; retain its status, quarantine
raw streams in ignored scratch storage and inspect before publication. Do not
commit quarantine material. Redact host paths in permitted text, then inspect the
allowlisted output before committing. No credentials are read or copied.

Bounds: 64 KiB per file/action/output, 20 candidate files, 1 MiB aggregate visible
transcript, 2 MiB raw CLI stream, 180 seconds per model call, 10 seconds per public
test/grading command, 32 MiB tmpfs, 256 MiB memory and 64 processes. The fixed
executor is supplied as immutable Python -I -c interpreter arguments, not a file
under candidate-writable /work; invoke commands as argument arrays without a shell.
Use a fresh container per execution, stop all of its processes before continuing
the action sequence, and retain only validated explicit file proposals between
calls. Revalidate export paths,
entry types and byte totals; reject links, devices, unknown files and oversized
outputs. Container inspection must confirm isolation flags before any code runs.
docs/EVIDENCE.md explains results and links raw evidence; README/VERIFICATION
must make claims no stronger than this small controlled experiment.

Initializer policy must classify all examples/evals files and the evidence/design
pages as maintainer artifacts, while continuing individual-file removal from the
checked manifest. Reusable workflow guards remain unchanged. Source CI executes
offline harness/reference tests only; live model/Docker runs are explicit commands,
not required CI or automatic recurring work.

## Verification, rollout and rollback

Two fresh read-only reviews challenge methodology and execution boundaries before
implementation. Test action/path validation, transcript sanitation, metric ordering,
ownership-checked cleanup and reference behavior with stdlib unittest. Use focused
red/green checks; run isolated protocol/container pilots before scored trials.
Independently review worked-reference correctness and the report's evidence links.
Report unavailable checks and partial/failed runs without inventing results.

Rollback: revert the PR; stop/remove only owned ephemeral containers and named
temporary fixtures. Preserve committed results as evidence rather than rerunning
silently. No global host configuration or application data should need restoration.

## Initial fresh review dispositions

Two fresh agents (f02_method_review, f02_boundary_review; fork_turns none) reviewed
the requirements/design. Accepted: define session/approval/reviewer semantics,
per-case rubric and grade boundary, reproducibility hashes, positive publication
schema, output/executor/export bounds and exact initializer classification. Those
changes are specified above. Native host-read denial remains a pilot prerequisite,
not a claim established by detecting tool use after execution. Affected-section
fresh review is required before implementation. No outcome-based trial reruns.
Affected-section fresh reviews (f02_method_rereview, f02_boundary_rereview;
fork_turns none) found no methodology blockers and one accepted technical finding:
move grading authority outside candidate Python. The parent-supervisor design
above resolves that finding; verify a forged-record candidate before scoring.

## Implementation verification before scoring

Fresh read-only implementation scopes (fork_turns none): execution boundary audit
f02_execution_audit, independent finding verification f02_candidate_verification,
pre-score f02_prescore_review/f02_final_prescore, and initializer f02_initializer_review.
Accepted parser findings: require a terminal success result; reject non-object and
wrong-type action/event fields; bound the joined assistant text before publication.
Parent regression checks passed; f02_final_prescore independently verified the
joined-text fix. Invalid assistant text has an explicit bounded failure schema;
partial timeout/overflow streams remain quarantined. Clarified that 20 author
actions include a review request, whose reviewer costs an extra model call.
The complete seven-dimension rubric and per-case clauses are in evals/README.md;
one review's missing-rubric claim was contradicted by a narrow file inspection.

Readiness passed with the actual pinned Node transport and empty allow list:
native outside Read and Shell tool-denied, JSON-only response parsed, inspected
restricted-container public test passed, forged grading records rejected. Windows
job ownership fixed an earlier temporary-directory lock by terminating only CLI
descendants. The leftover synthetic fixture was subsequently removed after exact
temporary-root verification. No user-level package/configuration was changed.
The run manifest hashes frozen runner/cases/rubric/treatment/protocol/reviewer
inputs. Source docs and initializer policy may be completed while the run executes;
those files are not model inputs. No scoring input changes or outcome-based retry.
