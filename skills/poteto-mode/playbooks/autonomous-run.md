### Autonomous run

**You own the exit condition. Define done, then drive to it without stopping.** For "going to bed" / "run until done" / "/loop until X".

1. State the exit condition as a checkable predicate before the first iteration (tests green, repro fixed, all N PRs merged, pixel-diff zero). A vague goal stalls; a predicate lets you stop.
2. Load **bstack-runtime** and pick its best available wake mechanism. An event to watch (CI, a merge, a ref advancing) gets an event-driven watcher when supported, with a time-based heartbeat as fallback. Without scheduling, use bounded waits in the current turn and preserve the unmet predicate for resumption.
3. Each iteration makes the smallest change the evidence justifies, verifies it against the predicate, commits if it advanced, discards changes that didn't help. Belt-and-suspenders that "might help" gets reverted, not left to ride.
   Sequence the work via the **sequence-verifiable-units** principle skill, verifying each unit before the next instead of batching checks at the end.
4. Mid-run discoveries stay bounded by the original request. Address blockers and directly related defects that are necessary to reach the predicate. Record out-of-scope improvements without implementing or publishing them. Use the runtime `ask` capability only for a genuine product or preference decision no experiment can settle. Keep the predicate as the main drive.
5. Checkpoint every iteration via the **show-me-your-work** skill, a row for what changed and whether the predicate moved. A run with no trail can't be audited or resumed.
6. Stop when the predicate is met. A plateau is not a stop, so keep going and pivot your approach to push past it. Surface a genuine dead end rather than spinning, and never relax the predicate to declare victory.

**Reply:** the exit condition, iterations run, what landed, what was discarded, final predicate state.
