# 4. Design before planning

Choose the types, boundaries and interaction before committing to a sequence of implementation steps. A plan organizes known work; an unresolved design needs exploration.

Use [architect](../../skills/architect/SKILL.md) to inspect the domain and sketch types, signatures and module structure. Ask it to stop at the design checkpoint when you want to agree on the sketch before implementation. Otherwise it proceeds through implementation under the task's authority.

```text
/architect design the refund state and service boundary. Show public types,
error handling and the simplest caller. Stop at the design checkpoint.
```

Use [arena](../../skills/arena/SKILL.md) when several plausible designs need comparison. Independent candidates work from shared grounding into separate outputs; the picker uses a task-specific rubric. A read-only judge from a different model family scores them too. When no model from another family can run, the picker skips the judge and says so. Use [swarm](../../skills/swarm/SKILL.md) for independent subtasks whose results should be combined. These serve different needs; additional agents are useful only when the task benefits from their work.

Use [interrogate](../../skills/interrogate/SKILL.md) to challenge a design or diff. Adversaries try to break it with runs against the real code. A finding survives only when rerunning its command shows a failure that breaks the intent. The report lists what each adversary dropped and why, and applies nothing. Use [blast-radius](../../skills/blast-radius/SKILL.md) to identify affected callers and consumers before a boundary changes.

## Try the uncertain part

For a new interaction, use Poteto Mode's [prototype](../../skills/poteto-mode/playbooks/prototype.md) with fixture data. Show the interaction and learn from it before production implementation. For an unfamiliar technology, ask for a short tutorial and one concrete experiment first. When adapting an existing design, [redesign from first principles](../../skills/principle-redesign-from-first-principles/SKILL.md) prevents another special case from concealing a broken premise.

Once the shape is clear, sequence independently verifiable units. Poteto Mode's [planning playbook](../../skills/poteto-mode/playbooks/multi-phase-plan.md) ties each unit to proof and a checkpoint. [Figure it out](../../skills/figure-it-out/SKILL.md) can create an auditable playbook when no narrower one fits.

[Next: build and clean](05-build-and-clean.md)
