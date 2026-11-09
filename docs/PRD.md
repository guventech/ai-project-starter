# Product requirements

Status: approved starter enhancement implemented; requirement evidence is recorded in docs/QUALITY_GATES.md. Bounded authenticated Cursor CLI smoke checks are complete; MAINT-002 recorded a matched-pair host-denied Write for `verifier`. Full workflow execution and OS-level isolation remain outside that evidence.

- Problem and target users: Cursor users need planning, test-first development and review workflows beyond the three starter skills.
- Primary user journey: clarify requirements, draft and review a design, approve implementation, build in tested slices, then verify release evidence.
- Goals and measurable success: nine local skills (project-helper plus eight workflows), two read-only reviewers and documented review gates, with both starter check commands passing.
- Constraints: retain a stack-agnostic template, existing Cursor metadata conventions and dependency-free validation. Keep secrets out of review inputs and reports.
- Functional requirements and acceptance criteria: see the table below.
- Out of scope: application code, stack selection, note-taking integration and application deployment. Follow-up authorization covers optional pack installation, repository protection and documentation commits.
- Assumptions: local workflows are independently written instructions informed by the linked packs, not vendored copies. Fresh-context reviews require host support; unavailable review execution must be reported as unverified.

## Requirement wording

shall means a requirement, will means a fact, and should means a goal.

Each requirement is one thought. It says what the product must do and leaves the design out.

Avoid these vague words: fast, easy, user-friendly, robust, adequate, minimize, maximize, flexible, sufficient, safe, portable, and other vague words ending in ly or ize.

These rows cover the starter enhancement requested in CURSOR_UPDATE_PROMPT.md. Replace them when adopting the template for an application.

## Requirements

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| REQ-001 | The starter shall include decision-interview, test-first-change, design-review and trust-boundary-audit skills. | Add the four workflows named in the update prompt, using collision-free local names. | All four folders contain a SKILL.md with matching name, description and explicit invocation metadata. | test |
| REQ-002 | The decision-interview skill shall require resolution of implementation-blocking questions before coding. | Turn assumptions into decisions and measurable criteria. | Instructions cover one-question-at-a-time interviews, decision recording and an exit condition with zero unresolved implementation blockers. | inspection |
| REQ-003 | The test-first-change skill shall prescribe a red-green-refactor cycle for each behavior slice. | Verify behavior before expanding implementation. | Instructions require observing a failing test for the intended reason, implementing one slice, rerunning tests and refactoring after green. | inspection |
| REQ-004 | The design-review skill shall require design drafting, fresh-context review and human approval before implementation. | Expose assumptions absent from the design document. | Instructions define both phases, at least two bounded fresh reviewers, finding resolution and an unverified outcome when fresh contexts are unavailable. | inspection |
| REQ-005 | The trust-boundary-audit skill shall define four audit phases with finding verification. | Distinguish supported findings from suspicions. | Reconnaissance, coverage-led hunting, fresh-agent verification and reporting each have inputs and outputs; reports include coverage gaps and finding dispositions. | inspection |
| REQ-006 | The planning and release skills shall reference the new review workflows and their exit criteria. | Connect the lifecycle without imposing application tooling. | Planning references decision-interview and design-review; release-check requires requirement evidence, applicable review results and disclosure of skipped or missing gates. | inspection |
| REQ-007 | Both review agents shall define read-only responsibilities for their review modes. | Preserve the author/reviewer boundary. | Architect includes requirements questioning and design review; verifier includes fresh-context design, diff and finding review with evidence and limitations; both retain readonly true. | inspection |
| REQ-008 | The documentation shall describe the nine local skills, review gates and four external pack installation commands. | Make local workflows and optional external installations discoverable. | docs/SKILLS.md names all nine skills; README, AGENTS and CONFIGURATION link that guide; README links OPTIONAL_SKILLS.md containing all four pack commands; QUALITY_GATES.md maps requirements to evidence; configuration docs state runtime verification limits. | inspection |
| REQ-009 | The validator shall detect removal of any required local skill. | Prevent future updates from dropping the requested workflows. | Tests remove each of the nine required skills in turn and assert a missing-skill error; inventory sources stay aligned; both configured starter check commands pass. | test |

The acceptance criterion needs a measurable value or a tolerance. The verification method is test, analysis, demonstration, or inspection.

## Authorized setup follow-up

The user requested all remaining checks and optional installations after the enhancement was pushed. Keep external packages in user-level Cursor directories to preserve the template's nine local skills and stack-agnostic scope. Do not configure application tooling before a stack is selected.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| SETUP-001 | The main branch shall require the Windows and Linux starter CI checks before merging changes. | Both Python 3.12 jobs passed for commit 8391565. | GitHub settings show both exact job names as required, strict status checks, and no force pushes or branch deletion. | inspection |
| SETUP-002 | The setup shall install the four optional upstream packs outside this repository. | Keep shared resources intact and preserve the nine local skills. | Each pack has a recorded source revision and installed path; EGM retains agents and document standards; no local skill is overwritten. | inspection |
| SETUP-003 | The verification record shall distinguish observed Cursor execution from unavailable checks. | CLI authentication and host capabilities can block runtime evidence. | Record installed editor/CLI versions, login status and results for skill discovery, read-only agents and fresh-context review; any missing result stays unverified. | demonstration |

Setup risks: upstream names can overlap project skills; full-package resources must remain beside their skills; live execution requires Cursor authentication. Rollback removes only the added user-level package directories and the new branch-protection configuration after checking current state. Existing user configuration remains untouched.

## Proposed maintenance follow-up

Status: MAINT-001 merged via PR #5 (`checkout@v5` + `setup-python@v6`). MAINT-002 demonstration recorded (`host-denied` matched-pair probe). MAINT-003 remains queued; the target for the full reviews is pending user selection.

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
| CHAT-002 | The installed command shall include the local procedures and reviewer instructions it needs. | Other projects should not need manual file copying or this repository's absolute path. | A dependency-free installer packages eight workflow files and two reviewer definitions with the entry skill; the installed command loads these files from another workspace. | test |
| CHAT-003 | New-project mode shall obtain an approved plan before implementation. | Project goals and target directory must be resolved before building. | The assistant gathers the idea and target folder, records measurable criteria, presents a plan, and writes no application code before approval; nonempty target folders require an explicit decision to use them. | demonstration |
| CHAT-004 | Existing-project mode shall inspect the open project's instructions and checks before proposing edits. | Existing conventions and user changes must be preserved. | Initial review reports findings and evidence without changing application files; implementation follows approval of a bounded plan. | demonstration |
| CHAT-005 | The command shall select bundled workflows by file path. | Upstream slash names have known collisions. | Installed-mode probes load the bundled paths for overlapping names and require no second slash command from the user. | demonstration |
| CHAT-006 | The installer shall refuse to replace an existing destination. | Global user skills must not be overwritten by setup. | Tests show an occupied or linked destination is rejected without changing its contents; install output identifies the command location and reload step. | test |

Implementation plan: add the project-helper entry skill; add a one-time Python installer that bundles the existing workflows and reviewers without dependencies or machine-specific paths; extend starter validation and installer tests; simplify README/AGENTS guidance; install into the user's Cursor skill directory; run isolated new/existing-mode CLI probes and both starter gates; commit through a pull request after CI. No standalone website, desktop window, application framework, automatic deployment or upstream skill rename is part of this change.

Risks and verification: the host must discover user-level skills after a reload; test invocation outside this repository. Keep new-project probes in temporary folders and existing-project probes read-only. Missing subagent capabilities or checks remain explicit limitations. Rollback removes only the added command package after checking for user edits, and reverts its repository diff.

## Prior-art research workflow

Status: merged via PR #7. Hybrid trigger, fit-first ranking, adopt-only-with-candidate-approval, and chat-plus-conditional-docs recording were decided with the user.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| PRIOR-001 | The starter shall include a prior-art skill with explicit invocation. | Reuse existing public work before inventing. | `.cursor/skills/prior-art/SKILL.md` exists with matching name, description and `disable-model-invocation: true`. | test |
| PRIOR-002 | The prior-art skill shall produce a capped candidate memo ranked by fit before popularity. | Stars alone mislead; token cost stays bounded. | Instructions require at most three candidates, rank fit then activity/license then stars, and continue when search is unavailable. | inspection |
| PRIOR-003 | The project-helper shall invoke prior-art under hybrid rules with an explicit skip path. | Always-on wastes tokens on tiny fixes; new work benefits from research. | New-project mode runs prior-art unless skipped; improve mode skips only tiny goals or an explicit skip; selection uses the local skill path. | inspection |
| PRIOR-004 | The workflows shall require explicit approval of a named candidate before cloning or copying third-party code into the target. | Plan approval must not silently import remote code. | prior-art and project-helper forbid clone/copy/vendor without explicit candidate approval. | inspection |
| PRIOR-005 | The validator and installer shall treat prior-art as a required bundled workflow. | Prevent silent loss of the research step. | Removal of prior-art fails validation; installer packages `references/prior-art.md`; docs list the skill. | test |

Design review for this change: not applicable; extends existing Markdown skill architecture with no new runtime trust boundary. Independent read-only review of the skill text is recorded before merge. Risks: unavailable search tools, over-triggering on improve-mode, stale global installs that omit the new reference. Rollback reverts the feature branch or PR.

## Phase B installer upgrade (approved)

Status: merged via PR #11; maintainer global install refreshed with `--upgrade --force`.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| UPGR-001 | A successful install shall write an installer manifest of managed-file digests. | Detect stock packages without trusting hand inspection. | `.installer-manifest.json` lists SHA-256 digests for every managed content path after install. | test |
| UPGR-002 | Default install shall refuse an occupied destination. | Preserve CHAT-006. | Occupied path or symlink exits non-zero without changing contents. | test |
| UPGR-003 | `--upgrade` shall replace a clean stock package or install when missing. | Allow updates without manual delete. | Manifest-matching packages are replaced from the repo; missing destinations are installed; extras, customized managed files, missing/incomplete/malformed manifests and symlinks refuse without `--force`. | test |
| UPGR-004 | `--upgrade --force` shall back up differing managed files then overwrite managed content when no extras exist. | Limit data loss while unblocking pre-manifest and customized packages. | Differing managed files appear under `project-helper.bak-<timestamp>/`; extras and bare `--force` still refuse. | test |

## Inventory and upgrade hardening (approved with Codex)

Status: HARD-001/HARD-002 merged via PR #14. HARD-003 implemented locally after Codex agreement; PRD wording automation and MAINT-003 remain deferred/blocked.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| HARD-001 | Non-forced upgrades shall require a complete installer manifest with valid SHA-256 digests for every planned managed path. | Incomplete manifests could skip customization checks for omitted paths. | Incomplete path sets or non-SHA-256 digests refuse without changing installed files; clean and forced upgrades retain documented behavior. | test |
| HARD-002 | The validator shall reject unregistered local skill directories and inventory tests shall require each required skill name in the canonical skill guide. | Unexpected skill folders and inventory drift weaken the template contract. | An extra valid skill folder fails validation; docs/SKILLS.md names every required skill; README, AGENTS and CONFIGURATION link the guide. | test |
| HARD-003 | Fresh installs shall stage managed files beside the destination and promote the package only after the staged contents and manifest validate. | Direct writes can leave a partial package after an I/O failure. | Injected write or manifest failures leave no destination and no staging directory; successful install and `--upgrade` when absent promote a complete digest-matched package; occupied destinations remain unchanged. Existing in-place upgrades stay unchanged. | test |

## Review remediation F-08 privacy hygiene

Status: merged via PR #16.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| PRIV-001 | Public starter documentation shall omit personal home-directory paths. | Named profile paths leak maintainer identity into template copies. | README, AGENTS and docs Markdown contain no Windows, macOS or Linux personal profile path forms; the validator reports injected samples for each OS. | test |

## Review remediation F-04 attribution

Status: merged via PR #17.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| ATTR-001 | The starter shall publish a third-party notice that records upstream sources, licences and the audited use classification for local skills. | Readers need provenance for overlapping skill names and inspiration claims. | `THIRD_PARTY.md` exists; the installer packages and digests it; README and skill footers match the audit language; an ADR records the comparison method and results. | test |

## Review remediation F-01 skill rename

Status: merged via PR #19.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| COLLIDE-001 | Local skills shall not use the colliding upstream names grill-me, tdd, systematic-debugging or security-audit. | Bare slash commands selected upstream packs under those names. | Required skills use decision-interview, test-first-change, hypothesis-debugging and trust-boundary-audit; the validator rejects the four colliding directory names; forced upgrades remove obsolete reference snapshots. | test |

## Review remediation F-03 skill decision guide

Status: merged via PR #20.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| GUIDE-001 | The starter shall publish a generated docs/SKILLS.md decision guide kept in sync with local skill metadata. | Duplicate skill lists drifted and lacked use/do-not-use guidance. | docs/SKILLS.md lists every required skill once with the required columns and a lifecycle diagram; the generator `--check` mode and validator fail when the guide is stale; README, AGENTS and CONFIGURATION link the guide instead of maintaining competing inventories. | test |

## Review remediation F-05 consumer AGENTS split

Status: merged via PR #21.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| CONSUME-001 | AGENTS.md shall contain only consumer behavioral rules and links, with maintainer and install details in separate docs. | Template copies inherited maintainer-only instructions and install ceremony. | AGENTS.md is at most 50 lines and omits maintainer markers; MAINTAINING.md and docs/INSTALL.md exist; the validator rejects maintainer content reintroduced into AGENTS.md. | test |

## Review remediation F-16 search hygiene

Status: approved scope implemented in [PR #23](https://github.com/guventech/ai-project-starter/pull/23); local verification and implementation-commit CI recorded in docs/QUALITY_GATES.md. Runtime scenario not run; require green checks on the PR head before merge.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| SEARCH-001 | The prior-art procedure shall require removal of confidential content before sending a search query. | Search providers receive query text. | Instructions exclude secrets, private PRD text, client names and internal identifiers from queries; require inspection of each outgoing query; skip search when no useful public query can be formed. | inspection |
| SEARCH-002 | The prior-art procedure shall treat retrieved instructions as untrusted data. | Search results can contain instructions to disclose project context. | Instructions reject requests to disclose context, change the workflow or run commands; retain the three-candidate cap and named-candidate adoption approval. | inspection |
| SEARCH-003 | The repository shall provide a synthetic search-hygiene scenario with a pass/fail rubric. | Written procedures do not establish agent enforcement. | One scenario covers confidential input, an injected result and a no-public-query variant; records expected outcomes and labels unexecuted runtime checks as not run. | inspection |
| SEARCH-004 | The installed prior-art reference shall retain the source procedure. | Global installations use a bundled snapshot. | The existing installer test compares the installed prior-art reference with the source and its manifest digest; both starter commands pass. | test |

Wording self-check: each row uses shall, contains one requirement, avoids the listed vague words, and has a verification method. Approved plan: revise the existing procedure, add one synthetic scenario, extend the existing packaging check, and record actual gate results. No new skills, dependencies or research harness. Risk: instruction inspection may be mistaken for runtime enforcement; report those evidence types apart. Rollback: revert the F-16 PR; installed snapshots change only on an authorized upgrade.

## Review remediation F-13 read-only installer check

Status: approved slice implemented in [PR #24](https://github.com/guventech/ai-project-starter/pull/24); local verification and implementation-commit CI recorded in docs/QUALITY_GATES.md. Versioning slice follows below; `--diff`, tags and GitHub Releases remain deferred.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| CHECK-001 | The installer shall report installed package status through --check without writing files. | Users need to inspect snapshots before choosing an upgrade. | Reports up to date, N files differ, not installed, manifest missing or manifest invalid; tests compare file bytes, modification times and directory entries before and after each check. | test |
| CHECK-002 | The check shall compare installed files with the current checkout and validate the installed manifest. | A manifest matching an older snapshot does not mean the snapshot matches the current source. | Changed, missing, extra and obsolete files count as differences; a stock older snapshot reports drift; malformed or incomplete manifests and linked entries are rejected. | test |
| CHECK-003 | The check command shall return documented exit codes. | Scripts need to distinguish drift from errors. | Exit 0 means up to date; exit 1 means drift, absent installation or absent manifest; exit 2 means invalid manifest, unsupported destination, read error or invalid arguments; --check with --upgrade or --force exits 2 without writes. | test |

## Review remediation F-13 version metadata slice

Status: merged via PR #32; `--diff` and published releases remain deferred.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| VER-001 | The repository shall publish a VERSION file and CHANGELOG.md that identify the current starter package revision. | Installers and readers need a local revision marker without implying a GitHub Release. | VERSION contains `0.1.0`; CHANGELOG.md records the 0.1.0 entry and states that tagged releases remain deferred. | inspection |
| VER-002 | The installer shall report the VERSION value through --version without writing files. | Operators need the packaged revision before changing an install. | `--version` prints the VERSION text and exits 0; combining it with `--check`, `--upgrade` or `--force` exits 2 without writes. | test |
| VER-003 | Successful install and upgrade shall ship VERSION inside the package and print that package version. | Installed snapshots must carry the revision they were built from. | Planned files include VERSION matching the source file; install stdout includes `Package version:` with that value. | test |

Wording self-check: each shall row is one requirement, avoids the listed vague words, and has a measurable criterion plus verification method. Approved scope: add VERSION/CHANGELOG, wire `--version` and install/upgrade version printing, package VERSION, update docs/tests/gates, regenerate the initialization baseline so VERSION/CHANGELOG are removed from application copies. Risk: changelog text can over-claim shipping; keep explicit “not a published GitHub Release” language.

Wording self-check: each shall row has one requirement, a measurable acceptance criterion and a test method; none uses the listed vague words. Approved plan: add check dispatch, fixture-based red/green tests and install documentation, then run both starter gates and PR CI. Risk: confusing manifest integrity with current-source freshness; test those comparisons apart. The manifest detects accidental edits, not tampering. No new dependencies or skills. Rollback: revert this slice's PR; check mode does not change installations.

## Review remediation F-10 rule-trigger coverage

Status: approved scope implemented in [PR #25](https://github.com/guventech/ai-project-starter/pull/25); static, bounded CLI probe and corrected implementation CI evidence recorded in docs/QUALITY_GATES.md and docs/SETUP.md. Require green checks on the PR head before merge.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| RULE-001 | The scoped rules shall cover the documented Node, Python and Go sample layouts. | Existing source globs miss app/lib and Go cmd/internal/pkg layouts; testing omits Go test names. | Existing unittest runner checks architecture/security matches for each layout's source files, testing matches for its tests, shared documentation/CI triggers, and an unrelated README exclusion. | test |
| RULE-002 | The repository shall document each rule's globs, trigger and intent. | Consumers need to adapt rule scope to their layout. | docs/RULES.md lists all three rules, copyable Node/Python/Go glob examples and a versioned live-attachment check procedure; README and CONFIGURATION link it. | inspection |
| RULE-003 | Rule verification shall distinguish static path matching from observed host attachment. | Python glob results cannot establish Cursor execution. | Evidence records static command results and live probe results or an unverified outcome; all three rules retain alwaysApply false. | inspection |

Wording self-check: one shall requirement per row; listed vague words absent; each row has a measurable criterion and a verification method. Approved plan: add layout regression fixtures, extend the existing globs, document triggers, run starter checks and attempt a bounded read-only host probe if available, then submit one PR. Risks: extra source matches increase attached context; retain explicit path scope and disclose unsupported layouts and glob-engine differences. No new skills, dependencies or application stack. Rollback: revert the F-10 PR.

## Review remediation F-14 contribution basics

Status: approved documentation slice implemented in [PR #26](https://github.com/guventech/ai-project-starter/pull/26); local inspection and implementation-commit CI recorded in docs/QUALITY_GATES.md. Require green checks on the PR head before merge. Security policy, code of conduct, repository settings, social preview and pinned content remain deferred.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| CONTRIB-001 | The repository shall provide a contributor entry point that links the existing project procedures. | Contributors need reporting and PR guidance without a second maintainer policy. | CONTRIBUTING.md links AGENTS, MAINTAINING, INSTALL, SKILLS, QUALITY_GATES and the PR template; README links CONTRIBUTING; all relative targets exist. | inspection |
| CONTRIB-002 | The repository shall provide bug-report and feature-request issue templates. | Reports need reproduction details or a concrete proposed outcome. | Two Markdown templates have distinct name/about metadata; bug reports request revision, host versions, steps, expected/actual results and optional redacted evidence; feature requests ask for problem, outcome and alternatives. | inspection |
| CONTRIB-003 | Contribution guidance shall ask reporters to exclude confidential content from public reports. | Logs and example project text can disclose private information. | Guide and both templates request synthetic or redacted details and omit assumed private reporting channels, labels and assignees. | inspection |

Wording self-check: each row uses shall, has one requirement, avoids the listed vague words and has an inspection method. Approved plan: add a short linked guide and two Markdown templates, inspect metadata/links/privacy wording, run existing starter checks, and submit one PR. Risk: template prompts are editable guidance, not enforced form validation; document that limit. No new skills, dependencies, workflow or repository settings. Rollback: revert this PR.

## Review remediation F-06 project initialization

Status: owner-approved initializer implemented in [PR #27](https://github.com/guventech/ai-project-starter/pull/27) after fresh design reviews and rereviews; local evidence, scoped security verification and implementation CI are recorded in docs/QUALITY_GATES.md. Require green checks on the PR head before merge. README positioning remains F-07 scope.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| INIT-001 | Initialization shall show an explicit reset/remove plan before changing a template copy. | A preview makes cleanup reviewable. | Default invocation writes nothing; --apply is required for mutation; docs list every reset/remove target and kept categories. | test |
| INIT-002 | Initialization shall refuse a copy that differs from the shipped baseline. | Cleanup must not overwrite application work. | Content changes other than line-ending conversion, missing/extra files (including bytecode caches), linked paths, invalid manifests, dirty Git worktrees and the upstream repository remote cause refusal before writes; controlled repeats refuse. | test |
| INIT-003 | Initialization shall replace starter project records with unfilled application records. | New projects must not inherit requirements or verification evidence from this starter. | Disposable-copy scan finds no own PR links, CI run IDs, personal paths or starter-enhancement requirements outside version-control metadata; attribution and licence remain. | test |
| INIT-004 | Initialized projects shall retain the workflow validation invariants. | Cleanup must preserve the established safeguards. | Explicit --project validation checks colliding skill names, generated-guide freshness, consumer-only AGENTS rules and privacy; default source validation retains maintainer requirements and baseline checks. | test |
| INIT-005 | A failed initialization shall retain recovery data for the affected stock files. | Filesystem errors can interrupt replacement or removal. | Backup bytes match every affected original before mutation; injected backup failure leaves the target unchanged; replacement/removal failures restore originals; documentation describes process-interruption recovery and excludes concurrent filesystem attacks. | test |

Wording self-check: each row uses shall, contains one requirement, avoids the listed vague words and has an executable or inspection method. Approved plan: assess scope, obtain two fresh read-only design reviews, implement preview/apply and baseline guard in tested slices, retain core validation through explicit project mode, verify disposable copies and failure recovery, then submit one focused PR. Risks: changed snapshots must refuse; interrupted processes need manual recovery from the sibling backup; no application stack or Git history rewrite is authorized. No new skills or dependencies.

## Review remediation F-07 README positioning

Status: authorized continuation implemented in [PR #28](https://github.com/guventech/ai-project-starter/pull/28); local checks, documentation review and implementation CI recorded in docs/QUALITY_GATES.md. Require green checks on the PR head before merge. Branding remains unchanged under ADR-015; F-02 comparative evaluations remain separate work.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| READ-001 | The README shall introduce the audience, purpose and two entry paths before detailed reference material. | Readers need to choose existing-project installation or new-copy initialization. | First 40 lines contain the value proposition, intended use, install/helper command and new-copy initialization pointer; prerequisites and preview/apply distinction are stated. | inspection |
| READ-002 | The README shall distinguish sourced workflow examples and comparisons from effectiveness claims. | Routing trials and upstream descriptions do not establish outcome improvements. | One recorded CLI trial is summarized with its source and limits; comparisons link primary upstream descriptions and make no better/faster claim or fabricated transcript. | inspection |
| READ-003 | The README shall link detailed setup and verification guidance from concise summaries. | Installation/migration and evidence details should have dedicated homes. | Verification summary links VERIFICATION.md; optional packs link OPTIONAL_SKILLS.md with four existing commands; canonical SKILLS guide and F-01 migration/install details remain discoverable; relative targets exist. | inspection |
| READ-004 | Initialized copies shall exclude the starter's new verification overview. | Documentation reorganization must preserve F-06 cleanup. | Existing applied-copy regression rejects inherited own PR/CI links; classify VERIFICATION.md as a maintainer-only removal and refresh the explicit plan/baseline. | test |

Wording self-check: one shall requirement per row, listed vague words absent, each with a verification method and observable criteria. Approved scope: rewrite README, move detailed caveats/optional setup to linked pages, preserve attribution/migration guidance, classify the evidence overview for initialization, regenerate its baseline and run existing checks. Risk: a concise summary can overstate evidence; use a bounded recorded example and source-linked comparisons. No new skill, dependency, branding or application behavior.

## Review remediation F-02 worked example and comparative evidence

Status: owner approved F-02 as the next batch; reference and first eight attempts recorded. Seven protocol failures prevent useful outcome comparison; complete native-tool isolation remains unverified, so live trials are blocked. F-02 remains partial; no outcome improvement is claimed.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| EVAL-001 | The repository shall include a complete stdlib task-CLI worked example with traceable workflow evidence. | A routing trial is not an implemented application. | Example has requirements, approved scope/plan, observed red/green slice evidence, executable CLI tests, independent verification and release limitations; synthetic data only. | test |
| EVAL-002 | The evaluation shall run four predefined scenarios with starter guidance and a baseline prompt. | Paired results need common tasks and explicit conditions. | Bug fix, feature, risky import and ambiguous import each have two fresh arms using Composer 2.5, the same initial code, tool protocol, limits and deterministic oracle; order alternates; no outcome-based reruns. | demonstration |
| EVAL-003 | The evidence shall retain observed artifacts and failures without disclosing host-private data. | Readers need to inspect results and distinguish missing checks. | Prompts, visible responses/actions, final changed files, test outputs, elapsed time, model/CLI/image versions and rubric dispositions are published; reasoning/private paths/session IDs omitted; timeouts and protocol failures remain in results. | inspection |
| EVAL-004 | Candidate code shall execute in disposable containers without host mounts, credentials or network access. | Native writable CLI permission controls did not establish a boundary on this Windows host. | Read-only model proposes typed actions; parent validates allowed paths/actions; restricted Docker containers execute writes/tests; cleanup checks owned labels/IDs; no source/global profile modification by candidates. | test |
| EVAL-005 | The repository shall distinguish exploratory measurements from native-host or general outcome claims. | One repetition and an artificial tool interface cannot establish universal benefit. | docs/EVIDENCE.md records method, actual results, confounds and limits; README/VERIFICATION link it; initializer excludes all example/evaluation records; no new skills or process weights. | inspection |

Wording self-check: each shall row contains one requirement, avoids listed vague words and has a verification method. Authorized plan: define/preregister method and rubric, obtain fresh design reviews, build the worked example and typed-action/container harness with focused tests, run one pair per scenario, inspect/verify artifacts, then submit one PR after source checks and both CI jobs. Limits: native Windows sandbox unavailable; global Cursor configuration stays unchanged; results apply to the controlled protocol and selected model, not the full IDE or bare system prompt.

## Review remediation F-09 process weights

Status: merged via PR #30.

| ID | Statement (shall) | Rationale or assumption | Acceptance criterion | Verification method |
|----|-------------------|-------------------------|----------------------|---------------------|
| WEIGHT-001 | The starter shall define Lite, Standard and Strict process weights in docs/SKILLS.md with required and skippable gates. | Small edits inherited full planning ceremony. | docs/SKILLS.md contains a Process weights section naming Lite, Standard and Strict with required and skippable columns. | inspection |
| WEIGHT-002 | The project-helper skill shall select a process weight from the stated goal when markers match, and ask one weight question only when the goal does not determine the weight. | Users need automatic ceremony reduction without a long questionnaire. | project-helper instructions require marker-based selection, one question when undetermined, Lite skipping PRD/design-review ceremony, and Strict retaining design/security gates when triggered. | inspection |
| WEIGHT-003 | The repository shall classify a typo or symbol-rename goal as Lite and a payment-feature goal as Strict through an executable check. | Weight selection must be regression-tested without claiming live IDE routing. | `infer_process_weight` returns lite for typo and symbol-rename goals and strict for a payment-feature goal. | test |

Wording self-check: each shall row is one requirement, avoids the listed vague words, and has a measurable criterion plus verification method. Approved scope: document weights in the generated skill guide, teach project-helper the selection rules, add `scripts/process_weight.py` with unit tests, run starter gates, and submit one PR. No new workflow skill, dependency, branding change or F-02 runner work. Risk: keyword markers can mis-classify; keep an ask-once fallback when undetermined and prefer Strict when Strict markers are present.

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
