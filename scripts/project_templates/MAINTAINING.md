# Maintaining workflow configuration

These instructions concern the reusable configuration in this project.

- Register local skills in `scripts/skill_inventory.py`; keep distinct names.
- Update skills-meta and run `python scripts/generate_skills_guide.py` after
  changing skill metadata. Do not hand-edit the generated guide.
- Run `python scripts/validate_starter.py --project` to check metadata, skill
  names, guide freshness, consumer AGENTS rules and documentation privacy.
- Configure this project's application checks in docs/QUALITY_GATES.md.
- Record local host observations in docs/SETUP.md without credentials or personal paths.

No upstream repository's branch settings or verification results apply here.
