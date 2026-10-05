# bstack

`bstack` is a host-neutral port of Lauren Tan's
[`pstack`](https://github.com/cursor/plugins/tree/main/pstack) engineering
workflows. It keeps Poteto Mode, its playbooks, principles, and review skills,
while moving host-specific operations behind a small runtime contract.

The initial source snapshot came from `cursor/plugins` commit
`b9ddc83c32972210b8a94d389130713e8eed346e` and remains available under the
MIT license in [LICENSE](LICENSE).

## Goals

- Run the same playbooks in Codex, Cursor, and other Agent Skills clients.
- Resolve delegation, model, and reasoning choices from capabilities available
  in the current host instead of hardcoded tool names or model slugs.
- Keep repository edits separate from publication authority. Committing,
  pushing, opening pull requests, merging, deploying, and external writes
  require explicit authorization by default.
- Preserve progressive disclosure. Poteto Mode loads one matched playbook and
  only the supporting skills needed for that task.
- Bound parallelism and review rounds through configuration.

## Layout

- `skills/poteto-mode` is the main entry point.
- `skills/bstack-runtime` resolves the host adapter, configuration, model
  roles, reasoning levels, executor routes, and authorization policy.
- Other folders under `skills/` are callable Agent Skills used by playbooks.
  Use `how` for explanations, `why` for historical rationale, and `interrogate`
  for explicit adversarial reviews.
- `principle-attack-the-premise` guides investigation after repeated failed
  fixes. `principle-test-behavior-not-implementation` checks whether tests
  reject relevant defects.
- `.agents/skills/pstack-sync` is a repo-local maintainer skill for reviewing
  upstream pstack changes. It is not part of the installed bstack bundle.
- `bstack.example.yaml` documents optional configuration.
- `scripts/validate_skills.py` validates the portable skill bundle.

## Validate measurements and prevent repeated mistakes

[Benchmark checklist](skills/benchmark-checklist/SKILL.md) vets a measured
baseline or speedup before it guides a decision. It checks the limiter,
production tuning, physical limits, errors, completed work, repeated
interleaved trials, and end-to-end relevance. The
[explain-the-number principle](skills/principle-explain-the-number/SKILL.md)
requires evidence that a number means what the report claims. A requested
ballpark can use one labeled run, with errors and completed work still checked.

[Correct](skills/correct/SKILL.md) finds repeated mistakes in authorized
repository and current-task evidence. It prefers architecture, then types,
lint or CI, behavior tests, and finally docs. Each enforcement check must reject
a past defect and accept a legitimate case. A scoped rule table records the
owner and check. Local implementation authority carries forward. Publication,
security changes, and broad CI policy changes need their own authority.

[Architect](skills/architect/SKILL.md) screens designs for split ownership,
duplicate supported paths, importable internals, and hand-synced lists. The
preferred design makes a locally sensible edit safe across the repository.

## Verify autonomous work in rounds

[Autopilot-full](skills/poteto-mode/playbooks/autopilot-full.md) assigns an owner
to each independent change. Root verification starts at the code-ready head,
then repeats when a fix changes the patch. A clean verdict applies only to the
verified patch. Merge-ready also requires the playbook's review and CI gates
and explicit merge authority. [Autopilot-stack](skills/poteto-mode/playbooks/autopilot-stack.md)
uses verification rounds for a linear stack that the operator lands.

Both workflows retain the runtime's model roles, panel and review-round limits,
and authorization rules. Unavailable native delegation uses the supported
local fallback and reports missing independent review. Required independent
verification remains a gate. Explicit executor failures follow the runtime
recovery rule.
A workflow name or clean verdict never grants publication authority.

## Development

Run validation from the repository root:

```sh
python3 scripts/validate_skills.py
```

## Install locally

Link the bundle into `~/.agents/skills`:

```sh
./scripts/link-skills.sh
```

Pass a skills directory as an argument to use another location, including a
repository-local installation. The installer refuses to replace an existing skill with the
same name; resolve those conflicts deliberately, then rerun it. Symlinks keep a
development checkout current as this repository changes.

After installation, run [setup-bstack](skills/setup-bstack/SKILL.md) to choose
personal or repository settings for models, reasoning, and agent counts. Setup
shows the current roles and offers Keep current/default, Large, Medium, and
Small reasoning presets. No configuration is required for the defaults.

For lower usage, start with Small, which caps explicit role reasoning at medium
while preserving lower efforts, model choices, and inherited settings. Setup
checks supported efforts and shows which roles would actually change. It also
shows panel size and review rounds, which control repeated agent work. The
preset is not a token or subscription cap and does not change the parent chat
or independently configured jobs. See the
[budget rules](skills/setup-bstack/SKILL.md#choose-a-reasoning-budget).

## Route work to native agents or CLIs

The executor value selects the execution path. `auto` uses native host
delegation. `codex` runs `codex exec`, and `claude` runs `claude -p`. A route
can also select the provider model and reasoning level, so a repository can
use Codex for implementation and Claude for independent judgment:

```yaml
version: 2
models:
  fast-code: {executor: codex, model: gpt-5.6-luna, reasoning: high}
  deep-code: {executor: codex, model: gpt-5.6-sol, reasoning: high}
  judgment: {executor: claude, model: fable, reasoning: high}
  critic: {executor: claude, model: fable, reasoning: high}
```

Version 1 scalar entries normalize to `{executor: auto, model: <scalar>}`.
Explicit executors always run their named CLI. The runtime never silently
replaces an explicit executor, model, or reasoning level. Omit `reasoning` or
set it to `auto` to inherit the native parent session or the explicit CLI's
provider default.

Write the complete worker prompt to a private scratch file before launching.
Replace `/absolute/scratch/worker-prompt.txt` below with its path. Codex
read-only routes use this command shape:

```sh
codex exec \
  --ephemeral \
  --sandbox read-only \
  -C "$PWD" \
  --json \
  --model gpt-5.6-sol \
  --config 'model_reasoning_effort="high"' \
  - < /absolute/scratch/worker-prompt.txt
```

Claude read-only routes use this command shape:

```sh
claude -p \
  --strict-mcp-config \
  --permission-mode plan \
  --output-format json \
  --no-session-persistence \
  --model fable \
  --effort high < /absolute/scratch/worker-prompt.txt
```

Recoverable Claude or Codex failures get up to three automatic retries after
the initial attempt, four attempts total, using the same configured route.
Repair missing stdin and mistaken worker permissions within existing task
authority before retrying. Stop dependent work after exhaustion or a genuine
access, authentication, or policy blocker; preserve completed work and required
review coverage. See the runtime's
[recovery rule](skills/bstack-runtime/SKILL.md#recover-explicit-executor-failures).

The host sends prompts over stdin and owns waiting and cancellation. LLM calls
have no wall-clock deadline. A terminal yield or polling interval only controls
progress delivery. It must not terminate the process.

An implementation request authorizes its necessary local edits. Launch that
worker in its isolated worktree with Codex `workspace-write` or Claude
`acceptEdits`, carrying the existing authorization forward. The runtime's
[executor reference](skills/bstack-runtime/references/executors.md) covers
scoped tool allowances for commands that still require permission.
CLI processes count against both bstack's
`max-parallel` limit and any lower host limit.

Host adapters describe execution mechanics; shared skills must not name a
host-specific primitive directly.
