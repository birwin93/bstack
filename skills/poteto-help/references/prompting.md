# Prompting bstack

Give the agent five facts when they matter:

- Goal: the behavior you want.
- Done: the condition that ends the task.
- Proof: the observable result that can pass or fail.
- Context: repository, branch, environment, files and relevant history.
- Constraints: boundaries, tradeoffs and authority.

You do not need a form for every small edit. A narrow request with one clear result can be one sentence. For ambiguous or expensive work, start with "restate what you think I mean before editing." Use the restatement to catch the wrong target or success condition.

```text
/poteto-mode fix the retry loop in this repo. Done means a failed first
request retries once and preserves the idempotency key. Prove it against the
local endpoint with one forced failure. Keep the public API unchanged.
Restate the task before editing.
```

## Establish context before choosing a design

Use **recall** to rebuild a topic's recent history when the host exposes it. Use **how** for runtime behavior, **why** for rationale and **teach** for a change you need to understand. Missing history is a coverage gap, not permission to search every project.

For a new interaction, try a prototype or design checkpoint first. For unfamiliar technology, request a short tutorial and a concrete experiment. Then plan independently verifiable units using what the experiment established. A plan can coordinate known work; it should not conceal unresolved design decisions.

## Steer without rewriting the task

Short follow-ups can constrain the active task: "use the existing permission helper," "prove the persisted value," or "keep the public API." Explicitly name a new task when changing objectives. Ask for a safe checkpoint before pausing sustained work.

```text
Read this diff with /interrogate. Then explain which findings matter and why.
Do not apply changes yet.
```

A catch-up uses **ketchup**. A context reconstruction uses **recall**. A plain rewrite of the last reply uses **bro**.

## Grant concrete autonomous authority

Name a finish condition, environment, escape conditions and allowed actions. "Keep working" does not grant arbitrary publication, customer messages, deletion or deployment. A scheduled run also needs a supported host scheduler and explicit scheduling instruction.

```text
/poteto-mode work on this locally until the seeded checkout flow passes.
You may edit code and run the harness. Stop for a product decision or missing
credentials. Keep a decision trail. Do not publish changes.
```

Inspect a trusted harness before using it as the finish condition. Specify whether it may create fixtures, mutate persisted data or clean them up. Separate local checks, PR publication, merge, deployment and real-flow evidence in the report.
