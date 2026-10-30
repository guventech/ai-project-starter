# Cursor AI Project Starter

A reusable, stack-agnostic template for planning, implementing and verifying software with Cursor.
No application framework, credentials or third-party integrations are preinstalled.

## Start a project

1. Use this repository as a GitHub template, then open your copy in Cursor.
2. Read AGENTS.md and fill in docs/PRD.md.
3. Invoke `/project-planning` and ask the architect subagent to review the proposed design.
4. Approve the implementation plan, then implement in small increments.
5. Run the project checks and ask the verifier to inspect the diff against acceptance criteria.

Suggested first prompt:

> Read AGENTS.md and docs/PRD.md. Use /project-planning and the architect subagent to define requirements, propose a suitable stack, identify risks and plan real application quality gates. Present the plan for approval before writing application code.

## Included

- AGENTS.md: concise shared operating instructions.
- .cursor/rules/: architecture, testing and security rules scoped by file patterns.
- .cursor/skills/: project-planning, systematic-debugging and release-check workflows.
- .cursor/agents/: read-only architect and verifier definitions.
- docs/: requirements, architecture, decisions, tasks, quality gates and integrations.
- .github/workflows/ci.yml: starter validation on Linux and Windows.
- publish-to-github.py and .sh: explicit public GitHub template publishing.

## Validate this template

Requires Python 3.11 or newer; no Python packages are needed.

```sh
python scripts/validate_starter.py
python -m unittest discover -s tests -v
```

These checks validate the template structure and metadata. They do not lint, build, secure or test an application. Configure actual application checks after choosing the stack; see docs/QUALITY_GATES.md.

## Publish an extracted copy

Install Git, GitHub CLI and Python. Sign in using `gh auth login`, then run:

```sh
python publish-to-github.py guventech/ai-project-starter
```

This creates a PUBLIC repository, pushes the starter, and enables its template setting.
It refuses existing Git repositories to avoid publishing unrelated work. An existing remote repository is never overwritten.
On Git Bash, macOS or Linux, `bash publish-to-github.sh guventech/ai-project-starter` is equivalent.

See docs/CONFIGURATION.md for documentation references and runtime verification limits.
