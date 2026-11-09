# Configuration references and limitations

Reconstructed on 2026-10-30 after the earlier ZIP was unavailable.
Configuration shapes checked against official documentation:
- Rules and AGENTS.md: https://cursor.com/docs/rules
- Skills: https://cursor.com/docs/skills
- Subagents: https://cursor.com/docs/subagents
- MCP: https://cursor.com/docs/mcp
- Publishing: https://cli.github.com/manual/gh_repo_create
- Template flag: https://cli.github.com/manual/gh_repo_edit

Rules use description, comma-separated globs and alwaysApply false. Adjust globs when adopting a different layout.
Skills use name/description and explicit invocation to keep ambient context small.
Agents inherit the chosen model and set readonly true. The verifier asks its parent to run checks that write artifacts.
AGENTS.md is the shared behavioral core; Cursor-specific files are not claimed portable to other agents.
Static checks cannot prove Cursor discovery or runtime behavior. Open the folder in your installed Cursor,
check all three rules and nine skills are discovered, invoke /project-helper or /project-planning, then ask for the architect and verifier.
Confirm read-only behavior before relying on it. Bounded live CLI smoke results are recorded in SETUP.md; editor UI discovery and complete workflow execution are not claimed.

## Local skills

The nine local skills are project-helper, project-planning, grill-me, prior-art, design-review, tdd, systematic-debugging, security-audit and release-check. Sibling links describe procedures a selected workflow can read; they do not change explicit invocation metadata.

## One-command installation

Run `python scripts/install_chat_command.py` once to install the user-level `/project-helper` entry point. `--destination /path/to/project-helper` selects a different new package directory for inspection/testing; its basename must remain project-helper. An occupied path or symlink is rejected. A filesystem error during writing can leave a partial new package; inspect that exact directory before retrying. The installer does not remove or replace files.

The package has one discoverable SKILL.md, the MIT license, and ten adjacent reference documents: eight workflow snapshots and two reviewer role snapshots. References use `.md` filenames rather than nested SKILL.md files to avoid duplicate skill discovery. The installer rewrites the known internal workflow references for the bundled layout. No machine-specific repository path, application code, secrets, historical PRD or third-party pack is copied.

The entry point resolves procedures relative to its actual attached source. Repository-local invocation uses sibling skills and `.cursor/agents`; user-level invocation uses the bundled references. Other workspaces keep their existing instructions and tests. A general fresh reviewer can read the bundled role when that workspace does not register architect/verifier by name. Unavailable host capabilities remain unverified.

The installed snapshots do not update when the checkout changes. Before updating, compare any existing user edits and preserve them; the first-install command refuses to overwrite. Reload/start a new Cursor chat after installation and verify `/project-helper` in the actual target workspace. Installation does not enable cloud sync or grant permission to publish, deploy or edit another project without its approved plan.

## Review isolation and optional packs

For goldfish reviews, start new agents with conversation inheritance disabled and give them only the design, requirements, source references, repository constraints and a bounded question. A fresh name alone does not prove isolation. Use at least two separate reviewer contexts for design-review. Security candidates need a verifier that did not discover them. If the installed host cannot provide isolation, record the corresponding gate as unverified; do not substitute a self-review and mark it passed.

Manual Cursor smoke check: invoke each new skill, verify the expected procedure is loaded, confirm both reviewers refuse writes, and inspect reviewer context setup for inherited chat. Record the installed Cursor version, inputs and observed results before claiming runtime support. Static validator success proves metadata shape and required files only.

The authenticated CLI attached project-planning, design-review, release-check and systematic-debugging from the project, while bare grill-me, tdd and security-audit attached optional upstream files. Select those three local procedures by their explicit `.cursor/skills/<name>/SKILL.md` paths; this loading route was tested. Explicit-only skills need not appear in the ambient skill inventory, so inventory absence alone is not a discovery failure.

Native Task calls with the architect and verifier names were observed. Both refused the requested write and reported no parent-only canary. The Task schema describes non-resumed calls as fresh and exposes no separate inheritance flag. Reviewers still receive standard host instructions; fresh conversation does not mean an empty system prompt. They also reported edit/shell tool categories, so this test establishes behavioral refusal, not proof of host-enforced write denial. Keep read-only metadata and scoped prompts; use host permissions when a permission boundary is required.

External pack commands and source links are in [README.md](../README.md#recommended-additional-skills). References checked on 2026-11-09 include the [Skills CLI](https://github.com/vercel-labs/skills) (Node.js prerequisite and selection flags), [Addy's pack](https://github.com/addyosmani/agent-skills) (shared-reference limitations for individual installs), and [EGM setup](https://github.com/google/elephant-goldfish-model#install) (complete-plugin recommendation). The follow-up installed complete user-level checkouts, with Matt's stable engineering/productivity skills selected, to retain shared resources without adding upstream files to this template. See [SETUP.md](SETUP.md) for paths, pinned source revisions, branch protection and actual runtime status. Local procedures remain original and self-contained. This adds no application runtime dependency or stack.
