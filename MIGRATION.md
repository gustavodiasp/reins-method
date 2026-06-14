# Migration — from the old `personal_ai_workflow` to REINS Method

This repo was redesigned from a project-coupled workflow (Rails/Angular + Hitax +
personal evaluation data, all in one repo) into REINS Method: a public, stack-agnostic
core (`~/.reins/core/`) plus user-owned adapters and historic data
(`~/.reins/user/`).

**Phase 1 (done in this repo):** the generic core, CLI, agent bridges, and docs
described in the rest of this repo.

**Phase 2 (TODO — separate, private session):** migrate everything stack-specific or
personal out of this repo into your local `~/.reins/user/`.

---

## What needs to move, and where

### 1. Hitax/Rails/Angular adapter → private adapter pack

The old `adapters/backend/` and `adapters/frontend/` directories contained Rails/RSpec
and Angular/hitax-ng conventions and skills (`hitax-*`, `reins-add-*`, etc.) tied to a
specific employer's stack and internal libraries (`hitax_ai`, `hitax_hub`, `hitax-ng`,
`HtxApiService`, ...).

To migrate:

1. `reins new-adapter hitax`
2. Move `standards/code_standards.md`, `personal_code_standards.md`,
   `test_conventions.md`, `test_runner.md` (backend) and
   `code_standards.md`, `frontend_standards.md`, `i18n_workflow.md`,
   `personal_code_standards.md` (frontend) into
   `~/.reins/user/adapters/hitax/standards/` — split/merge into `floor.md` (precedence 1)
   and `personal.md` (precedence 2) per `ADAPTERS.md`.
3. Move `adapters/backend/workflow/3_stdd_instructions.md` and
   `adapters/frontend/workflow/3_sdd_instructions.md` into
   `~/.reins/user/adapters/hitax/workflow/3_implement.md` — pick (or merge) whichever
   applies based on the stack the adapter targets, following the structure of
   `core/workflow/3_implement.md`.
4. Move all `hitax-*` skills and the `reins-*` frontend/backend skills into
   `~/.reins/user/adapters/hitax/skills/`.
5. Set `ADAPTER.md` `stacks: [ruby, node]` (or split into two adapters,
   `hitax-backend` / `hitax-frontend`, if they should load independently).
6. Keep this adapter **private** — it references an employer's internal libraries and
   processes (`hitax apps`, `Deloitte TaxIT`, etc.).

### 2. Personal evaluation data → `~/.reins/user/historic/`

The old `core/evaluation/monthly/*.md` files (2025-11 through 2026-06) contain real
performance-review content. Move them as-is to `~/.reins/user/historic/`:

```bash
mkdir -p ~/.reins/user/historic
mv core/evaluation/monthly/*.md ~/.reins/user/historic/
reins historic on
```

Then remove `core/evaluation/monthly/` from this repo (already done in Phase 1 — this
repo only ships empty templates now).

### 3. Active project contexts/specs → `~/.reins/user/projects/<project-slug>/`

The old `projects/contexts/*.md` and `projects/specs/*.md` described in-progress
company work. For each active context:

1. Determine `<project-slug>` for the project it belongs to (per
   `core/workflow/1_orchestrator.md` §1).
2. `mkdir -p ~/.reins/user/projects/<project-slug>/{contexts,specs}`
3. Move the relevant context/spec files there.
4. Update the frontmatter to the new model (`branches`/`prs` as maps — see
   `core/templates/context.md`) if it used the old single `branch`/`pr` fields.

---

## After migrating

- `reins doctor` should report no issues.
- Open a project that matches the `hitax` adapter's `stacks:` and confirm the
  orchestrator loads it.
- Confirm `reins historic on` picks up the current month correctly and that closing a
  task appends to it.
- This repo (REINS Method core) should now contain **no personal data and nothing
  proprietary** — safe to make public.
