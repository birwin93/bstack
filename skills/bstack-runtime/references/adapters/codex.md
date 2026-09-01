# Codex adapter

Use the collaboration tools exposed by the current Codex session for
delegation and waiting. Respect the session's concurrency limit and any rule
that restricts when subagents may be created.

Use Codex task, goal, automation, or heartbeat capabilities only when the
current session exposes them and the requested workflow needs them. Use current
thread history or memory tools only within their stated scope.

Model identifiers and supported reasoning levels come from the current host.
Omit model overrides when a semantic role resolves to `auto`.
