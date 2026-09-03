# Generic Agent Skills adapter

Use native delegation only for `auto` routes. For explicit `codex` and `claude`
routes, read [../executors.md](../executors.md). The client must expose a
process capability that can send stdin, wait without terminating the process,
and cancel on request. Otherwise report the explicit route as unavailable.

Use only capabilities described by the current client. If the client exposes
no subagents, run an `auto` route serially. If it exposes no scheduler, use
bounded waiting or hand back the unmet predicate. If it exposes no history API
or connected tools, state that limitation in the result.

Inherit the parent model and reasoning level unless the client provides an
enumerable catalog and accepts those overrides for delegated work. If a route
requests an explicit reasoning level that native delegation cannot apply,
report the route as unavailable instead of silently inheriting.
