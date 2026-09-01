# Generic Agent Skills adapter

Use only capabilities described by the current client. If the client exposes no
subagents, run the playbook serially. If it exposes no scheduler, use bounded
waiting or hand back the unmet predicate. If it exposes no history API or
connected tools, state that limitation in the result.

Inherit the parent model unless the client provides an enumerable model catalog
and accepts model overrides for delegated work.
