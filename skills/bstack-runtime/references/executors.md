# CLI executors

`bstack_exec.py` is the fallback process boundary for hosts that cannot
delegate natively. It has a fixed registry: `codex` and `claude`. It accepts a
resolved role route, sends the prompt on standard input, and prints one bounded
JSON result. It does not parse bstack YAML.

Use `plan` to inspect the exact argv without running a model, `probe` to check
whether a binary is available, and `run` to execute a prompt:

```sh
python3 skills/bstack-runtime/scripts/bstack_exec.py plan \
  --executor codex --model gpt-5.6-luna --cwd /repo --access read-only
```

Read-only routes use Codex's ephemeral read-only sandbox or Claude's restricted
plan mode with strict MCP configuration. Claude keeps `--restricted` and
`--strict-mcp-config` for workspace-write too, changing only to
`--permission-mode acceptEdits`. Codex workspace-write uses its corresponding
sandbox mode. Workspace-write requires explicit local-write authority and an
isolated worktree. Do not pass provider bypass, approval, or arbitrary flag
options.

The normalized result includes status, exit code, final text, bounded provider
metadata, bounded stderr, output-cap indicators, and a structured error when
needed. It never includes the prompt or process environment.
