# 5. Build and clean

Route implementation through the matching Poteto Mode playbook. Make the observable behavior explicit before editing.

| Task | Playbook and proof |
| --- | --- |
| Bug | [Bug fix](../../skills/poteto-mode/playbooks/bug-fix.md): reproduce, trace the root cause, fix and repeat the real failing path. |
| Feature | [Feature](../../skills/poteto-mode/playbooks/feature.md): implement the accepted behavior and verify the user flow. |
| Refactor | [Refactoring](../../skills/poteto-mode/playbooks/refactoring.md): identify behavior to preserve and check affected consumers. |
| Performance | [Perf issue](../../skills/poteto-mode/playbooks/perf-issue.md): validate the baseline, profile the limiter and check each claimed result. |
| Iterative optimization | [Hillclimb](../../skills/poteto-mode/playbooks/hillclimb.md): freeze a trusted harness and evaluate bounded changes. |
| Live process problem | [Runtime forensics](../../skills/poteto-mode/playbooks/runtime-forensics.md): capture process evidence through available tools. |
| Existing trace | [Trace forensics](../../skills/poteto-mode/playbooks/trace-forensics.md): reconstruct the event from the captured artifact. |

For repeated steps, [build the lever](../../skills/principle-build-the-lever/SKILL.md): create the smallest reusable operation and prove it from a clean start before scaling it. [Subtract before adding](../../skills/principle-subtract-before-you-add/SKILL.md) keeps obsolete code and adapters from multiplying.

## Keep tests connected to behavior

[Tests](../../skills/principle-test-behavior-not-implementation/SKILL.md) need a distinct behavioral contract, a credible defect and an owner. Check user-visible output or independently expected effects. A regression test should fail on the pre-fix behavior for the intended reason. Negative and security cases can protect real contracts; their value is not decided by test shape alone.

Invoke [tdd](../../skills/tdd/SKILL.md) when you explicitly want a failing test first. It is not an automatic step for every reversible edit. Use the project's available language and framework skills when they matter to implementation.

## Clean what the change touches

[Comment sicko](../../skills/comment-sicko/SKILL.md) performs a read-only audit. [No comments](../../skills/no-comments/SKILL.md) applies accepted findings. [Technical writing](../../skills/technical-writing/SKILL.md) and [unslop](../../skills/unslop/SKILL.md) keep explanations useful. A missing optional tool is a reported limitation, not installation authority.

For performance, do not select a winner from one untuned run or a benchmark that counted errors as work. Use the [verification chapter](06-verify-and-ship.md) before making an adoption claim.

[Next: verify and ship](06-verify-and-ship.md)
