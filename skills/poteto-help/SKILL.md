---
name: poteto-help
description: Answer bstack setup, skill-selection and prompting questions, or suggest a concrete next prompt. Use only when explicitly invoked as poteto-help, /poteto-help or $poteto-help. Suggest poteto-mode when the user wants its full engineering workflow.
metadata:
  compatibility: Read-only guidance from available bstack skills, configuration and current-task context. No particular host, model catalog or delegation capability is required.
---

# Poteto help

Run only when explicitly invoked. Answer the question using current local bstack guidance. Do not make changes or start an engineering workflow from a help question. When the invocation explicitly asks you to perform the underlying task, load **poteto-mode** and the matching skill/playbook within that authority.

An ordinary engineering request without this invocation does not trigger help or implicitly opt the user into Poteto Mode. Follow the request and the host's applicable workflow instructions.

## Find the answer

Read the relevant local skill or guide before describing its behavior. Use the map below, then inspect the available skill catalog for routes not listed. Installed skills and host capabilities may differ from this repository.

| Need | Route |
| --- | --- |
| Setup, models, reasoning, usage or agent limits | [setup-bstack](../setup-bstack/SKILL.md), [setup guide](../../docs/guide/01-setup.md) |
| Start work or select a playbook | [poteto-mode](../poteto-mode/SKILL.md), [task prompts](../../docs/guide/02-poteto-mode.md) |
| Explain runtime behavior | [how](../how/SKILL.md) |
| Explain design intent or history | [why](../why/SKILL.md) |
| Teach a completed change | [teach](../teach/SKILL.md) |
| Rebuild recent context on a topic | [recall](../recall/SKILL.md) |
| Catch up in this chat | [ketchup](../ketchup/SKILL.md) |
| Simplify the last reply | [bro](../bro/SKILL.md) |
| Design types and boundaries before implementation | [architect](../architect/SKILL.md) |
| Compare independent candidate designs | [arena](../arena/SKILL.md) |
| Split independent work | [swarm](../swarm/SKILL.md) |
| Challenge a design or diff | [interrogate](../interrogate/SKILL.md) |
| Inspect affected consumers | [blast-radius](../blast-radius/SKILL.md) |
| Audit comments | [comment-sicko](../comment-sicko/SKILL.md) |
| Clean up accepted comment findings | [no-comments](../no-comments/SKILL.md) |
| Vet performance evidence | [benchmark-checklist](../benchmark-checklist/SKILL.md) |
| Request a failing test first | [tdd](../tdd/SKILL.md) |
| Create or maintain a project verification harness | [create-verification-skill](../create-verification-skill/SKILL.md), [maintain-verification-skill](../maintain-verification-skill/SKILL.md) |
| Capture a repeatable personal workflow | [automate-me](../automate-me/SKILL.md) |
| Propose durable lessons | [reflect](../reflect/SKILL.md) |
| Build an auditable plan for unfamiliar work | [figure-it-out](../figure-it-out/SKILL.md) |
| Keep a decision trail during sustained work | [show-me-your-work](../show-me-your-work/SKILL.md) |
| Improve prose | [technical-writing](../technical-writing/SKILL.md), [unslop](../unslop/SKILL.md) |

Principles are under `skills/principle-<name>/SKILL.md`; playbooks are under `skills/poteto-mode/playbooks/`. Read the exact file instead of inventing a slash command for a playbook. The [guide index](../../docs/guide/README.md) connects these routes into a workflow.

## Setup and usage questions

Load **bstack-runtime** and inspect available capabilities before naming a model, reasoning effort or supported command. Read personal and repository configuration when accessible. A missing personal file does not establish effective defaults: repository overrides and host inheritance still matter. Do not expose unrelated settings or secrets.

Explain the four semantic roles (`fast-code`, `deep-code`, `judgment`, `critic`). Saved explicit choices persist when host defaults change; rerunning setup preserves them. `auto` inherits on native routes and uses provider defaults on explicit CLI routes. Never silently substitute a configured executor or model.

[Setup](../setup-bstack/SKILL.md#choose-a-reasoning-budget) offers Keep current/default, Highest supported, Large, Medium and Small. Highest supported raises explicit efforts to each model/executor's confirmed maximum. Large/Medium/Small are ceilings that preserve lower efforts. Inherited efforts remain inherited. An unavailable catalog leaves changed efforts unresolved; it does not justify guessing. These presets do not cap tokens, spend or subscriptions or change the parent chat's settings.

Panel size and review rounds affect total calls. `max-parallel` controls concurrency; reducing it alone does not prove lower total usage. Host limits still apply. Recommend Small when lower usage matters, without promising savings for unchanged inherited roles.

When missing effective configuration matters to the user's question, offer setup once and explain the scope choices. A help request never authorizes creating configuration. Do not interrupt every later help answer with setup. If the question can be answered without configuration, answer it.

## Prompting and next steps

Read [prompting](references/prompting.md) for goals, done conditions, proof, context and constraints. Read [recipes](references/recipes.md) for concrete starter prompts. If intent is unclear, ask one short question or suggest the likely next prompt with a stated assumption.

Inspect existing project verification guidance before recommending a new harness. If none exists and the work needs real-flow proof, suggest **create-verification-skill**. Offer creation as a next prompt; do not create it from a guidance request.

Do not claim a persistent mode, scheduled wake-up or background run unless the current host supports it and the user has authorized that action. Hosts without persistent instructions can use an explicit `/poteto-mode` invocation at the start of each new task.

## Reply

Answer first. Explain the choice and give one copyable prompt when useful. Link the local skill or guide that supports the advice. Keep setup advice, proposed work and actions actually performed distinct. Help answers should be shorter than the workflow they explain.
