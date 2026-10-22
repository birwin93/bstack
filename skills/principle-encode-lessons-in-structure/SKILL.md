---
name: principle-encode-lessons-in-structure
description: "Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text."
---

# Encode Lessons in Structure

Before you encode a lesson as a lint rule, metadata flag, runtime check, or script, test a representative violation, a legitimate exception, and an equivalent expression of the same mistake. Existing-code findings help measure signal. Zero findings alone do not disqualify a preventative rule. Encode the part the mechanism can reliably detect.

If the lesson needs judgment and cannot be encoded, make the instruction more prominent and add an example of the failure mode.

**Corollary:** If the fix is structural, only use the structural fix for the behavior it fully enforces. Keep guidance for judgment the mechanism cannot decide.
