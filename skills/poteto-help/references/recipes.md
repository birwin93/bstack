# Starter prompts

Adapt the repository, environment and proof to your task. Invoke **poteto-mode** for engineering work, then name a specialist when useful. Playbook titles are routes inside Poteto Mode, not independent slash commands.

| Goal | Prompt |
| --- | --- |
| Check the goal first | `/in-your-own-words` after a long or messy request, before any work starts. |
| Deepen a prompt | `/sharpen write a migration guide for the v2 config format.` Read the rewrite, then send it. |
| Understand behavior | `/how explain how checkout retries preserve the idempotency key. Read only.` |
| Understand a decision | `/why why did we choose this timeout? Cite accessible records and label inference.` |
| Read a finished change | `/teach this branch's diff and the tradeoffs that matter.` |
| Rebuild topic context | `/recall the checkout retry work; say which history is unavailable.` |
| Catch up | `/ketchup` |
| Design before editing | `/architect design the retry state and public signatures; stop at the design checkpoint.` |
| Compare designs | `/arena compare three designs for this queue. Return the selected artifact and tradeoffs.` |
| Challenge a diff | `/interrogate this branch against main; report findings before applying any.` |
| Check consumers | `/blast-radius this response shape change; inspect affected callers.` |
| Fix a bug | `/poteto-mode reproduce this retry failure locally, fix the root cause and prove the corrected flow.` |
| Prototype | `/poteto-mode prototype this navigation with fixture data, then show the interaction before planning production work.` |
| Verify performance | `/benchmark-checklist vet these before/after runs before recommending either implementation.` |
| Build a harness | `/create-verification-skill add a seeded local flow that checks both rendered success and persisted data.` |
| Refresh proof | `/maintain-verification-skill reconcile this repo's harness and feature map with the current app.` |
| Prove a property | `/create-formal-verification-skill prove a job never runs twice at once in the lease module, even when retries overlap.` |
| Refresh a formal check | `/maintain-formal-verification-skill bring the lease model back in line with the code merged since its sync commit.` |
| Capture a workflow | `/automate-me turn this approved release workflow into a personal skill; include its proof and stop conditions.` |
| Capture lessons | `/reflect propose durable lessons from this task and their strongest practical enforcement.` |
| Prepare a PR | `/poteto-mode open a PR for the verified scoped change. Describe what changed, why and the proof. Leave merge and deployment for later.` |

For an autonomous run, give an observable finish condition and concrete authority:

```text
/poteto-mode finish the seeded refund flow in this isolated checkout.
You may edit code, run local checks, commit and open a draft PR for this change.
Stop for missing credentials or an unresolved product choice. Keep a decision
trail and report PR state separately from merge, deployment and live-flow proof.
```

A wake-up or recurring check needs a separate explicit request to a supported host scheduler. Do not imply a named loop command is portable across hosts.
