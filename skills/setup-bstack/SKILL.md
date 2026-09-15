---
name: setup-bstack
description: Configure bstack model roles, reasoning levels, fan-out limits, and authorization defaults for a user or repository. Use when the user asks to set up bstack, change Poteto Mode models or reasoning, choose a reasoning budget, or tune its execution limits.
metadata:
  compatibility: Requires file access. Model and reasoning enumeration are optional. Unavailable catalogs fall back to auto.
---

# Setup bstack

Create or update a host-neutral bstack configuration. Do not configure a host's
global rules or invent model identifiers or reasoning levels. Role entries can
select a fixed executor (`codex`, `claude`, or `auto`), a confirmed provider
model, and a confirmed reasoning level.

## Choose scope

Use repository scope when the user wants shared project policy or project-
specific limits. Write `<repo>/.bstack/config.yaml`.

Use personal scope when the settings express the user's cross-repository
preferences. Write `$XDG_CONFIG_HOME/bstack/config.yaml`, or
`~/.config/bstack/config.yaml` when `XDG_CONFIG_HOME` is unset.

If scope is not stated, show the proposed personal path and repository path and
ask before writing. Do not infer a team-wide policy from a personal setup task.

## Detect available models and reasoning levels

Load **bstack-runtime**. Enumerate models and reasoning levels only when the
current host or selected provider CLI exposes a dependable catalog. Never guess
a provider slug or reasoning value. `auto` is always valid. For native routes
it inherits the parent model or reasoning level. For explicit CLI routes it
uses that provider's default.

Map these semantic roles:

- `fast-code` for narrow mechanical work.
- `deep-code` for difficult precise implementation.
- `judgment` for architecture and synthesis.
- `critic` for independent review.

For cross-CLI routing, write version 2 structured entries:

```yaml
version: 2
models:
  fast-code: {executor: codex, model: gpt-5.6-luna, reasoning: high}
  deep-code: {executor: codex, model: gpt-5.6-sol, reasoning: high}
  judgment: {executor: claude, model: fable, reasoning: high}
  critic: {executor: claude, model: fable, reasoning: high}
```

The version 1 scalar form remains valid and normalizes to
`{executor: auto, model: <scalar>}`. `auto` preserves native host inheritance.
An explicit `codex` route always runs `codex exec`. An explicit `claude` route
always runs `claude -p`. A version 2 route may omit `reasoning` or set it to
`auto` to preserve inheritance/default behavior. Never silently substitute a
different explicit executor, model, or reasoning level.

The supported CLI commands are fixed. Do not write arbitrary commands or
provider flags into configuration. `reasoning` is translated by the runtime to
the selected host or CLI's supported control. Inspection uses read-only mode.
Implementation uses workspace-write in an isolated worktree with the local
write authority already granted by the user's request. Delegation does not
require a second permission prompt. Follow the runtime's
[recovery rule](../bstack-runtime/SKILL.md#recover-explicit-executor-failures)
for launch errors and permission mismatches within that authority.

When a configured model or reasoning level is no longer available, propose
`auto` or a confirmed replacement. A panel's size, not repeated model names,
controls its fan-out.

## Choose a reasoning budget

Read the existing configuration and its `# reasoning-budget` comment before
proposing changes. Show the current per-role settings. A saved preset is a
record of the last setup choice; the role values remain authoritative.

Offer these choices through the runtime's `ask` capability unless the user
already chose one:

| Preset | Reasoning target |
| --- | --- |
| Keep current/default | Preserve every role's current effort or inheritance. |
| Large | At most `xhigh`. |
| Medium | At most `high`. |
| Small | At most `medium`. |

Recommend Small when the user prioritizes usage. These are reasoning ceilings
for configured roles, not token, spending, or subscription caps. They do not
change the parent chat's settings, scheduled jobs, or other tools' model choices.

Apply the selected ceiling to explicit reasoning values. Preserve lower
confirmed efforts, model identifiers, executors, and unrelated settings.
Resolve the highest supported effort at or below the ceiling for each selected
model/executor using its confirmed catalog. Never rewrite a model slug to encode
effort or use the native host's catalog for a different CLI. If the catalog is
unavailable or has no suitable value, leave that role unresolved in the preview
and ask for a confirmed choice before writing its changed reasoning value.

Omitted reasoning and `reasoning: auto` keep inheritance or provider defaults,
even with a fixed model. Missing roles and version 1 scalar roles stay inherited
unless the user explicitly chooses reasoning for them. If no role would change,
say so; do not claim that choosing Small reduced usage. Offer explicit reasoning
for inherited roles only when the model and supported effort can be confirmed.
For a newly configured explicit reasoning value, use the chosen ceiling unless
the user specifies a lower supported effort. Keep current/default never restores
an earlier higher effort. Raising reasoning requires an explicit user choice.

Show the resulting role table, including executor, model, reasoning, inherited
values, and unresolved choices. Show repository overrides that would mask a
personal change in the current repository. Apply an already-authorized choice
without asking again; ask only for missing choices.

When saving, replace the existing budget comment with one line such as
`# reasoning-budget: small (ceiling medium; inherited roles unchanged)`.
Write effective values in the existing per-role `reasoning` fields; do not add
a runtime configuration key. Keep current/default retains the previous comment
when it still describes the settings, otherwise label the result custom.

## Configure limits

Default to:

```yaml
limits:
  max-parallel: 3
  max-review-rounds: 2
  panel-size: 2
```

Preserve existing limits unless the user asks to change them. Host limits always
win when lower. Panel size and review rounds affect how many agent calls run;
max-parallel controls concurrency and is not a cap on total calls. Show these
limits alongside the reasoning choices when usage is the concern. Never present
lower concurrency alone as evidence of lower total usage.

## Configure authorization defaults

Keep publication and external writes explicit unless the user deliberately
chooses a narrower policy for a known environment:

```yaml
authorization:
  commit: explicit
  push: explicit
  open-pr: explicit
  merge: explicit
  deploy: explicit
  external-writes: explicit
```

Configuration cannot override host policy or grant authority absent from the
current request. Never offer an option that bypasses approval for destructive
actions, deployments, customer messages, or data deletion.

## Write idempotently

Read any existing configuration, preserve unrelated supported keys, and write
the complete resulting YAML once. Validate role names, positive integer
limits, authorization values, and configured reasoning levels supported by
each model/executor combination. Re-read the file and summarize the effective
scope, models, reasoning levels, limits, and publication policy.
