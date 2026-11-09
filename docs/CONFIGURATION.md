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
check all three rules and seven skills are discovered, invoke /project-planning, then ask for the architect and verifier.
Confirm read-only behavior before relying on it. No live Cursor invocation is claimed by this template.

## Review isolation and optional packs

The seven local skills are project-planning, grill-me, design-review, tdd, systematic-debugging, security-audit and release-check. Sibling links describe procedures a selected workflow can read; they do not change explicit invocation metadata.

For goldfish reviews, start new agents with conversation inheritance disabled and give them only the design, requirements, source references, repository constraints and a bounded question. A fresh name alone does not prove isolation. Use at least two separate reviewer contexts for design-review. Security candidates need a verifier that did not discover them. If the installed host cannot provide isolation, record the corresponding gate as unverified; do not substitute a self-review and mark it passed.

Manual Cursor smoke check: invoke each new skill, verify the expected procedure is loaded, confirm both reviewers refuse writes, and inspect reviewer context setup for inherited chat. Record the installed Cursor version, inputs and observed results before claiming runtime support. Static validator success proves metadata shape and required files only.

External pack commands and source links are in [README.md](../README.md#recommended-additional-skills). References checked on 2026-11-09 include the [Skills CLI](https://github.com/vercel-labs/skills) (Node.js prerequisite and selection flags), [Addy's pack](https://github.com/addyosmani/agent-skills) (shared-reference limitations for individual installs), and [EGM setup](https://github.com/google/elephant-goldfish-model#install) (complete-plugin recommendation). Commands are documented, not executed. Local procedures are original and self-contained; external packs may depend on files beyond SKILL.md. This update adds no runtime dependency or application stack.
