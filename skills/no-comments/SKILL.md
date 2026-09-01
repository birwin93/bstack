---
name: no-comments
description: "Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints."
metadata:
  compatibility: Uses comment-sicko and optional bstack-runtime delegation. The reviewer is read-only; the caller applies accepted changes.
---

# No comments

Spawn Comment Sicko. Act on accepted findings.

Authoring agents defend comments. Defer to Comment Sicko's fresh perspective.

## Scope

Use the caller's files or diff. Otherwise use the current diff against the base branch, default `main`, including the working tree.

## Steps

1. Load **comment-sicko** and pass it the scope through a read-only worker resolved by **bstack-runtime**. When delegation is unavailable, apply the comment-sicko audit contract directly.
2. Inspect its report. Reject scope escapes, misstated reasons, and flags that treat proven exceptions as guilty. Audit missed scoped lint and TypeScript suppressions. Correctness or safety suppressions remain actionable. Before accepting thin `IMPORTANT` or `do not remove` findings, run **how** or **why** on the symbol. Rerun one rejected report with the failure named; after a second rejection, report the audit as inconclusive.
3. Fix trivial accepted flags directly by deleting a dead path, dropping a parameter, or using the real API. If any fix needs a shape, run `/architect` once for the accepted set and surrounding code. Stop at the sketch. Architect shapes. Step 4 implements.
4. Implement the smallest root-cause fix in scope. Remove every named workaround. If the root cause is out of scope, land the smallest in-scope fix and report the rest open. The **principle-fix-root-causes** and **principle-redesign-from-first-principles** skills guide intent only: fix real causes, redesign as if requirements always existed, never bolt on symptom guards. Neither authorizes widening the fence nor fixing instances outside it.
5. Constraint comments say `do not remove`, `do not change wording`, or `talk to X before changing`. Leave keeps about things we cannot change. Offer the cheapest in-scope type, runtime, test, or CI lint. Encoding outside the user's requested scope requires approval. If not approved, preserve the proven constraint comment and report the unenforced invariant.
6. Report the deletion count, restored comments, reruns, architect sketch, fixes, encoding offers, encodings, unenforced constraints, and other open work.
