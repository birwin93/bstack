### Opening a PR

Run only when the user explicitly asks to open or prepare a pull request.
Drafting a title or description does not require publication. Before committing,
pushing, or opening the PR, load **bstack-runtime** and confirm authorization
for the needed action. Opening a pull request normally implies the necessary
commit and push for the scoped change, but never implies merge or deployment
authority.

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

**Description.** Write a briefing a reviewer can read in under a minute. Explain
why the change exists, what behavior changes, and how you verified it. Aim for
about 40 lines or fewer, while honoring the repository template and retaining
material evidence and limitations. Use `##` headings for the following sections in order, except where the repository template requires otherwise. Include only sections that carry information:

- `## Why` for the problem and approach in one to three short sentences. Omit
  SHA histories and rebase details.
- `## What changed` for one to three short bullets about the concrete changes.
  Name real symbols or paths when useful, including both sides of a rename.
- `## Scope` for boundaries, known gaps, or related work deliberately left out.
  Keep it separate from the change list and avoid a file-by-file essay.
- `## Tradeoffs` for alternatives a reviewer would otherwise ask about.
- `## Blast Radius` for affected consumers and risk in one to three sentences.
- `## Verification` for each real run path and outcome. For performance work,
  give the primary before and after measurement with units. Include uncertainty
  or methodology when it changes how the result should be interpreted.

Link detailed logs, experiment tables, and review artifacts instead of copying
them into the body. Attach screenshots or recordings when they prove a claim.
Never claim verification that was not run.

**PR tooling.** Prefer a built-in PR capability when the host provides it for
creation, editing, retargeting, or marking ready. Follow its supported schema.
Use the repository's forge tooling for operations it does not cover or when no
built-in capability is available. Tool availability never grants authority.

**Stacks.** Use Graphite or another stack tool only when the repository already
uses it and the user requested or accepted stacked delivery. Verify parentage
before submitting. Otherwise use the repository's normal branch workflow.

**Readiness.** Open ready for review unless the user asks for a draft or the
repository requires drafts. Re-read the created pull request and verify its
head SHA, base, title, body, and state before reporting success.

**Monitoring.** Opening a pull request does not authorize babysitting, merging,
or deployment. Return the URL to the parent and continue the assigned work.
An Autopilot-full or Autopilot-stack owner whose brief explicitly assigns the
babysit loop starts that loop after its code-ready report. It reports merge-ready
or STACK-READY under that playbook. Ordinary PR work still waits for a monitoring
request. Reused verification follows [Shipping's rule](shipping.md#verification-reuse);
opening or updating a PR does not make old evidence current.

**Reply:** pull request URL, head and base, commits published, verification,
and any remaining risk or follow-up.
