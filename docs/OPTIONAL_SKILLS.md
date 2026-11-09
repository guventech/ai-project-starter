# Optional external skill packs

The local `/project-helper` and eight focused procedures need no external pack.
They are independently written, reduced workflows informed by upstream ideas;
attribution and pinned comparison classifications are in [THIRD_PARTY.md](../THIRD_PARTY.md).

Optional installation commands:

```sh
npx skills add mattpocock/skills
npx skills add addyosmani/agent-skills
npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit
npx skills add google/elephant-goldfish-model
```

- [Matt Pocock's skills](https://github.com/mattpocock/skills): engineering skills,
  including interviews, specifications, TDD and reviews.
- [Addy Osmani's skills](https://github.com/addyosmani/agent-skills): development
  lifecycle procedures; retain any shared references the selected skill needs.
- [Cloudflare's security audit](https://github.com/cloudflare/security-audit-skill):
  a larger audit workflow with its own supporting material and validators.
- [Google EGM](https://github.com/google/elephant-goldfish-model#install): upstream
  recommends its complete plugin for reviewer prompts and document standards.
  The skills-only command above does not establish complete-plugin setup or compatibility.

The [Skills CLI](https://github.com/vercel-labs/skills#install-a-skill) documents
Node.js 22.20+ as a prerequisite (checked 2026-11-09). Node.js is optional for this
starter's Python checks. Run optional installation from the intended project,
choose Cursor and the needed skills, and inspect changes before any overwrite.
Follow each upstream's current setup for shared resources and host capabilities.

Upstream names such as grill-me, tdd, systematic-debugging and security-audit are
distinct from this starter's local names. Use the [canonical guide](SKILLS.md)
to select local workflows and the [installation guidance](INSTALL.md)
for older global snapshots. Note-taking packs remain outside the starter's scope.
