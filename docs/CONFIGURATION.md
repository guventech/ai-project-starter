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
check the three rules and skills are discovered, invoke /project-planning, then ask for the architect and verifier.
Confirm read-only behavior before relying on it. No live Cursor invocation is claimed by this template.
