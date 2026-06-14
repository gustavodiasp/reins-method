# Skill Template

A skill is a single `SKILL.md` file describing an on-demand procedure the agent can
follow when invoked. Skills are **never loaded proactively** — only when the user
explicitly asks, or the active workflow phase calls for it.

Scaffold a new one with:
```
reins new-skill <name>
```
or invoke the `skill-creator` meta-skill (`~/.reins/core/skills/skill-creator/SKILL.md`)
for guided creation.

---

## Required structure

```
<skill-name>/
└── SKILL.md
```

## `SKILL.md` format

```yaml
---
name: <skill-name>
description: >
  One or two sentences: what this skill does and when to use it. Be specific —
  this description is what the agent uses to decide whether the skill applies.
allowed-tools: bash   # optional, restrict tool usage if relevant
tags: [tag1, tag2]    # optional, free-form
---

# <Skill Title>

## Trigger
When should this skill be invoked? List explicit phrases, file patterns, or
situations that should cause the agent to load this skill.

## Context
What does the agent need to know before acting — relevant files, conventions,
prerequisites, flags to check (e.g. "only valid if `package.json` exists").

## Steps
The procedure, step by step. Be explicit about what requires user confirmation
before proceeding (especially anything destructive or irreversible).

## Output
What the agent should produce or report back when the skill completes.
```

---

## Conventions

- Keep skills **read-only by default** unless their purpose is explicitly to scaffold
  or modify files — and even then, preview changes and confirm before writing.
- Name skills by **what they do**, not after a character/persona (e.g.
  `reins-code-review`, `reins-business-analyst`) — never `persona-<name>`. The `reins-`
  prefix is suggested for core/user skills but not mandatory — `reins sync` adds it
  automatically if missing, so the skill is always registered as `reins-*` either
  way. Adapter skills are usually named without the prefix (`reins sync` assembles
  `reins-<adapter>-<function>` automatically). Avoid generic names that could collide
  across adapters (e.g. prefer `rails-crud-scaffold` over `scaffold`).
- If a skill only makes sense for a specific stack/company, it belongs in an adapter
  pack (`<adapter>/skills/`), not in `~/.reins/core/skills/` or `~/.reins/user/skills/`.
