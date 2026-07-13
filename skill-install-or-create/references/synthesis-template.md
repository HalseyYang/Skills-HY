# Synthesis Template

Use this structure when generating a local replacement skill:

```markdown
---
name: <skill-name>
description: <what it does and when to use it>
---

# <Title>

One short sentence explaining the skill's job.

## Workflow

1. <First decision or action>
2. <Second action>
3. <Validation or output>

## Output Patterns

- <Common output shape>
- <Alternative output shape>

## Quality Rules

- <Rule that prevents weak or unsafe output>
- <Rule that preserves traceability>

## References

- `references/<file>.md`: <when to read it>
```

Keep the skill compact. Add references only for reusable details that would otherwise bloat `SKILL.md`.
