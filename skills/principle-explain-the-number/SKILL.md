---
name: principle-explain-the-number
description: Apply before measuring, and before trusting, reporting, or acting on a measured speedup, regression, throughput, latency, or eval result. Find the limiter and rule out errors, skipped work, untuned sides, and noise.
---

# Explain the number

- Write the decision before you run. Name the result that would change a decision, and the noise floor. Stop when the run-to-run spread is larger than the effect.
- Ask why the number is not twice as good. Name the limiting resource or code path from a profile or counter, map it to source and check the load generator. Reading code alone does not establish a limiter.
- Rule out other explanations with evidence: errors, incorrect output, cached/skipped work, code that never ran, untuned settings, noise and a component too small to matter end to end.
- Keep the command, revision, workload, trial count, spread and limiter evidence with the number in a linked artifact.

For performance, run [benchmark-checklist](../benchmark-checklist/SKILL.md). Tune both sides for production, interleave at least five trials per side, report median/range and check physical limits. Label a claimed difference inconclusive when its evidence is missing or invalid.

A user-requested ballpark may use one labeled run under the checklist's exception. Errors, correct outputs and completed work still need checks. Choosing between options does not qualify.

For evals, check that each trial did the task, the gap holds across trials and relevant models, and the scenarios matter. Report incomplete trials and model coverage gaps.

You skipped this when a run started without the result that would change a decision, or when the evidence behind a number has no run count, no spread, or no named limiter.

[Prove it works](../principle-prove-it-works/SKILL.md) checks that an output is real. This principle checks that a measurement supports its conclusion.
