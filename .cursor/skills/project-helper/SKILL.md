---
name: project-helper
description: Guides starting a new project or improving the open project through one chat command. Use when the user invokes project-helper.
disable-model-invocation: true
---

<!-- skills-meta
use_when: Starting a new project or improving the open project from one entry point
do_not_use_when: You already know which single specialized workflow to run and do not need routing
needs_first: Open the target folder in Cursor
produces: Mode choice, bounded plan or assessment, selected procedure path
done_when: Approved plan ready or review-only findings delivered
typical_next: project-planning or the selected specialized workflow
weight: standard
-->


# Project Helper

## Start with the person

The user needs one entry point, not a list of skills. If their message does not identify a mode, ask only: **Would you like to start a new project or improve the project you have open?** Offer those two choices and wait. Do not inspect files or write anything before this choice. If the goal already identifies the mode, use it without asking again.

After that, ask one relevant question at a time. Explain decisions in plain language. Do not ask the user to invoke another slash command, copy configuration, install extra skill packs or understand agent roles. Continue the conversation after each answer; carry out the approved work and its checks instead of stopping at a plan.

Inspection, relevant questions and preparing a proposed plan are already authorized by this command; do not add approval gates merely to read a procedure or outline requirements. Obtain approval of the concrete implementation plan before edits. Respect narrower user requests such as review-only or no writes.

## Locate your procedures

Resolve paths relative to this skill's **actual attached source**, never relative to the open project by assumption. A user-level installation has adjacent `references/<name>.md` files. In this repository, workflows are at `../<name>/SKILL.md` and reviewer roles at `../../agents/<name>.md`. Read only the relevant files. If neither layout is present, report the missing resource; do not substitute an upstream skill by its slash name.

Workflow names: project-planning, decision-interview, design-review, test-first-change, hypothesis-debugging, trust-boundary-audit, release-check, prior-art. Reviewer names: architect, verifier. Installed reference files are snapshots of these local procedures.

Read the target project's own instructions before its source. Those instructions and the user's choices govern that project; the starter's historical requirements, CI and stack are not its requirements. When a bundled procedure refers to docs, use the target project's corresponding documents and checks. If they do not exist, propose suitable paths and checks during planning. Do not import template history or overwrite existing instructions.

## Start a new project

1. Ask what the person wants to build if not given. Confirm the target folder; default to the open folder only after checking its contents. Treat a folder containing files other than version-control/editor metadata as nonempty. If nonempty, describe the existing contents and ask whether to use this folder or choose a separate folder; wait for that informed decision before writing planning notes or application files. An earlier "build here" request made before inspection does not settle this choice. Never erase files or switch into improvement mode without an explicit decision from the user.
2. Unless the user skips research, run prior-art for the stated goal before locking a stack or implementation plan. Keep the memo capped; do not clone or copy a candidate without explicit approval of that candidate.
3. Use project-planning and, for unresolved decisions, decision-interview. Gather the audience, main journey, constraints and measurable success. Recommend a stack only after these are understood, using prior-art findings when present. Requirements/design notes may be drafted for review; do not install dependencies, scaffold application code or create external repositories before plan approval.
4. Use design-review for a new system or material design choice. Invoke fresh reviewers with the architect/verifier instructions. If the host has no named reviewer, give a fresh general reviewer the resolved role file and relevant procedure path. Report missing fresh-context capability as unverified; never claim self-review is independent.
5. Present a short concrete plan: what will be built, target folder, acceptance criteria, key risks and checks. Obtain approval. Existing approval covers routine work within the same scope.
6. After approval, create the project using its chosen conventions, implement in tested slices with test-first-change, debug failures with hypothesis-debugging, run applicable trust-boundary-audit checks and finish with release-check. Record exact check results and remaining limitations. Publishing, deployment and external messages need their own authorization.

## Improve the open project

1. Confirm the current workspace is the intended project. Read its instructions, relevant docs, source, test configuration, CI and working-tree state. Ask which problem or goal matters if it was not given; offer a general assessment if the user wants one.
2. Unless the user skips research, run prior-art when the goal is not clearly tiny (typo, docs-only, CI/config bump, or single-file fix). Keep the memo capped; do not clone or copy a candidate without explicit approval of that candidate.
3. Start with a read-only assessment scoped to that goal. Use design-review for design questions, trust-boundary-audit for a scoped security assessment, hypothesis-debugging for a reproducible failure, and release-check for readiness. Track evidence and unverified claims; distinguish defects against actual requirements from optional improvements and unanswered contract questions. Give a release-readiness verdict only when requested; missing starter-specific document names alone do not make another project defective. Do not change application files or run state-changing commands during assessment. Read-only commands can still require host permission.
4. Explain the main findings and propose a bounded improvement plan with measurable acceptance criteria and checks. Preserve the project's stack, conventions and uncommitted work. Do not replace its AGENTS.md, application CI or documentation with this starter's files.
5. Obtain approval before edits, then implement the approved scope using the relevant procedures, run its checks and verify the resulting diff. Report what changed, actual results and remaining limitations. Do not merge, push, publish or deploy unless authorized for that project.

## Finish

Give a short outcome and the next decision only when one is needed. Missing tools, reviewers or tests must stay visible. An initial assessment is complete without fixes when the user requested review only. No additional slash command is required at any stage.
