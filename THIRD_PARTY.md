# Third-party notices

This starter is MIT-licensed (see `LICENSE`). Local skill and agent instruction text in this repository was compared against the upstream packages listed below on 2026-11-09. Comparison method: strip YAML frontmatter, measure character length, shared nonempty lines, and token Jaccard similarity against the pinned upstream revisions listed in this notice. The table uses current local paths and records former names for provenance. This inherited attribution is not evidence of execution in a derived application.

## Summary

| Local path | Upstream | Revision (maintainer install) | Licence | Use classification | Result |
|------------|----------|-------------------------------|---------|--------------------|--------|
| `.cursor/skills/decision-interview/SKILL.md` (formerly `grill-me`) | [mattpocock/skills](https://github.com/mattpocock/skills) `grill-me` | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | MIT | Idea and former name | Independently written local body; installed upstream file is a stub that delegates to another skill. Shared nonempty lines: 0. Token Jaccard ≈ 0.01. |
| `.cursor/skills/test-first-change/SKILL.md` (formerly `tdd`) | [mattpocock/skills](https://github.com/mattpocock/skills) `tdd` | `4ae2317ddb22b046e26455e4f9c9b3aaaf62212d` | MIT | Idea and former name (red-green-refactor) | Independently written local body. Shared nonempty lines: 0. Token Jaccard ≈ 0.14. No long shared fragments found. |
| `.cursor/skills/trust-boundary-audit/SKILL.md` (formerly `security-audit`) | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) | `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8` | MIT | Idea and structure (coverage-led audit phases) | Independently written four-phase local body; omits upstream schemas, harness and validators. Shared nonempty lines: 1 (heading only). Token Jaccard ≈ 0.17. |
| `.cursor/skills/design-review/SKILL.md` | [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) `egm-review` | `5382b17619be07811a14b2146c7672620b34a791` | Apache-2.0 | Idea (fresh-context / goldfish review) | Independently written local body; does not copy plugin personas or document standards. Shared nonempty lines: 0. Token Jaccard ≈ 0.14. |
| `.cursor/skills/hypothesis-debugging/SKILL.md` (formerly `systematic-debugging`) | [obra/superpowers](https://github.com/obra/superpowers) `systematic-debugging` | Cursor cache package `d884ae04edebef577e82ff7c4e143debd0bbec99` | MIT | Idea and former name | Independently written local body. Shared nonempty lines: 1 (heading only). Token Jaccard ≈ 0.08. |
| Lifecycle inspiration only | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | `301b02b12bff98e4688e6984af6556802322bbde` | MIT | Idea (phase exit criteria) | Cited from `release-check` and README; no local skill is a counterpart file. |
| `.cursor/skills/project-helper/SKILL.md` | None | n/a | n/a | Local | No upstream counterpart audited. |
| `.cursor/skills/project-planning/SKILL.md` | None | n/a | n/a | Local | No upstream counterpart audited. |
| `.cursor/skills/prior-art/SKILL.md` | None | n/a | n/a | Local | No upstream counterpart audited. |
| `.cursor/skills/release-check/SKILL.md` | Addy Osmani lifecycle ideas only | see above | MIT | Idea | Independently written; cites Addy Osmani as inspiration. |
| `.cursor/agents/architect.md` | None as a vendored file | n/a | n/a | Local | Read-only reviewer role for this starter. |
| `.cursor/agents/verifier.md` | None as a vendored file | n/a | n/a | Local | Read-only reviewer role for this starter. |

## Licence notes

- **MIT upstreams (Matt Pocock, Cloudflare, Addy Osmani, obra/superpowers):** this repository does not include substantial portions of those files. Copyright notices are recorded here for attribution of ideas and names. Full licence text remains with each upstream checkout.
- **Apache-2.0 (EGM):** this repository does not reproduce EGM plugin text, NOTICE contents or document standards. Ideas about fresh-context review are credited; no modified Apache-licensed file is redistributed here. The EGM `LICENSE` remains with the installed plugin.
- Optional pack installation remains separate from this template. Installing those packs is governed by their own licences.

## Unresolved items

- Upstream package trees can change after the pinned revisions above; re-run the comparison before claiming equivalence.
- Cursor plugin cache paths are machine-local evidence of the compared superpowers revision; they are not shipped with template copies.
