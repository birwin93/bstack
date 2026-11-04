### Autopilot-stack

**Autopilot-full without the merge.** Use for "autopilot-stack", "autopilot, don't merge", "stack them, don't ship", or an equivalent explicit request. Run [Autopilot-full](autopilot-full.md) with the changes below. Each audit re-reads both playbooks, and this one wins where they differ.

1. **Hold the no-merge boundary.** Record authority per Autopilot-full step 1. Merge, merge-when-ready, and deploy stay forbidden. Commit, push, and PR operations still need their own grants. Without them, deliver local branches and report the blocked actions.
2. **In place of step 5, stop at verified.** Stop when each PR is verified and green at its current head, then hand the PRs to the operator. After the handoff, nobody pushes without the operator's go. Every audit prompt names this file, so each audit sees the no-merge rule.
3. **Stack a PR only when it builds on another PR.** This is the one exception to step 2's rule against stacking owners. Base the PR on the other PR's branch in place of trunk, per **Stacks** in [Opening a PR](opening-a-pr.md). In place of step 3's rebase onto trunk, each owner rebases onto its parent PR's branch, and the stack root rebases onto trunk. A new head on the lower PR restacks the PRs above it. A PR keeps its verdict across a restack only under [Shipping's verification reuse rule](shipping.md#verification-reuse).

**Reply:** follow Autopilot-full's reply, and list each PR with its verdict in place of what merged.
