# Contributing

This guide covers contributions to the starter itself. For installation and
upgrades, see [INSTALL.md](docs/INSTALL.md); for choosing a workflow, see the
[skill guide](docs/SKILLS.md).

## Report a bug or propose a feature

Search existing issues first, then choose the bug-report or feature-request
template when opening an issue. Use a small synthetic example. Remove credentials,
private project text, client names, internal identifiers, personal paths and
session IDs from reports, logs and screenshots before posting them publicly.

For bugs, include the starter commit, installation mode, relevant host versions,
reproduction steps and expected versus observed results. For features, explain
the problem, a concrete outcome and alternatives considered. The templates are
editable prompts; they do not enforce required fields.

## Propose a change

1. Read [AGENTS.md](AGENTS.md). For nontrivial changes, agree on scope, measurable
   acceptance criteria and a plan before implementation.
2. Follow [MAINTAINING.md](MAINTAINING.md) for skill metadata, generated docs and
   this repository's protected-branch process. Keep one focused change per PR.
3. Run the configured commands in [QUALITY_GATES.md](docs/QUALITY_GATES.md),
   using Python 3.12 as in CI. Record actual results and skipped checks; distinguish
   static inspection from observed Cursor execution.
4. Use the [PR template](.github/pull_request_template.md) to explain the change,
   verification, risks and rollback. Both required CI jobs must pass before merge.

Keep feedback specific and respectful. Maintainer procedures belong in
MAINTAINING.md; consumer behavioral rules belong in AGENTS.md.
