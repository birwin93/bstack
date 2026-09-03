# Codex adapter

Resolve routes by executor:

- For `auto`, use the collaboration tools exposed by the current Codex session
  for delegation and waiting. Pass an explicit configured `reasoning` value as
  the native reasoning-effort override only when the selected model supports
  it; omit the override when `reasoning` is omitted or `auto`.
- For `codex`, start `codex exec` through the terminal execution tool.
- For `claude`, start `claude -p` through the terminal execution tool.

Read [../executors.md](../executors.md) for the fixed CLI arguments. Set the
terminal's working directory to the worker's repository or owned worktree.
Start the CLI with a PTY when the terminal tool needs one to keep stdin open.
Send the prompt through the terminal session's stdin, then send EOF. Never put
the prompt in the shell command.

If a terminal call yields before the CLI exits, keep its session identifier
and wait on the same session. Yield and polling durations only control when
Codex receives another progress update. They must not terminate the LLM call.
Cancel the terminal session only when the parent task or user cancels the
worker.

For Codex JSONL output, use the final completed agent message as the worker's
result. For Claude JSON output, use the top-level `result` text. Report a
nonzero exit or malformed result to the parent without substituting another
route.

Respect the session's concurrency limit and any rule that restricts when
subagents or terminal workers may be created. Count native and CLI workers
together.

Use Codex task, goal, automation, or heartbeat capabilities only when the
current session exposes them and the requested workflow needs them. Use current
thread history or memory tools only within their stated scope.

Model identifiers and supported reasoning levels come from the current host.
Apply that catalog only to native `auto` routes. Omit model or reasoning
overrides when the corresponding semantic-role value resolves to `auto`.
