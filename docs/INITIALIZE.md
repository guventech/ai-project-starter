# Initialize a new template copy

Use this only in a fresh copy made with GitHub's template button or an extracted
archive. It removes the starter's own development records so they cannot be
mistaken for your application's requirements or check results. It does not pick
a stack, create application code, rewrite Git history or alter account settings.

Requires Python 3.12+. A Git-backed copy also needs Git 2.36+, a clean worktree and
its own remote; any remote pointing to the upstream starter causes refusal.
Partial-clone/promisor repositories are unsupported. Git inspection uses index
metadata rather than status, so configured worktree content filters do not run.

## Preview and apply

Before editing project files, preview the exact reset/remove list:

```sh
python scripts/init_project.py
```

If that list matches the intended fresh-copy setup, apply it:

```sh
python scripts/init_project.py --apply
```

To inspect or initialize another fresh copy, pass `--destination <copy-folder>`.
Preview makes no backup or file changes. Modified, missing, extra or linked files
cause refusal before mutation; Python bytecode caches count as extras. Do not
delete user work to force a match: use a separate fresh template copy instead.
The initializer suppresses its own local import caches. Text line-ending
conversion alone is accepted; all other stock text content must match.

## Keep, reset and remove

Keep .cursor skills, rules and agents, AGENTS.md, the licence and attribution,
generated skill guide, generic architecture/integration guidance, the environment
example and reusable installer/configuration checks. The default source validator
remains strict. Initialized projects use the explicit --project profile, retaining
the skill-name denylist, generated-guide check, consumer-only AGENTS rules and
privacy checks. Their CI checks configuration only; application checks start
unconfigured. No previous host observations or application successes are copied.

Reset resources live at `scripts/project_templates/<reset-target>` and are
reviewable text. The following inventory is also printed by preview:

<!-- initialization-plan -->
```text
RESET .github/workflows/ci.yml
RESET CONTRIBUTING.md
RESET MAINTAINING.md
RESET README.md
RESET docs/CONFIGURATION.md
RESET docs/DECISIONS.md
RESET docs/INSTALL.md
RESET docs/PRD.md
RESET docs/QUALITY_GATES.md
RESET docs/RULES.md
RESET docs/SETUP.md
RESET docs/TASKS.md
REMOVE .github/ISSUE_TEMPLATE/bug_report.md
REMOVE .github/ISSUE_TEMPLATE/feature_request.md
REMOVE CURSOR_UPDATE_PROMPT.md
REMOVE docs/INITIALIZE.md
REMOVE docs/designs/project-initialization.md
REMOVE docs/superpowers/plans/2026-11-09-maint-002-permission-probe.md
REMOVE docs/superpowers/specs/2026-11-09-maint-002-permission-probe-design.md
REMOVE evals/prior-art-search-hygiene.md
REMOVE publish-to-github.py
REMOVE publish-to-github.sh
REMOVE scripts/init_project.py
REMOVE scripts/project-manifest.json
REMOVE scripts/project_manifest.py
REMOVE scripts/project_templates/.github/workflows/ci.yml
REMOVE scripts/project_templates/CONTRIBUTING.md
REMOVE scripts/project_templates/MAINTAINING.md
REMOVE scripts/project_templates/README.md
REMOVE scripts/project_templates/docs/CONFIGURATION.md
REMOVE scripts/project_templates/docs/DECISIONS.md
REMOVE scripts/project_templates/docs/INSTALL.md
REMOVE scripts/project_templates/docs/PRD.md
REMOVE scripts/project_templates/docs/QUALITY_GATES.md
REMOVE scripts/project_templates/docs/RULES.md
REMOVE scripts/project_templates/docs/SETUP.md
REMOVE scripts/project_templates/docs/TASKS.md
REMOVE tests/test_init_project.py
REMOVE tests/test_install_chat_command.py
REMOVE tests/test_starter.py
```
<!-- end-initialization-plan -->

Each resource is removed as an individual file after use; no project directory
tree is recursively deleted. Empty directories may remain. Third-party provenance
is retained as attribution, not as application verification. The initialization
command, its baseline and resources are removed after success, so it cannot be
run twice from the initialized project.

## Recovery and limits

Apply first creates a unique sibling `<copy-name>.init-backup-*` folder and
verifies that every affected original is copied byte for byte, including original
line endings. The backup is outside the project and contains old starter records.
Keep it until you inspect the resulting Git diff. No global install is upgraded.

An ordinary replacement/removal error attempts to restore the originals and
retains the backup. A killed process, power loss or rollback error needs manual
recovery: inspect the project diff and backup, then restore only the intended
files after checking for later edits. Do not copy a backup over subsequent work.
The command is not an atomic multi-file transaction or protection against hostile
concurrent filesystem changes. A partial backup from a pre-mutation error is not
a recovery snapshot; the target is unchanged in that case.

After success, fill docs/PRD.md and configure application quality gates. Run
`python scripts/validate_starter.py --project` for retained configuration checks.

## Maintaining this command

The baseline detects stock content, not authenticity. In this upstream source,
regenerate `scripts/project-manifest.json` with
`python scripts/project_manifest.py` after editing baseline files. Inspect its
inventory before committing. Default source validation checks freshness; no
--project marker or auto-detection can disable that default check. The manifest
and generator support the template's UTF-8 text files, not binary application data.
