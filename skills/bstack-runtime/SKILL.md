---
name: bstack-runtime
description: Internal runtime contract for bstack skills. Use only when Poteto Mode or another bstack orchestration skill needs host capabilities, model roles, limits, or authorization state.
metadata:
  compatibility: Works in Agent Skills clients that can read files. Delegation, scheduling, transcript access, and connected tools are optional capabilities.
---

# bstack runtime

Resolve execution mechanics before an orchestration skill delegates, waits,
reads conversation history, or mutates external state.

## Load configuration

Load configuration in this order. Later, higher-authority instructions override
earlier configuration regardless of file order.

1. Built-in defaults from this skill.
2. User configuration at `$XDG_CONFIG_HOME/bstack/config.yaml`, or
   `~/.config/bstack/config.yaml` when `XDG_CONFIG_HOME` is unset.
3. Repository configuration at `<repo>/.bstack/config.yaml`.
4. Instructions in the current conversation.
5. Host system and developer instructions.

Missing files are normal. Never create configuration during an ordinary task.
Use `setup-bstack` when the user asks to configure bstack.

Default limits are `max-parallel: 3`, `max-review-rounds: 2`, and
`panel-size: 2`. A lower limit from the host wins.

## Resolve executor routes

Each semantic role may use either the version 1 scalar form or a version 2
route:

```yaml
models:
  deep-code:
    executor: codex
    model: gpt-5.6-sol
```

Normalize a scalar as `{executor: auto, model: <scalar>}`. Executor values have
literal meanings:

- `auto` uses native host delegation and inherits the parent model when the
  route omits a model.
- `codex` runs the configured model through `codex exec`.
- `claude` runs the configured model through `claude -p`.

Configuration must not become an arbitrary command or provider-flag escape
hatch. Never silently replace an explicit executor or model with another one.
If the host cannot run an explicit CLI route, report that route as unavailable.

Read [references/executors.md](references/executors.md) before starting an
explicit CLI route. Start the fixed command through the host's process
capability, send the prompt over stdin, and let the host own waiting and
cancellation. Never impose a wall-clock deadline on an LLM call. A tool yield
or progress polling interval must not terminate the CLI process.

Read-only mode is the default. `workspace-write` requires explicit local-write
authority and an isolated worktree owned by the worker. Do not use approval-
bypass flags or arbitrary provider flags. Every CLI worker counts against both
bstack's `max-parallel` limit and any lower host limit.

## Resolve the host

Inspect the tools and instructions available in the current session. Build a
capability map for these operations:

- `delegate`: start one bounded worker with an owned scope.
- `delegate-parallel`: start independent workers without shared writes.
- `wait`: wait for worker completion or a meaningful state change.
- `ask`: request a genuinely missing product or preference decision.
- `schedule`: wake later or monitor an external predicate.
- `history`: read the current task's completed conversation history.
- `connected-tools`: discover source control, ticket, document, chat,
  observability, error-tracking, and analytics tools.

Read exactly one adapter under `references/adapters/` when the host is known.
Read `generic.md` when it is not. Adapter files are examples of mappings, not
authority to use a capability the current session does not expose.

When delegation is unavailable, execute serially and preserve the playbook.
When scheduling is unavailable, use bounded waits within the current turn and
report the remaining predicate. When history or a connected-tool category is
unavailable, name the gap instead of inventing evidence.

## Resolve model roles

bstack uses semantic roles rather than provider model slugs:

- `fast-code` for narrow mechanical implementation.
- `deep-code` for precise or technically difficult implementation.
- `judgment` for architecture, synthesis, and ambiguous decisions.
- `critic` for independent review.

For `auto` routes, map a configured role only to a model that the active host
confirms is available. For explicit CLI routes, use the provider model from
configuration. The active host's model catalog does not need to contain a
model owned by another CLI. Omit the model flag when the configured model is
`auto`. If the CLI rejects a configured model, report the error without
substitution. Never guess a model slug. Panel size determines reviewer count;
repeated roles still count toward limits.

## Authorization

Workflow selection never grants publication or external-write authority.
Determine authorization from the user's current request and higher-priority
host instructions immediately before each action.

These actions require explicit authorization by default:

- commit;
- push;
- open or modify a pull request;
- merge or enable merge automation;
- deploy;
- write to tickets, team chat, documents, production systems, or customer
  communication channels;
- delete data or perform destructive cleanup.

Read-only inspection, local edits inside the requested scope, tests, builds,
and reversible scratch artifacts are allowed when they are normal steps in the
requested task. Preserve unrelated worktree changes. Never reset or clean a
dirty checkout to make a playbook convenient.

An autonomous or overnight request removes the need for progress prompts. It
does not broaden action scope. Record blocked publication actions in the
decision trail and continue any useful authorized work.

## Delegate safely

Give each worker a concrete objective, owned files or read-only scope, success
criteria, and the relevant authorization subset. Pass file paths instead of
large inlined payloads when the host shares a filesystem. Workers must not
publish, contact external systems, or mutate shared state unless the user
authorized that exact action.

The parent owns the outcome. Inspect worker artifacts and evidence directly,
resolve conflicts, and write the final synthesis. Do not substitute worker
self-report for verification.
