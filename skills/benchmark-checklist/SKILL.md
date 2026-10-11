---
name: benchmark-checklist
description: Vet measured performance before reporting or acting on a speedup, regression, throughput, latency, or benchmark comparison. Check the limiter, tuning, physical limits, errors, repeatability, relevance, and completed work.
metadata:
  compatibility: Uses available local measurement tools. Discover macOS or Linux diagnostics and report missing evidence without installing tools automatically.
---

# Benchmark checklist

Vet a baseline before planning from it, and a result before reporting it. Read [explain-the-number](../principle-explain-the-number/SKILL.md). Answer each question with run evidence.

For a ballpark the user explicitly requested, one labeled run is enough. Still check errors, correct outputs and completed work in questions 4 and 7. Skip the other checks unless the result looks wrong. Choosing between options is not a ballpark.

## Prepare the measurement

Write the claim and unit. Read what the script times, counts and excludes. Record each side's revision, command, workload, build, environment and output artifact.

Discover the host and tools with `uname -s` and `command -v` when available. On macOS, options include `sysctl -n hw.logicalcpu`, `uptime`, `top`, `sample` and `iostat`. On Linux, discover `getconf _NPROCESSORS_ONLN`, `uptime`, `top`, `pidstat`, `perf` or `strace`. Check local help for flags; do not assume `nproc` exists or that flags match across hosts. Use an available runtime profiler. Report missing counters or permissions without installing tools or raising privileges implicitly.

Check load and competing processes. Do not stop another user's work. If load cannot be controlled, interleave the sides and disclose the noise.

## Validate the run

1. Name the limiter from profiles or counters and map it to source. Profile in a separate run to exclude diagnostic overhead. Check the load generator; if it saturates first, the result bounds the generator. Find the limiter before rejecting an optimization that did not move the number.
2. Tune both sides for production. Match data, versions, release builds, flags, batching, transactions, pools and cache conditions. A debug build, missing index or per-row commit makes a side untuned. Tune and rerun before choosing an implementation. If tuning is impossible, report inconclusive; renaming the result a comparison of today's defaults does not justify an adoption decision.
3. Check physical limits. Compare throughput with disk/network bandwidth and CPU cost with available cores. Time saved cannot exceed the changed component's original cost. Removing 10% of elapsed time allows at most about 1.11 times the speed. Investigate impossible results for caches, skipped work or bugs.
4. Count errors, non-success responses, retries and timeouts. Validate correct outputs, not just their presence. Add missing error counts before using the number; fast rejections and slow retries are not successful work.
5. Interleave at least five trials per side with the same warmup/cache policy. Report each median and range. A gap smaller than run variation is no measurable difference. For close calls, use the harness's statistical analysis or more trials.
6. Measure the end-to-end path a user waits on with realistic data and concurrency. Give the micro result's share of total time. A component using 1% of request time can save at most 1% of that time.
7. Count successful work inside the timed region. Confirm requests reached the server, rows were written, bytes were read and results were consumed. Await promises and exhaust generators. Check expected work counts and correct outputs so no-ops or discarded results cannot count as wins.

## Report the verdict

Report faster, slower, no measurable difference or inconclusive, with units, each median/range, trial count, limiter, errors, work counts and output evidence. Link raw trials and diagnostics. Label a requested ballpark as one run and name omitted checks.

A claimed difference is inconclusive when the limiter is unknown, a side is untuned or correct/completed work cannot be verified. Repair the measurement before recommending an option. Keep an authorized PR body to one primary number and link its evidence.

[Perf issue](../poteto-mode/playbooks/perf-issue.md) vets its baseline and each result. [Hillclimb](../poteto-mode/playbooks/hillclimb.md) vets the harness before freezing it, then checks errors and work counts at each keep-or-revert decision.
