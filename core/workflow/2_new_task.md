---
scope: phase-specific
phase: new-task
trigger: when a new task or ticket is handed to the agent
---

# New Task — Start Procedure

This file defines how we start working on any new task. Follow this procedure before writing any code, any test, or any SPEC.

---

## Step 1 — Understand the task

Read everything I give you: the task description, acceptance criteria, comments, linked tickets. Then answer these questions back to me:

- What is the **direct goal** of this task? (one sentence)
- What **existing behavior** does it touch or depend on?
- What **services, modules, or components** are likely involved?
- Are there any **ambiguities or missing information** that would block a clean implementation?

Do not assume. If something is unclear, ask before moving on.

---

## Bugfix — Investigate first

If the task type is `bugfix` (context type `bugfix`, or the user describes broken
behaviour), invoke `core/skills/reins-investigate/SKILL.md` immediately after Step 1,
before proposing the breakdown. Do not begin the breakdown (Step 3) until the
investigation finding is confirmed by the user.

---

## Step 2 — Understand the Epic (if provided)

If I give you an Epic or broader context, answer:

- What is the **overall goal** of the Epic?
- What **role does this task play** in the Epic? Is it a foundation, a step, or a finishing piece?
- Are there **adjacent tasks** in the Epic that this task must not break or must align with?

This context shapes every decision we make — architecture, naming, scope.

---

## Optional — Party Mode discussion

If the user asks for a multi-perspective discussion ("party mode", "discuss this
first", or the task has real ambiguity, multiple stakeholders, or an unclear "why"),
invoke `core/skills/reins-party-mode/SKILL.md` now, before proposing the breakdown. Its
synthesis informs Step 3 and Step 4 below — it does not replace them.

---

## Step 3 — Break down the task

Before any implementation, propose a breakdown of the task into clear, ordered steps.

Rules for the breakdown:
- Each step must have a **single, well-defined responsibility**
- Steps must be **ordered by dependency** — foundational changes come first
- Each step should be **independently testable or verifiable**
- If a step feels large, split it further
- If the project is multi-stack (see `1_orchestrator.md` §2), label each step by component (e.g. `(backend)`, `(frontend)`, `(integration)`)

Present the breakdown as a numbered list with a one-line description per step. Wait for my confirmation before proceeding.

---

## Step 4 — Flag architecture decisions

Before we write the SPEC, identify if any step requires an **architecture decision** — a choice between two or more valid approaches with different trade-offs.

For each decision point:
- Describe the options concisely
- State the trade-offs for each
- Give me your recommendation and why

I will make the final decision. Once decided, the rationale goes into the SPEC under `## Architecture decision`.

---

## Step 5 — Create the context file

After I confirm the breakdown and any architecture decisions, create the context file for this task at `~/.reins/user/projects/<project-slug>/contexts/<type>_<slug>.md` (see `1_orchestrator.md` §1 and §4 for how `<project-slug>` is determined).

1. **Check for an active context** — glob `contexts/*.md` and read frontmatter. If a file already has `status: active`, follow the interrupt procedure in `1_orchestrator.md` §4 before continuing.

2. **Determine the slug** — kebab-case short version of the task title (e.g. `invoice-by-supplier`).

3. **Create `<type>_<slug>.md`** using `core/templates/context.md` as base. Fill in:

```yaml
---
type: feature  # or hotfix / bugfix / chore / spike
stack: <detected stack(s)>
status: active
branches: { <component>: <current git branch> }
title: <task title>
updated_at: <today>
---
```

4. Fill in `## Task` and `## Epic` from what I provided
5. Fill in `## Breakdown` with the confirmed steps as unchecked items
6. Fill in `## Current step` with the first pending step
7. Fill in `## Decisions made` with any architecture decisions I confirmed
8. Leave `## Objective` and `## My notes` untouched — those are mine

Do not infer or summarize my intent in any of these fields. Write only what was explicitly stated.

---

## Step 6 — Begin development

Once the context file exists and architecture decisions are resolved, proceed to the development phase for the first step, following `3_implement.md` (or the active adapter's override of it — see `1_orchestrator.md` §3).

Do not start writing tests or code until I have provided the SPEC for that step.

---

## Permanent constraints

- Do not start any implementation before the full procedure above is complete
- Do not collapse the breakdown into a single step to move faster
- Do not make architecture decisions silently — surface them explicitly in step 4
- Do not modify `## Objective` or `## My notes` in the context file — those fields are mine only
- Do not infer my intent when filling the context file — write only what was explicitly stated
- The breakdown is a proposal — I confirm it before we proceed

---

## Start prompt

When I hand you a new task, begin by:

1. Summarizing your understanding of the task (step 1)
2. Summarizing the Epic context if provided (step 2)
3. Proposing the breakdown (step 3)
4. Flagging any architecture decisions (step 4)
5. Waiting for my confirmation before anything else
