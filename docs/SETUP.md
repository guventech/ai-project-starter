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

Earlier authenticated testing found bare `/grill-me`, `/tdd` and `/security-audit` selecting upstream packs while this starter still used those local names. F-01 renamed the local skills to `decision-interview`, `test-first-change`, `hypothesis-debugging` and `trust-boundary-audit` so bare slash commands no longer collide. Keep the optional packs for their references and broader workflows; refresh a global project-helper install with `--upgrade --force` after pulling this change.

Update a package only after inspecting its diff and verifying shared resources and names. Do not run an indiscriminate update over customized local skills. To undo this installation, remove only the four recorded package directories after verifying their resolved paths and checking for user edits.

## Cursor runtime verification

- Installed editor: Cursor 3.29.9 on Windows x64.
- Installed official Agent CLI: `2026.11.05-86047df`, under `%LOCALAPPDATA%/cursor-agent`. The installer was inspected before execution; its target did not already exist.
- `agent status`: authenticated after the user completed the official browser login. No credentials were read or copied from the editor. Account identifiers and authentication tokens are omitted from this record.
- The workspace was trusted for these CLI runs. Read-only skill checks used `--print --mode ask`; reviewer probes used native Task calls in a separate session. No blanket tool-approval flag was enabled.

### Observed smoke results

- Project planning: `/project-planning` attached the project's SKILL.md and returned its requirements-first step and approval exit condition.
- Six-skill attachment check (pre-rename): design-review, release-check and systematic-debugging attached project files; grill-me, tdd and security-audit attached upstream files. That collision motivated the F-01 rename.
- Explicit-path fallback (pre-rename): a read-only session read the three exact local paths and returned their distinctive local instructions.
- EGM: `/egm-review` attached the installed plugin's canonical review skill with its reviewer/standards references. No full EGM pipeline or artifact generation was executed.
- Custom reviewers: the Task trace shows separate non-resumed `architect` and `verifier` calls with bounded prompts and no parent-only canary in their inputs. Both refused the probe write and reported the canary absent. The parent-only canary was not placed in a file.
- The reviewer probe file was absent and `git status --short` was empty after the runs.

### MAINT-002 matched-pair write probe (2026-11-09)

Isolated fixture: a uniquely named directory under the host temp folder (no git remotes). Spec: `docs/superpowers/specs/2026-11-09-maint-002-permission-probe-design.md`.

| Role | Agent | Write attempt | Host result | Marker |
|------|-------|---------------|-------------|--------|
| Control | `generalPurpose` | Write tool called | success | control marker present with expected contents |
| Probe | `verifier` (readonly) | Write tool called | denied: ask mode / non-read-only tools | probe marker absent |

Classification: **`host-denied`**. Parent listing after both Tasks showed only the control file. Repo tree was not used as the write target. Fixture directory removed after evidence capture.

Limits: this demonstrates tool-level denial for one fresh local `verifier` Task on this host when Write is attempted; it is not an OS sandbox proof, not a general isolation proof, and not coverage of every reviewer or Shell write routes. The control is a different subagent type, so attribution is to the readonly verifier path versus a writable generalPurpose path, not a perfect twin.

### Limits of the observations

The Task schema states new non-resumed calls start fresh; it exposes no separate context-inheritance or read-only switch. Reviewers received standard host instructions. The canary probe supports absence of earlier parent conversation in these two calls; it is not a general proof of isolation. The earlier custom-reviewer smoke observed behavioral refusal without a Write attempt. The MAINT-002 matched-pair probe above separately recorded a Write attempt with a permission/read-only host denial for `verifier` while the control Write succeeded. Keep the read-only metadata and scoped prompts; do not treat them as an operating-system security boundary.

The editor UI, complete EGM/security audit pipelines, every upstream skill and all optional third-party tools were not exercised. A smoke check of attachment and role behavior is distinct from end-to-end workflow validation. Repeat these probes after Cursor or package updates that affect loading or delegation.

Application-specific build, lint, security, browser and accessibility gates remain out of scope until an application stack and requirements exist. Installing a pack does not install its optional tools, provision services, publish issues or deploy an application.

## One-command project helper

The approved `/project-helper` command is installed at `~/.cursor/skills/project-helper`. It has one SKILL.md, eight workflow reference documents and two reviewer reference documents (ten reference files total). No source checkout path or upstream package is needed at invocation time. The installed entry file matches the repository version (SHA256 `419b1b802763e54475b1ac4c0db50744f7fce01efaefe694b6939012a452c091`). Snapshots are not auto-updated.

Authenticated CLI trials used isolated temporary workspaces outside this repository:

- Menu: invoked only `/project-helper` and returned the two-choice new/improve question.
- New project: identified the user-level helper and `references/project-planning.md` without a source checkout dependency.
- Existing project: read a calculator fixture's own AGENTS.md, source and tests; loaded bundled `tdd.md` and `verifier.md`; and returned findings and proposed checks without edits or shell execution. A general reviewer used the bundled verifier role rather than requiring copied agent configuration. An initial overbroad readiness statement prompted a clarification in the entry instructions: distinguish actual defects from optional suggestions, and give readiness verdicts only when requested.
- Nonempty target: listed the existing calculator/test/instructions files and waited for a decision to use that folder or select another. This exercised the independent review's applied clarification.
- Concrete new-project plan: loaded bundled planning, interview and design procedures; returned requirements, assumptions, proposed paths, checks and an approval request for a stdlib todo CLI. It disclosed that goldfish design review was unverified under that no-write Ask-mode trial.

After the trials, the new-project folder was still empty and the existing-project folder still contained only its three original fixture files. These trials ran in CLI Ask mode: they verify discovery, source selection and conversational boundaries, not end-to-end app implementation or host-enforced write denial. Building/applying fixes needs Cursor Agent mode and the target project's approved implementation plan. No other user project was modified.

Installer validation: occupied destination and repeat-install tests preserve user contents; Linux PR CI runs the symlink cases skipped on this Windows host. Fresh installs stage beside the destination and promote only after validation; failure-injection tests assert no destination and no leftover staging directory. Existing-package upgrades still write in place.
