---
name: principle-test-behavior-not-implementation
description: "Apply when you write, change, or keep a test. Call the code the way its users do and assert the result they observe against an independently expected value or observable effect. Check that a plausible defect makes the test fail."
---

# Test Behavior, Not Implementation

A test calls the code the way its users do and asserts the result they observe against an independently expected value or observable effect. A test that only asserts internal call counts or restates an implementation constant may miss the behavior that matters.

The check: before you keep a test, name a plausible defect in its subject and confirm the assertion would reject it. Returning `undefined` is one probe when that would violate the contract. If that return is valid, use a different defect. Rewrite or delete a test that cannot distinguish the intended behavior from a relevant defect.

**Why:** A test that cannot fail for a defect costs CI time and review attention and catches nothing. A constant pin also fails when someone edits the constant or the prompt it restates, so it prevents that edit.

**Five shapes to examine for weak defect detection:**

- **Weak or no assertion.** No behavioral check, or only broad shape checks such as `toBeDefined`, `toBeTruthy`, `not.toThrow`, `toBeInstanceOf`, `toBeGreaterThan(0)`.
- **Mock or absence only.** Only `toHaveBeenCalled`, `not.toHaveBeenCalled`, `toBeUndefined`, `toEqual([])`, `toHaveLength(0)`, `not.toBe(wrongValue)`.
- **Self-referential.** The expected value comes from the code under test: `expect(f(a)).toBe(f(a))`, `expect(parsed.url).toBe(buildUrl(...))`.
- **Constant pin.** The assertion restates a hand-maintained constant, config default, table row, or prompt string: `expect(LIMITS.maxTools).toBe(8)`, `expect(PROMPT).toContain("You are")`.
- **Fixture asserts fixture.** The assertion reads data the test built or a value computed in `beforeEach`, and the subject never runs inside the body.

These assertions are not automatically wrong. For example, `toBeDefined` rejects `undefined`, and absence can be the required behavior. Judge the complete test against the defect it should catch.

**The fix:** call the subject inside the test body with one concrete input and assert the literal output or the observable effect, `expect(slugify("Hello, World!")).toBe("hello-world")`. For an absence, use a contrasting input or deliberate defect to establish that the test distinguishes the intended absence from a missing implementation. For a constant, test the mechanism that reads it with one input instead of restating the value. For a mock, assert the payload it received or the state after the call, not that it was called. When no such assertion exists, delete the test.

**Keep** meaningful negative, error, side-effect, property, and public-contract tests. Also keep a test of a relation across a table's rows (a key present in two tables, a parent that exists), and a compile-time check in a `*.test-d.ts` file.
