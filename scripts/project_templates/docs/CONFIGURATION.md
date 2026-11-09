# Workflow configuration

- AGENTS.md supplies shared behavioral rules for this project.
- .cursor/rules/*.mdc contain scoped Cursor guidance; see [RULES.md](RULES.md).
- .cursor/skills/*/SKILL.md contain explicitly selected workflows; see [SKILLS.md](SKILLS.md).
- .cursor/agents/*.md define read-only architect/verifier roles.

Run `python scripts/validate_starter.py --project` for static configuration
checks. Default source-maintainer validation is not the initialized-project mode.
The checks do not establish live Cursor behavior or application correctness.

Confirm discovery and procedure loading in your installed host. Fresh-context
review needs host support; record unavailable isolation as unverified. Configure
application checks in [QUALITY_GATES.md](QUALITY_GATES.md) after choosing a stack.

User-level procedures are snapshots installed with [INSTALL.md](INSTALL.md).
The retained THIRD_PARTY.md is attribution for the inherited workflow text,
not evidence that this application's workflows have run.
