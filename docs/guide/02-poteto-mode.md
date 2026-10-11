# 2. Start a task

[Poteto Mode](../../skills/poteto-mode/SKILL.md) selects a playbook and applies principles at their relevant decisions. Give it an outcome it can verify.

| Fact | Example |
| --- | --- |
| Goal | Failed checkout requests retry once. |
| Done | The seeded local flow reaches success after one forced failure. |
| Proof | The UI shows success and persisted data contains one order. |
| Context | This repo and branch, local environment, linked failure report. |
| Constraints | Preserve the public API and idempotency key; publish only when authorized. |

```text
/poteto-mode fix this checkout retry failure in the local environment.
Done means the seeded flow passes after one forced timeout. Verify rendered
success and one persisted order. Keep the public API. Restate before editing.
```

A short narrow task needs less ceremony. For ambiguous work, restating catches the wrong target before edits. For an unfamiliar design, request a tutorial or experiment, then use [design](04-design.md) before planning production work.

## Steer the active work

Follow-ups such as "use the existing helper," "prove the persisted value," and "keep the API" constrain the current objective. Say explicitly when starting a different task. Use [ketchup](../../skills/ketchup/SKILL.md) for progress since your previous human message, including decisions still waiting on you.

The runtime checks available capabilities rather than assuming the host has delegation, a model catalog, background execution or cloud access. It can use serial work when delegation is unavailable. A failed explicit executor follows its recovery rule, without silently changing models or configuration.

## Isolate and preserve work

When the task needs an isolated checkout, use a worktree through supported host tools or Git. Inspect branch, base and status first. Preserve unrelated changes. Delegated writers need separate owned outputs; shared branch or file mutations must be serialized.

A remote or cloud environment is an explicit target, not a default you can infer from the word "agent." Prove its service connections and the app's real flow separately. Use the [worktree cleanup playbook](../../skills/poteto-mode/playbooks/worktree-cleanup.md) when the checkout is no longer needed.

A host may support persistent instructions; another may require `/poteto-mode` at the start of every new task. Use only the persistence the current host documents.

[Next: understand](03-understand.md)
