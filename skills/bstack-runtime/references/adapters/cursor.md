# Cursor adapter

Use Cursor's native delegation for `auto` routes. For explicit `codex` and
`claude` routes, read [../executors.md](../executors.md) and use a terminal
process capability that can send stdin, wait without terminating the process,
and cancel on request. If Cursor does not expose those capabilities, report the
explicit route as unavailable.

Map background execution, waiting, model selection, and recurring wakeups to
the operations exposed by the current Cursor session. Do not assume a command
name, custom agent registration, or model catalog from an older Cursor release.

Use the current workspace's transcript and connected-tool capabilities when
available. Never scan unrelated workspace histories.
