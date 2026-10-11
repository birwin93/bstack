# 7. Autonomous runs

A useful unattended task has a trusted finish condition and concrete authority. Check the harness before making it the stopping rule. Set the environment, scope, allowed mutations, publication steps and conditions that require a human decision.

```text
/poteto-mode work until the seeded local refund flow passes in this checkout.
You may edit code, run local checks, commit and open a draft PR for this change.
Stop for missing credentials or an unresolved product decision. Keep a decision
trail. Report PR state separately from merge, deployment and live-flow proof.
```

## Choose the coordination shape

| Shape | Use |
| --- | --- |
| [Autonomous run](../../skills/poteto-mode/playbooks/autonomous-run.md) | One scoped outcome with an observable finish condition. |
| [Orchestrate](../../skills/poteto-mode/playbooks/orchestrate.md) | Coordinate task dependencies and owned outputs. |
| [Autopilot-full](../../skills/poteto-mode/playbooks/autopilot-full.md) | Carry an explicitly authorized full workflow through its assigned gates. |
| [Autopilot-stack](../../skills/poteto-mode/playbooks/autopilot-stack.md) | Coordinate accepted stacked delivery and its dependent branches. |

The host may lack delegation or persistent background execution. Apply the documented serial fallback when available and disclose unsupported capabilities. Scheduling a wake-up or recurring check requires a supported scheduler and an explicit request. Invoking an autonomous playbook does not create a schedule.

## Make progress reviewable

Use [show-me-your-work](../../skills/show-me-your-work/SKILL.md) to preserve goals, decisions, proof and open gaps in a reviewable artifact. Give long work independently verifiable units so an interruption leaves useful evidence. The runtime retries recoverable explicit-executor failures within existing authority and reports remaining failures without silently switching routes.

Use [pause safely](../../skills/poteto-mode/playbooks/pause-safely.md) when the user asks to pause, and [session pickup](../../skills/poteto-mode/playbooks/session-pickup.md) to resume from the checkpoint. A temporary uncertainty can be investigated; it does not justify asking the human to approve every reversible step.

Before handing the task back, recheck volatile status. Use [ketchup](../../skills/ketchup/SKILL.md) for a concise catch-up and the decisions still waiting on the human. A stop condition should name the missing decision and the concrete evidence needed to continue.

[Next: principles](08-principles.md)
