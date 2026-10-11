---
name: reflect
description: Review the current task for durable workflow learnings and propose concrete skill or lint-rule changes. Use only when the user explicitly asks to reflect or capture lessons from the task.
metadata:
  compatibility: Uses bstack-runtime for current-task history and optional bounded review delegation. Makes no skill, lint, or tracker changes without explicit approval.
---

# Reflect

Mine this task for durable lessons and propose their strongest practical enforcement. Use only when the user asks to reflect or capture a reusable lesson. Skip trivial, unrelated or one-off lessons. Reject duplicate skill prose; an already-written rule can still need structural enforcement when the transcript shows a repeatable violation. Reject a lint candidate only when an effective mechanism already covers it.

## 1. Locate the active history

Load **bstack-runtime** for this task's completed history. Without that capability, pass a tight digest of the visible conversation. Never scan other projects or conversations.

## 2. Review

Start up to three read-only reviewers within `panel-size` and `max-parallel`, or apply the lenses serially when delegation is unavailable. Give each the current history and only the connected evidence needed to check a cited item. Explicit-route failures follow the runtime recovery rule.

| Lens | Semantic role | Prompt |
| --- | --- | --- |
| Judgment | `judgment` | `references/judgment-reviewer.md` |
| Tooling | `deep-code` | `references/tooling-reviewer.md` |
| Divergent | `judgment` | `references/divergent-reviewer.md` |

Use each template with the history reference or digest. The parent applies approved edits.

## 3. Synthesize

Give one read-only `judgment` synthesizer `references/synthesizer.md` and all findings, or synthesize directly when delegation is unavailable. Return Accepted / Rejected / Backlog.

## 4. Check structural enforcement

For repeatable code practices, inspect the codebase's lint rules, configuration and lint entry point. Prefer an existing or scoped new rule with useful signal. An Accepted lint proposal names the practice, codebase, rule, diagnostic, enforcement scope and checks for a violation and a valid case. Preserve the existing rollout; do not add hooks, CI or default lint enforcement silently.

Reject duplicate enforcement. Put promising but unproven mechanisms in Backlog with the next investigation step. Use skill prose for judgment a mechanism cannot check. See **encode-lessons-in-structure**.

## 5. Apply approved changes

Present the full Accepted / Rejected / Backlog output before applying edits. The user chooses the subset and routing. Do not auto-apply. File backlog items only with explicit tracker-write authorization.

Follow each approved row's routing:

- Trivial skill edit: the parent edits it.
- Substantive edit, description tuning or new skill: use the host's skill-authoring workflow and its draft/test/iterate loop.
- Lint rule/configuration: use the named codebase's setup and approved enforcement scope. Prove a violation fails, a valid case passes and the relevant lint command runs.

Run the available skill validator on touched skills.

## 6. Report

List applied skill/lint changes and their paths, new skills, authorized tracker items, and rejected findings with reasons. Keep proposed backlog distinct from filed items.
