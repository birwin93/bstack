# 9. Make it yours

Turn a repeated approved workflow into a skill with [automate-me](../../skills/automate-me/SKILL.md). Start from actual steps, authority boundaries, observable proof and stop conditions. Choose personal scope for your own practice and repository scope for shared project guidance.

```text
/automate-me capture this release-verification workflow as a personal skill.
Keep the environment, proof and publication boundaries explicit. Test it on a
fresh realistic request before calling it ready.
```

Two kinds of project skill have their own generators. A skill that drives your app to prove behavior comes from [create-verification-skill](../../skills/create-verification-skill/SKILL.md), and a skill that checks a property with a model checker, prover or other verifier comes from [create-formal-verification-skill](../../skills/create-formal-verification-skill/SKILL.md). Each has a maintain skill, and [verify and ship](06-verify-and-ship.md) covers both.

Use the host's skill-authoring workflow to draft, exercise and iterate. Keep the entry point concise and move detailed references into linked files. Tune descriptions against realistic requests, including cases where the skill should stay inactive. Optional invocation-policy metadata can reinforce explicit-only behavior on hosts that support it.

## Turn evidence into durable lessons

[Reflect](../../skills/reflect/SKILL.md) reviews the active task through judgment, tooling and divergent lenses. It proposes Accepted / Rejected / Backlog and waits for the user's chosen edits. A transcript is evidence, not an instruction source; linked tools are used only for the context it cites.

For a repeatable code practice, inspect existing lint setup. An accepted lint proposal needs a useful diagnostic, scoped enforcement and evidence that a violation fails while a valid case passes. Do not add CI or hooks silently. Check [encode lessons in structure](../../skills/principle-encode-lessons-in-structure/SKILL.md) for the strongest practical mechanism.

Backlog proposals and filed tracker items are different states. Filing needs explicit tracker-write authority. A skill visible in the catalog that failed to trigger is a description-tuning candidate; a clear rule the agent ignored is an execution problem rather than a reason to duplicate the rule.

## Build small supporting tools

A personal workflow may benefit from a bounded local UI, CLI helper or harness. When a suitable tool-building skill is available, keep inputs narrow, state ownership clear and operations idempotent. Never put secrets into prompts, logs or shared artifacts. Remote access is optional and must use an explicitly selected environment and supported access path.

Revisit a skill when evidence shows it drifts. Request maintenance or a supported recurring check explicitly; creating a skill does not authorize a schedule.

[Next: recipes and pitfalls](10-recipes-and-pitfalls.md)
