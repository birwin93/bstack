---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration."
metadata:
  compatibility: Uses bstack-runtime for bounded delegation, waiting, and semantic model roles. Runs serially when delegation is unavailable.
---

# Swarm

Fan out N bounded workers. They may cover separate slices, race the same brief, or mix both. The parent waits, aggregates, and returns one report.

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Load **bstack-runtime**. Set N from the user or derive it from the shape, then cap active workers at `max-parallel` and queue any remainder.
4. Pick a semantic model role. Default to `fast-code`; for a model race, name each arm's role up front and resolve it through the runtime.
5. Give each worker its own writable output when it writes. Use a worktree, branch, or `/tmp/swarm-<slug>/worker-<n>/`.

## Phase B: Fan out

Start independent workers through the runtime's parallel delegation capability. Give each the **poteto-worker** contract, configured semantic role, and only the environment and tool access its slice needs. Run them serially when delegation is unavailable.

When a worker needs a non-default branch or environment, resolve it explicitly from current repository state. Do not require a push merely to make delegation convenient.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

Keep a compact result table, one-line evidenced issues, and explicit gaps or dropouts.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.
