### Authoring or modifying a skill

**You own the skill's voice.**

1. Use the host's skill-authoring skill when available. Otherwise follow the Agent Skills specification directly and record the fallback.
2. Validate the skill: frontmatter has `name` and `description`, referenced files exist, cross-skill links resolve.
3. When workflow decisions change, exercise realistic scenarios covering the affected supported modes, such as no delegation, supplied evidence, or drafting without publication authority. Rerun a scenario after fixing a failure it exposed.
4. Run **Opening a PR** only when the user authorized publication. Otherwise leave the validated skill change local.

When in doubt, delete. Keep only prose that changes a decision. Tell it to do the thing and skip the reason. Explain only when the rule is confusing without one. Match tone to scope. Point at structural sources (types, READMEs, config) per the **encode-lessons-in-structure** principle skill. Delegate to other skills by path. Don't restate. A workflow you keep hitting but isn't captured → propose a new skill.

**Reply:** summary of the skill, key design decisions, validation notes.
