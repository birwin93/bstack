---
name: benchmark-checklist
description: Vet measured performance before reporting or acting on a speedup, regression, throughput, latency, or benchmark comparison. Check the limiter, tuning, physical limits, errors, repeatability, relevance, and completed work.
metadata:
  compatibility: Uses available local measurement tools. Discover macOS or Linux diagnostics and report missing evidence without installing tools automatically.
---

# Benchmark checklist

Vet the claim before planning from a baseline or reporting a result. Read
[explain-the-number](../principle-explain-the-number/SKILL.md). Answer the
questions below with run evidence.

For a ballpark the user explicitly requested, one labeled run is enough.
Still check errors, output correctness, and completed work in questions 4 and
7. The other checks may be skipped unless the result looks wrong. Choosing
between implementations or configurations is not a ballpark.

## Prepare the measurement

Write the exact claim and unit you intend to report. Read the measurement
script. Identify what it times, counts, and excludes. Record the revision,
command, workload, build, environment, and output artifact for each side.

Discover the host and available tools before choosing diagnostics. Use
`uname -s` and `command -v` where a shell supports them. On macOS, available
options include `sysctl -n hw.logicalcpu`, `uptime`, `top`, `sample`, and
`iostat`. On Linux, discover `getconf _NPROCESSORS_ONLN`, `uptime`, `top`,
`pidstat`, `perf`, or `strace`. Check each tool's local help for supported
flags. Do not assume `nproc` exists or that macOS and Linux flags match.
Use an available runtime profiler where appropriate. Report missing counters
or permissions. Do not install tools or raise privileges implicitly.

Check machine load and competing processes. Do not stop another user's work.
If load cannot be controlled, interleave the sides and disclose the noise.

## Validate the run

1. Name the limiter. Use a separate diagnostic run so profiler overhead does not enter the reported timings. Map a measured hot path or counter to the source and resource that limits throughput or latency. Check the load generator too. If it saturates first, the number bounds the generator. Explain an unchanged result through the limiter before rejecting an optimization.
2. Tune every side for its intended production workload. Match data, versions, release builds, flags, batching, transactions, pools, and cache conditions. Debug builds, missing indexes, and per-row commits can dominate the result. Tune and rerun before selecting an implementation. If a side cannot be tuned, report the comparison as inconclusive. Renaming it a comparison of today's defaults does not justify an adoption recommendation.
3. Check physical limits. Compare bytes per second with disk and network bandwidth and CPU cost per operation with available cores. Time saved cannot exceed the original cost of the changed component. Removing 10% of elapsed time allows at most a speedup of about 1.11 times. Investigate impossible results for caches, skipped work, or bugs.
4. Count errors, non-success responses, retries, and timeouts. Validate output correctness, not just output presence. Fast rejections and slow retries must not masquerade as completed work. Add missing error counts before using the measurement.
5. Interleave at least five trials per side, such as A, B, A, B, through five runs of each. Apply the same warmup and cache policy to both. Report each side's median and range. A gap smaller than run-to-run variation is no measurable difference. Use the harness's statistical analysis or more trials for close calls.
6. Measure end-to-end relevance. Pair a microbenchmark with the path a user waits on at realistic data sizes and concurrency. State the changed component's share of elapsed time. A component using 1% of request time can save at most 1% of that time.
7. Count successful work inside the timed region. Confirm requests reached the server, rows were written, bytes were read, and results were consumed. Await promises and exhaust generators. Verify expected work counts and correct outputs so a no-op, timeout, or optimized-away result cannot count as a win.

## Report the verdict

Report faster, slower, no measurable difference, or inconclusive. Include the
unit, median and range for each side, trial count, measured limiter, errors,
work counts, and output validation evidence. Keep raw trials and diagnostics in
a linked local artifact. A requested ballpark must say it is one run and state
which checks were omitted.

Call a claimed difference inconclusive when the limiter is unknown, a side is
untuned, or correctness and completed work cannot be verified. Repair invalid
measurements before making a recommendation. Keep any authorized PR body to
one primary number with supporting evidence linked.

[Perf issue](../poteto-mode/playbooks/perf-issue.md) uses this checklist before
planning from a baseline and after each fix.
[Hillclimb](../poteto-mode/playbooks/hillclimb.md) vets the harness before
freezing it, then checks error and work counts on every keep-or-revert decision.
