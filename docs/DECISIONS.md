# Decision log

## ADR-019: Scoped rule coverage for three sample layouts (F-10)

Date: 2026-11-09. Status: accepted; bounded scope approved by the owner.
Context: architecture/security covered src but missed root app/lib and Go cmd/internal/pkg; testing missed Go's _test.go convention. No trigger guide or layout regression existed.
Options: extend scoped globs with examples; switch generic rules to description-based selection; make rules always apply.
Decision: retain alwaysApply false and the existing scoped-rule contract; extend source-root globs and root Python/Go modules, add the Go test pattern, document exact triggers and adoption examples in docs/RULES.md, and test actual metadata against three temporary layouts with the existing unittest runner.
Consequences: more source paths attach concise guidance; colocated tests can match multiple rules. Arbitrary package roots and monorepos still require adoption choices. Python Path.glob is static evidence, not proof of Cursor attachment; record bounded live probes apart. No new skills, dependencies or general glob engine.
Rollback: revert this PR's globs, guide and regression fixture.
Related paths: `.cursor/rules/`, docs/RULES.md, docs/CONFIGURATION.md, README.md, tests/test_starter.py, scripts/validate_starter.py, docs/QUALITY_GATES.md.

## ADR-018: Read-only installed snapshot check (F-13 slice)

Date: 2026-11-09. Status: accepted; bounded slice approved by the owner.
Context: global installations are snapshots; upgrade refusal cannot tell users whether installed content matches the current checkout without attempting an upgrade.
Options: add a read-only check; implement versioning, releases and diff output together; leave inspection manual.
Decision: add --check with exit 0 for up to date, 1 for drift or absent installation/manifest, and 2 for invalid manifests, destinations, arguments or read errors. Compare current-source content and installed-manifest digests apart; count each differing file path once. Reject linked destinations/entries and never use manifest keys as filesystem paths. Reject upgrade flags in check mode.
Consequences: no network lookup, installation writes, new dependency or skill. A stock older snapshot can report drift; missing/invalid manifests take precedence. The manifest checks accidental integrity, not authenticity; concurrent filesystem changes remain outside the snapshot guarantee. Versioning, --diff and releases remain deferred.
Rollback: revert this slice's PR; installations are unchanged by check mode.
Related paths: scripts/install_chat_command.py, tests/test_install_chat_command.py, docs/INSTALL.md, docs/PRD.md, docs/TASKS.md, docs/QUALITY_GATES.md.

## ADR-017: Redact prior-art queries before search (F-16)

Date: 2026-11-09. Status: accepted; bounded remediation approved by the owner.
Context: prior-art treats remote content as untrusted and caps candidates, but did not require removal of private project details before queries leave the workspace.
Options: retain the existing text; add a pre-query check and synthetic scenario; build a search proxy or broader evaluation harness.
Decision: require generic public terms, inspect every outgoing query, skip when no useful public query can be formed, and reject retrieved instructions to disclose context or run commands. Add one synthetic scenario and verify bundled text through the existing installer test.
Consequences: no new skill, dependency or runtime enforcement layer; procedure inspection and packaging checks do not establish live agent compliance. The comparative F-02 work remains deferred.
Rollback: revert the F-16 PR; existing global snapshots stay unchanged until an authorized upgrade.
Related paths: `.cursor/skills/prior-art/SKILL.md`, evals/prior-art-search-hygiene.md, tests/test_install_chat_command.py, docs/PRD.md, docs/TASKS.md, docs/QUALITY_GATES.md.

## ADR-016: Split consumer AGENTS from maintainer docs (F-05)

Date: 2026-11-09. Status: accepted; next step after F-03 per Cursor + Codex agreement.
Context: AGENTS.md mixed always-loaded consumer rules with install ceremony, optional pack commands and maintainer process that every template copy inherited.
Options: keep a single AGENTS.md; move only maintainer notes; split into AGENTS.md, docs/INSTALL.md and MAINTAINING.md.
Decision: keep AGENTS.md as short consumer behavioral rules plus links to docs/SKILLS.md and docs/INSTALL.md; put install/upgrade in docs/INSTALL.md; put starter-maintainer process in MAINTAINING.md; reject maintainer markers and length over 50 lines in validation.
Consequences: template copies stay lean; pack install commands remain in README; maintainer edits no longer expand always-loaded context.
Rollback: restore the previous AGENTS.md sections and remove the split files.
Related paths: AGENTS.md, MAINTAINING.md, docs/INSTALL.md, README.md, docs/CONFIGURATION.md, scripts/validate_starter.py, tests/test_starter.py.

## ADR-015: Keep repository brand for now (F-12)

Date: 2026-11-09. Status: accepted; reaffirmed by Cursor + Codex after owner uncertainty.
Context: External review F-12 flags name collision with other "AI Project Starter" projects; owner was unsure whether to rename now.
Options: rename the GitHub repository and package identifiers immediately; keep the current name and revisit later.
Decision: keep `guventech/ai-project-starter` / local `cursor-optimized-starter` for now; do not rename until branding clearly blocks positioning, discovery or commercialization.
Consequences: F-01 skill renames remain the collision fix; README and publish paths stay stable; F-12 stays deferred on the review backlog.
Rollback: choose a distinctive name later and rename with GitHub redirects.
Related paths: README.md, docs/SETUP.md, scripts/install_chat_command.py, publish docs.

## ADR-014: Generated skill decision guide (F-03)

Date: 2026-11-09. Status: accepted; next step after F-01 per Cursor + Codex agreement.
Context: README, AGENTS and CONFIGURATION each listed skills differently without use/do-not-use guidance.
Options: keep triple lists; hand-maintain one guide; generate a guide from per-skill metadata.
Decision: embed `skills-meta` blocks in each SKILL.md; generate `docs/SKILLS.md` with a lifecycle diagram and decision table; fail validation when the guide is stale; replace competing inventories with links.
Consequences: one authoritative decision page; skill metadata edits require regenerating the guide; weight fields prepare for a later Lite/Standard/Strict helper question (F-09).
Rollback: revert the generator, guide and linking changes.
Related paths: scripts/generate_skills_guide.py, docs/SKILLS.md, `.cursor/skills/*/SKILL.md`, scripts/validate_starter.py, README.md, AGENTS.md, docs/CONFIGURATION.md.

## ADR-013: Rename colliding local skills (F-01)

Date: 2026-11-09. Status: accepted; Cursor + Codex agreed to keep the repository name and rename only colliding local skills.
Context: Optional packs installed for inspiration caused bare `/grill-me`, `/tdd`, `/security-audit` and `/systematic-debugging` to load upstream files. ADR-004 documented an explicit-path workaround.
Options: keep path workaround; brand-prefix all skills; rename only colliding skills to functional names.
Decision: rename to `decision-interview`, `test-first-change`, `trust-boundary-audit` and `hypothesis-debugging`; deny the old names in the validator; treat obsolete installer reference paths as migratable and remove them on upgrade (rename migration requires `--upgrade --force` when the old manifest lacks the new paths).
Consequences: bare local slash names no longer collide with the four optional upstream skills; global installs need one forced upgrade; ADR-004 path workaround is historical for pre-rename evidence.
Rollback: revert the rename commit/PR and reinstall the previous package snapshot if needed.
Related paths: `.cursor/skills/`, `scripts/skill_inventory.py`, `scripts/install_chat_command.py`, `scripts/validate_starter.py`, README.md, AGENTS.md, docs/, THIRD_PARTY.md.

## ADR-012: Third-party attribution audit (F-04)

Date: 2026-11-09. Status: accepted; Cursor + Codex review remediation plan.
Context: External review F-04 asked whether "original, reduced workflows" claims were backed by a visible comparison and notice file.
Options: leave README claims unchanged; vendor upstream text with notices; audit and publish a notice without vendoring.
Decision: compare each overlapping local skill against the maintainer-installed upstream revision; classify use as idea, structure or text; publish `THIRD_PARTY.md`; ship that notice with the project-helper installer package; replace unsupported blanket "original" wording with "independently written" where the audit supports it.
Consequences: provenance is documented; no substantial upstream text was found to redistribute; name collisions remain documented under ADR-004 until an approved rename (F-01). Cache paths used for the obra/superpowers comparison are machine-local evidence only.
Rollback: revert the notice, installer packaging and wording changes.
Related paths: THIRD_PARTY.md, README.md, scripts/install_chat_command.py, docs/SETUP.md revisions, `.cursor/skills/*/SKILL.md` footers.

## ADR-001: Keep the starter stack-agnostic
Status: accepted for the template.
Context: projects have different runtime, UI and storage needs.
Decision: ship agent configuration and starter validation; choose the stack during planning.
Consequence: starter CI is not an application readiness signal.

## ADR-002: Keep requirement writing short
Status: accepted for the template.
Context: the starter should teach clear requirements and stay small.
Decision: keep a small requirements table, TBR rows and risks in docs/PRD.md, and link each shall to evidence in docs/QUALITY_GATES.md.
Consequence: a glossary, a concept of operations, and a full verification matrix wait until a real project needs them.

## ADR-003: Compose concise local review workflows

Date: 2026-11-09. Status: accepted; enhancement plan approved by the user.
Context: CURSOR_UPDATE_PROMPT.md requests interviews, TDD, fresh-context design review and a multi-phase security audit without growing a stack-specific framework.
Options: vendor full external packs; depend on user-installed packs; write concise local procedures and document optional upstream installation.
Decision: use the third option, retaining explicit skill invocation, inherited models and read-only review agents. Local procedures use original wording and link their inspirations. Keep the existing Python validator and extend its required-skill coverage without dependencies.
Consequences: the original seven local workflows (later expanded; see ADR-005 and ADR-007) work as documented procedures without upstream installation, but do not include upstream harnesses, schemas or complete review coverage. Fresh-context reviews require host support and remain unverified when unavailable. Optional installations can collide with local names or omit shared references.
Rollback: revert the enhancement diff; no application, dependency, storage or deployment changes require migration. Preserve unrelated user changes.
Related paths: .cursor/skills/, .cursor/agents/, README.md, docs/CONFIGURATION.md, scripts/validate_starter.py, tests/test_starter.py.

## ADR-004: Select overlapping local skills by file path

Date: 2026-11-09. Status: accepted within the authorized setup verification scope.
Context: authenticated Cursor CLI slash attachment selected optional upstream grill-me, tdd and security-audit instead of the project files. The local bodies and installed packs are both intentional.
Options: rename local skills; rewrite upstream names; remove overlapping upstream files; select local workflows by explicit source path.
Decision: document explicit `.cursor/skills/<name>/SKILL.md` selection for these three workflows. Keep the requested local names and complete upstream files intact. The explicit-path loading route was tested.
Consequences: bare slash names remain available for the upstream variants; tasks using this starter's acceptance criteria must select its local paths. Runtime behavior can change with host updates, so record the loaded source when retesting.
Rollback: retire the workaround only after retesting name resolution on the installed host; no package or application migration is needed.
Related paths: AGENTS.md, README.md, docs/CONFIGURATION.md, docs/SETUP.md.

## ADR-005: Bundle a single user-level project command

Date: 2026-11-09. Status: accepted; concrete plan approved by the user.
Context: manually copying skills and choosing workflows made both new-project setup and existing-project assessment too complicated for the user.
Options: build a separate desktop/web app; maintain instructions for manual adoption; add one user-level chat entry point that selects the existing procedures.
Decision: implement `/project-helper` with two modes and a dependency-free installer. Package the then-existing procedures and two reviewer roles as `.md` references beside the entry skill, rewriting their known internal paths (eight workflows after ADR-007). Keep only one discoverable SKILL.md in the global package.
Consequences: the command runs from other workspaces without installing upstream packs or retaining the source checkout path. Installed snapshots need a deliberate update and cannot silently overwrite customizations. Host permissions, fresh reviewers and project-specific checks remain external capabilities; the command cannot guarantee them.
Rollback: revert the entry point/installer diff; remove the installed package only after checking its resolved path and user edits. Other projects are not modified by installation.
Related paths: .cursor/skills/project-helper/, scripts/install_chat_command.py, tests/test_install_chat_command.py, README.md, docs/CONFIGURATION.md.

## ADR-006: Prefer checkout v5 for the Node.js 24 CI bump

Date: 2026-11-09. Status: accepted; maintenance plan approved by the user.
Context: MAINT-001 requires Node.js 24 action releases. Both `actions/checkout@v5` and `@v6` run on Node.js 24; `@v6` also changes credential persistence.
Options: bump only to the minimum Node.js 24 majors; jump checkout to `@v6` with setup-python `@v6`; pin exact patch tags.
Decision: use `actions/checkout@v5` and `actions/setup-python@v6`, keep floating major tags, and verify both OS jobs on a PR before merge.
Consequences: clears the Node.js 20 deprecation path with less behavioral change than checkout `@v6`. Future checkout `@v6` adoption stays a separate decision.
Rollback: revert the workflow/docs commit on the maintenance branch or close the PR.
Related paths: .github/workflows/ci.yml, docs/PRD.md, docs/QUALITY_GATES.md, docs/TASKS.md.

## ADR-007: Add hybrid prior-art research before planning

Date: 2026-11-09. Status: accepted; concrete plan approved by the user.
Context: Users want GitHub/web prior art for new projects and substantial improvements without burning tokens on tiny fixes or adopting a repo because it has many stars.
Options: always-on search; opt-in only; hybrid trigger with a dedicated skill invoked by project-helper.
Decision: add `/prior-art`, invoke it from `/project-helper` by path, run always for new projects and for non-tiny improve goals, rank fit then activity/license then stars, adopt only after explicit candidate approval, and persist docs only when a candidate is adopted or seriously considered.
Consequences: eight bundled workflows ship with the installer; global installs need a manual reinstall to receive the new reference; missing search tools leave the gate unverified and planning continues.
Rollback: revert the prior-art skill and helper/installer/docs changes; remove only a freshly installed package after checking for user edits.
Related paths: .cursor/skills/prior-art/, .cursor/skills/project-helper/, .cursor/skills/project-planning/, scripts/install_chat_command.py, scripts/validate_starter.py, tests/, README.md, AGENTS.md.

## ADR-009: Manifest-based project-helper upgrade with forced backups

Date: 2026-11-09. Status: accepted; Phase B plan with backups approved by the user.
Context: Global `/project-helper` installs went stale because the installer refused all occupied destinations.
Options: document manual delete only; `--upgrade` that always overwrites managed files; manifest-checked `--upgrade` plus `--upgrade --force` with backups.
Decision: write `.installer-manifest.json` on install; allow `--upgrade` only for symlink-free packages with no extras and an exact planned-path manifest whose digests are valid SHA-256 values matching managed files; require `--upgrade --force` for missing/incomplete/malformed manifests or customized managed files; before force overwrite, copy differing managed files to a sibling `project-helper.bak-<timestamp>/` directory.
Consequences: clean upgrades are one command; pre-Phase-B installs and incomplete manifests need one forced upgrade; extras still require manual relocation; force can replace customizations after backup.
Rollback: revert the installer/docs/test changes; leave existing user packages and any `.bak-*` folders untouched.
Related paths: scripts/install_chat_command.py, tests/test_install_chat_command.py, README.md, AGENTS.md, docs/CONFIGURATION.md, docs/PRD.md, docs/QUALITY_GATES.md.

## ADR-011: Transactional fresh project-helper installs

Date: 2026-11-09. Status: accepted; next step agreed by Cursor and Codex CLI after HARD-001/002.
Context: Fresh installs wrote directly into the destination, so an I/O failure could leave a partial package.
Options: keep direct writes with stronger warnings; stage beside the destination then rename; stage under a temp root then copy.
Decision: write `project-helper.staging-<stamp>-<nonce>/` beside the destination, validate managed paths and digests, then rename into `project-helper`. On failure, remove only that staging directory. Existing-package upgrades remain in place.
Consequences: successful fresh installs appear atomically from the destination path's perspective; failure-injection tests cover mid-write and manifest failures; cross-volume rename is not required because staging shares the destination parent.
Rollback: revert the installer/docs/test changes.
Related paths: scripts/install_chat_command.py, tests/test_install_chat_command.py, docs/CONFIGURATION.md, docs/SETUP.md, docs/PRD.md, docs/QUALITY_GATES.md.

## ADR-010: Matched-pair permission probe for MAINT-002

Date: 2026-11-09. Status: accepted; design agreed by parent and Codex CLI; demonstration completed.
Context: Earlier reviewer probes refused writes without a tool attempt, so behavioral refusal was confused with host denial.
Options: verifier-only forced Write; matched writable control plus readonly verifier; add sandbox/permissions deny rules.
Decision: use an isolated temp fixture with a `generalPurpose` control Write and a fresh `verifier` Write to distinct nonce files; classify from tool name, tool result and listing; require a permission/read-only denial plus successful control for `host-denied`.
Consequences: MAINT-002 can record host-denied evidence when the host blocks the attempted Write; missing or ambiguous denial stays unverified; control is not a perfect twin of verifier.
Rollback: revert docs/evidence only; no product code changed. Discard only the named temp fixture directory after path check.
Related paths: docs/superpowers/specs/2026-11-09-maint-002-permission-probe-design.md, docs/SETUP.md, docs/QUALITY_GATES.md, docs/PRD.md, docs/TASKS.md.

## ADR-008: Single skill-inventory source for docs and tools

Date: 2026-11-09. Status: accepted; Phase A integrity plan approved by the user.
Context: After prior-art landed, PRD/QUALITY_GATES/CONFIGURATION/SETUP still said seven skills or omitted prior-art while the validator required nine.
Options: edit docs once without tests; add inventory assertions without sharing constants; centralize WORKFLOWS/REQUIRED_SKILLS and test CONFIGURATION/README coverage.
Decision: add `scripts/skill_inventory.py`, import it from the validator and installer, fail validation on unexpected local skill directories, and fail tests when CONFIGURATION, README or AGENTS omit a required skill name.
Consequences: skill-count drift and unregistered skill folders are caught by CI; docs must list every required skill by exact name.
Rollback: revert the inventory module and doc/test changes on the feature branch or PR.
Related paths: scripts/skill_inventory.py, scripts/validate_starter.py, scripts/install_chat_command.py, tests/test_starter.py, docs/CONFIGURATION.md, docs/PRD.md, docs/QUALITY_GATES.md, docs/SETUP.md.

## New decision template

ID/title, date, status, context, options, decision, consequences, rollback and related paths.
