# Adapters

An adapter teaches PAW about a specific stack, company, or team. It's the only place
where stack-specific or proprietary content should live — the `core/` engine never
contains it.

Adapters are **user-owned**: they live at `~/.paw/user/adapters/<name>/`, are never
modified by `paw update`, and you decide whether to keep them local, share them
privately within a team, or publish them.

---

## Creating an adapter

```bash
paw new-adapter my-company
```

This scaffolds:

```
~/.paw/user/adapters/my-company/
├── ADAPTER.md
├── standards/
│   └── floor.md
├── workflow/      (empty — add 3_implement.md only if needed)
└── skills/        (empty — add SKILL.md dirs as needed)
```

### 1. `ADAPTER.md`

```yaml
---
name: my-company
stacks: [ruby, node]   # which detected stacks this adapter applies to
author: you
version: 0.1.0
description: >
  Conventions and skills for ACME Corp's Rails + Angular stack.
---
```

`stacks` is matched against the marker-derived identifiers the orchestrator detects
(`core/workflow/1_orchestrator.md` §2 — `ruby` for `Gemfile`, `node` for
`package.json`, `python`, `go`, `jvm`, `rust`, `php`, ...). If more than one installed
adapter matches a project, all of them load.

### 2. `standards/floor.md`

The non-negotiable baseline for this stack: naming, architecture, test conventions —
whatever must always apply. Optionally add `standards/personal.md` for personal style
on top of the floor (precedence 2 — must never contradict the floor).

### 3. `workflow/3_implement.md` (optional)

Only add this if the stack needs a different development loop than the generic
SPEC → PLAN → IMPLEMENT → VERIFY → CONFIRM cycle in
`core/workflow/3_implement.md`. Common variants:

- **TDD/STDD** (backend with a test suite): `SPEC → TESTS → REVIEW → RED → GREEN`
- **SDD** (UI-only frontend, no automated tests): `SPEC → IMPLEMENT → VISUAL REVIEW → CONFIRM`

Keep the same "Permanent constraints" and "Start prompt" structure as the generic file
so behavior stays predictable.

### 4. `skills/`

Stack-specific, on-demand skills (scaffold generators, library reference browsers,
hotfix workflows, etc.). See [SKILLS.md](SKILLS.md).

---

## Example: a minimal Rails adapter

```
~/.paw/user/adapters/rails/
├── ADAPTER.md          # stacks: [ruby]
├── standards/
│   └── floor.md         # "use RSpec", "service objects under app/services", ...
└── workflow/
    └── 3_implement.md    # STDD cycle: SPEC -> TESTS -> RED -> GREEN
```

## Example: a minimal Python/FastAPI adapter

```
~/.paw/user/adapters/fastapi/
├── ADAPTER.md          # stacks: [python]
├── standards/
│   └── floor.md         # "pydantic models in schemas/", "pytest", ...
└── skills/
    └── new-router/SKILL.md   # scaffolds a new FastAPI router + schema + test
```

---

## Multi-stack projects

If a project matches more than one adapter (e.g. a `ruby` backend + `node` frontend
repo), the orchestrator loads both. Breakdown steps in `2_new_task.md` get labeled by
component (`(backend)`, `(frontend)`, `(integration)`), and the context file's
`branches`/`prs` fields become maps with one entry per component.

---

## Sharing adapters

- **Local only**: do nothing — it's already at `~/.paw/user/adapters/<name>/`.
- **Private team sharing**: put it in a private git repo, `git clone` it into
  `~/.paw/user/adapters/<name>/` on each machine.
- **Public**: publish it if there's nothing proprietary (no internal library names,
  no internal process docs, no personal data). Review it the same way you'd review
  any other open-source contribution before publishing.

PAW core never inspects adapter contents beyond `ADAPTER.md`'s `stacks:` field and the
optional `workflow/3_implement.md` override — it's safe to keep adapters completely
separate from this repo.
