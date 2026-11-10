# Maintaining this starter

Consumer behavioral rules live in `AGENTS.md`. Keep that file free of maintainer-only process, branch policy and machine records.

## Local skills

- Register each skill name in `scripts/skill_inventory.py`.
- Add a `skills-meta` block to the skill's `SKILL.md`.
- Regenerate `docs/SKILLS.md` with `python scripts/generate_skills_guide.py`.
- Extend removal regression coverage in `tests/test_starter.py`.
- Do not reintroduce local skill directory names listed in `COLLIDING_UPSTREAM_NAMES`.

## Template vs this repository

- When adopting the template for an application, replace starter enhancement requirements and evidence with the project's requirements; retain relevant decisions and verification limits.
- Record procedure inspection apart from live Cursor execution. Keep requirements, task status and quality-gate evidence aligned with the scope being delivered.
- Machine-specific installations and host verification belong in `docs/SETUP.md`; they do not transfer to template copies.
- Fresh copies can use the opt-in [initialization plan](docs/INITIALIZE.md). The upstream source keeps its history; do not initialize it.
- After changing baseline source files, run `python scripts/project_manifest.py` and inspect the inventory before committing. Default source validation checks freshness; `--project` is only for initialized application copies.

## Repository process

- This repository's `main` branch requires pull requests and both starter CI jobs, including for admins.
- Commit identity policy and release hygiene notes stay here or in release docs, not in consumer `AGENTS.md`.
- Record noteworthy starter changes in `CHANGELOG.md` in the same implementation PR that ships them. Prefer that over evidence-only follow-up PRs. Keep `VERSION` aligned with exactly one matching `## [version]` section; check with `python scripts/changelog_release.py --check` and print notes with `python scripts/changelog_release.py`.

## Tagged prereleases

The first release is `v0.1.0`, designated as a GitHub prerelease rather than latest
stable. Record measurable release criteria and the decision in PRD/DECISIONS;
align CHANGELOG's date, scope and limits before publication. The user authorized
this first publication after Cursor and Codex agreed on the decision.

Run both configured starter checks and the changelog check. Installer tests cover
fresh install, clean/forced upgrade, backup/refusal and inspection behavior;
initializer tests cover preview, applied copies and recovery. Merge the release
documentation PR through the required Windows/Linux Python 3.12 jobs. Verify the
selected merged main commit also has both green jobs before tagging it.

Extract notes with `python scripts/changelog_release.py`. Include the starter-only
scope, partial/blocked comparative evidence, unverified native isolation and
universal enforcement, and deferred multi-host work. Create an annotated
`v0.1.0` tag at the checked commit, then publish with `gh release create` using
`--verify-tag`, `--prerelease`, `--latest=false` and `--notes-file`.
Verify release metadata, note contents and tag target after publication.

Do not move a published version tag. A defective release can be marked as a
prerelease with an explanatory notice and superseded by a new reviewed version;
reverting source changes follows the protected PR process. Existing installations
remain snapshots until their owners choose an upgrade.

## Installer package

See [docs/INSTALL.md](docs/INSTALL.md) and [docs/CONFIGURATION.md](docs/CONFIGURATION.md). Forced upgrades remove obsolete renamed reference snapshots when authorized.

## Publishing helpers

The root publish-to-github.py/.sh helpers publish an extracted starter as a PUBLIC
GitHub template. They require Git, GitHub CLI and Python, refuse an existing local
Git repository and never overwrite an existing remote repository. Authenticate
with GitHub CLI and obtain authorization before running
`python publish-to-github.py OWNER/REPOSITORY` (or the Bash wrapper).
Initialization removes these starter-maintainer helpers from application copies.
