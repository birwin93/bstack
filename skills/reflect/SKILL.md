---
name: reflect
description: Review the current task for durable workflow learnings and propose concrete skill changes. Use only when the user explicitly asks to reflect or capture lessons from the task.
metadata:
  compatibility: Uses bstack-runtime for current-task history and optional bounded review delegation. Makes no skill or tracker changes without explicit approval.
---

# Reflect

Mine the current conversation for durable learnings, then route them into skill edits.

## When to invoke

- The user said "reflect" or "/reflect".
- The user explicitly asks to capture a recipe, correction, or reusable workflow from the current task.

Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## Process

### 1. Locate the active transcript

Load **bstack-runtime** and request only the current task's completed history. If the host cannot provide it, write a tight digest from the visible conversation and pass that instead. Never scan unrelated projects or conversations.

### 2. Spawn three reviewers in parallel

Start up to three read-only reviewers through the runtime, bounded by `panel-size` and `max-parallel`. Give them access only to the current-task history and connected evidence needed to verify an existing citation. The parent applies approved edits.

| Lens | `model` | Prompt template |
|---|---|---|
| Judgment | your configured reflect-judgment model (default `judgment`) | `references/judgment-reviewer.md` |
| Tooling | your configured reflect-tooling model (default `deep-code`) | `references/tooling-reviewer.md` |
| Divergent | your configured reflect-judgment model (default `judgment`) | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the current-task history reference or digest where marked. Reviewers return findings through the host's worker result channel.

### 3. Synthesize

Start one read-only synthesizer through the runtime using the `judgment` role, or synthesize directly when delegation is unavailable. Use `references/synthesizer.md` with each reviewer's output. The synthesizer returns a structured Accepted / Rejected / Backlog list.

### 4. Structural enforcement check

Sanity-check the synthesizer's Accepted list. For any item that would be enforced more reliably by a lint rule, script, metadata flag, or runtime check, move it from Accepted to Backlog. The synthesizer already applies this criterion; this is a final pass before edits land. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted edit, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill changes affect every future agent in the org; do not auto-apply.

Backlog items remain proposed until the user explicitly authorizes writing them to a tracker. Tracker submissions and skill edits are separate external actions.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the host's available skill-authoring workflow and run its draft, test, and iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `create-skill` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `create-skill`. Do not invent the shape ad hoc.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
