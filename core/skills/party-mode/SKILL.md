---
name: party-mode
description: >
  Run a multi-perspective discussion over a task description before proposing a
  breakdown. Michael (Facilitator) picks the relevant persona lenses (always
  including Toby) and announces them; each adopted persona speaks in turn; Jim
  (Synthesizer) then distills it all into what matters for the breakdown. Use when
  the user asks to "discuss this first", "party mode", or before breaking down a
  task with real ambiguity or trade-offs.
tags: [party-mode, discussion, meta]
---

# Party Mode

A lightweight, native version of BMAD's "Party Mode": instead of installing and
coordinating separate agents, you (the same agent) sequentially adopt each relevant
persona's lens — defined in `core/skills/<role>/SKILL.md` — over the task
description, framed by two roles that control flow but contribute no domain opinion
of their own: Michael opens the session, Jim closes it.

## Trigger

- The user explicitly asks for "party mode" or "discuss this before we break it
  down"
- Optionally referenced from `core/workflow/2_new_task.md` before Step 3
  (breakdown) when the task has real ambiguity, multiple stakeholders, or an
  unclear "why"

## Context

Read the task description and any Epic context (per `2_new_task.md` Steps 1-2)
before running this skill — Party Mode discusses an already-understood task, it
doesn't replace understanding it.

## Steps

1. **Michael (Facilitator) opens the session.** Read the task context and decide
   which personas are relevant:
   - **Always include `reins-business-analyst`** (Toby) — no exceptions.
   - Select additional personas based on the task:
     - `reins-ux-designer` (Erin) — if the task has a user-facing UI/flow dimension
     - `reins-system-architect` (David) — if an architecture decision is likely
     - `reins-product-manager` (Jim) — if job-to-be-done/user-value framing is still
       unclear
     - `reins-technical-writer` (Pam) — if the task is primarily about docs/spec/API
       clarity
     - `reins-senior-engineer` (Angela) — if the implementation approach itself is in
       question
   If unsure which apply beyond Toby, default to adding Jim + David + Erin (the most
   common trio for feature work).
   Announce the lineup with energy, in Michael's voice, before anyone speaks — e.g.
   *"Okay, this is VERY important. I'm gonna need Toby, David, and Erin on this
   one."* Michael does not contribute a domain opinion of his own.
2. **Run each selected persona's lens sequentially**, in the order announced — each
   producing its short output as defined in its own `SKILL.md`.
3. **Jim (Synthesizer) closes the session.** After every persona has spoken, cut
   through the noise — ignore tangents — and distill it all into what actually
   matters for the breakdown: agreements, tensions between perspectives (e.g., Erin
   wants X, David flags it's costly), and open questions for the user. Voice: *"Alright.
   Here's what actually matters from all of that..."* If Jim was also selected in
   step 1 as a contributing persona, he still gives this closing synthesis in
   addition to his own lens output.
4. Hand the synthesis back into `core/workflow/2_new_task.md` Step 3 (breakdown) and
   Step 4 (architecture decisions) — Party Mode informs these, it doesn't replace the
   user's confirmation.

## Output

A discussion summary structured as:
- **Lineup** (from Michael) — who was called in and why
- **Perspectives** — one short subsection per persona invoked in step 2
- **What actually matters** (from Jim) — tensions/trade-offs and open questions for
  the user

This feeds directly into the breakdown proposal — it is not a separate deliverable
the user has to act on independently.
