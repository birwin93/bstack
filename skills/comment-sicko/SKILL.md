---
name: comment-sicko
description: Perform a read-only, adversarial comment audit over a named diff or file scope. Use through no-comments or when explicitly asked to identify narration, stale suppressions, and comments that should be encoded in code.
metadata:
  compatibility: Requires read access to the scoped diff or files. Makes no edits.
---

# Comment Sicko

Audit only the supplied scope. Never edit application code or comments.

Keep legal headers, public API contract documentation, issue or RFC links that
carry non-code context, and explanations of non-obvious behavior forced by an
external system that cannot be reshaped locally.

Flag narration, commented-out code, stale workaround stories, and comments
that merely restate code. Treat correctness and safety suppressions as review
findings when the underlying issue can be fixed. When a comment claims an
invariant, propose a type, test, lint, or runtime check that would enforce it.

Report touched files, proposed deletions, required code reshapes, uncertain
cases, and proven exceptions. The caller decides which findings to apply.
