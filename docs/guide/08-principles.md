# 8. Principles

Principles are short rules applied at the decision they protect. Poteto Mode loads the relevant ones; you can name one explicitly when steering a task. The current inventory lives under `skills/principle-*/SKILL.md`.

| Decision | Useful principles |
| --- | --- |
| Choose a design | [Foundational thinking](../../skills/principle-foundational-thinking/SKILL.md), [model the domain](../../skills/principle-model-the-domain/SKILL.md), [experience first](../../skills/principle-experience-first/SKILL.md). |
| Add or refactor logic | [Subtract before adding](../../skills/principle-subtract-before-you-add/SKILL.md), [laziness protocol](../../skills/principle-laziness-protocol/SKILL.md), [minimize reader load](../../skills/principle-minimize-reader-load/SKILL.md), [type system discipline](../../skills/principle-type-system-discipline/SKILL.md). |
| Debug a repeated failure | [Fix root causes](../../skills/principle-fix-root-causes/SKILL.md), [attack the premise](../../skills/principle-attack-the-premise/SKILL.md). |
| Scale repeated operations | [Build the lever](../../skills/principle-build-the-lever/SKILL.md), [make operations idempotent](../../skills/principle-make-operations-idempotent/SKILL.md), [sequence verifiable units](../../skills/principle-sequence-verifiable-units/SKILL.md). |
| Share state across workers | [Separate before serializing shared state](../../skills/principle-separate-before-serializing-shared-state/SKILL.md). |
| Decide whether a check proves a claim | [Prove it works](../../skills/principle-prove-it-works/SKILL.md), [test behavior](../../skills/principle-test-behavior-not-implementation/SKILL.md), [explain the number](../../skills/principle-explain-the-number/SKILL.md). |
| Preserve a lesson | [Encode lessons in structure](../../skills/principle-encode-lessons-in-structure/SKILL.md). |
| Continue authorized work | [Never block on the human](../../skills/principle-never-block-on-the-human/SKILL.md), [outcome oriented execution](../../skills/principle-outcome-oriented-execution/SKILL.md). |

For example, **build the lever** asks you to prove a reusable operation from a clean start before scaling it. **Explain the number** asks for the limiter and plausible alternatives to a measured win. **Encode lessons in structure** prefers types, constraints or useful lint rules to repeating a warning, while leaving judgment in prose when it cannot be mechanically checked.

A structural rule should reject a real violation, accept legitimate exceptions and survive an equivalent expression of the same behavior. Partial enforcement needs explicit coverage gaps. A test earns its place by protecting a credible behavioral defect, rather than repeating the implementation's constants.

[Next: make it yours](09-make-it-yours.md)
