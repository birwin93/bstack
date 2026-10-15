# BillyBot adapter

You are in BillyBot when the session offers `run_subtask` (the owner of a task)
or `delegate_task` (BillyBot's main chat). BillyBot runs every bot through Pi on
Billy's subscriptions and shows each delegated worker to Billy as a subtask he
can open, so delegation always goes through BillyBot, never a CLI.

## Routes

Every route runs as a `run_subtask` call, including explicit `codex` and
`claude` routes. This is not a substitution: BillyBot runs the same model at the
same reasoning level, as a subtask it tracks and recovers.

- `executor: codex` → `provider: "openai-codex"`, `modelId` = the route's model.
- `executor: claude` → `provider: "anthropic"`, `modelId` = the route's model.
- `executor: auto` → leave out `provider` and `modelId`; the worker runs on your
  own model.
- `reasoning` → pass it as `reasoning`. Leave it out when the route omits it or
  says `auto`; the worker then reasons at BillyBot's default, high.

Give `botId` only when a configured specialist owns the area better than a
role's model. A `botId` subtask runs on that bot's own model, so do not use it
for a route that names a model. If BillyBot refuses a provider or model, report
the route as unavailable under the runtime's recovery rule; never pick another.

## Operations

- `delegate`: one `run_subtask` call with a title, a description and a
  complete prompt. The worker starts from nothing: give it the objective, owned
  files or a read-only scope, the success criteria and file paths to read.
- `delegate-parallel`: several `run_subtask` calls in one response. They run at
  the same time and the response continues when every one has ended. The
  lower of bstack's `max-parallel` and BillyBot's limit (eight subtasks under
  one owner) applies.
- `wait`: a `run_subtask` call returns the worker's final answer. With
  `background: true` it returns at once and the answer arrives later as a
  message; use that only for long work you can do other work beside.
- `ask`: `ask_billy`, for a decision only Billy can make.
- `schedule`: unavailable to task owners. Use bounded waits and report the
  remaining predicate.
- `history`: your conversation is the task's history, including earlier
  attempts and follow-ups. There is no transcript-reading tool.
- `connected-tools`: the terminal, including `gh` for GitHub.

## Workers

A subtask works on its own branch made from your current branch. Commit before
delegating a writer, and merge its branch after. For a read-only reviewer or
explorer, say in the prompt that it must change nothing; BillyBot has no
sandbox flag, so the instruction is the scope. A subtask cannot start
subtasks of its own, so a playbook's nested fan-out runs from you.

A subtask that ends `failed` or `stopped` is a failed worker attempt under the
runtime's recovery rule. Its answer says why.
