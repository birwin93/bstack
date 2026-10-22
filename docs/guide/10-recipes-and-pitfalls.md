# 10. Recipes and pitfalls

Use these starters with your actual repository and environment. Each prompt says what to do and what evidence matters.

| Task | Starter |
| --- | --- |
| Check the goal first | `/in-your-own-words` |
| Deepen a prompt | `/sharpen write a migration guide for the v2 config format.` |
| Understand before editing | `/how explain this flow and its state transitions. Read only.` |
| Recover context | `/recall the refund work, then identify missing history before interpreting this report.` |
| Catch up | `/ketchup` |
| Design | `/architect sketch the domain types and simplest caller. Stop at the checkpoint.` |
| Compare designs | `/arena compare three designs using this goal and constraints.` |
| Challenge work | `/interrogate this diff against main. Report actionable findings before edits.` |
| Fix a bug | `/poteto-mode reproduce this seeded failure, fix the root cause and prove the real path.` |
| Learn an unfamiliar tool | `/poteto-mode explain the relevant model, run one bounded experiment, then design the integration.` |
| Prototype an interaction | `/poteto-mode prototype this with fixture data and show the interaction before production planning.` |
| Audit performance | `/benchmark-checklist vet these trials, including limiter, errors and completed work, before selecting a winner.` |
| Build proof | `/create-verification-skill add a seeded local flow that checks rendered success and stored state.` |
| Prove a property | `/create-formal-verification-skill the job lease and retry logic. A job must never run twice at once.` |
| Show behavior to its owner | `/statechart what the user sees when they edit a note offline.` |
| Prepare a PR | `/poteto-mode open a PR for this verified change. Explain what changed, why and the proof.` |
| Capture lessons | `/reflect propose the durable lessons and strongest practical enforcement from this task.` |
| Choose a route | `/poteto-help which skill fits this task, and what should I send?` |

## Common gaps

- A vague goal needs a pass/fail finish condition. Restate the task before a costly edit.
- A detailed plan can conceal an unsettled design. Prototype or experiment, decide the shape, then sequence work.
- A passing suite does not prove a UI or persisted-data claim. Observe the named real flow.
- A benchmark can measure errors, cached work or a saturated load generator. Check the seven questions before an adoption recommendation.
- More agents and higher reasoning do not guarantee better results. Read effective roles, limits and available catalogs; reduce calls when extra work has no purpose.
- Missing personal configuration does not imply defaults. Repository overrides and inheritance still apply.
- An old green check does not prove today's revision, deployment or live state. Recheck volatile evidence.
- A help question does not authorize edits. A review does not auto-apply findings. A PR does not authorize merge or deployment.
- A scheduler or loop command may be host-specific. Use supported capabilities and explicit scheduling authority.
- A lesson already stated clearly needs execution discipline. Improve weak placement or enforce a real mechanism before adding duplicate prose.

For longer runs, use the [autonomous chapter](07-overnight.md) to set finish conditions and escape boundaries. For concrete copyable prompts, see [help recipes](../../skills/poteto-help/references/recipes.md).

[Back to the guide](README.md)
