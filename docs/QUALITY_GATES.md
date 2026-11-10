# Quality gates

## Installer diff verification (2026-11-10)

Scope: DIFF-001–DIFF-003; local --diff continuation, no release publication.

- DIFF-001: `test_diff_previews_changed_and_missing_managed_text_without_writes` observed red (unrecognized --diff, exit 2), then green with installed-to-checkout text and missing-final-newline markers. Fixture bytes, mtimes and directory entries are compared; newline-only changes have a separate case.
- DIFF-002: extra/obsolete names and manifest-only drift are tested without reading extra contents (including a non-UTF-8 extra file). Absent installation/manifest, malformed/path-invalid manifests and unreadable managed text retain inspection outcomes. Existing link tests also invoke --diff; symlink execution is skipped on this Windows host.
- DIFF-003: current/drift/error statuses and all conflicting modes are tested. A fresh read-only verifier (no inherited author conversation) found one output-encoding error: printing outside the handler caused an ASCII-output Unicode customization to exit 1 with a traceback. A subprocess regression observed that red result, then green exit 2 with no traceback after moving output into the handler. The verifier inspected the fix and marked the finding resolved; no other concrete finding was reported. Test execution was performed by the author, not independently rerun by the verifier.
- `python -m unittest discover -s tests -v`: passed, 90 methods, six host symlink skips, Windows/Python 3.13. Fixture writes required an outside-sandbox run because Windows temporary-directory writes are blocked in the sandbox.
- `python scripts/validate_starter.py`: passed. `git diff --check`: passed. Initialization baseline regenerated; inventory unchanged, only affected content digests updated. Final documentation/status updates receive refreshed baseline and validation checks.
- Local `python scripts/install_chat_command.py --diff`: `up to date` for the installed package. The implementation lives in the checkout's installer; packaged workflow content was not changed by this feature.
- Design gate: not applicable to this bounded inspection extension using the existing installer architecture. Security review scope: inspected shared manifest/link preflight, fixed-path managed reads and extra-content exclusion; no complete security audit or concurrent-filesystem guarantee is claimed.
- [PR #36](https://github.com/guventech/ai-project-starter/pull/36) implementation commit `67eff1c` passed Python 3.12 jobs `Starter validation (windows-latest)` and `Starter validation (ubuntu-latest)` in [run 42783168886](https://github.com/guventech/ai-project-starter/actions/runs/42783168886). Each job passed starter validation and the unittest suite. Both jobs remain required on the final PR head before merge. Rollback is reversion of the feature changes; inspection does not modify installations.

## Starter checks (configured)
- `python scripts/validate_starter.py`: required files and Cursor metadata.
- `python -m unittest discover -s tests -v`: validator failure detection and chat-command installation/overwrite protection.
CI runs both on Linux and Windows using Python 3.12.

## Review gates

- Requirements/planning: before nontrivial implementation, fill docs/PRD.md, check requirement wording and verification methods, resolve blocking questions with `/decision-interview` when needed, and obtain approval of the concrete plan. Existing approval covers unchanged scope.
- Design: use `/design-review` for a new system or material design change. Record the design revision, at least two fresh reviewer contexts and scopes, finding dispositions and human approval. No inherited conversation is allowed for goldfish reviewers. If the host cannot provide fresh contexts, the gate is unverified. A bounded change under an approved design can record this gate as not applicable with a reason.
- Behavior: use `/test-first-change` for executable behavior changes. Record the intended red failure, green result and affected regression results for each slice. Documentation changes use inspection and template validation rather than artificial behavior tests.
- Security: use `/trust-boundary-audit` for a requested audit or sensitive trust-boundary changes. Record reconnaissance, a coverage ledger, hunting evidence, independent candidate verification and a structured report. Every candidate needs a disposition. Missing verification remains needs-validation; missing coverage remains visible. Record non-applicability for changes without security-boundary effects.
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
| EVAL-001 | test | Authored todo CLI has requirements/plan/delegated authority, three observed red/green slices, six executable CLI boundary tests and fresh read-only verifier findings/dispositions in examples/todo_cli/README.md. Educational scope only. |
| EVAL-002 | demonstration | Eight frozen paired attempts retained: seven protocol failures and one accepted finish. Two final baseline artifacts pass all named checks, but useful comparative outcome evidence remains open; no superiority or general quality claim. |
| EVAL-003 | inspection | Published actions/results/final files/diffs, seven allowlisted visible-failure supplements and exact inputs.json hashes inspected by f02_results_review and f02_release_review. No private home paths, session IDs, reasoning or native payload bodies observed in that tree. |
| EVAL-004 | test | Inspected no-network/no-mount/nonroot/read-only-root container pilot passed; parent-owned grader rejected forged pass records. Native Read/Shell denial was observed, but complete native isolation is unverified, including search. Live --run/direct trial guards now refuse before result/model/Docker effects; offline parser/ownership/output/timeout tests pass. |
| EVAL-005 | inspection | EVIDENCE/VERIFICATION/README distinguish artifact checks, protocol failures and native-host/general claims. All checked examples/evals expand to individual initializer removals; no skills, weights or global account configuration changed during F-02. F-02 remains partial. |
| WEIGHT-001 | inspection | docs/SKILLS.md Process weights section names Lite, Standard and Strict with required and skippable columns. |
| WEIGHT-002 | inspection | project-helper Process weight section requires marker selection, one question when undetermined, Lite ceremony skips and Strict design/security retention. |
| WEIGHT-003 | test | `tests/test_process_weight.py` maps typo and symbol-rename goals to lite and a payment-feature goal to strict. |
| VER-001 | inspection | VERSION is `0.1.0`; CHANGELOG.md has a 0.1.0 section and states tagged GitHub Releases remain deferred. |
| VER-002 | test | `test_version_reports_source_version_without_writes` and `test_version_rejects_mutating_or_check_flags`. |
| VER-003 | test | Fresh install packages VERSION and prints `Package version:` matching `package_version()`. |
| LOG-001 | test | `tests/test_changelog_release.py` covers success, missing, duplicate and malformed heading cases without writes. |
| LOG-002 | test | Notes mode prints the VERSION heading and body; repository `--check` passes. |
| LOG-003 | test | Maintainer `validate_starter` includes changelog validation; absent files are skipped for initialized copies. |
| READ-001 | inspection | First 40 README lines contain purpose, audience, prerequisites, existing-project install/helper command and new-copy preview/apply path. No timed reading or usability-study result is claimed. |
| READ-002 | inspection | Calculator example links recorded Ask-mode evidence and is labeled a summary; comparison links upstream descriptions and marks fit as editorial judgment, with outcome comparisons unmeasured. |
| READ-003 | inspection | README links VERIFICATION, OPTIONAL_SKILLS, canonical SKILLS and migration guidance. One-off inspection resolved 37 relative links/anchors and confirmed all four existing pack commands. |
| READ-004 | test | Existing applied-copy test first caught the new overview's own PR link; adding VERIFICATION.md to the explicit removal inventory made the same test pass. Current plan has 12 resets/29 removals. |
| INIT-001 | test | Preview fixture checks directory entries, bytes and modification times; displayed RESET/REMOVE inventory is documented in INITIALIZE.md. No backup is created by preview. |
| INIT-002 | test | Modified/missing/extra/cache, malformed/aliased manifests, upstream fetch/push remotes and staged Git changes refuse. Symlink tests run where permitted; Windows junction refusal was observed locally. CRLF stock preview preserves bytes. |
| INIT-003 | test | Applied-copy fixture scans retained text for own PR/CI links and prior enhancement wording; reset PRD retains wording rules; LICENSE, attribution, AGENTS and workflow text remain byte-identical. |
| INIT-004 | test | Applied copy passes --project validation. Mutating its denylist, generated guide, AGENTS or privacy inputs causes rejection. Default source mode additionally checks required maintainer assets and baseline freshness. |
| INIT-005 | test | Exact originals match the sibling backup, including CRLF bytes. Corrupt/injected-failure backups cause no target changes; early replacement and late removal failures restore all target file bytes. Process interruption and rollback-disk failure remain documented limits. |
| CONTRIB-001 | inspection | CONTRIBUTING.md links the six existing project procedures; README links CONTRIBUTING. One-off inspection resolved all 17 local links across CONTRIBUTING/README to existing paths. |
| CONTRIB-002 | inspection | Bug-report and feature-request Markdown templates have distinct name/about metadata and title prefixes; prompts cover the specified report details. Existing scalar metadata reader accepted both blocks. |
| CONTRIB-003 | inspection | Guide and both templates ask for synthetic/redacted public reports; none assigns labels, assignees or a private reporting channel. All three new docs passed an explicit scan using the existing home-path patterns. |
| RULE-001 | test | test_rule_globs_cover_node_python_go_layouts checks actual metadata against three file layouts; observed nine missed-match subcases before the glob changes, then green. |
| RULE-002 | inspection | docs/RULES.md lists exact globs, trigger/intent, sample scope, copyable per-stack examples and a versioned host-check procedure; README/CONFIGURATION link it. |
| RULE-003 | inspection | All three rules retain alwaysApply false. SETUP.md records CLI Go positive/README control marker evidence and empty per-read attachment fields; static Node/Python results and editor/runtime limits are stated apart. |
| CHECK-001 | test | Check-mode fixtures compare bytes, modification times and directory entries before/after each invocation; absent destinations remain absent. |
| CHECK-002 | test | Installer tests cover current and old stock snapshots, changed/missing/extra/obsolete files, manifest-digest drift and malformed/incomplete/unknown-path manifests. Linked-entry/destination tests run where host symlink support permits. |
| CHECK-003 | test | CLI tests assert exit 0/1/2 for the documented states, invalid destination/content and each prohibited upgrade-flag combination. |
| SEARCH-001 | inspection | prior-art step 2 requires generic public terms, removal of confidential details, inspection of every outgoing query and skip when no useful public query can be formed. |
| SEARCH-002 | inspection | prior-art steps 3–6 reject retrieved disclosure/workflow/command instructions and retain the three-candidate cap and named-candidate adoption approval. |
| SEARCH-003 | inspection | evals/prior-art-search-hygiene.md defines synthetic confidential context, an injected result, a no-public-query variant and a pass/fail rubric; runtime execution is marked not run. |
| SEARCH-004 | test | Existing installer test compares the complete installed prior-art reference and manifest digest with the source; local suite passes with the host symlink skips described below. |
| REQ-001 | test | `python scripts/validate_starter.py` passes with all four new skill files and their explicit invocation metadata. |
| REQ-002 | inspection | decision-interview steps 2–6 require one question at a time, recorded decisions, zero implementation blockers and plan approval before code. |
| REQ-003 | inspection | test-first-change steps 2–5 require observed red for the intended reason, one behavior slice, green, refactor and regression checks. |
| REQ-004 | inspection | design-review defines elephant drafting, two isolated goldfish scopes, finding resolution and human approval; unavailable contexts keep review unverified. Skill attachment and two fresh Task probes were observed; the full design workflow was not executed. |
| REQ-005 | inspection | trust-boundary-audit defines inputs/outputs for four phases, a coverage ledger, fresh verification, three candidate dispositions and report fields including gaps. |
| REQ-006 | inspection | project-planning links interviews/design review and slice exit criteria; release-check maps requirements to evidence and discloses missing, stale or skipped gates. |
| REQ-007 | inspection | Architect questions assumptions and routes user decisions through the parent; verifier defines goldfish, diff and security modes. Both retain readonly true; starter validation passes. |
| REQ-008 | inspection | docs/SKILLS.md names all nine skills; README/AGENTS/CONFIGURATION link it; README lists the four pack commands; CONFIGURATION.md records host/installation limits. |
| REQ-009 | test | `test_each_required_skill_removal_detected` checks each of nine skills from `scripts/skill_inventory.py`. `test_skill_inventory_sources_agree` keeps installer, validator and CONFIGURATION/README inventories aligned. |
| SETUP-001 | inspection | GitHub branch-protection PUT response confirms both job names restricted to app 15368, strict checks, admin enforcement, pull requests, resolved conversations and blocked force pushes/deletion. |
| SETUP-002 | inspection | Four user-level checkouts and source SHAs are recorded in SETUP.md. Counts: Matt 27, Addy 25, Cloudflare 1, EGM 7 canonical skills. EGM standards and Addy shared references exist; the nine project skill files have no diff. |
| SETUP-003 | demonstration | Authenticated CLI smoke sessions recorded in SETUP.md show explicit attachment/path loading, native reviewer calls, write refusal and an absent parent canary. Three bare slash names selected upstream files; explicit local paths loaded the intended workflows. MAINT-002 later recorded tool-level Write denial for `verifier` with a successful control; general context isolation remains unproven. |
| MAINT-001 | test | Workflow uses `actions/checkout@v5` and `actions/setup-python@v6` (Node.js 24 majors). Job name, OS matrix, Python 3.12 and `contents: read` unchanged. Local `validate_starter.py` and unittest suite passed on Windows after the bump. PR CI run [42583862239](https://github.com/guventech/ai-project-starter/actions/runs/42583862239) passed both `Starter validation (ubuntu-latest)` and `Starter validation (windows-latest)`. |
| MAINT-002 | demonstration | Matched-pair host temp fixture: control `generalPurpose` Write succeeded; fresh `verifier` Write attempted and host-denied ask-mode/non-read-only; probe marker absent; control marker present. Label `host-denied`. Details in SETUP.md. |
| MAINT-003 | inspection | Queued maintenance scope; the target repository for full design/security review still awaits selection. |
| CHAT-001 | demonstration | User-level `/project-helper` in an empty temporary workspace asked exactly the new/improve mode question. Explicit new/existing goals selected their modes without repeating it. Session IDs are in SETUP.md. |
| CHAT-002 | test | Installer tests verify one discoverable SKILL.md, all eight workflow references and both reviewer references, with rewritten internal paths and no environment files. A separate workspace loaded the installed planning/TDD/verifier references. |
| CHAT-003 | demonstration | New-project planning probe used the installed planning reference and wrote no application files; the nonempty-target guard was strengthened after independent review. Final probe evidence is recorded in SETUP.md. |
| CHAT-004 | demonstration | Existing-project fixture review read its own AGENTS.md, calculator source and tests, used bundled TDD/verifier references and returned findings/proposed checks without changing files. This is a bounded routing trial, not a full application audit. |
| CHAT-005 | demonstration | Existing-project routing loaded a bundled workflow reference despite an optional upstream skill of the former colliding name. Bundled references use direct paths; no second slash command or configuration copy was requested. Installer tests cover all eight workflow references plus both reviewers. |
| COLLIDE-001 | test | Local skills use decision-interview, test-first-change, hypothesis-debugging and trust-boundary-audit; validator rejects colliding upstream directory names; forced upgrade removes obsolete reference snapshots. Merged via [PR #19](https://github.com/guventech/ai-project-starter/pull/19). |
| GUIDE-001 | test | `docs/SKILLS.md` is generated from skills-meta; `--check` and validator detect drift; README/AGENTS/CONFIGURATION link the guide. |
| CONSUME-001 | test | `AGENTS.md` stays ≤50 lines without maintainer markers; `MAINTAINING.md` and `docs/INSTALL.md` exist; `test_agents_maintainer_content_detected` fails when maintainer content returns. |
| CHAT-006 | test | Installer tests preserve an occupied destination and a customized command on repeat install. The symlink case is skipped when the host cannot create links; Linux CI executes that case. |
| PRIOR-001 | test | `python scripts/validate_starter.py` requires `.cursor/skills/prior-art`; `test_each_required_skill_removal_detected` covers `prior-art`. |
| PRIOR-002 | inspection | prior-art steps cap candidates at three, rank fit then activity/license then stars, and continue when search is unavailable. |
| PRIOR-003 | inspection | project-helper new-project step 2 and improve step 2 encode the hybrid trigger and skip path; workflow list includes prior-art for path selection. |
| PRIOR-004 | inspection | prior-art step 5 and project-helper prior-art steps forbid clone/copy without explicit candidate approval. |
| PRIOR-005 | test | Installer `WORKFLOWS` includes `prior-art`; installer tests expect `references/prior-art.md`; README/AGENTS list `/prior-art`. |
| UPGR-001 | test | Fresh install writes `.installer-manifest.json` with digests for managed content paths including `references/prior-art.md`. |
| UPGR-002 | test | Occupied destination and modified-command cases still refuse default install without changing user content. |
| UPGR-003 | test | `--upgrade` replaces a manifest-matching stock package; refuses extras, customized managed files, missing/incomplete/malformed manifests and (when links work) symlinks. |
| UPGR-004 | test | `--upgrade --force` backs up differing `SKILL.md` under `project-helper.bak-*` then restores planned content; extras and bare `--force` refuse. |
| HARD-001 | test | `test_upgrade_refuses_incomplete_manifest` and `test_upgrade_refuses_malformed_manifest_digest` refuse without changing files; clean/force upgrade regressions remain green. |
| HARD-002 | test | `test_unregistered_skill_detected` fails validation for an extra skill folder; `test_skill_inventory_sources_agree` requires each required skill in docs/SKILLS.md and guide links from README, CONFIGURATION and AGENTS. |
| HARD-003 | test | Fresh install stages then promotes a digest-matched package; injected `SKILL.md` and manifest write failures leave no destination and no `project-helper.staging-*`; `--upgrade` with an absent destination uses the same path; occupied destinations stay unchanged. |
| PRIV-001 | test | Public docs omit personal home paths; `test_personal_home_paths_detected` fails validation for Windows, macOS and Linux sample paths. Merged via [PR #16](https://github.com/guventech/ai-project-starter/pull/16). |
| ATTR-001 | test | `THIRD_PARTY.md` records upstream sources and classifications; installer tests expect the packaged notice and manifest digest entry; README links the notice. |

## F-02 partial evidence verification (2026-11-09)

Scope: authored reference, recorded exploratory attempts, blocked live model entry
points and initializer hygiene. Useful comparative outcomes are still missing;
this is not a readiness claim for the native workflow or an application release.

- Full local configured suite: 71 tests in 104.725 seconds on Windows/Python
  3.13.14; passed with six host symlink skips. Windows junction refusal passed.
  Applied-copy checks covered all 90 individual removals, exact backup/rollback
  bytes and preservation of the four source/project configuration safeguards.
- Source validation, project-manifest --check, skills-guide --check and
  git diff --check passed. Final evidence-only doc/baseline refresh receives the
  same source checks; both OS/Python 3.12 PR CI jobs remain required before merge.
- Observed red/green: add/list stub exit 2 -> green; missing done command -> green;
  missing pending filter -> green; five invalid action inputs were initially
  accepted -> rejected; initializer omitted five new evidence paths -> complete
  individual inventory. Additional boundary tests passed when added; no invented
  red result is claimed for them.
- Fresh reviews used fork_turns none: methodology and execution design, grading
  provenance rereview, implementation audit/independent candidate verification,
  pre-score, reference, initializer, result publication and release scope. Accepted
  findings fixed terminal-result/type validation, joined-response bounds, partial
  quarantine, process descendant ownership and grading authority. Final guard/hash
  review found no blocker to the explicitly partial source PR.
- Live demonstration: fixed Composer 2.5/CLI 2026.11.05-86047df and pinned Python
  3.12 image; eight attempts, 13 model calls, zero reviews. Frozen hashes verified
  before archiving, and a regression checks all six archived input hashes. No
  outcome-based retries. Readiness is distinct from the scored outcomes.
- Post-run search control used only an owned synthetic canary. Success without
  sentinel disclosure established neither outside content access nor denial.
  Native isolation therefore remains unverified; the live guards prevent further
  runs. No credentials were read/copied, new authenticated host provisioned or
  global helper package upgraded. No containers with the evaluation owner label
  remained after cleanup inspection.

Security coverage: model JSON -> typed action and publication allowlist reviewed
and tested; proposal paths -> container execution/limits and parent-owned grading
reviewed with bounded pilots; process/container ownership reviewed/tested; exact
initializer cleanup covered by existing refusal/backup/rollback tests. Native
host isolation is blocked/unverified, not passed. Docker/CLI internals, hostile
concurrency and provider revision identity remain outside these checks. Static
parser candidates were independently confirmed and fixed; no unresolved source
finding remains in the shippable offline/blocked-live scope. This is bounded
coverage, not proof that all vulnerabilities are absent.

Rollback: revert the PR. Historical failed results remain evidence; do not silently
rerun/replace them. No deployed application, user package or account needs rollback.

## F-07 README positioning verification (2026-11-09)

Scope: value/audience/entry-path rewrite and linked setup/evidence detail; retain brand and workflow behavior. The initialization inventory gains only the maintainer verification overview; the reusable optional guide remains.

- `python scripts/validate_starter.py`, `python scripts/project_manifest.py --check`, `python scripts/generate_skills_guide.py --check`, and `git diff --check`: passed after baseline refresh.
- `python -m unittest discover -s tests -v`: passed on Windows/Python 3.13.14 (56 tests, 6 host symlink skips). No new test runner or dependency.
- Applied-copy regression: observed red on the new VERIFICATION.md retaining an own PR link, then green after classifying it for removal and refreshing the plan/baseline. Four existing safeguards remain checked in both source/project coverage.
- One-off inspection: first-40-line criteria, 37 local links/anchors, all four optional commands, exact 12-reset/29-remove plan and existing home-path patterns passed.
- Fresh read-only documentation review (readme_clarity_review, fork_turns none): quickstart/example/evidence claims were coherent; one accepted finding corrected install guidance that overpromised --force recovery for unreadable manifest structures. Docs now distinguish missing/incomplete/invalid-digest manifests from unparseable JSON or missing/non-object files maps. Installer behavior was not changed.
- Comparison descriptions were checked against primary upstream README pages for Matt Pocock, Superpowers and Google EGM; Skills CLI's Node prerequisite was checked against its own README on 2026-11-09. Fit advice is editorial, not measured performance. No new outcome evaluation, exact transcript or complete-app demo is claimed.
- Design/security gates: not applicable to prose reorganization and classification of a new maintainer-only document under the existing initialization design. No new application boundary, skill or dependency. No user reading-time study or new live Cursor trial was performed.
- Implementation CI: [run 42667510658](https://github.com/guventech/ai-project-starter/actions/runs/42667510658) passed both Python 3.12 OS jobs for commit `c8cb629`. PR #28 includes this evidence follow-up and a regenerated baseline; both jobs remain required on its head before merge. PR #27 was reviewed in place and merged before this branch; no initializer or global upgrade was run on the source workspace.

## F-06 initialization verification (2026-11-09)

Scope: opt-in cleanup of stock copies; no initializer was applied to the upstream working tree, no global installation changed, and no application was published.

- Design gate: two fresh requirements/technical contexts and affected-section rereviews used fork_turns none. Findings on line endings, caches, backup verification, Windows aliases and Git monitor side effects were accepted and resolved; details and context names are in docs/designs/project-initialization.md. The owner's approval selected the initializer and delegated routine design choices; no material change to that choice was made.
- Observed red/green: preview test first failed because init_project.py was absent, then passed. Independent implementation review found a Git clean-filter execution path during status inspection; a disposable pass-through filter wrote its marker in the failing regression. Replacing status with cached index/HEAD metadata made that same regression pass.
- Final local full suite: `python -m unittest discover -s tests -v` passed on Windows/Python 3.13.14 (56 tests, 6 host symlink skips); the Windows-junction refusal case passed. An earlier 55-test suite also passed before that case was added.
- `python scripts/validate_starter.py`, `python scripts/project_manifest.py --check`, `python scripts/generate_skills_guide.py --check`, and `git diff --check`: passed after baseline regeneration. Source-document updates require regenerating the baseline before committing.
- One-off inspection matched INITIALIZE.md to all 12 reset and 28 remove paths, and resolved 21 documentation/resource links to retained outputs.
- Disposable copies: preview/apply, no-write refusal, normalized CRLF stock hashes, exact-byte backup verification, corrupt backup, early/late rollback, upstream fetch/push remotes, staged changes, monitor/filter nonexecution, clean records and the four --project invariants were exercised. No live Cursor application workflow is implied by these fixtures.

Scoped security coverage:

- Manifest/path boundary: reviewed schema, duplicate keys, normalized text hashing, traversal/drive/ADS/device/case aliases, symlinks/ancestors and junction rejection; hostile concurrent path replacement is excluded.
- Filesystem mutation: reviewed individual-file allowlist, checked sibling boundary, byte-complete backup, atomic per-file writes and ordinary-error restoration. Power loss, killed processes and disk errors during rollback require manual recovery and remain untested limits.
- Git metadata/helpers: reviewed monitor suppression, cached-only index/HEAD comparison, disabled external diff/text conversion and partial-clone refusal. Fixture monitor/filter calls stayed inert after the correction. No network command is used by initialization.
- INIT-SEC-001: confirmed pre-fix Git status could execute a configured clean filter during preview; parent reproduction observed the marker. Fixed current: status is no longer used. A separate fresh read-only verifier (init_security_verification, fork_turns none) checked reachability and correction against source and parent-run red/green evidence; it did not run fixtures itself. No other confirmed finding was reported in this bounded review.
- Validation/profile boundary: reviewed explicit --project selection; default source requirements and all four existing invariants are retained. No application authentication/production surface exists in this command.

Implementation CI: [run 42646464439](https://github.com/guventech/ai-project-starter/actions/runs/42646464439) passed both Python 3.12 jobs, `Starter validation (ubuntu-latest)` and `Starter validation (windows-latest)`, for commit `f15c605`. PR #27 includes this evidence follow-up and a regenerated baseline; both jobs remain required on its head before merge. This is a bounded initializer review, not a claim of host isolation or protection against all filesystem/configuration attacks.

## F-14 contribution basics verification (2026-11-09)

Scope: contributor guide, two Markdown issue templates and README entry link; remaining F-14 policies and repository/discoverability settings stay deferred.

- `python scripts/validate_starter.py`: passed.
- `python scripts/generate_skills_guide.py --check`: passed; generated guide unchanged.
- `python -m unittest discover -s tests -v`: passed on Windows/Python 3.13.14 (42 tests, 4 host symlink skips).
- `git diff --check`: passed.
- One-off local inspection: 17 relative links in CONTRIBUTING/README resolved within the repository; both templates parsed with the existing scalar metadata reader, had distinct names and nonempty about/title fields, and omitted labels/assignees. All three new public docs were checked against existing HOME_PATH_PATTERNS. This extends inspection to the new docs without changing validator scan scope or adding a dependency/test harness.
- Metadata/location inspection used the [official GitHub template guidance](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository). No issue was created and no live default-branch template chooser was verified. Markdown templates provide editable prompts, not required-field validation.
- Design/security/test-first gates: not applicable to documentation and Markdown prompts; no executable behavior, architecture or application trust boundary changed. Author inspection is not an independent fresh-context review. Existing F-01/F-03/F-05/privacy checks were not changed.
- PR CI: [run 42637969555](https://github.com/guventech/ai-project-starter/actions/runs/42637969555) passed both Python 3.12 jobs, `Starter validation (ubuntu-latest)` and `Starter validation (windows-latest)`, for implementation commit `0ed9131`. PR #26 includes this evidence follow-up; require green checks on its head before merge. No repository settings or global installations were changed.

## F-10 rule-trigger coverage verification (2026-11-09)

Scope: existing three rule globs, one layout regression test, trigger/adoption documentation and a bounded host probe. No new skills or dependencies.

- Observed red: layout regression failed nine subcases for Node app/lib, root Python/Go source, Go source directories and Go test filenames. After adding scoped roots and the Go test pattern, the same test passed.
- Initial PR CI [42636153183](https://github.com/guventech/ai-project-starter/actions/runs/42636153183) failed the layout fixture on Ubuntu/Python 3.12; Windows was cancelled by matrix fail-fast. Python 3.12 enumerates only directories for a trailing **, unlike local Python 3.13. The test now expands a trailing /** to /**/* for file enumeration; required matches and shipped rule globs are unchanged. The focused local rerun passed; corrected Python 3.12 CI remains required.
- `python scripts/validate_starter.py`: passed; docs/RULES.md is a required document. Existing F-01/F-03/F-05/privacy checks are retained.
- `python scripts/generate_skills_guide.py --check`: passed; generated guide unchanged.
- `python -m unittest discover -s tests -v`: passed on Windows/Python 3.13.14 (42 tests, 4 host symlink skips).
- `git diff --check`: passed.
- Live CLI probe: Windows Agent CLI `2026.11.05-86047df`; Go source/test session returned all three fixture-only rule markers, fresh README-only control returned none. Tool traces showed only sample-file Reads, no explicit rule reads or writes. This supports implicit rule inclusion in that fixture; per-read attachment arrays were empty. SETUP.md records method and limits without personal paths or session IDs.
- Static matching uses Python Path.glob, not Cursor's glob engine. No live Node/Python session, editor UI attachment check, universal engine-parity test or rule-enforcement claim.
- Design/security gates: not applicable to this bounded path-scope revision; no new architecture, credential use, application trust boundary or rule-body security behavior. This is author verification, not an independent fresh-context audit.
- Corrected implementation CI: [run 42636385652](https://github.com/guventech/ai-project-starter/actions/runs/42636385652) passed both Python 3.12 jobs, `Starter validation (ubuntu-latest)` and `Starter validation (windows-latest)`, for commit `9d69289`. PR #25 includes this evidence follow-up; require green checks on its head before merge. Global installations were not changed.

## F-13 read-only installer check verification (2026-11-09)

Scope: --check only; versioning, --diff and releases remain deferred.

- Observed red: current-package CLI test failed on unrecognized --check. After core status dispatch passed, manifest/absence/error cases failed on missing validation or incorrect status; adding validation made the focused 11-test run pass (2 host symlink skips).
- `python scripts/validate_starter.py`: passed.
- `python scripts/generate_skills_guide.py --check`: passed; no skill metadata changed.
- `python -m unittest discover -s tests -v`: passed on Windows/Python 3.13.14 (41 tests, 4 symlink skips because this host cannot create links).
- `git diff --check`: passed.
- Author inspection: check dispatch never calls install or a write helper; it compares source and manifest digests apart and does not open paths taken from the manifest. Existing upgrade behavior and F-01/F-03/F-05/privacy gates remain intact.
- Read-only user-install smoke check: --check reported `manifest invalid`; no repair or upgrade was attempted. The synthetic fixtures provide the no-write assertions and controlled state coverage.
- Design gate: not applicable; bounded CLI option within the existing installer architecture. Security evidence: malformed-manifest and link-rejection tests cover check-mode input boundaries; no independent fresh-context audit, hostile concurrent filesystem test or Windows junction fixture was executed. Snapshot limits are documented.
- PR CI: [run 42632489560](https://github.com/guventech/ai-project-starter/actions/runs/42632489560) passed both Python 3.12 jobs, `Starter validation (ubuntu-latest)` and `Starter validation (windows-latest)`, for implementation commit `d3476d0`. PR #24 includes this evidence follow-up; require green checks on its head before merge. No global installation was upgraded.

## F-16 search hygiene verification (2026-11-09)

Scope: query-redaction and confidentiality-skip instructions in the existing prior-art procedure, one synthetic scenario, and an extension to the existing packaging test. No new skill, dependency or runtime search layer.

- `python scripts/validate_starter.py`: passed.
- `python scripts/generate_skills_guide.py --check`: passed; metadata and generated guide unchanged.
- `python -m unittest discover -s tests -v`: passed on Windows/Python 3.13.14 (30 tests, 2 symlink skips because host link creation is unavailable). The first sandbox run failed to access temporary fixtures; the permitted rerun reached the tests and passed. This was an environment failure, not a test-first behavior failure.
- `git diff --check`: passed.
- Procedure and scenario inspection: SEARCH-001–SEARCH-003 map to the text and rubric above; the installer test covers SEARCH-004. This is author inspection, not an independent fresh-context review or live Cursor execution.
- Design gate: not applicable; bounded revision of the existing Markdown procedure and packaging check, with no new architecture. Security evidence: inspected the outgoing-query and retrieved-content instructions; live enforcement remains unverified. No completed runtime security audit is claimed.
- Runtime scenario: not run; model/host traces and isolation evidence unavailable in this batch. Comparative F-02 evals remain deferred.
- PR CI: [run 42630609973](https://github.com/guventech/ai-project-starter/actions/runs/42630609973) passed both Python 3.12 jobs, `Starter validation (ubuntu-latest)` and `Starter validation (windows-latest)`, for implementation commit `e1a0338`. PR #23 includes the evidence follow-up; require green checks on its head before merge. Existing global snapshots were not upgraded.

## Inventory and upgrade hardening verification

Scope: exact-path/digest manifest checks for non-forced upgrades; reject unregistered local skills; AGENTS inventory coverage. Observed red: incomplete-manifest upgrade returned 0 and would overwrite a customized omitted path; unregistered-skill and AGENTS assertions added with the implementation. After green: `python scripts/validate_starter.py` passed; `python -m unittest discover -s tests -v` passed (21 methods, 2 symlink skips); `git diff --check` passed. Merged via [PR #14](https://github.com/guventech/ai-project-starter/pull/14).

## Transactional fresh install verification

Scope: sibling staging directory, validate-then-rename promotion for fresh installs and `--upgrade` when absent; existing in-place upgrades unchanged. Observed red: `fail_after` was rejected by `install()`. After green: `python scripts/validate_starter.py` passed; `python -m unittest discover -s tests -v` passed (25 methods, 2 symlink skips); `git diff --check` passed. PR CI pending.

## Phase B installer upgrade verification

Scope: manifest-based `--upgrade` / `--upgrade --force` with sibling backups. Observed red: installer tests failed on unrecognized `--upgrade`/`--force` before implementation. After implementation: `python scripts/validate_starter.py` passed on Windows; `python -m unittest discover -s tests -v` passed (18 methods, 2 symlink skips); `git diff --check` passed. PR CI run [42592357225](https://github.com/guventech/ai-project-starter/actions/runs/42592357225) passed both OS jobs. Merged via [PR #11](https://github.com/guventech/ai-project-starter/pull/11) (`02600a2`). Maintainer global package upgraded with `--upgrade --force`; `.installer-manifest.json` is present at `~/.cursor/skills/project-helper`.

## Phase A inventory integrity verification

Scope: shared skill inventory, doc/evidence alignment for nine skills / eight workflows, and drift regression. Observed red: `test_skill_inventory_sources_agree` failed with `prior-art missing from CONFIGURATION.md`. After the CONFIGURATION and evidence updates: `python scripts/validate_starter.py` passed on Windows; `python -m unittest discover -s tests -v` passed (10 methods, 1 symlink skip); `git diff --check` passed. PR CI run [42589919473](https://github.com/guventech/ai-project-starter/actions/runs/42589919473) passed both OS jobs. Merged via [PR #9](https://github.com/guventech/ai-project-starter/pull/9) (`25ca0ee`).

## Prior-art verification

Local Windows checks after implementation: `python scripts/validate_starter.py` passed; `python -m unittest discover -s tests -v` passed (9 methods, 1 symlink skip). `git diff --check` passed. PR CI run [42586480260](https://github.com/guventech/ai-project-starter/actions/runs/42586480260) passed both OS jobs.

Independent read-only verifier review (fresh Task, no inherited conversation claimed by the parent; host isolation remains unverified) marked PRIOR-001–PRIOR-005 pass against the skill, helper, planning pointer, validator and installer sources. One non-blocking wording gap was fixed: project-planning now restates the clone/copy approval rule. Live Cursor attachment of `/prior-art` and a reinstall of the global project-helper package were not executed in this delivery.

## Project-helper verification

The approved command is installed under `~/.cursor/skills/project-helper`. Initial tests observed the absent installer and missing project-helper validator requirement before implementation. After implementation, the validator passes and the unittest suite runs nine test methods; on this Windows host eight pass and the symlink test is skipped because link creation is unavailable. PR CI provides the cross-platform result. `git diff --check` passes.

A fresh read-only reviewer inspected the entry skill, installer and tests. Its nonempty-target clarification was applied: disclose existing contents and wait for the user's decision before planning writes. The reviewer found no additional concrete installer bug. The final live fixture runs and their limits are recorded in SETUP.md. They exercise menu/routing/approval boundaries in CLI Ask mode, not autonomous application creation, editor UI behavior or OS-enforced write restrictions.

## Enhancement verification record (2026-11-09)

Scope: the approved starter workflow enhancement in docs/PRD.md. This record covers procedure content and starter validation, not a live application release or execution of the prescribed audits.

- `python scripts/validate_starter.py`: passed on Windows, Python 3.13.14.
- `python -m unittest discover -s tests -v`: originally passed five test methods including seven skill-removal subcases; the suite later grew to nine methods (installer coverage plus prior-art) and then ten with inventory-alignment coverage. Initial sandbox run could not access Windows temporary directories; rerunning with permission reached the expected red failures, then passed after the validator change.
- `git diff --check`: passed.
- Independent procedure review: a read-only reviewer started with no inherited conversation inspected the six planning/review skills and both agents. It checked unavailable fresh contexts and unavailable security reproduction scenarios: the procedures retain unverified/needs-validation outcomes. Its one wording clarification was applied to project-planning's exit criterion to require both fresh reviews when the design gate applies. This is a document review, not live Cursor execution.
- Design gate for this change: not applicable; this extends existing Markdown procedures and required-skill validation within the approved stack-agnostic architecture. The added design-review procedure was inspected, not executed as a live Cursor workflow.
- Security audit gate for this change: not applicable; no application trust boundary, runtime dependency or publishing behavior changed. The audit procedure was inspected, not executed against a target.
- Original local validation did not run Linux/Python 3.12 checks. Subsequent GitHub run [42577848331](https://github.com/guventech/ai-project-starter/actions/runs/42577848331) passed both OS jobs on Python 3.12 for commit 8391565. The authorized setup follow-up installed the optional packs outside the repository and configured branch protection. Authenticated CLI smoke checks then exercised attachment/path loading and both native reviewers; SETUP.md records observations, collisions and limits. Application checks remain unconfigured.
