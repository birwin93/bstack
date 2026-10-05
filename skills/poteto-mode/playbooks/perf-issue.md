### Perf issue

**You own the measurement story. Plan, review, verify the numbers.** Tie every fix to a measurement, don't read source instead of measuring.

1. Capture a baseline trace via the matching control skill or available local measurement tools. Name the target. Vet the baseline, and each later number, with [benchmark-checklist](../../benchmark-checklist/SKILL.md).
2. Run **how** to ground hypotheses. Don't claim a performance ceiling without measuring it. Try the performance mantras in order, cheapest first:

   1. Don't do it.
   2. Do it, but don't do it again.
   3. Do it less.
   4. Do it later.
   5. Do it when they're not looking.
   6. Do it concurrently.
   7. Do it cheaper.

   Attempt a strategy only when the trace and architecture support it. When an earlier strategy meets the target with valid work and correct results, stop.
3. Plan the fix from the trace. If it crosses a function boundary, run **architect** first. Resolve implementation through **bstack-runtime**, using `deep-code` by default and its configured bounds. Use its serial fallback when native delegation is unavailable or disallowed. Explicit-route failures follow the runtime recovery rule. Review the diff. Capture a post-fix trace.
   Apply the **sequence-verifiable-units** principle skill, verifying each attempt before trying the next.
4. Parse and compare the artifacts. An inconclusive measurement or a measurement of the wrong workload is not a pass. Name the gap.
5. Cite the measurement in the final report and, when publication is authorized, in the PR.
6. Run **Opening a PR** only when the user authorized publication. Otherwise report the verified local improvement.

For sustained improvement against a metric, use [Hillclimb](hillclimb.md). It borrows the strategy order and keeps its own stop predicate.

**Reply:** baseline number, post-fix number, delta, artifact path.
