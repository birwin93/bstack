---
name: ketchup
description: Catch up on this chat since your previous human message, with verified status and decisions waiting on you. Use only when explicitly invoked as ketchup, /ketchup or $ketchup. Use recall for context across recent work and bro to simplify only the last reply.
metadata:
  compatibility: Uses available current-task history and read-only status tools. Falls back to visible messages with an explicit coverage gap.
---

# Ketchup

Catch the human up on what changed in this chat since their previous message. Help them understand each change, not only where it stands. Then lay out every call waiting on them so they can make it from the reply alone. Run only on explicit invocation. This is a read-only report.

Use the voice of **bro** without its restating task. Write plain words and short sentences with no jargon, like one person catching up another. Say what changed for the human, not how you did it. Say "the tests pass", not "CI is green". Leave out hashes, file paths, commands, build numbers and test counts unless the human needs one to act. Call each PR, branch or agent by a name the human would know, not by a label you invented. If a fact needs context to make sense, give the context or leave the fact out.

## Establish the window

Load **bstack-runtime**. Use available current-task history, or the visible conversation when full history is unavailable. Find the previous human message before this invocation. Agent replies, delegated results and scheduler notifications do not reset the window. Cover work since that message. If you cannot find it, state the visible window and the history gap; never imply full coverage.

Include older unresolved decisions that still need the human. Do not scan unrelated chats or workspaces.

## Check status

Keep the turn read-only. Make visuals only from what you already have. Do not change code, start an app or a job, or post anything.

Read current evidence for relevant PRs, CI, jobs and delegated agents through available tools. Recheck volatile status before reporting it. If access is missing, label the last observed status and its time, or say it is unverified. Do not turn an old successful run into a current success claim. Check each number you will show against the facts it comes from, and say so when you correct one.

An action item is a call or step only the human can take. Examples are a product choice, an approval, an irreversible action, or access you lack. Continuing code work, retrying a recoverable check and collecting available evidence belong to the agent, so they are not action items. Never make up a call to fill the reply. A step the human did not ask for and the work does not need is not an action item. The exception is an irreversible step waiting on the human, which gets one line and no visual.

One call can cover many items, such as each PR in a set awaiting merge. For each item, collect its link, what it changes for users, the evidence behind your pick, its risk, and your pick. Write "unknown" for a fact the call needs that you do not know. Leave out a link you do not have.

## Reply

Spend words on the calls, not on the story. Keep what happened under 100 words, not counting pictures, and shorter when less happened. Leave out work that changed nothing for the human. Give each action item about 30 words. The reply grows with the number of items. Two items need well under 150 words in all, and thirty need far more. Never cut items or shrink them to stay under a word count. Do not give a count in place of a list, or a link in place of an item. A link can add depth, but the reply alone must be enough to decide.

Open with one short sentence that names what waits on the human, or says nothing does. The action items give the detail. If nothing happened and nothing waits on the human, say so and stop.

Then show what happened, pictures first. Embed the screenshots and videos the work produced, then any diagram that explains a change. Then give one short bullet per thing the human asked for. Say what came of it, and whether it is done, still running, failed, or not checked. Write each line the way you would say it out loud. Write "Search was slow from a missing index", not "Search review: done". Name any bug found and fixed on the way. Each line must stay true when read alone. Never mark something done that still waits on the human, and leave out anything the action items say. Under the summary, give at most three short lines that change what the human knows or must do. Then name in one line any remaining agent work.

Then list the action items. Ask the call the human owns, such as merge, approve or pick, and give your pick. A step you would take first goes in your pick. So does anything that must happen first, and anything that cannot be undone. Give the number or link of each PR, issue or agent a call is about, also in a call between options. Put an existing pending question or approval in context; do not invent a new approval gate.

Fit the shape to the call. A call about one item is one bullet. It holds the call, your pick, what it changes for users, the evidence behind your pick and its risk, with the item named once. When items share a call, write the call and your pick once. Then give each item its own bullet, riskiest first, with its link and name, what it changes for users, the evidence and its risk. Name an item's pick only where it differs from the call's. Give each item's risk even when it is low, such as "Low risk, only the colors change." Say what waiting costs only when it is more than a delay, such as a deadline or lost data.

For a call between options, give every option the work weighed. Give each one what it gets the human and what it costs, plus the current state when there is one. Those costs are the call's risk, so add no separate risk line. When the screenshots above show the options, write each option's gain and cost under its screenshot.

Finish with the next agent step when one is authorized.

## Visuals

A visual is a picture. It can be a screenshot, a video, a Mermaid diagram, a chart or a generated image. A Markdown table is not a visual, even with before and after columns.

Draw a picture when it is easier to grasp than sentences. Good subjects are how a design or system works, a PR stack with each PR's state, a before and after of a fix, or options side by side. Never draw a status list, a list of action items, or boxes with nothing connecting them. Never give a fact twice, in text or across visuals.

Keep each visual small enough to read at a glance. Use at most six boxes, with at most eight words in each. Write labels as plain words a person would say, not tags like "Tests: pass". A fact that needs a sentence belongs in the text, or nowhere.

Embed screenshots and videos inline when the change is visible, not only as links. If a visible change has none, mark its summary line "No screenshot yet" and say there what changed on screen. Draw diagrams and charts only from facts on hand. Use a Mermaid diagram for how things connect and a chart for numbers. Never invent a number, and never draw or generate a picture of a screen you did not capture. Link only artifacts that exist.
