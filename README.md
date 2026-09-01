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
- Resolve delegation and model choices from capabilities available in the
  current host instead of hardcoded tool names or model slugs.
- Keep repository edits separate from publication authority. Committing,
  pushing, opening pull requests, merging, deploying, and external writes
  require explicit authorization by default.
- Preserve progressive disclosure. Poteto Mode loads one matched playbook and
  only the supporting skills needed for that task.
- Bound parallelism and review rounds through configuration.

## Layout

- `skills/poteto-mode` is the main entry point.
- `skills/bstack-runtime` resolves the host adapter, configuration, model
  roles, executor routes, and authorization policy.
- Other folders under `skills/` are callable Agent Skills used by playbooks.
- `bstack.example.yaml` documents optional configuration.
- `scripts/validate_skills.py` validates the portable skill bundle.

## Development

Run validation from the repository root:

```sh
python3 scripts/validate_skills.py
```

## Install locally

Link the bundle into any Agent Skills-compatible client by passing its skills
directory explicitly:

```sh
./scripts/link-skills.sh ~/.agents/skills
```

For a repository-local installation, pass that repository's supported skills
directory instead. The installer refuses to replace an existing skill with the
same name; resolve those conflicts deliberately, then rerun it. Symlinks keep a
development checkout current as this repository changes.

After installation, ask the client to run `setup-bstack` if you want personal
or repository model-role and fan-out configuration. No configuration is
required for the defaults.

## Route work to native agents or CLIs

The executor value selects the execution path. `auto` uses native host
delegation. `codex` runs `codex exec`, and `claude` runs `claude -p`. A route
also selects the provider model, so a repository can use Codex for
implementation and Claude for independent judgment:

```yaml
version: 2
models:
  fast-code: {executor: codex, model: gpt-5.6-luna}
  deep-code: {executor: codex, model: gpt-5.6-sol}
  judgment: {executor: claude, model: fable}
  critic: {executor: claude, model: fable}
```

Version 1 scalar entries normalize to `{executor: auto, model: <scalar>}`.
Explicit executors always run their named CLI. The runtime never silently
replaces an explicit executor or model.

Codex read-only routes use this command shape:

```sh
codex exec \
  --ephemeral \
  --sandbox read-only \
  -C "$PWD" \
  --json \
  --model gpt-5.6-sol \
  -
```

Claude read-only routes use this command shape:

```sh
claude -p \
  --restricted \
  --strict-mcp-config \
  --permission-mode plan \
  --output-format json \
  --no-session-persistence \
  --model fable
```

The host sends prompts over stdin and owns waiting and cancellation. LLM calls
have no wall-clock deadline. A terminal yield or polling interval only controls
progress delivery. It must not terminate the process.

`workspace-write` requires explicit local-write authority and an isolated
worktree owned by the worker. CLI processes count against both bstack's
`max-parallel` limit and any lower host limit.

Host adapters describe execution mechanics; shared skills must not name a
host-specific primitive directly.
