# 1. Setup

Install the portable skills using the [repository instructions](../../README.md#install-locally). The link script has personal and project scopes. Choose the host and scope you intend; do not install a second copy just because a task's context is incomplete.

Invoke [setup-bstack](../../skills/setup-bstack/SKILL.md) when you want to configure models, reasoning or limits. Configuration is optional. Without explicit role choices, the runtime uses the host's available defaults; that does not guarantee a particular provider or effort.

## Inspect effective settings

Personal configuration lives at `$XDG_CONFIG_HOME/bstack/config.yaml`, or `~/.config/bstack/config.yaml` when that variable is unset. Project configuration lives at `<repo>/.bstack/config.yaml`. Repository settings override personal settings. Read both before concluding which role or limit applies.

A saved explicit model or effort stays explicit when host defaults change. Setup preserves existing routes, unrelated keys and unapproved migrations. A rerun is not a reset. If you want inheritance back, identify the specific override to change.

| Role | Purpose |
| --- | --- |
| `fast-code` | Narrow mechanical work. |
| `deep-code` | Difficult implementation. |
| `judgment` | Architecture and synthesis. |
| `critic` | Independent review. |

`auto` inherits on native routes and uses provider defaults on explicit CLI routes. Fixed `codex` and `claude` routes use their named CLI; failure does not permit a silent replacement. The runtime can retry recoverable failures within existing authority.

## Choose effort and fan-out

| Preset | Effect |
| --- | --- |
| Keep current/default | Preserve explicit efforts and inheritance. |
| Highest supported | Raise explicit efforts to each selected model/executor's confirmed maximum. |
| Large | Cap explicit effort at a supported value no higher than `xhigh`. |
| Medium | Cap it at a supported value no higher than `high`. |
| Small | Cap it at a supported value no higher than `medium`. |

Ceilings preserve lower efforts. All presets preserve inherited efforts unless you explicitly choose one for that role. Catalogs may differ across providers; unavailable catalogs leave changed values unresolved. These are not spending, token or subscription caps and do not change the parent chat's settings.

For lower usage, start with Small and inspect the resulting table. If every role remains inherited, there may be no change to effort. Panel size and review rounds affect total agent calls. `max-parallel` controls concurrency, so lowering it alone does not establish lower total usage. Stronger roles can suit harder tasks; choose from measured needs rather than promising a universal cost saving.

```text
/setup-bstack use personal scope and Small. Show repository overrides and
leave inherited roles inherited. Preserve my model and executor choices.
```

## Make the first proof concrete

Start a small task with a check that can pass or fail. Inspect the project's verification harness and feature map before trusting them. If they are absent, [create-verification-skill](../../skills/create-verification-skill/SKILL.md) can build an approved harness around a real flow. Installation and setup alone do not prove the app works.

[Next: start a task](02-poteto-mode.md)
