# Configuration references and limitations

Configuration shapes checked against official documentation:
- Rules and AGENTS.md: https://cursor.com/docs/rules
- Skills: https://cursor.com/docs/skills
- Subagents: https://cursor.com/docs/subagents
- MCP: https://cursor.com/docs/mcp
- Publishing: https://cli.github.com/manual/gh_repo_create
- Template flag: https://cli.github.com/manual/gh_repo_edit

Rules use description, comma-separated globs and alwaysApply false. See [RULES.md](RULES.md) for all three triggers, Node/Python/Go sample coverage, scope examples and live-attachment checks. Adjust globs when adopting a different layout.
Skills use name/description and explicit invocation to keep ambient context small.
Agents inherit the chosen model and set readonly true. The verifier asks its parent to run checks that write artifacts.
AGENTS.md is the shared behavioral core; Cursor-specific files are not claimed portable to other agents.
Static checks cannot prove Cursor discovery or runtime behavior. Open the folder in your installed Cursor,
check all three rules and nine skills are discovered, invoke /project-helper or /project-planning, then ask for the architect and verifier.
Confirm read-only behavior before relying on it. Bounded live CLI smoke results are recorded in SETUP.md; editor UI discovery and complete workflow execution are not claimed.

## Local skills

The nine required local skills and their use/do-not-use guidance are listed in [SKILLS.md](SKILLS.md). Sibling links describe procedures a selected workflow can read; they do not change explicit invocation metadata. Regenerate that guide with `python scripts/generate_skills_guide.py` after editing skill metadata.

## One-command installation

Consumer install and upgrade commands are in [INSTALL.md](INSTALL.md). `--destination /path/to/project-helper` selects a different package directory for inspection/testing; its basename must remain project-helper. Without `--upgrade`, an occupied path or symlink is rejected. Fresh installs write a sibling `project-helper.staging-*` directory first and rename it into place only after the staged package validates; a failed fresh install removes that staging directory and leaves no destination.

The package has one discoverable SKILL.md, the MIT license, ten adjacent reference documents (eight workflow snapshots and two reviewer role snapshots), and `.installer-manifest.json` with SHA-256 digests of the managed content files. References use `.md` filenames rather than nested SKILL.md files to avoid duplicate skill discovery. The installer rewrites the known internal workflow references for the bundled layout. No machine-specific repository path, application code, secrets, historical PRD or third-party pack is copied.

### Upgrade

| Situation | Command |
|-----------|---------|
| Clean stock package (manifest matches managed files exactly) | `python scripts/install_chat_command.py --upgrade` |
| Pre-manifest install, incomplete/malformed manifest, edited managed files, or renamed skill references | `python scripts/install_chat_command.py --upgrade --force` |
| Extra files beside the managed set (notes, scripts) | Move extras out, then upgrade; `--force` still refuses extras |
| Customized managed files you want to keep | Copy the folder aside first; `--force` backs up differing managed files to `project-helper.bak-<timestamp>/` then overwrites them |

`--force` requires `--upgrade`. Symlink destinations are always refused. Reload/start a new Cursor chat after installation or upgrade and verify `/project-helper` in the actual target workspace. Installation does not enable cloud sync or grant permission to publish, deploy or edit another project without its approved plan.

The entry point resolves procedures relative to its actual attached source. Repository-local invocation uses sibling skills and `.cursor/agents`; user-level invocation uses the bundled references. Other workspaces keep their existing instructions and tests. A general fresh reviewer can read the bundled role when that workspace does not register architect/verifier by name. Unavailable host capabilities remain unverified.

## Review isolation and optional packs

For goldfish reviews, start new agents with conversation inheritance disabled and give them only the design, requirements, source references, repository constraints and a bounded question. A fresh name alone does not prove isolation. Use at least two separate reviewer contexts for design-review. Security candidates need a verifier that did not discover them. If the installed host cannot provide isolation, record the corresponding gate as unverified; do not substitute a self-review and mark it passed.

Manual Cursor smoke check: invoke each new skill, verify the expected procedure is loaded, confirm both reviewers refuse writes, and inspect reviewer context setup for inherited chat. Record the installed Cursor version, inputs and observed results before claiming runtime support. Static validator success proves metadata shape and required files only.

Earlier authenticated CLI attachment selected upstream grill-me, tdd and security-audit while this starter used those local names. Local skills were renamed in F-01; optional packs may still install under the upstream names. Explicit-only skills need not appear in the ambient skill inventory, so inventory absence alone is not a discovery failure.

Native Task calls with the architect and verifier names were observed. Both refused the requested write and reported no parent-only canary. The Task schema describes non-resumed calls as fresh and exposes no separate inheritance flag. Reviewers still receive standard host instructions; fresh conversation does not mean an empty system prompt. The earlier smoke established behavioral refusal. A later matched-pair MAINT-002 probe recorded a `verifier` Write attempt that the host denied (ask mode / non-read-only tools) while a `generalPurpose` control Write succeeded in the same temp fixture; see SETUP.md. Keep read-only metadata and scoped prompts; do not treat them as an operating-system security boundary.

External pack commands and source links are in [README.md](../README.md#recommended-additional-skills). References checked on 2026-11-09 include the [Skills CLI](https://github.com/vercel-labs/skills) (Node.js prerequisite and selection flags), [Addy's pack](https://github.com/addyosmani/agent-skills) (shared-reference limitations for individual installs), and [EGM setup](https://github.com/google/elephant-goldfish-model#install) (complete-plugin recommendation). The follow-up installed complete user-level checkouts, with Matt's stable engineering/productivity skills selected, to retain shared resources without adding upstream files to this template. See [SETUP.md](SETUP.md) for paths, pinned source revisions, branch protection and actual runtime status. Local procedures remain independently written and self-contained. This adds no application runtime dependency or stack.
