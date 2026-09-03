### Autopilot-stack

**You own the stack, never the landing. Build and verify a linear review chain, then hand it to the operator.** Use for "autopilot-stack", "stack them, don't ship", or an equivalent explicit request. Nothing auto-merges.

1. **Load the runtime and hold the boundary.** Resolve delegation, waiting, scheduling, control, and history through **bstack-runtime**. Record the authorized repository, branches, and publication operations. Merge and deploy remain forbidden.
2. **Give one owner each stack unit.** Each owner gets an isolated branch or worktree, a precise write scope, its intended parent, acceptance checks, and the **poteto-worker** contract. Owners build, test, exercise the real artifact, triage findings, run **no-comments**, and report a stack-ready head SHA plus a decision trail.
3. **Verify every exact head independently.** Use **swarm** for repository gates, live behavior, and a receipts-and-diff audit. Findings return to the owner. Nothing enters the chain without a clean verdict.
4. **Keep topology single-writer.** The coordinator alone appends verified units in the operator's order. Use Graphite only when the repository already uses it or the operator requested it. Otherwise build a base-branch chain. Rebase each child onto its parent's exact tip and set its PR base to the parent branch. Only the root PR targets trunk. Force-push only when explicitly authorized and protected by a current remote-SHA check.
5. **Absorb drift and re-verify what moved.** Record the base SHA, head SHA, and stable base-to-head patch-id with each verdict. Rebase the chain from bottom to top when trunk moves. An unchanged patch-id preserves the code verdict, but rewritten heads still need fresh mergeability and CI results. Send every changed patch through step 3 again.
6. **Audit through the runtime.** Use supported schedule or wake capabilities for periodic checks. Probe owners through runtime status and durable repository evidence. Replace genuinely stuck work without widening its scope.
7. **Deliver, never land.** Provide one ordered chain of verified PRs or branches for bottom-up review and merge. The operator lands it. A hold or stop sends every owner a zero-writes instruction immediately.

**Choosing between the autopilots.** Use Autopilot-full only when independent PRs and explicit merge authority are both present. Use Autopilot-stack when review is retained by the operator or the changes are coupled.

**Reply:** the chain root and tip, one verdict line per unit, and anything excluded with the reason.
