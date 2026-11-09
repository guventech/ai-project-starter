# Cursor AI Project Starter

Plan a change, agree on the scope, then build with tests and recorded checks.
This Cursor template combines `/project-helper`, eight focused workflows and configuration validation.
Use a fresh template copy for a new project, or install the helper for an existing one.

For Cursor users who want requirements, implementation approval and review evidence
in one workflow. Bring your own application framework and checks. Choose a
framework starter when you need prebuilt application code.

## Quickstart

Requires Cursor and Python 3.12+; CI uses Python 3.12. Optional external packs are
not needed for the local workflows.

**Already have a project?** From a checkout of this repository, install once:

```sh
python scripts/install_chat_command.py
```

Reload Cursor, open your actual project in **Agent** chat mode, and type:

```text
/project-helper Review this project's tests
```

The helper reads that project's instructions and proposes a plan before edits.
Install/upgrade details and snapshot checks: [docs/INSTALL.md](docs/INSTALL.md).

**Starting a new project?** Use this repository as a GitHub template. Before editing
the copy, preview `python scripts/init_project.py`; review the list before choosing
`python scripts/init_project.py --apply`. Git-backed copies require Git 2.36+.
The [initialization guide](docs/INITIALIZE.md) explains refusal checks and backups.
Then open the initialized copy in Cursor and use `/project-helper` with your goal.

## A recorded routing example

An isolated calculator-fixture review produced this sequence:

```text
Task: review an existing project's code and tests
Read: that project's AGENTS.md, calculator source and tests
Selected: bundled test-first and verifier procedures
Returned: findings and proposed checks; no edits
```

This summarizes the [recorded CLI Ask-mode trial](docs/SETUP.md#one-command-project-helper),
not a verbatim transcript or an end-to-end application demo. Agent mode and an
approved target-project plan are needed to apply changes.

## How it compares

These are differences in packaging and workflow scope, based on the linked
upstream descriptions. They are not comparative performance results.

| Project | Focus | When to consider it |
|---------|-------|---------------------|
| This starter | Cursor template, one new/improve entry point, bundled snapshots and configuration checks | You want a small project workflow with an installer and clean-copy initialization. |
| [Matt Pocock's skills](https://github.com/mattpocock/skills) | A collection of engineering skills | You want to select individual procedures from that collection. |
| [Superpowers](https://github.com/obra/superpowers#how-it-works) | A composable development methodology with automatic skill triggering and harness-specific installation | You want to adopt that methodology and its integrations. |
| [Google EGM](https://github.com/google/elephant-goldfish-model#how-it-works) | Context-rich specification drafting and fresh-context review | You want its specification/review workflow with the complete plugin resources. |

Fit guidance is an editorial judgment. Outcome comparisons with a plain prompt
remain unmeasured. Local procedures are independently written, reduced workflows;
sources and comparison classifications are in [THIRD_PARTY.md](THIRD_PARTY.md).

## Choose a workflow

Start with `/project-helper`, or use the generated [skill decision guide](docs/SKILLS.md)
for use/do-not-use conditions, prerequisites and exit criteria. [Rule triggers](docs/RULES.md)
describe the default file scopes. Host-specific setup is covered in [configuration](docs/CONFIGURATION.md).

## Verification at a glance

| Verified in bounded checks | Not established | How to check the details |
|----------------------------|-----------------|--------------------------|
| Starter metadata, installer behavior and initializer recovery fixtures on Windows/Linux CI | Application quality or release readiness | [Quality gates and commands](docs/QUALITY_GATES.md) |
| Recorded CLI routing/loading trials and a Go rule-marker probe | General editor UI behavior, universal context isolation or complete workflow execution | [Verification scope](docs/VERIFICATION.md) and [host observations](docs/SETUP.md) |
| Read-only reviewer refusal and one matched-pair host-denied Write observation | OS-level isolation across hosts | [Verification limits](docs/VERIFICATION.md) |
| No comparative outcome claim | Better results or faster delivery than a bare prompt | [Evidence gaps](docs/VERIFICATION.md#outcome-evidence) |

## Recommended additional skills

Optional packs, installation commands, prerequisites and full-plugin limits are in
[docs/OPTIONAL_SKILLS.md](docs/OPTIONAL_SKILLS.md). The local workflows work without them.
Existing global installs with former skill names have a [migration note](docs/INSTALL.md#renamed-workflow-references).

## Contribute or maintain

See [CONTRIBUTING.md](CONTRIBUTING.md) for reporting and PR guidance, and
[MAINTAINING.md](MAINTAINING.md) for source validation, baseline updates and publishing helpers.
The checks validate workflow configuration; select application checks after choosing a stack.

MIT licensed — [LICENSE](LICENSE). Upstream attribution: [THIRD_PARTY.md](THIRD_PARTY.md).
