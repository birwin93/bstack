---
name: principle-test-behavior-not-implementation
description: "Apply when writing, changing, reviewing, or auditing tests. Require a distinct behavioral contract, a credible defect the test catches, and an owning boundary before adding or retaining coverage."
---

# Test behavior, not implementation

Call the code as its users do and assert an independently expected result or observable effect. Internal call counts and restated implementation constants may miss the behavior that matters.

## Before adding or keeping a test

Answer these questions from the complete test and production path:

1. What observable behavior, invariant, or independent contract does it protect?
2. What plausible defect would make it fail for the intended reason? Returning `undefined` is one probe when that violates the contract. Choose another defect when it does not.
3. What existing coverage would catch the same defect, if any? Give each contract one primary test owner at the strongest practical boundary. Another layer needs a distinct risk, such as transport or lifecycle behavior. Extend an existing case when it can cover the defect without a duplicate scenario.
4. Does the test require an export, flag, wrapper, or injection hook that no production caller needs? Exercise the real boundary instead of adding a production seam solely for the test.

If a question has no good answer, improve the test or use a more useful verification method. Do not add a unit test just to increase coverage. For a bug regression, show that the test fails on the pre-fix code for the intended reason and passes after the fix.

Design the test around that defect:

- Choose cases for distinct undesirable outcomes and meaningful boundaries, not a target test count. A smaller set of tests that catches real failures is more useful than many cases that repeat the same assertion.
- Move repeated or involved setup into shared test helpers organized by purpose. Let helpers create the needed state and return useful handles; keep the action and expected behavior visible in the test. Do not add a helper for a trivial one-off fixture.
- Spend assertions on what happens after the action. Do not repeatedly assert that fixtures contain the values the test just supplied. Check setup only when setup itself is under test or a failed prerequisite could make the behavior assertion pass for the wrong reason.

A test that cannot fail for a defect costs CI time and review attention. A constant pin can block a legitimate edit without showing whether behavior broke.

## Patterns to inspect

- **Weak or no assertion.** No behavioral check, or only broad shape checks such as `toBeDefined`, `toBeTruthy`, `not.toThrow`, `toBeInstanceOf`, `toBeGreaterThan(0)`.
- **Mock or absence only.** Only `toHaveBeenCalled`, `not.toHaveBeenCalled`, `toBeUndefined`, `toEqual([])`, `toHaveLength(0)`, `not.toBe(wrongValue)`.
- **Self-referential.** The expected value comes from the code under test: `expect(f(a)).toBe(f(a))`, `expect(parsed.url).toBe(buildUrl(...))`.
- **Constant pin.** The assertion restates a hand-maintained constant, config default, table row, or prompt string: `expect(LIMITS.maxTools).toBe(8)`, `expect(PROMPT).toContain("You are")`.
- **Fixture asserts fixture.** The assertion reads data the test built or a value computed in `beforeEach`, and the subject never runs inside the body.
- **Mock supplies the result.** The fixture or mock implements the behavior the assertion claims to check, so the production owner could be wrong without failing the test.
- **Duplicate proof.** Several tests replay the same contract at private helpers, providers, or layers without checking a distinct failure each.
- **Wrong-path negative.** A rejection passes because an unrelated guard fires before the intended path runs.

These patterns flag candidates, not automatic deletions. Absence, call order, defaults, exact bytes, source inspection, and narrow unit behavior may be the independent contract. Keep meaningful negative, error, side-effect, property, public API, migration, security, and compile-time tests when each catches a distinct failure. Judge the complete test against its contract and defect.

Call the subject with a concrete input and assert its independently expected output or effect, such as `expect(slugify("Hello, World!")).toBe("hello-world")`. For absence, add a contrasting input that distinguishes it from missing behavior. For a mock, check the payload or resulting state. For a constant, test its reader when the value itself is not the contract. Check ownership and overlap before deleting.

For a focused sweep of existing tests, read [the audit workflow](references/audit.md) before editing.
