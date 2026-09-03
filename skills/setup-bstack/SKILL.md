---
name: setup-bstack
description: Configure bstack model roles, reasoning levels, fan-out limits, and authorization defaults for a user or repository. Use when the user asks to set up bstack, change Poteto Mode models or reasoning, or tune its execution limits.
metadata:
  compatibility: Requires file access. Model and reasoning enumeration are optional; unavailable catalogs fall back to auto.
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
it inherits the parent model or reasoning level; for explicit CLI routes it
uses that provider's default.

Map these semantic roles:

- `fast-code` for narrow mechanical work;
- `deep-code` for difficult precise implementation;
- `judgment` for architecture and synthesis;
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
the selected host or CLI's supported control. Read-only execution is the
default. Workspace-write execution requires explicit local-write authority and
an isolated worktree.

When a configured model or reasoning level is no longer available, propose
`auto` or a confirmed replacement. A panel's size, not repeated model names,
controls its fan-out.

## Configure limits

Default to:

```yaml
limits:
  max-parallel: 3
  max-review-rounds: 2
  panel-size: 2
```

Host limits always win when lower. Explain that increasing these values can
increase latency and model usage.

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
