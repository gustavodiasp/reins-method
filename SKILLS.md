# Skills

A skill is a single `SKILL.md` file describing an on-demand procedure. Skills are
**never loaded proactively** — the agent reads them only when you explicitly ask, or
when a workflow phase clearly calls for it.

---

## Where skills live

| Skill applies to... | Location |
|---|---|
| Everyone, any stack (rare — keep core minimal) | `~/.paw/core/skills/<name>/` |
| Only you, any project | `~/.paw/user/skills/<name>/` |
| Only a specific stack/company | `~/.paw/user/adapters/<adapter>/skills/<name>/` |

Most custom skills belong in an adapter (if stack/company-specific) or in
`~/.paw/user/skills/` (if personal and general-purpose).

---

## Creating a skill

```bash
paw new-skill my-skill
```

This scaffolds `~/.paw/user/skills/my-skill/SKILL.md`. Or, for guided creation, ask
your agent to use the **skill-creator** meta-skill
(`~/.paw/core/skills/paw-skill-creator/SKILL.md`) — it will ask what the skill should do,
when it should trigger, whether it's read-only, and where it belongs (user vs.
adapter), then draft the file for your review before writing it.

---

## `SKILL.md` format

```yaml
---
name: my-skill
description: >
  One or two sentences: what this skill does and when to use it. Be specific —
  this is what the agent uses to decide whether the skill applies.
allowed-tools: bash   # optional
tags: [tag1, tag2]    # optional
---

# My Skill

## Trigger
Explicit phrases, file patterns, or situations that should cause this skill to load.

## Context
What the agent needs to know before acting: relevant files, conventions,
prerequisites, flags to check.

## Steps
The procedure, step by step. Be explicit about what requires confirmation before
proceeding — especially anything destructive or irreversible.

## Output
What the agent should produce or report when done.
```

---

## Conventions

- **Read-only by default.** If a skill scaffolds or modifies files, it must preview
  the changes and ask for confirmation before writing.
- **Specific names.** Avoid generic names that could collide across adapters (prefer
  `rails-crud-scaffold` over `scaffold`).
- **Specific descriptions.** The `description` field is how the agent decides whether
  to load the skill — vague descriptions cause skills to be missed or over-triggered.
- **Stack-specific skills belong in adapters**, not in `core/` or `user/skills/`.

---

## Example

```yaml
---
name: rails-crud-scaffold
description: >
  Generate a CRUD scaffold (model, migration, controller, serializer, request specs)
  for a new Rails resource, following this project's conventions. Use when asked to
  "scaffold", "generate CRUD", or "add a new resource" in a Ruby/Rails project.
allowed-tools: bash
tags: [scaffold, ruby]
---

# Rails CRUD Scaffold

## Trigger
User asks to scaffold/generate a new resource in a Rails project (`Gemfile` present).

## Context
Read `standards/floor.md` for naming and folder conventions before generating
anything. Determine the resource name and attributes from the request; ask if
ambiguous.

## Steps
1. Propose the list of files to be created/modified and their contents (preview only).
2. Wait for confirmation.
3. Write the files.
4. Run the relevant generator/test command (if any) and report the result.

## Output
- List of files created/modified
- Any follow-up steps (e.g. run migrations)
```
