# Task File Template — SPEC + PLAN per step

**Single-component task** (the common case — `branches` has exactly one entry):
one file per task, at:

```
~/.reins/user/projects/<project-slug>/specs/<type>_<slug>.md
```

**Multi-component task** (`branches` has more than one entry): one file **per
component**, never shared — each component's steps append only to its own file,
in its own monotonic sequence, independent of any other component's pace:

```
~/.reins/user/projects/<project-slug>/specs/<type>_<slug>_<component>.md
```

e.g. `specs/feature_invoice-by-supplier_backend.md` and
`specs/feature_invoice-by-supplier_frontend.md`. This is not a concurrency
mechanism — it's isolation by construction: two components never name the same
path, so there is nothing to coordinate or lock.

**Single→multi-component transition (edge case):** a task that starts
single-component and later gains a second component mid-task leaves behind an
orphaned, unsuffixed `specs/<type>_<slug>.md` holding the steps recorded
before the split — it is never auto-renamed or auto-merged (`3_implement.md`
stops and asks before creating the new component's first file, precisely
because this is irreversible by construction once a second component's file
exists). Whichever option the user picks, **the original component's *next*
step still goes to its own new `specs/<type>_<slug>_<component>.md`** — once
`branches` has more than one entry, every component writes to a
`_<component>.md` file, including the one that pre-dates the split. The
choice only affects the orphan's *existing* content:
- *Rename it* to the first component's own `_<component>.md` — its prior
  steps become that component's own continuous history, so there end up
  being exactly two files (one per component), matching the normal
  multi-component layout.
- *Leave it as shared pre-split history* — the orphan stays on disk as a
  third, frozen file (no further steps are ever appended to it); the task
  then has three spec files in total: the orphan plus one per component
  going forward. `4_close_task.md` Step 9 and `reins-code-review/SKILL.md`
  Step 1.3 both account for this file explicitly so it is never silently
  skipped at close or during review.

Either way, `<type>_<slug>` matches the active context file's name (without
`.md`). Holds one section per confirmed step, appended **in order**, exactly
when that step is reached — never pre-written for a future step, and (for
multi-component) never referencing or waiting on another component's section.
The per-step confirmation cadence in `core/workflow/3_implement.md` (SPEC →
PLAN → IMPLEMENT → VERIFY → CONFIRM, never skipping ahead) is unchanged by this
layout — only the file count is reduced, from two files per step to one section
per step (per component, where applicable).

---

```markdown
## Step NN — [Step title, from the breakdown]

### SPEC
<!-- Written by the user, never by the agent (see 3_implement.md Permanent
     constraints). -->

**Context**
What exists today, where it lives, and what is wrong or missing.

**Goal**
What changes and why.

**Expected behavior**
- Main flow
- Secondary flows
- Edge cases / error states

**Guarantees**
- [ ] Guarantee 1
- [ ] Guarantee 2
- [ ] Existing entry points / behavior outside this scope are unchanged

**Verification**
- [ ] Automated tests: <files / framework, or "none — manual review">
- [ ] Manual review steps (if applicable)

**Architecture decision**
Chosen approach and rationale (if an architecture decision was made prior to this
SPEC).

**Out of scope**
What explicitly does not change in this step.

**Files likely affected**
- [ ] path/to/file

### PLAN
<!-- Written by the agent, after reading this step's SPEC, as part of Step 2 of
     3_implement.md. -->

**Guarantees covered**
Restate each guarantee from the SPEC and confirm it will be addressed.

**Standards consulted**
List each applicable standards file and the specific rule(s) that apply to this
step. "None apply" is valid only if the step touches nothing the standards
govern — state why.

**Context consulted**
Name the active project context file and any existing patterns/decisions in it
that this step must align with. If no active project context exists, state that
explicitly.

**Verification approach**
- Automated tests: <files to add/change, or "none — manual review">
- Manual review steps (if applicable): what the user should see and check

**Open questions / risks**
Anything in the SPEC that conflicts with existing code, or any assumption that
needs confirmation before implementation starts. Empty if none.

### PR
<!-- Added only once per file, under its highest-numbered step, when a PR is
     opened for this component (or the whole task, if single-component) — see
     core/workflow/4_close_task.md Step 6. Matches this component's entry in
     the context frontmatter's `prs: {}` map. -->
<url>
```

---

Once the user approves a step's PLAN, proceed to Step 3 (Implement) of
`3_implement.md`. The next `## Step NN` section is appended only once the current
step is confirmed done — never written ahead of time.
