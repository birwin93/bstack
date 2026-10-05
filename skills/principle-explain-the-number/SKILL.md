---
name: principle-explain-the-number
description: Apply before trusting, reporting, or acting on a measured speedup, regression, throughput, latency, or eval result. Find the limiter and rule out errors, skipped work, untuned sides, and noise.
---

# Explain the number

A measured number is a claim about a system. Name what limits it and rule out
other explanations before trusting it. Failed requests, cached or skipped
work, untuned settings, and noise can all print plausible numbers.

Use profiles or counters to identify the limiting resource or code path and
map it to source. Check whether the load generator limits the result. A guess
from reading code does not establish a limiter.

For performance claims, run [benchmark-checklist](../benchmark-checklist/SKILL.md).
Validate errors, correct outputs, and completed work. Tune both sides for
production, interleave at least five trials per side, and report median and
range. Check physical limits and the component's share of end-to-end time.
Keep the command, revision, workload, trial count, spread, and limiter evidence
with the number. Label a claimed difference inconclusive when that evidence
is missing or invalid.

A user-requested ballpark may use one labeled run under the checklist's
exception. Errors, output correctness, and completed work still need checks.
A choice between options does not qualify.

For evals, check that every trial completed the intended task, that the gap
survives repeated trials across the relevant models, and that the scenarios
represent the intended use. Report incomplete runs and model coverage gaps.

[Prove it works](../principle-prove-it-works/SKILL.md) checks that an output is
real. This principle checks that a measurement supports the stated conclusion.
