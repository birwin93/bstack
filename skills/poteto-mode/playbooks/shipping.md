### Shipping a stack

**You own the release boundary. Verify first, then advance only the contiguous safe portion of a stack.** Use only when the operator explicitly authorizes the relevant publication or merge operations. Load **bstack-runtime** before any external write.

1. **Verify each PR independently.** Give one read-only verifier each PR. It must exercise the real surface through a control capability the runtime actually exposes and return `PASS`, `PASS+NOTES`, or `FAIL` at an exact head SHA. CI green and approving bots are supporting evidence, not the verdict. Post the verdict externally only when comment-writing is authorized. Otherwise retain it in the local report.
2. **Find the contiguous verified run.** Walk upward from the lowest unmerged PR and stop at the first missing or failing verdict. A verified PR above that gap is not landable. A proven defect labeled as a note remains a finding to fix and verify, not a passing exception.
3. **Confirm verdict freshness.** Apply the [verification reuse rule](#verification-reuse) before landing each PR and after every rebase or retarget. Keep the evidence with the verdict.
4. **Respect the runtime authorization matrix.** Verification does not authorize commit, push, merge, deployment, or comments. Perform only the operations explicitly granted for the named stack.
5. **Use the repository's stack mechanism.** If the repository uses Graphite or another stack-aware queue, inspect its current topology and queue state before arming anything. Otherwise treat the stack as a base-branch chain. Fetch current trunk, rebase the bottom verified branch onto that exact tip when needed, push only with authority, retarget only that PR to trunk, and repeat step 3. Do not infer state from a provider field whose semantics are unclear.
6. **Land through one ordering authority.** For a native base-branch chain, merge or arm merge-when-ready only for the current bottom PR. Do not arm descendants. Wait until the provider reports that PR merged, fetch trunk, and confirm the merged change is present. Remove it from the frozen bottom-to-top list, then inspect the new bottom PR's base, head, checks, mergeability, and patch-id before acting again. For a stack-aware queue, arm only the contiguous verified run and let that queue serialize the same order.
7. **Do not mutate around an active frontier.** Watch through the runtime's wait or scheduling capability. While a merge or merge-when-ready request is active, do not restack, retarget descendants, or push speculative changes into the chain. Diagnose a stalled requirement before changing topology.
8. **Stop at the ceiling.** Report what landed, the next unverified PR, and the evidence needed to extend the run. Extending the ceiling requires another verification pass and the same authority check.

**Reply:** the verified ceiling, verdict and head SHA for each included PR, what landed, and why the next PR is excluded.

#### Verification reuse

This is the canonical freshness rule for Shipping, both autopilots, and their plans. Record the verdict base and head SHAs, stable base-to-head patch-id, lane, build commands, toolchain, dependencies, configuration, feature flags, artifact paths and hashes, and the evidence each lane exercised.

An unchanged patch-id can preserve the code verdict. Re-run CI and mergeability at the current head and review changes in the base, runtime inputs, and configuration. Matching patch-ids do not excuse changed security behavior, data behavior, runtime output, feature flags, or build configuration. Those changes invalidate affected verification.

A changed patch normally requires fresh verification. Consider lane-specific reuse only when the actual changes are limited to tests, documentation, or lint and cannot affect runtime behavior. Judge content and its consumers, not file extensions. Documentation can generate runtime assets, and lint or test configuration can affect builds.

For each potentially reusable lane, build the actual artifacts it exercised twice at the verdict SHA and once at the current SHA. Keep comparable environments and retain all three outputs and exact SHA, build, and configuration evidence. Enumerate every difference, including its files, and judge it with concrete evidence. Repetition across the two verdict builds identifies variability; it does not prove harmless noise. Allow only proven non-runtime noise or a proven embedded commit identifier with no runtime effect. Any runtime-relevant or unexplained difference, or any feature-flag or build-configuration difference, requires re-verification. Security and data behavior changes also invalidate reuse even if the build outputs match.

Preserve only the eligible lane results after that proof. Run tests, review the change, and check CI and mergeability fresh at the current head. Never reuse dev-server or other no-build lane results. Re-run those lanes for current live or performance verification even when an unchanged patch-id preserves the code verdict. Also re-run any lane whose actual output or build evidence is missing. Record each reuse decision and its evidence rather than claiming the whole verdict survives.
