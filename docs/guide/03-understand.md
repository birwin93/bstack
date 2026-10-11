# 3. Understand before editing

An investigation can end with an answer. It does not imply implementation authority. Select the question you need answered:

| Question | Skill |
| --- | --- |
| What does this code do at runtime? | [how](../../skills/how/SKILL.md) |
| What led to this design? | [why](../../skills/why/SKILL.md) |
| How should I read this finished change? | [teach](../../skills/teach/SKILL.md) |
| What recent context exists on this topic? | [recall](../../skills/recall/SKILL.md) |
| What happened in this chat while I was away? | [ketchup](../../skills/ketchup/SKILL.md) |
| Can you simplify the last reply? | [bro](../../skills/bro/SKILL.md) |

```text
/how explain this refund path, including data writes and error boundaries.
Read only. Show where the observable result is produced.
```

```text
/why why did we choose this timeout? Search accessible history and connected
sources. Separate recorded evidence, inference and missing access.
```

For a subsystem, **how** can split exploration by angle and synthesize a mental model. For rationale, **why** builds a code anchor and searches accessible evidence categories. Both use bounded read-only delegation when supported, or serial work otherwise. A missing chat or observability connection is a coverage gap; it is not a reason to invent a rationale.

## Reconstruct context deliberately

Use recall before interpreting a report whose history you have lost. Limit it to the named topic and accessible task history. Do not imply access to every workspace or conversation. For a paused engineering task, Poteto Mode's [session pickup](../../skills/poteto-mode/playbooks/session-pickup.md) reconstructs branch, artifacts, current state and next work.

The [investigation playbook](../../skills/poteto-mode/playbooks/investigation.md) traces a concrete question to evidence. When the answer will guide a change, translate it into what to preserve, change, avoid and recheck. That makes the next [design](04-design.md) grounded in observed constraints.

[Next: design](04-design.md)
