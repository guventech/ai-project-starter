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

## Installer package

See [docs/INSTALL.md](docs/INSTALL.md) and [docs/CONFIGURATION.md](docs/CONFIGURATION.md). Forced upgrades remove obsolete renamed reference snapshots when authorized.
