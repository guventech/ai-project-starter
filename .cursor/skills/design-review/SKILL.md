---
name: design-review
description: Drafts a design and challenges it with fresh-context reviewers. Use before implementation of a new system or a material design change.
disable-model-invocation: true
---

# Design Review

## Elephant: draft with context

Read relevant code, docs/PRD.md and prior decisions. Resolve blocking requirements using decision-interview style questioning. Draft the design in docs/ARCHITECTURE.md (or a named design document for a larger change): goals, exclusions, requirement IDs, alternatives, interfaces, data flow, trust boundaries, failure/recovery behavior, rollout/rollback, risks and verification. Put essential assumptions in the document so a reviewer needs no chat history.

## Goldfish: review without the conversation

Start at least two new, read-only reviewer agents with no inherited conversation, author summary or prior findings. Give each the design path, requirement paths, relevant source references, repository constraints and a bounded question:

- Requirements reviewer: which promises, terms, edge cases or acceptance criteria cannot be understood or verified from these documents?
- Technical reviewer: which interface, data, security, failure or rollout assumptions conflict with the referenced code or make the design fail?

Use the verifier's goldfish mode where available. In a host with a context-inheritance option, disable it (for example, `fork_turns: none`); do not assume a new agent name guarantees isolation. Reviewers return findings with document/source locations, evidence, impact and open questions. They must not change files or approve the design.

If the host cannot create fresh contexts, report the goldfish gate as unverified and stop the review before claiming completion. A same-conversation self-review is not independent evidence. Reviewers may run sequentially in separate fresh contexts when concurrency is unavailable.

## Resolve and approve

Resolve findings in the document, recording accepted/rejected/deferred dispositions with reasons. Re-review affected sections with fresh context after material revisions. Present unresolved risks and the concrete implementation plan to the user. Only proceed after human approval; approval for unchanged scope remains valid, but a material design change needs renewed approval.

Output: design path/revision, reviewer scopes and isolation method, findings/dispositions, verification plan and approval status.
Exit: both fresh reviews completed, zero unresolved implementation blockers, and human approval recorded. Missing reviewer execution keeps the gate unverified.

Inspiration: [Google's Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model). Independently written workflow that does not bundle or reproduce the full plugin. See THIRD_PARTY.md.
