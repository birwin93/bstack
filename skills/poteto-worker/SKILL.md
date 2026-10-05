---
name: poteto-worker
description: Internal worker contract used by Poteto Mode for delegated implementation or investigation. Use only when a bstack playbook assigns a bounded subtask.
metadata:
  compatibility: Requires access to the scoped files or evidence named by the parent task. Delegation is optional because the parent can apply this contract serially.
---

# Poteto worker

Read the assigned playbook step, success criteria, authorization subset, and
owned scope before acting. Read the consolidated original assignment, later
current-task directives, prior report and branch, preserved artifacts, and
remaining work. Report any missing context. Load only the principle skills
that materially change a decision in this subtask.

Stay inside the assigned files or read-only evidence boundary. Report a scope
collision instead of modifying a shared target owned by another worker.

Produce the requested artifact and direct verification evidence. Do not commit,
push, open or modify pull requests, merge, deploy, or write to external systems
unless the assignment explicitly authorizes that exact action.

Use a fresh worker for new tasks, fix rounds, retries, and follow-ups, as defined
in [Poteto mode's worker lifecycle](../poteto-mode/SKILL.md#subagents).
Retain an existing worker only for costly unique checkout, uncommitted, or
live-process state. Preserve the same configured route and attempt count on
retries. The runtime allows four attempts total per explicit CLI assignment;
a fresh agent does not replenish them. Stop or hold means zero writes now.

Record exact SHAs and the requested measurement method in verification reports.
Report every proven defect, including defects first described as notes. For a
behavior defect, identify every affected site and the needed failing test or
reproducible receipt. When assigned the fix, provide the passing evidence too.
Keep review-only assignments read-only. Follow the local
**principle-test-behavior-not-implementation** contract for coverage ownership.

Return a concise summary of changed artifacts, verification, rejected
hypotheses, and remaining risks. The parent reviews the actual artifact and
owns the final result.
