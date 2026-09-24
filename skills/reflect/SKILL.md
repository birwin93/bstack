---
name: reflect
description: Review the current task for durable workflow learnings and propose concrete skill or lint-rule changes. Use only when the user explicitly asks to reflect or capture lessons from the task.
metadata:
  compatibility: Uses bstack-runtime for current-task history and optional bounded review delegation. Makes no skill, lint, or tracker changes without explicit approval.
---

# Reflect

Mine the current conversation for durable learnings, then route them to the strongest practical enforcement in the relevant codebase.

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

Sanity-check the synthesizer's Accepted list against the relevant codebase. For a repeatable code practice, inspect existing lint rules, configuration, and how lint is run. Prefer an existing rule or a scoped new rule when it can detect the violation with useful signal. An Accepted lint proposal must name the practice, target codebase, proposed rule and diagnostic, enforcement scope, and a way to verify a violation and a valid case. Preserve the codebase's current lint rollout; do not silently add a rule to hooks, CI, or default linting. If the practice is already enforced, reject the duplicate. If structural enforcement is promising but cannot be made concrete from the available evidence, put it in Backlog with the next investigation step. Use skill prose for judgment that a rule cannot reliably check. See the **encode-lessons-in-structure** principle skill.

### 5. Apply

Before applying any Accepted change, present the synthesizer's full Accepted/Rejected/Backlog output to the user and wait for explicit approval. The user picks which subset to apply and may redirect routings. Skill and lint changes can affect future work across the codebase. Do not auto-apply.

Backlog items remain proposed until the user explicitly authorizes writing them to a tracker. Tracker submissions and skill edits are separate external actions.

For each approved Accepted item, follow the Routing field exactly:

- Trivial existing-skill edit (a one-line bullet, a tightened sentence, a stale fact corrected): parent does directly.
- Substantive existing-skill edit (a new section, a new pattern table, more than ~10 lines): hand to the host's available skill-authoring workflow and run its draft, test, and iterate loop.
- `tune description: <skill path>` (the skill exists but didn't trigger when it should have): hand to `create-skill` and run its description-optimization loop.
- `new skill via create-skill: <kebab-name>`: hand creation to `create-skill`. Do not invent the shape ad hoc.
- Lint rule or configuration: implement in the named codebase using its existing lint setup and the approved enforcement scope. Verify that a representative violation is caught, a valid case passes, and the relevant lint command runs.

If your environment ships a SKILL.md validator, run it on every touched skill before declaring done. Skip this step if it doesn't.

### 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<skill path>`. What changed, one line each.
- Lint rules applied: `<rule or config path>`. Practice enforced and scope, one line each.
- New skills created: `<skill path>`. One line each (rare).
- Backlog filed to the devex tracker: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.
