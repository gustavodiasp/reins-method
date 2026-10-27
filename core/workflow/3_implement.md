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

Once I give you the SPEC for this step, save it verbatim under a new `## Step NN`
section in:

```
~/.reins/user/projects/<project-slug>/specs/<type>_<slug>.md
```

— or, if this step belongs to a component and `branches` has more than one
entry, in that component's own file:

```
~/.reins/user/projects/<project-slug>/specs/<type>_<slug>_<component>.md
```

— `<type>_<slug>` matches the active context file's name, `NN` is this step's
two-digit number in `## Breakdown`. Create the file if this is the first step
**for that component** (single-component: the first step overall); otherwise
append the new section after that same file's previous section — never a
sibling component's file. See `core/templates/task.md` for the section
structure and the multi-component path.

**Before using `<slug>` or `<component>` in any path here**: both are
interpolated directly into a file path — `<slug>` always, `<component>` once
multi-component — including, at close time, a *delete* path
(`4_close_task.md` Step 9). Confirm `<slug>` (set once, in `2_new_task.md`
Step 5) and every `<component>` key (set in `2_new_task.md` Step 3, or added
here if a new component is introduced) are each a single lowercase word —
letters, digits, and `-` only. If either was set by hand-editing the context
file rather than through that step, or contains anything else, stop and fix
it (ask the user to confirm the intended value) before creating, appending
to, or deleting any file built from it — don't let an unvalidated value reach
a create/append/delete path just because the proposal step already checked
it once.

**Before creating a brand-new `specs/<type>_<slug>_<component>.md` for a
component that has never had its own file yet**: check whether an orphaned
pre-multi-component file, `specs/<type>_<slug>.md` (no suffix), already
exists with prior step history. If it does, this is a single→multi-component
transition happening right now — do not silently create the new file and
leave the orphan as-is. Stop and ask the user how to handle the existing
file's content (e.g. rename it to the first component's own
`_<component>.md`, or leave it as shared pre-split history) before creating
the second component's file. Note either choice still sends the original
component's *next* step to its own new `_<component>.md` going forward —
the choice only affects what happens to the orphan's *existing* content, not
whether a second file gets created. Only proceed once they've decided — this
mirrors `core/templates/task.md`'s multi-component edge case (see that file
for the full consequence of each option), enforced here at the point the
split actually happens, not just noticed later at close.

### Step 2 — Plan

- Read the entire SPEC before writing any line of code
- Restate the guarantees you will cover
- State explicitly how this step will be verified — if the project/adapter has tests, propose which test files will be added or changed; if not, describe what manual verification looks like
- If the SPEC conflicts with existing code, stop and ask before deciding
- Save your plan under the `### PLAN` subsection of this step's `## Step NN`
  section, in the same file this step's SPEC was saved to (task file or that
  component's own file), following `core/templates/task.md`
- **The PLAN is not complete without its "Standards consulted" and "Context
  consulted" sections filled with real citations** (specific file + rule, or
  specific decision from the active context) — a placeholder like "N/A" with no
  justification does not satisfy this. This is the actual check, not a reminder:
  do not proceed to Step 3 until both sections name something real or explicitly
  justify why nothing applies.
- If no adapter override defines a TDD/SDD process for this stack, the
  `core/skills/reins-senior-engineer/SKILL.md` lens (test-first, red/green/refactor) applies
  by default for Step 3

### Step 3 — Implement

> **Divergence check:** If at any point during implementation the confirmed spec
> cannot be satisfied as written, or the user signals a mismatch, pause and invoke
> `core/skills/reins-correct-course/SKILL.md`. Do not continue implementing until
> the divergence is resolved and the spec is updated.

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

Once the step is confirmed done, update `~/.reins/user/projects/<project-slug>/contexts/<active-context>.md`
using **a short-lived lock around a targeted edit — never read-then-overwrite
the whole file, and never a targeted edit without the lock.**

History: the first fix here was "re-read right before writing, re-check the
file hasn't changed, retry on mismatch" with no real lock ("optimistic
concurrency"). Re-testing it at a stricter standard (`tools/tests/context_concurrency_test.py`,
function `unsafe_optimistic_edit`) found it still produces a rare but real
silent double-success collision — about 1 in 20 runs under stress — because
the last change-check and the actual write are two separate steps with a gap
between them that another session can land in. The current fix closes that
gap with an actual mutex, re-tested at 0/60 silent collisions and 0 lost
updates across repeated runs (vs. consistent lost updates and silent
corruption without it). Use this exact procedure:

1. **Acquire the lock**: `mkdir` is the one filesystem operation every
   POSIX filesystem (macOS, Linux, WSL2) guarantees is atomic with no extra
   tool required — it either creates the directory or fails because another
   session already holds it, with nothing in between. Run (adjust the path
   to this context file):
   ```
   until mkdir "<context-file>.lock" 2>/dev/null; do sleep 0.2; done
   ```
   If this doesn't succeed within ~10 seconds, another session's write is
   unexpectedly stuck — stop and tell the user rather than removing someone
   else's lock.
2. **While holding the lock**: read the file fresh (even if you read it
   earlier this session — another session may have changed it since), build
   a targeted find-and-replace of only the specific line(s) you're
   changing — your own `## Breakdown` item, your own `## Current step`
   component line (see `core/templates/context.md`), your own `## SPEC
   status` entry — never the surrounding content, write the result, and
   remove the lock directory (`rmdir "<context-file>.lock"`) immediately
   after — in a `finally`-equivalent: if the edit itself fails for any
   reason, still remove the lock before reporting the failure, so a crash
   never leaves the file locked for the next session.
3. **If the edit fails because the text you expected is no longer there**
   even while holding the lock, that means your own in-session copy was
   stale (you read it before this step, not fresh in step 2) — re-read and
   retry the same edit before releasing the lock. This should be rare: the
   lock means no one else can be mid-edit while you hold it.
4. If a new decision was confirmed during this step, add it to
   `## Decisions made` the same way — same lock, targeted append, fresh read.
5. Leave `## Objective` and `## My notes` untouched.

Do not fall back to a whole-file read-modify-write to "simplify" this, and do
not skip the lock because the targeted-edit part alone looks safe — both
failure modes this procedure prevents were measured, not theoretical.

---

## SPEC and PLAN structure

See `core/templates/task.md` for the `### SPEC` (written by me) and `### PLAN`
(written by you) subsection structure, both saved under the same `## Step NN`
section in `specs/<type>_<slug>.md`.

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
