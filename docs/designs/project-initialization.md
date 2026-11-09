# F-06: opt-in initialization of a template copy

## Scope and authority

The owner selected the recommended cleanup-command approach and delegated
routine design choices after assessment. Requirements: INIT-001–INIT-005 in
docs/PRD.md. This design does not authorize executing cleanup on this upstream
working tree, editing global installations, rewriting Git history or publishing
an application. Deliver through one PR with both existing CI jobs green.

## Assessment and selected design

Keep one repository. An opt-in initializer has lower maintenance cost than a
second repository and removes inherited records, unlike merely moving them into
another folder. Default is a read-only preview; --apply explicitly requests the
displayed action list. --destination selects a fresh copy; without it, use the
script's repository root. No project name or application stack is inferred.

Keep reusable configuration checks and the installer. Existing validation
requires publishing helpers that initialization removes, so add an explicit
--project profile to validate_starter.py. It skips only a named maintainer-file
inventory and the initialization baseline check. Skill denylist, guide freshness,
AGENTS consumer-only checks, metadata/rule checks and privacy run in both modes.
Default source mode remains unchanged or stricter. Do not infer mode from a file
that could disable source validation. Source CI keeps its existing commands.

## Exact content policy

Reset from readable resources under scripts/project_templates/:

- README.md: neutral project entry point and planning/validation steps.
- CONTRIBUTING.md: project contribution placeholder, no upstream-specific policy.
- MAINTAINING.md: maintenance of the reusable workflow configuration, no upstream
  branch settings or machine records; retain skill_inventory.py guidance.
- docs/PRD.md: unfilled requirements plus existing wording rules.
- docs/TASKS.md, docs/QUALITY_GATES.md, docs/DECISIONS.md, docs/SETUP.md: unfilled
  project tasks, quality-gate configuration, decisions and host observations.
- docs/CONFIGURATION.md, docs/INSTALL.md, docs/RULES.md: reusable configuration
  instructions, without old runtime claims or references to removed tests.
- .github/workflows/ci.yml: only template-configuration validation with --project
  on Python 3.12/Windows+Linux, explicitly not application CI.

Remove individual stock files, never arbitrary directory trees:

- CURSOR_UPDATE_PROMPT.md and publish-to-github.py/.sh.
- tests/test_starter.py, tests/test_install_chat_command.py and
  tests/test_init_project.py; these test the starter, not an application.
- evals/prior-art-search-hygiene.md and the two existing docs/superpowers records.
- CONTRIBUTING issue templates under .github/ISSUE_TEMPLATE/ (upstream-specific
  reporting prompts); the generic PR template remains.
- docs/designs/project-initialization.md, docs/INITIALIZE.md,
  scripts/init_project.py, scripts/project_manifest.py,
  scripts/project-manifest.json and each reset resource under
  scripts/project_templates/<target-path>. Resource mapping determines the
  individual removal list without an unbounded directory delete.

Keep everything else from the baseline, including .cursor rules/skills/agents,
LICENSE, THIRD_PARTY.md, .env.example, source-directory placeholder, generic
integration/architecture docs, generated SKILLS.md and reusable scripts. Make the
source notice's introduction self-contained so retained attribution does not
depend on resetting SETUP.md. Legal provenance is retained as attribution, not
application verification evidence. No application tests/results are invented.

## Baseline and paths

Add scripts/project-manifest.json, a generated baseline of all template text
files and SHA-256 digests, excluding the manifest itself. Canonical hashing
decodes UTF-8 and normalizes CRLF/CR to LF, like Python text reads and the existing
installer. Preflight does not normalize files on disk. All current template files
are UTF-8 text; unsupported bytes refuse rather than guessing an encoding.
Record reset-resource mapping and
the exact individual remove list. Source validation checks baseline freshness;
the generator's --check works in test copies without Git using the recorded file
inventory. With Git, regeneration inventories tracked and nonignored new source
files. Changes to baseline files require regeneration; document this cost.

Before preview/apply, validate manifest shape and relative POSIX paths. Reject
absolute paths, dot/dotdot segments, drive names, backslashes and .git targets.
Reject colons/alternate streams, reserved Windows device names, trailing dots or
spaces, control characters and case-insensitive duplicate paths. Reset/remove
sets are disjoint and contain only the fixed intended targets.
Reject symlinks and Windows junctions in the root or managed entries/ancestors;
validate resolved paths remain inside the target. Never follow an untrusted
manifest path outside it. Reject extra working-tree files except .git metadata;
bytecode caches are extra files and refuse. The initializer suppresses bytecode
before any local imports. Source baseline validation may ignore untracked caches
while checking recorded files; initialization does not. Compare all expected
normalized text digests before mutation. Compare parsed destination/source
manifests when the executing source is external, so JSON line endings alone do
not cause refusal. This is stock-snapshot detection, not tamper authentication.

If .git exists, require Git, a clean worktree and no remote URL pointing at
guventech/ai-project-starter. Run only read-only Git inspection with optional
locks disabled. Require Git 2.36+ for Git-backed copies and invoke inspection
with command-line core.fsmonitor=false and core.untrackedCache=false so a
configured monitor hook/daemon cannot run during preview. Do not run git status:
it can execute clean/process filters. Use cached diff-index with external diff
and text conversion disabled, plus ls-files index metadata and file-mode checks;
worktree content/extras were already checked against the stock baseline. Reject
partial-clone/promisor configuration before loading HEAD metadata. Test configured
monitor and pass-through clean-filter fixtures and assert neither executes.
Never run Git aliases, hooks,
network operations or automatic maintenance. Preserve .git and its contents.
No Git metadata means an extracted
stock copy; it still requires the baseline and --apply. A second initialization
refuses because initialization assets are removed.

## Apply, failures and recovery

Load resources and validate every reset/remove path before mutation. Print the
complete plan in both modes. For apply, create a uniquely named sibling backup
directory and copy all reset/remove originals plus the manifest there before any
replacement. Verify completeness and exact backup bytes against all originals,
including their original line endings; backup failure leaves the target alone.
Verify source/target/backup absolute boundaries. Write replacements
via same-directory temporary files and os.replace; unlink only approved stock
files. Empty directories may remain. Never recursively remove the target.

On an ordinary apply error, restore affected originals from the backup and
report failure, preserving the backup. On process termination/power loss, manual
recovery is required: inspect the Git diff and sibling backup before restoring
its files; do not blindly overwrite later work. Backups intentionally contain
old starter records outside the initialized project and are not application files.
No backup is made for a preview or preflight refusal. Concurrent hostile file
changes, disk failure during rollback and atomic multi-file commits are outside
this command's guarantee and must be disclosed.

## Verification and rollout

Use stdlib unittest and isolated temp copies. Observe red/green for preview/apply,
no-write refusal, changed/missing/extra files, invalid/traversal manifests, linked
paths, upstream remote/dirty Git, repeat refusal, CRLF stock copies, backup failure
before mutation, early replacement and late removal rollback, and clean
output scan. Run default source validation and project validation; mutate copies
to prove the denylist, generated guide, AGENTS and privacy still reject violations
under --project. Run the two source CI jobs, unchanged in name and matrix. Record
fresh reviewers/scopes/findings and actual evidence, not runtime assumptions.

User-selected approach approval covers this scope; any material departure needs
renewed approval. Rollback is the PR revert for source, and the named sibling
backup for an initialized disposable/new project after inspecting later edits.

## Fresh-review dispositions

- Initial requirements reviewer: canonical hash policy, cache-exception mismatch,
  backup verification and exact removal names. Accepted; addressed above and in
  INIT-002/005. No source content is normalized during preview.
- Initial technical reviewer: canonical hashes, preview bytecode writes and
  Windows aliases. Accepted; normalized text hashes, no cache exception/bytecode
  writes, and canonical unique ordinary paths are now specified.
- Fresh requirements/technical reviews and affected-section rereviews used new
  agents with fork_turns none (init_requirements_review, init_technical_review,
  init_requirements_rereview, init_technical_rereview and init_git_rereview).
  No inherited conversation was requested. Reviews found no remaining design
  blockers after the accepted revisions; they did not approve for the owner.
- Fresh requirements rereview found no remaining implementation blockers.
  Technical rereview accepted the main design but identified configured Git
  filesystem-monitor side effects. Accepted; the Git version/override policy
  and monitor-hook regression above resolve that boundary before implementation.
- Implementation review found that git status can execute clean/process filters.
  A parent-run pass-through filter fixture reproduced the write side effect.
  Accepted: replace status with cached index/HEAD checks and explicit worktree
  baseline/file-mode comparison; verify the same filter fixture stays inert.
- A separate fresh init_security_verification reviewer inspected the correction
  and the parent-run red/green fixture evidence: INIT-SEC-001 confirmed pre-fix,
  fixed in current code. No additional concrete helper/data-loss gap was reported
  in that bounded inspection. Runtime checks were run by the parent, not reviewer.
