---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
metadata:
  compatibility: Uses bstack-runtime for optional read-only delegation and semantic model roles. Can explore and explain serially.
---

# How

Explain how the code works at the level of an engineer onboarding onto the subsystem. Build a working mental model rather than annotating every source line.

Load **bstack-runtime** before choosing roles or delegating. Use read-only access and configured limits. When delegation is unavailable or disallowed, explore and explain serially. Explicit-route failures follow the runtime recovery rule.

## 1. Assess complexity

If scope is ambiguous, state your interpretation and explore. The user can redirect.

- Simple, such as one module or a narrow function question: one `judgment` explainer explores and explains in a pass, or do it directly. Use `references/explainer-prompt.md` without explorer findings, then go to step 4.
- Complex, such as a subsystem across files or services: go to step 2.

When in doubt, take the simple path.

## 2. Explore, complex only

Split the question into 2 to 4 distinct angles. Give each read-only `fast-code` explorer its angle, repository paths and `references/explorer-prompt.md`. Start independent explorers through the runtime within `max-parallel`, or explore the angles serially.

## 3. Synthesize, complex only

After every explorer returns, give one read-only `judgment` explainer `references/explainer-prompt.md` with all findings. Synthesize directly when delegation is unavailable.

## 4. Present

Present the explanation with light edits for clarity or conversation context. Do not substantially rewrite it. Use the applicable sections in `references/explainer-prompt.md`: Overview, Key Concepts, How It Works, Where Things Live, Gotchas.
