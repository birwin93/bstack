---
name: grill-me
description: Interview the user relentlessly, in rounds of numbered questions with recommended answers, until a plan, design or decision is fully settled. Use only when explicitly invoked as grill-me, /grill-me or $grill-me.
disable-model-invocation: true
---

# Grill Me

Interview the user relentlessly until you reach a shared understanding. Map the plan as a **design tree**: every decision branches into the decisions that hang off it.

## Work in rounds

The **frontier** is every decision whose prerequisites are already settled: the questions you can ask now without guessing at answers you haven't heard yet. Ask the whole frontier in one round. Number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like this:

```text
❓ **Q1** - **<question title>**: <question body, might be multiple paragraphs, including multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer. Keep numbering across rounds, so a later answer like "Q7 yes" stays unambiguous.

Each round of answers reshapes the tree. Settled decisions push the frontier outward and unblock the questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a later round.

If the user skips a question, ask it again next round. An unanswered question is not a yes.

## Facts are yours, decisions are theirs

Finding facts is your job, never the user's. When a frontier question needs a fact from the environment, such as files, code, tools or current state, look it up before asking. If the host can delegate, send the lookup to a helper through [bstack-runtime](../bstack-runtime/SKILL.md) and keep going: a running lookup is an unsettled prerequisite, so only the questions downstream of it wait. Ask the rest of the frontier now.

Decisions belong to the user. Put each one to them and wait.

## Finish

Start each round with a short list of what the previous round settled.

The session is done when the frontier is empty: every branch of the design tree visited and nothing left silently assumed. Then summarize every settled decision in one list. Do not act on the plan until the user confirms you have reached a shared understanding.

Adapted from Matt Pocock's [grill-me and grilling skills](https://github.com/mattpocock/skills) under the MIT license in [LICENSE](LICENSE).
