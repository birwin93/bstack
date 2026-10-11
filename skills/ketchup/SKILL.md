---
name: ketchup
description: Catch up on this chat since your previous human message, with verified status and decisions waiting on you. Use only when explicitly invoked as ketchup, /ketchup or $ketchup. Use recall for context across recent work and bro to simplify only the last reply.
metadata:
  compatibility: Uses available current-task history and read-only status tools. Falls back to visible messages with an explicit coverage gap.
---

# Ketchup

Give a concise catch-up in plain language. Run only on explicit invocation. This is a read-only report.

## Establish the window

Load **bstack-runtime**. Use available current-task history, or the visible conversation when full history is unavailable. Find the previous human message before this invocation. Agent replies, delegated results and scheduler notifications do not reset the window. Cover work since that message. If you cannot find it, state the visible window and the history gap; never imply full coverage.

Include older unresolved decisions that still need the human. Do not scan unrelated chats or workspaces.

## Check status

Read current evidence for relevant PRs, CI, jobs and delegated agents through available tools. Recheck volatile status before reporting it. If access is missing, label the last observed status and its time, or say it is unverified. Do not turn an old successful run into a current success claim.

Separate a human decision from work the agent can continue within existing authority. Continuing code work, retrying a recoverable check and collecting available evidence belong to the agent.

## Reply

Start with one sentence summarizing progress and the number of human items. If none, say so.

Lead with the most important results and what they mean. Give remaining agent work in one short line when useful. Use concrete task names and links; do not invent status labels.

For each human item, explain the decision, why it matters, realistic options and their costs, your recommendation, and what happens without an answer. Put an existing pending question or approval in context; do not invent a new approval gate. Finish with the next agent step when one is authorized.
