---
scope: phase-specific
phase: implement
trigger: for every development step confirmed in the breakdown
---

# Implement — Generic Development Phase

This is the **default** development phase. If the active adapter provides its own
`workflow/3_implement.md`, that file overrides this one entirely for stacks it covers
(see `1_orchestrator.md` §3) — typical adapter overrides implement Test-Driven
Development (TDD/STDD) or Spec-Driven Development (SDD) variants suited to that stack.

This generic version makes no assumption about whether the stack uses automated tests.

---

## The process

Always follow this order. Do not move to the next step without explicit confirmation.

```
1. SPEC      — I write the expected behavior, purpose, edge cases, and concerns
2. PLAN      — You confirm understanding and state how this step will be verified
               (automated tests, manual/visual review, or both)
3. IMPLEMENT — You implement based on the SPEC
4. VERIFY    — Tests are run and/or I perform manual/visual review
5. CONFIRM   — I confirm the step is done or request adjustments
```

Do not write any implementation before the SPEC is provided for that step.

---

## What you do at each step

### Step 1 — Spec

Once I give you the SPEC for this step, save it verbatim to:

```
~/.reins/user/projects/<project-slug>/specs/<type>_<slug>/step-NN-spec.md
```

— `<type>_<slug>` matches the active context file's name, `NN` is this step's
two-digit number in `## Breakdown`. Create the `specs/<type>_<slug>/` directory if
this is the first step. See `core/templates/spec.md` for the structure.

### Step 2 — Plan

- Read the entire SPEC before writing any line of code
- Restate the guarantees you will cover
- State explicitly how this step will be verified — if the project/adapter has tests, propose which test files will be added or changed; if not, describe what manual verification looks like
- If the SPEC conflicts with existing code, stop and ask before deciding
- Save your plan to `step-NN-plan.md` alongside the SPEC, following
  `core/templates/plan.md`
- If no adapter override defines a TDD/SDD process for this stack, the
  `core/skills/reins-senior-engineer/SKILL.md` lens (test-first, red/green/refactor) applies
  by default for Step 3

### Step 3 — Implement

- Cover the main flow, all listed edge cases, and every listed guarantee
- Apply the active adapter's standards (or `~/.reins/user/standards/*.md` if no adapter) throughout
- Do not modify any approved test
- If existing code contradicts the SPEC, stop and ask before deciding

### Step 4 — Verify

- If automated tests exist for this change, run them and report pass/fail
- If verification is manual, describe clearly what I should see and interact with, and list the specific behaviors to check (happy path, edge cases, error states)
- Report any failure unrelated to this step (flag it, do not fix it silently)

### Step 5 — Adjustments

- Minor corrections (naming, style, small logic fix) → apply directly
- Significant changes (new behavior, different architecture) → request a SPEC update first

---

## After confirmation — update the context file

Once the step is confirmed done, update `~/.reins/user/projects/<project-slug>/contexts/<active-context>.md`:

- Mark the current step as done in `## Breakdown`
- Update `## Current step` to the next pending step
- Update `## SPEC status` for the completed step to `implemented` (referencing
  `specs/<type>_<slug>/step-NN-{spec,plan}.md`)
- If a new decision was confirmed during this step, add it to `## Decisions made`
- Leave `## Objective` and `## My notes` untouched

---

## SPEC and PLAN structure

See `core/templates/spec.md` for the SPEC structure (written by me, saved by you to
`step-NN-spec.md`) and `core/templates/plan.md` for the PLAN structure (written by
you, saved to `step-NN-plan.md`).

---

## Permanent constraints

- Do not modify tests to make the implementation pass — modify the implementation instead
- Do not write the SPEC — that step is mine
- Do not move to step 4 without completing step 3 as scoped by the SPEC
- Do not modify `## Objective` or `## My notes` in the context file — those fields are mine only
- Apply the active adapter's standards and conventions at all times — they are not optional and do not require a task to be active

---

## Start prompt

When I hand you a SPEC, always begin by:

1. Confirming you read the SPEC and summarizing the guarantees you will cover
2. Stating how this step will be verified
3. Waiting for my explicit approval before any implementation
