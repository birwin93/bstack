# CLI executors

Explicit executor routes run provider CLIs directly. `executor: codex` runs
`codex exec`. `executor: claude` runs `claude -p`. Native host delegation is
reserved for `executor: auto`.

The host owns the process lifecycle. Connect the complete prompt to stdin when
starting the fixed command, wait until the process exits, and cancel only when
the parent task or user cancels the worker. Never impose a wall-clock deadline on an LLM call.
A host tool's yield or polling interval only controls progress delivery.

Write the worker's complete prompt to a private scratch file outside the
repository using the host's file-writing API. In these templates, replace
`/absolute/scratch/worker-prompt.txt` with that file's path and verify it is
nonempty before launching. The redirection supplies stdin at process start
and closes it at EOF, even when the host cannot send input after launch.

## Codex

Run a read-only worker with this argument template:

```sh
codex exec \
  --ephemeral \
  --sandbox read-only \
  -C /absolute/repository/path \
  --json \
  --model gpt-5.6-sol \
  --config 'model_reasoning_effort="high"' \
  - < /absolute/scratch/worker-prompt.txt
```

For an authorized writer, change the sandbox to `workspace-write` and set `-C`
to the worker's isolated worktree. Omit `--model` when the route's model is
`auto`. When `reasoning` is explicit, pass it as the fixed
`model_reasoning_effort` config override shown above; omit that override when
`reasoning` is omitted or `auto`. Do not pass approval-bypass flags.

Codex emits JSONL. Use the final completed agent message as the worker result.
Treat a nonzero exit, a missing final agent message, or a reported execution
error as a failed route. Follow the runtime's
[recovery rule](../SKILL.md#recover-explicit-executor-failures).

## Claude

Run a read-only worker from the repository directory with this argument
template:

```sh
claude -p \
  --strict-mcp-config \
  --permission-mode plan \
  --output-format json \
  --no-session-persistence \
  --model fable \
  --effort high < /absolute/scratch/worker-prompt.txt
```

For an authorized writer, run from the worker's isolated worktree and change
the permission mode to `acceptEdits`. Keep `--strict-mcp-config`.
An implementation request already authorizes its scoped local edits; do not
launch that worker in `plan` mode or ask the user to authorize those edits again.
Omit `--model` when the route's model is `auto`. Do not
pass `--effort` when `reasoning` is omitted or `auto`. Do not pass
permission-bypass flags.

`acceptEdits` does not approve every shell command. Pre-approve only the
commands needed by the authorized assignment with `--allowedTools`, for
example `--allowedTools 'Bash(npm run build)'` when that build is in scope.
Inspect the command or project script first. Do not grant unrestricted `Bash`
or override an existing deny. Check the installed CLI's help before using an
optional flag. If it supports `--permission-prompts none`, use it for an
unattended worker so an unresolved prompt returns a denial instead of waiting.
See Claude's [permission modes](https://code.claude.com/docs/en/permissions)
and [programmatic permissions](https://code.claude.com/docs/en/headless#auto-approve-tools).

If `--strict-mcp-config` leaves the worker without a needed connected tool,
have the parent collect authorized evidence and pass it as an artifact when
that satisfies the assignment. Do not enable all configured servers to repair
one missing capability.

Claude emits one JSON object. Use its top-level `result` text as the worker
result. Treat a nonzero exit, a missing `result`, or a provider error indicator
such as `is_error: true` as a failed route even if result text is present.
Inspect `permission_denials` and the worker's report for required steps left
undone; a denial is not itself a blocker if equivalent permitted work completed
the assignment and the artifacts verify it.
Follow the runtime's
[recovery rule](../SKILL.md#recover-explicit-executor-failures).

## Prompt and process handling

Pass the prompt separately from the command. Use an argv-capable process API
when the host exposes one. If the host only accepts a command string, quote the
fixed model, reasoning, and path values for that shell. Never interpolate the
prompt into the command. Prefer the scratch-file redirection shown above; only
the quoted file path belongs in the command. Keep that file available for the
bounded retries and remove it after the assignment ends.

An argv-capable API may instead supply stdin directly. Use a writable process
session only if the host guarantees stdin stays open until the prompt and EOF
arrive. Do not launch a print-mode CLI with empty or already-closed stdin and
assume a later terminal write will reach it.

Retain the process or session identifier when the host yields. Continue waiting
on that identifier until the process exits. On cancellation, ask the host to
stop the process and its children. Do not add a provider timeout, shell timeout,
or host execution deadline.

Use `codex --version` or `claude --version` when a short binary availability
check is useful. A timeout on that local check does not authorize a timeout on
the later LLM call.

Every CLI process counts against both bstack's `max-parallel` limit and any
lower host concurrency limit.
