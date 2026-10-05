---
name: correct
description: Find repeated agent mistakes in authorized repository and current-task evidence, then prevent them with architecture, types, lint or CI, behavior tests, and finally docs. Use for /correct or a request to stop a recurring mistake.
metadata:
  compatibility: Uses local repository evidence and bstack-runtime for available current-task history and authorization. Works without history tools or delegation.
---

# Correct

Change the repository so the next contributor cannot repeat an observed
mistake. Assume an agent sees only the files it opens and copies the nearest
example. Make a change that looks right locally safe across the repository.

## Find recurring mistake classes

Load [bstack-runtime](../bstack-runtime/SKILL.md). Establish the requested
scope and existing authority. Inspect recent commits, reverts, supplied review
comments, repository instructions, and workaround comments in that scope.
Use only authorized current-repository and current-task evidence. Do not scan
private or unrelated chat history. If history access is unavailable, use local
evidence and report the gap.

Group two or more distinct occurrences into a mistake class. Cite each
occurrence. A written rule alone is not proof of a second incident. For a
single correction, fix the authorized defect and record a candidate rule
without claiming recurrence. Rank repeated classes by frequency and impact.

## Choose the strongest practical prevention

Try these levels in order. Record why a higher level does not fit before
moving down.

1. Change architecture. Give state one owner and each task one supported path. Make internals inaccessible. Derive repeated lists from one source. Migrate callers before deleting obsolete paths that agents might copy.
2. Enforce the invariant with types. Make the invalid state unrepresentable and derive types from the owning schema. Use the repository's existing schema library rather than adding one for a guard.
3. Add a scoped lint or CI check when types cannot enforce it. Make the error name the supported file, type, or function. For existing violations, reject newly introduced violations without hiding them in an unowned baseline.
4. Test observable behavior. Follow [test-behavior-not-implementation](../principle-test-behavior-not-implementation/SKILL.md) and its [audit workflow](../principle-test-behavior-not-implementation/references/audit.md). Name the contract, credible defect, and primary test owner. Preserve valid absence, side-effect, error, security, public API, and compile-time contracts. Returning nothing is only a defect probe when it violates that contract. Do not delete tests by assertion spelling or add duplicate coverage.
5. Write docs or agent rules for judgment that cannot be enforced. Give each rule a named owner and scoped location.

## Implement and prove enforcement

Carry the user's local implementation authority forward. Make normal scoped
edits without another approval prompt. Security or access changes, broad CI
policy changes, and uniquely destructive deletion require explicit approval
for those actions. Prepare a concrete proposal for any unauthorized action
and continue independent authorized work. Commits, publication, and external
writes still require the runtime's explicit authority. A correction request
does not authorize them.

Implement the most frequent classes as separate reviewable units. For every
new enforcement mechanism, reproduce a real past defect in a reversible
fixture and show the check fails for the intended reason. Then show it passes
both the corrected defect and a legitimate contrasting case. Use the same
check command locally and in CI where that CI change is authorized. If CI
wiring is outside scope, report it as pending rather than implying enforcement
is active there.

Attach exceptions to the offending code or the nearest supported exception
record. Require a reason, expiry date, named owner, and explicit human
approval. Never invent an approval or silently renew an expired exception.

## Keep a scoped rule table

Update the nearest in-scope agent instruction file or existing rule registry.
If that file is outside the assignment, include the proposed table in the
local report. Do not create a competing policy file. Record these columns:

| Rule and scope | Named owner | Evidence | Enforcement and command | Red and green proof | Exception and expiry |
| --- | --- | --- | --- | --- | --- |
| Concrete invariant and affected paths | Person or owning team/module | Two occurrence references | Check path and runnable command | Past defect rejected; valid case accepted | Approval reference or none |

On the next correction, check this table before adding a rule. If a known
class still recurs, repair enforcement at the highest practical level. Remove
redundant prose only after structural enforcement makes it unnecessary. Keep
real contracts and their primary coverage.

Report each class, evidence, chosen level, rejected higher levels, proof
commands and results, owners, and any pending approval or incomplete work.
