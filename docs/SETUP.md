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

Packages were installed as upstream Git checkouts outside the starter. Full source layouts preserve shared references; the seven project skills were not overwritten. Node.js v24.22.2 and Skills CLI 1.7.6 were available; all four sources were listed with the CLI before installation.

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

### Limits of the observations

The Task schema states new non-resumed calls start fresh; it exposes no separate context-inheritance or read-only switch. Reviewers received standard host instructions. The canary probe supports absence of earlier parent conversation in these two calls; it is not a general proof of isolation. Both reviewers reported edit/shell tool categories, and neither attempted a prohibited operation, so behavioral refusal was observed while tool-level permission denial remains untested. Keep the read-only metadata and scoped prompts; do not treat them as an operating-system security boundary.

The editor UI, complete EGM/security audit pipelines, every upstream skill and all optional third-party tools were not exercised. A smoke check of attachment and role behavior is distinct from end-to-end workflow validation. Repeat these probes after Cursor or package updates that affect loading or delegation.

Application-specific build, lint, security, browser and accessibility gates remain out of scope until an application stack and requirements exist. Installing a pack does not install its optional tools, provision services, publish issues or deploy an application.
