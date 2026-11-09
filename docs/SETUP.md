# Maintainer setup record

Date: 2026-11-09. Scope: the user-authorized follow-up for optional packages, GitHub CI enforcement and Cursor runtime verification. These are machine/repository settings; copies made from this template do not inherit them.

## GitHub

Repository: guventech/ai-project-starter. The enhancement commit `83915658d34445ac3e396c1eadaf861d183d470c` passed both Python 3.12 jobs in [run 42577848331](https://github.com/guventech/ai-project-starter/actions/runs/42577848331).

The `main` branch protection API confirmed:

- Required checks: `Starter validation (ubuntu-latest)` and `Starter validation (windows-latest)`, each restricted to GitHub Actions app ID 15368.
- Strict/up-to-date status checks and administrator enforcement are enabled.
- Pull requests and resolved review conversations are required. Zero approving reviews are required so a sole maintainer can merge after CI passes.
- Force pushes and deletion are disabled.

Use branches and pull requests for subsequent changes. This protection belongs to this repository; configure it again for a new template copy. Before rollback, inspect the current settings and preserve any later changes. There was no protection or ruleset before this follow-up.

## Optional user-level packages

Packages were installed as upstream Git checkouts outside the starter. Full source layouts preserve shared references; the nine project skills were not overwritten. Node.js v24.22.2 and Skills CLI 1.7.6 were available; all four sources were listed with the CLI before installation.

- Matt Pocock: `~/.cursor/skills/optional/mattpocock-skills`, revision `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d`. Sparse checkout includes `skills/engineering` and `skills/productivity`: 27 stable skills. General and in-progress experiments were excluded; the CLI reported malformed YAML in an in-progress skill during discovery.
- Addy Osmani: `~/.cursor/skills/optional/addyosmani-agent-skills`, revision `301b02b12bff98e4688e6984af6556802322bbde`. All 25 skills and repository-level references are present.
- Cloudflare: `~/.cursor/skills/optional/cloudflare-security-audit`, revision `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`. The security-audit skill includes its supporting audit documents and validators.
- EGM: `~/.cursor/plugins/local/egm`, revision `5382b17619be07811a14b2146c7672620b34a791`. The complete plugin includes seven canonical skills, reviewer personas and `resources/document_standards`; its Claude distribution also contains seven copies, which are not additional canonical skills.

Cursor documents [recursive skill discovery](https://cursor.com/docs/skills) and [local plugin imports](https://cursor.com/docs/plugins#test-plugins-locally). Reload Cursor to discover these packages. Local plugin loading can be restricted by organization policy. This installation preserves upstream files and is not a claim that every upstream workflow has been executed in Cursor.

Upstream `grill-me`, `tdd` and `security-audit` names overlap project skills. Authenticated testing found bare slash invocation selected the upstream versions. For this starter's acceptance criteria, ask the agent to read and follow the exact `.cursor/skills/<name>/SKILL.md` path. That route loaded all three local bodies in a separate smoke test. Keep the complete packages for their references and optional broader workflows; no upstream or local skill was renamed or overwritten.

Update a package only after inspecting its diff and verifying shared resources and names. Do not run an indiscriminate update over customized local skills. To undo this installation, remove only the four recorded package directories after verifying their resolved paths and checking for user edits.

## Cursor runtime verification

- Installed editor: Cursor 3.29.9, build `306d153d51d714882ab7b1bc49649cab624e8a30`, Windows x64.
- Installed official Agent CLI: `2026.11.05-86047df`, under `%LOCALAPPDATA%/cursor-agent`. The installer was inspected before execution; its target did not already exist.
- `agent status`: authenticated after the user completed the official browser login. No credentials were read or copied from the editor. Account identifiers and authentication tokens are omitted from this record.
- The workspace was trusted for these CLI runs. Read-only skill checks used `--print --mode ask`; reviewer probes used native Task calls in a separate session. No blanket tool-approval flag was enabled.

### Observed smoke results

- Project planning: `/project-planning` attached the project's SKILL.md and returned its requirements-first step and approval exit condition. CLI session `98d12976-75ea-471a-b35b-90c497431d4b`.
- Six-skill attachment check: design-review, release-check and systematic-debugging attached project files; grill-me, tdd and security-audit attached upstream files. CLI session `18a0a0f6-93a1-489e-ba1e-c4e2782a39ce`. This is an observed name collision, not a missing local file.
- Explicit-path fallback: a read-only session read the three exact local paths and returned their distinctive local instructions. CLI session `ffd108eb-82d7-49e5-a41d-430b76269c96`. This proves path loading, not bare-slash precedence.
- EGM: `/egm-review` attached the installed plugin's canonical review skill with its reviewer/standards references. CLI session `cc46c326-ea96-41fe-bd2f-4ab4f88c368b`. No full EGM pipeline or artifact generation was executed.
- Custom reviewers: the Task trace shows separate non-resumed `architect` and `verifier` calls with bounded prompts and no parent-only canary in their inputs. Both refused the probe write and reported the canary absent. The parent-only canary was not placed in a file. CLI session `cb48b912-c725-4e7f-8504-7347ca3e544a`.
- The reviewer probe file was absent and `git status --short` was empty after the runs.

### MAINT-002 matched-pair write probe (2026-11-09)

Isolated fixture: `C:\Users\guven\AppData\Local\Temp\maint-002-20261109104726` (no git remotes). Nonce payload `MAINT002-20261109104726`. Spec: `docs/superpowers/specs/2026-11-09-maint-002-permission-probe-design.md`.

| Role | Agent | Agent id | Write attempt | Host result | Marker |
|------|-------|----------|---------------|-------------|--------|
| Control | `generalPurpose` | `6cc95764-39f3-41a6-8d93-1c876664d738` | Write tool called | success | `control-20261109104726.txt` present (24 bytes, expected contents) |
| Probe | `verifier` (readonly) | `bc21ba24-37ae-40c1-9a4b-a0134bc58981` | Write tool called | denied: "You are in ask mode and cannot run non read-only tools..." | `probe-20261109104726.txt` absent |

Classification: **`host-denied`**. Parent listing after both Tasks showed only the control file. Repo tree was not used as the write target. Fixture directory removed after evidence capture.

Limits: this demonstrates tool-level denial for one fresh local `verifier` Task on this host when Write is attempted; it is not an OS sandbox proof, not a general isolation proof, and not coverage of every reviewer or Shell write routes. The control is a different subagent type, so attribution is to the readonly verifier path versus a writable generalPurpose path, not a perfect twin.

### Limits of the observations

The Task schema states new non-resumed calls start fresh; it exposes no separate context-inheritance or read-only switch. Reviewers received standard host instructions. The canary probe supports absence of earlier parent conversation in these two calls; it is not a general proof of isolation. The earlier custom-reviewer smoke (session `cb48b912-c725-4e7f-8504-7347ca3e544a`) observed behavioral refusal without a Write attempt. The MAINT-002 matched-pair probe above separately recorded a Write attempt with a permission/read-only host denial for `verifier` while the control Write succeeded. Keep the read-only metadata and scoped prompts; do not treat them as an operating-system security boundary.

The editor UI, complete EGM/security audit pipelines, every upstream skill and all optional third-party tools were not exercised. A smoke check of attachment and role behavior is distinct from end-to-end workflow validation. Repeat these probes after Cursor or package updates that affect loading or delegation.

Application-specific build, lint, security, browser and accessibility gates remain out of scope until an application stack and requirements exist. Installing a pack does not install its optional tools, provision services, publish issues or deploy an application.

## One-command project helper

The approved `/project-helper` command is installed at `~/.cursor/skills/project-helper`. It has one SKILL.md, eight workflow reference documents and two reviewer reference documents (ten reference files total). No source checkout path or upstream package is needed at invocation time. The installed entry file matches the repository version (SHA256 `419b1b802763e54475b1ac4c0db50744f7fce01efaefe694b6939012a452c091`). Snapshots are not auto-updated.

Authenticated CLI trials used isolated temporary workspaces outside this repository:

- Menu: session `09b85146-9efe-4645-91f2-576844fc6a1b` invoked only `/project-helper` and returned the two-choice new/improve question.
- New project: session `9ad7bdcf-f8ec-4c65-967d-f983c1ad746b` identified the user-level helper and `references/project-planning.md` without a source checkout dependency.
- Existing project: session `97b9e9f2-b94e-4964-bad8-722b3b37e7cc` read a calculator fixture's own AGENTS.md, source and tests; loaded bundled `tdd.md` and `verifier.md`; and returned findings and proposed checks without edits or shell execution. A general reviewer used the bundled verifier role rather than requiring copied agent configuration. An initial overbroad readiness statement prompted a clarification in the entry instructions: distinguish actual defects from optional suggestions, and give readiness verdicts only when requested.
- Nonempty target: session `39c899cf-4ada-4059-839e-820ee93354a0` listed the existing calculator/test/instructions files and waited for a decision to use that folder or select another. This exercised the independent review's applied clarification.
- Concrete new-project plan: session `95aafaac-67dd-45eb-861f-60d82f0faacd` loaded bundled planning, interview and design procedures; returned requirements, assumptions, proposed paths, checks and an approval request for a stdlib todo CLI. It disclosed that goldfish design review was unverified under that no-write Ask-mode trial.

After the trials, the new-project folder was still empty and the existing-project folder still contained only its three original fixture files. These trials ran in CLI Ask mode: they verify discovery, source selection and conversational boundaries, not end-to-end app implementation or host-enforced write denial. Building/applying fixes needs Cursor Agent mode and the target project's approved implementation plan. No other user project was modified.

Installer validation: ten unittest methods run on Windows after the inventory-alignment change, with nine passing and the symlink creation case skipped because this host lacks permission to create links. Occupied destination and repeat-install tests preserved user contents. Linux PR CI runs the symlink case. A partial new installation can remain on an I/O failure; the installer reports that and never removes or replaces an existing package.
