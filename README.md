# Cursor AI Project Starter

A reusable, stack-agnostic template for planning, implementing and verifying software with Cursor.
No application framework, credentials or third-party integrations are preinstalled.

## One command for new and existing projects

Open a folder in Cursor and type:

```text
/project-helper
```

Choose **Start a new project** or **Improve the project you have open**, then answer in normal language. The helper selects the planning, review, testing and debugging workflows for you. It presents a plan for approval before implementation. For an existing project, it starts by inspecting the project and proposing changes; you do not need to copy starter configuration into that project.

Use Cursor's **Agent** chat mode when you want it to build or apply fixes. **Ask** mode can assess and plan, but cannot make those changes.

Examples: `/project-helper Start a personal budgeting app` or `/project-helper Review this project's tests`. If no goal is given, the command asks which mode you want. You do not need another slash command to continue.

### Install once for use in other folders

Install and upgrade steps live in [docs/INSTALL.md](docs/INSTALL.md). The repository-local command is also available when working in this starter itself. See [configuration and verification](docs/CONFIGURATION.md) for package layout and limits.

## Advanced: individual workflows and template adoption

1. Use this repository as a GitHub template, then open your copy in Cursor.
2. Read AGENTS.md and fill in docs/PRD.md.
3. Invoke `/project-planning`. Use `/decision-interview` for unresolved decisions and `/design-review` for a new system or material design change; the architect reviews requirements and the verifier can review with fresh context.
4. Approve the implementation plan, then implement in small increments.
5. Build behavior changes with `/test-first-change`, run the project checks and ask the verifier to inspect the diff against acceptance criteria. Use `/trust-boundary-audit` for sensitive boundaries and `/release-check` to assess release evidence.

Suggested first prompt:

> Read AGENTS.md and docs/PRD.md. Use /project-planning and the architect subagent to define requirements, propose a suitable stack, identify risks and plan real application quality gates. Present the plan for approval before writing application code.

## Included

- AGENTS.md: concise shared operating instructions for every project copy.
- MAINTAINING.md: maintainer-only process for this starter repository.
- docs/INSTALL.md: user-level `/project-helper` install and upgrade.
- .cursor/rules/: architecture, testing and security rules scoped by file patterns.
- .cursor/skills/: the project-helper entry point plus eight focused workflows for planning, interviewing, prior-art search, design review, TDD, debugging, security audit and release checks.
- .cursor/agents/: read-only architect and verifier definitions.
- docs/: requirements, architecture, decisions, tasks, quality gates and integrations.
- LICENSE: MIT license, copyright Guven Bircan 2026.
- .env.example: placeholder values only. Copy it to .env for local secrets.
- .github/workflows/ci.yml: starter validation on Linux and Windows.
- publish-to-github.py and .sh: explicit public GitHub template publishing.
- scripts/install_chat_command.py: one-time installation of the user-level project-helper command.

## Local skill workflow

Start with `/project-helper` for routing. The canonical use/do-not-use table, lifecycle map and weights live in [docs/SKILLS.md](docs/SKILLS.md). Skills require explicit invocation to keep ambient context small. Review agents remain read-only. Fresh-context isolation is a host capability, not a guarantee supplied by a Markdown file. See [configuration limits](docs/CONFIGURATION.md) and [quality gates](docs/QUALITY_GATES.md).

Former local names `grill-me`, `tdd`, `systematic-debugging` and `security-audit` were renamed so bare slash commands no longer collide with optional upstream packs. Existing global installs need `python scripts/install_chat_command.py --upgrade --force` once to drop obsolete reference snapshots.

## Recommended Additional Skills

These local files are independently written, reduced workflows informed by ideas from the packs below; they do not vendor the full packs or provide their complete tooling. Attribution and comparison results are in [THIRD_PARTY.md](THIRD_PARTY.md). Optional installation commands:

```sh
npx skills add mattpocock/skills
npx skills add addyosmani/agent-skills
npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit
npx skills add google/elephant-goldfish-model
```

- [Matt Pocock's skills](https://github.com/mattpocock/skills): requirements interviews, specifications, TDD and rigorous code reviews.
- [Addy Osmani's agent skills](https://github.com/addyosmani/agent-skills): development lifecycle workflows with phase exit criteria.
- [Cloudflare's security audit skill](https://github.com/cloudflare/security-audit-skill): a larger audit workflow with coverage ledgers, independent verification and report validators.
- [Google's Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model): context-rich drafting and fresh-context design review. Upstream recommends the complete plugin so reviewer prompts and document standards are available; a skills-only install does not establish full-plugin compatibility.

The [Skills CLI](https://github.com/vercel-labs/skills) requires Node.js 22.20 or later at the time of this update. Node.js is optional for this template; its checks use only Python. Run installation from your project, choose Cursor and select skills; add `--list` to browse or `--skill <name> --agent cursor` to select a skill and agent. Inspect proposed changes before accepting an overwrite. Upstream packs may still use names such as `grill-me`, `tdd` and `security-audit`; this starter's local counterparts use distinct names listed above. External packs can require shared references, tools or subagent capabilities; follow their upstream setup instructions. The maintainer's optional packages were installed outside the repository; see [the setup record](docs/SETUP.md) for paths, revisions and runtime limits. Note-taking packs are outside this starter's scope.

## Validate this template

Requires Python 3.12, the version used in CI. No Python packages are needed.

```sh
python scripts/validate_starter.py
python -m unittest discover -s tests -v
```

These checks validate the template structure and metadata. They do not lint, build, secure or test an application. Configure actual application checks after choosing the stack; see docs/QUALITY_GATES.md.

## Adoption and remaining setup

The current PRD, completed task list and verification record describe this starter's skill enhancement. When creating an application from the template, replace those requirements and evidence with your application's scope; keep the requirement wording rules and relevant decisions.

Before relying on the workflows in your installed Cursor version:

1. Confirm discovery of all nine skills and both agents, then invoke the new skills and verify the expected procedures load.
2. Confirm review agents remain read-only and goldfish reviewers receive no inherited conversation. Record the Cursor version and observed results in `docs/QUALITY_GATES.md`.
3. Check the GitHub Actions results for Python 3.12 on Windows and Linux. Configure required status checks through GitHub repository settings if you want merges gated on CI.
4. After choosing an application stack, configure its formatting, linting, tests, build and relevant security/accessibility checks. Optional external skill packs can be installed when needed; the local workflows do not require them.

Local enhancement checks passed on Windows with Python 3.13.14; GitHub CI passed on Windows and Linux with Python 3.12. This repository requires both CI jobs through `main` branch protection. Authenticated Cursor CLI smoke checks verified skill attachment/loading, custom reviewer invocation, write refusal and a parent-context canary probe. A later MAINT-002 matched-pair probe recorded host denial of a `verifier` Write attempt while a writable control Write succeeded. These bounded observations do not establish OS-level isolation, universal context isolation or complete upstream workflow execution. Optional packs and machine settings are not bundled into template copies. See [the setup record](docs/SETUP.md) and [verification record](docs/QUALITY_GATES.md#enhancement-verification-record-2026-11-09) for evidence and limitations.

## Publish an extracted copy

Install Git, GitHub CLI and Python. Sign in using `gh auth login`, then run:

```sh
python publish-to-github.py guventech/ai-project-starter
```

This creates a PUBLIC repository, pushes the starter, and enables its template setting.
It refuses existing Git repositories to avoid publishing unrelated work. An existing remote repository is never overwritten.
On Git Bash, macOS or Linux, `bash publish-to-github.sh guventech/ai-project-starter` is equivalent.

See docs/CONFIGURATION.md for documentation references and runtime verification limits.
