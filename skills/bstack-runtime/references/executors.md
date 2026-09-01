# CLI executors

Explicit executor routes run provider CLIs directly. `executor: codex` runs
`codex exec`. `executor: claude` runs `claude -p`. Native host delegation is
reserved for `executor: auto`.

The host owns the process lifecycle. Start the fixed command, send the prompt
over stdin, wait until the process exits, and cancel only when the parent task
or user cancels the worker. Never impose a wall-clock deadline on an LLM call.
A host tool's yield or polling interval only controls progress delivery.

## Codex

Run a read-only worker with this argument template:

```sh
codex exec \
  --ephemeral \
  --sandbox read-only \
  -C /absolute/repository/path \
  --json \
  --model gpt-5.6-sol \
  -
```

For an authorized writer, change the sandbox to `workspace-write` and set `-C`
to the worker's isolated worktree. Omit `--model` when the route's model is
`auto`. Do not pass approval-bypass flags.

Codex emits JSONL. Use the final completed agent message as the worker result.
Treat a nonzero exit or a missing final agent message as a failed route.

## Claude

Run a read-only worker from the repository directory with this argument
template:

```sh
claude -p \
  --restricted \
  --strict-mcp-config \
  --permission-mode plan \
  --output-format json \
  --no-session-persistence \
  --model fable
```

For an authorized writer, run from the worker's isolated worktree and change
the permission mode to `acceptEdits`. Keep `--restricted` and
`--strict-mcp-config`. Omit `--model` when the route's model is `auto`. Do not
pass permission-bypass flags.

Claude emits one JSON object. Use its top-level `result` text as the worker
result. Treat a nonzero exit or a missing `result` as a failed route.

## Prompt and process handling

Pass the prompt separately from the command. Use an argv-capable process API
when the host exposes one. If the host only accepts a command string, quote the
fixed model and path values for that shell. Never interpolate the prompt into
the command. Send the prompt through stdin and close stdin after the final
byte.

Retain the process or session identifier when the host yields. Continue waiting
on that identifier until the process exits. On cancellation, ask the host to
stop the process and its children. Do not add a provider timeout, shell timeout,
or host execution deadline.

Use `codex --version` or `claude --version` when a short binary availability
check is useful. A timeout on that local check does not authorize a timeout on
the later LLM call.

Every CLI process counts against both bstack's `max-parallel` limit and any
lower host concurrency limit.
