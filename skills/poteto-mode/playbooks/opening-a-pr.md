### Opening a PR

Run only when the user explicitly asks to open or prepare a pull request. Load
**bstack-runtime** and confirm that `commit`, `push`, and `open-pr` are
authorized. Opening a pull request normally implies the necessary commit and
push for the scoped change, but never implies merge or deployment authority.

**Worktree.** Inspect the current branch, status, base, and remotes before
editing history. Preserve unrelated changes. When the checkout contains
unrelated work, create a fresh worktree from the exact intended base and move
only the scoped change. Never reset or clean a dirty checkout to satisfy this
playbook.

**Commits.** Build small ordered commits when the change naturally decomposes
into independently verifiable units. Do not split a cohesive change merely to
produce a stack. Amend only when the new change belongs to the same unit and
the branch is safe to rewrite.

**Cleanup and review.** Run **no-comments**, **technical-writing**, and
**unslop** where applicable. Optional host cleanup or verification skills may
be used when already available. A missing optional skill is a reported gap, not
permission to install another package or widen scope.

**Title.** Use the repository's convention. When none exists, use
`type(scope): imperative subject` with a concrete changed area.

**Description.** Include only sections that carry information:

- `## Why` for intent and approach.
- `## Scope` for changed behavior and explicit boundaries.
- `## Tradeoffs` for real choices.
- `## Blast Radius` for affected consumers and risk.
- `## Verification` for commands, surfaces, and outcomes.

Attach screenshots or recordings only when they prove a claim. Never claim
verification that was not run.

**Stacks.** Use Graphite or another stack tool only when the repository already
uses it and the user requested or accepted stacked delivery. Verify parentage
before submitting. Otherwise use the repository's normal branch workflow.

**Readiness.** Open ready for review unless the user asks for a draft or the
repository requires drafts. Re-read the created pull request and verify its
head SHA, base, title, body, and state before reporting success.

**Monitoring.** Opening a pull request does not authorize babysitting, merging,
or deployment. Run those playbooks only when requested.

**Reply:** pull request URL, head and base, commits published, verification,
and any remaining risk or follow-up.
