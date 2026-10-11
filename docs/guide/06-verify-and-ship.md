# 6. Verify and ship

Choose proof for the actual claim. A local check, a PR, a merge, a deployment and a live user flow are separate observations.

## Verify the path that matters

Read the project's harness and feature map. Run the named environment and seeded flow. For a UI success claim, observe the rendered result; for a persisted-data claim, read the stored result. An HTTP success or passing unit suite may support the claim without proving the complete user flow. Poteto Mode's [visual parity](../../skills/poteto-mode/playbooks/visual-parity.md) compares the rendered interaction with its target when appearance matters.

[Create-verification-skill](../../skills/create-verification-skill/SKILL.md) builds a project-specific harness around a real flow. [Maintain-verification-skill](../../skills/maintain-verification-skill/SKILL.md) updates it when the app changes. Request maintenance when needed; do not silently schedule recurring work.

The harness should expose clear inputs, fixture ownership, environment selection, observable assertions and cleanup. Read what a command does before running it. A flag named `--dry-run` does not establish that every downstream operation is read-only. Destructive resets and shared or production data writes need the corresponding authority.

## Explain measurements

Run [benchmark-checklist](../../skills/benchmark-checklist/SKILL.md) for baseline and result evidence. Answer its seven questions: limiter, production tuning, physical limits, errors, repeated trials, end-to-end relevance and successful completed work. Interleave at least five trials per side and report median and range. Keep profiles separate from timed runs.

A user-requested ballpark can use one labeled run, but still checks errors, correct outputs and completed work. Choosing between options does not qualify. Unknown limiters, untuned sides or unverified work make a claimed difference inconclusive. A tiny microbenchmark component can have only a tiny end-to-end effect.

## Carry authorized work through release gates

Use [opening a PR](../../skills/poteto-mode/playbooks/opening-a-pr.md) when asked to prepare or publish one. Describe what changed, why and the real proof; link longer logs. Keep material uncertainty. Verify the remote head, base and state before reporting publication.

Use [shipping](../../skills/poteto-mode/playbooks/shipping.md) for an authorized delivery task and [babysit](../../skills/poteto-mode/playbooks/babysit.md) for requested monitoring. Opening a PR does not grant merge or deployment authority. Reused proof must still match the relevant revision and environment; volatile state needs a fresh read.

Report what passed, what was published and what remains unproved. A failed or unavailable real flow stays a gap even if the change has merged.

[Next: autonomous runs](07-overnight.md)
