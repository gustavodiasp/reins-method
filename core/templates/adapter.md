# Adapter Pack Template

An **adapter** teaches REINS about a specific stack, company, or team's conventions. Adapters
are user-owned: they live in `~/.reins/user/adapters/<name>/`, are never modified by `reins update`,
and can be shared (or kept private) independently of REINS core.

Scaffold a new one with:
```
reins new-adapter <name>
```

---

## Required structure

```
<name>/
├── ADAPTER.md          ← metadata (this file's frontmatter, see below)
├── standards/
│   ├── floor.md         ← non-negotiable conventions for this stack (precedence: 1)
│   └── personal.md      ← optional personal style on top of floor.md (precedence: 2)
├── workflow/
│   └── 3_implement.md   ← optional override of core/workflow/3_implement.md
└── skills/               ← optional, stack-specific skills
    └── <skill-name>/
        └── SKILL.md
```

Only `ADAPTER.md` and `standards/floor.md` are required. Everything else is optional —
omit `workflow/3_implement.md` to fall back to the generic development phase in
`core/workflow/3_implement.md`.

---

## `ADAPTER.md` frontmatter

```yaml
---
name: <name>                  # matches the directory name
stacks: [ruby, node]          # marker-derived stack identifiers this adapter applies to
                               # (see core/workflow/1_orchestrator.md §2 for the marker table)
author: <your name or handle>
version: 1.0.0
description: >
  One paragraph: what this adapter is for, and what conventions/skills it adds.
---
```

The orchestrator matches `stacks` against the markers it detects in the project root.
If more than one installed adapter matches, all matching adapters are loaded.

---

## `standards/floor.md`

The non-negotiable baseline for this stack — naming conventions, architectural rules,
test conventions, anything that must always be applied without exception. If
`standards/personal.md` ever contradicts this file, the orchestrator stops and asks
the user to resolve the conflict.

---

## `workflow/3_implement.md` (optional override)

Only create this if the stack needs a development process different from the generic
SPEC → PLAN → IMPLEMENT → VERIFY → CONFIRM loop in `core/workflow/3_implement.md` —
for example, a strict TDD/STDD cycle (SPEC → TESTS → REVIEW → RED → GREEN) for a
backend with a test suite, or an SDD cycle (SPEC → IMPLEMENT → VISUAL REVIEW →
CONFIRM) for a UI-only frontend with no automated tests.

Use `core/workflow/3_implement.md` as the structural reference — keep the same
"Permanent constraints" and "Start prompt" sections so behavior stays predictable
across adapters.

---

## `skills/`

Stack-specific, on-demand skills (e.g. a scaffold generator, a library reference
browser, a hotfix workflow). Follow `core/templates/skill.md` for the format. These
are never loaded proactively — only invoked when the user asks or the task calls
for them.

---

## Sharing an adapter

Adapters can be:
- Kept entirely local under `~/.reins/user/adapters/<name>/`
- Shared as a private git repo and cloned into that path
- Published publicly if the conventions/skills inside contain nothing proprietary

REINS core never inspects adapter contents beyond `ADAPTER.md`'s `stacks:` field and
the optional `workflow/3_implement.md` override.
