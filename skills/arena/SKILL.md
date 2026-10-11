---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
metadata:
  compatibility: Uses bstack-runtime for bounded delegation and semantic model roles. Runs serially when parallel delegation is unavailable.
---

# Arena

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive 3-6 concrete gradeable criteria for success on *this* task. The rubric belongs to the picker in Phase D. Candidates see only the task.
3. Load **bstack-runtime**. Pick runners from the configured semantic roles and cap N at `max-parallel`. Default to the configured `panel-size`, using `judgment` and `deep-code` first. Repeating a role is valid when the work is generation-bound rather than judgment-sensitive.
4. Assign output paths. Each candidate writes to its own location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle skill.

## Phase B: Fan out

Start independent candidates through the runtime within its limits. Give each the task, grounding path, owned output path and **poteto-worker** contract. Require the artifact and a short rationale naming alternatives and rejections. Without parallel delegation, run serially with the same rubric.

If an explicit `claude` or `codex` candidate or judge route fails, apply the runtime's [recovery rule](../bstack-runtime/SKILL.md#recover-explicit-executor-failures), including up to three retries for recoverable errors. For an `auto` candidate dropout, proceed with N-1 and note the dropout in the synthesis record.

## Phase C: Cross-judge

After all Phase B candidates complete, choose the configured `critic` role, preferring an independently resolved model when the host exposes that distinction. Start one read-only judge through the runtime. It sees the rubric and candidates by path label, scores each criterion, and recommends a base with rationale. Run it in parallel with the parent's reading in Phase D when available, but never while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
