### Shipping a stack

**You own the release boundary. Verify first, then advance only the contiguous safe portion of a stack.** Use only when the operator explicitly authorizes the relevant publication or merge operations. Load **bstack-runtime** before any external write.

1. **Verify each PR independently.** Give one read-only verifier each PR. It must exercise the real surface through a control capability the runtime actually exposes and return `PASS`, `PASS+NOTES`, or `FAIL` at an exact head SHA. CI green and approving bots are supporting evidence, not the verdict. Post the verdict externally only when comment-writing is authorized; otherwise retain it in the local report.
2. **Find the contiguous verified run.** Walk upward from the lowest unmerged PR and stop at the first missing or failing verdict. A verified PR above that gap is not landable.
3. **Confirm verdict freshness.** Restacks rewrite SHAs. Compare patch-ids or re-verify whenever the content described by an older verdict may have changed.
4. **Respect the runtime authorization matrix.** Verification does not authorize commit, push, merge, deployment, or comments. Perform only the operations explicitly granted for the named stack.
5. **Use the repository's stack mechanism.** If the repository uses Graphite, inspect its current topology and queue state before arming merge-when-ready. Otherwise use the repository's native PR dependencies and merge controls. Do not infer state from a provider field whose semantics are unclear.
6. **Stop mutating once the queue drains.** Watch through the runtime's wait or scheduling capability. Report progress without restacking, retargeting, or speculative pushing into a live merge queue.
7. **Stop at the ceiling.** Report what landed, the next unverified PR, and the evidence needed to extend the run. Extending the ceiling requires another verification pass and the same authority check.

**Reply:** the verified ceiling, verdict and head SHA for each included PR, what landed, and why the next PR is excluded.
