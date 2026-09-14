# Cursor adapter

Use Cursor's native delegation for `auto` routes. For explicit `codex` and
`claude` routes, read [../executors.md](../executors.md) and use a terminal
process capability that can supply stdin at launch or through a writable
session, wait without terminating the process, and cancel on request. Prefer
a prompt file redirected to stdin. For launch errors or unavailable
capabilities, follow the runtime's
[recovery rule](../../SKILL.md#recover-explicit-executor-failures).

Map background execution, waiting, model/reasoning selection, and recurring
wakeups to the operations exposed by the current Cursor session. Apply an
explicit `reasoning` value only when the native delegation capability accepts
that value for the selected model; omission or `auto` inherits the parent
session. Do not assume a command name, custom agent registration, or model
catalog from an older Cursor release.

Use the current workspace's transcript and connected-tool capabilities when
available. Never scan unrelated workspace histories.
