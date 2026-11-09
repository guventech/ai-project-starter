# Cursor Update Prompt – Enhance ai-project-starter with High-Quality Agent Skills

You are updating the `guventech/ai-project-starter` repository so it includes the most valuable missing capabilities from these public skill packs:

- mattpocock/skills (grill-me, TDD, specs, rigorous reviews)
- addyosmani/agent-skills (full lifecycle, exit criteria)
- cloudflare/security-audit-skill (multi-phase audit with independent verification)
- google/elephant-goldfish-model (fresh-context design review)
- (Optional) kepano/obsidian-skills (only if note-taking is in scope)

## Goals

1. Keep the starter stack-agnostic and Cursor-friendly.
2. Add high-signal skills that force better planning, testing, security, and design review.
3. Document how users can also install the full external packs via `npx skills`.
4. Do not bloat the repo — prefer concise, high-quality SKILL.md files and clear references.

## Required Changes

### 1. Add / Update Skills in `.cursor/skills/`

Create or strengthen these skills (each as its own folder with a `SKILL.md`):

#### a) `grill-me`
Force the agent to interview the user until the plan is fully resolved before writing code.

#### b) `tdd`
Red-green-refactor loop. Write a failing test first, implement the minimum to pass, then refactor. One vertical slice at a time.

#### c) `design-review` (Elephant-Goldfish style)
- Elephant phase: draft design/spec with full context.
- Goldfish phase: spawn fresh agents with zero prior conversation to review the design document and try to find gaps, ambiguities, and risks.
- Only proceed to implementation after human approval.

#### d) `security-audit`
Simplified multi-phase security review:
1. Reconnaissance (architecture, trust boundaries, input surfaces)
2. Coverage-led hunting
3. Independent verification (fresh agent tries to disprove findings)
4. Structured report

#### e) Strengthen existing skills
- Improve `project-planning` so it can call or reference `grill-me` and `design-review`.
- Improve `release-check` with stronger quality gates.

### 2. Update Agents

In `.cursor/agents/` (or equivalent):
- Make the `architect` agent explicitly use design-review / grill-me style questioning.
- Make the `verifier` agent able to act as a “goldfish” (fresh context) when reviewing design docs or diffs.

### 3. Update Documentation

- **AGENTS.md**: Add a short section listing the recommended skills and when to use them. Include the one-line install commands for the full external packs.
- **README.md**: Add a “Recommended Additional Skills” section with install commands and short descriptions.
- **docs/QUALITY_GATES.md**: Reference the new security-audit and design-review gates.

### 4. Suggested Install Commands (document these)

```bash
# Full high-value packs (users can install selectively)
npx skills add mattpocock/skills
npx skills add addyosmani/agent-skills
npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit
npx skills add google/elephant-goldfish-model