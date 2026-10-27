---
scope: phase-specific
phase: close-task
trigger: when the user gives the order to close a task
---

# Close Task — Procedure

This file defines what you do when I give the order to close a task. Execute every step in order without skipping.

---

## Step 1 — Run the test suite (if applicable)

If the project has automated tests, run the full suite — not just the ones related to this task. Use the test command documented in the active adapter's standards, or ask me if none is documented.

Report back:
- Total passing / failing / pending
- Any failure unrelated to this task that was already present (flag it, do not fix it silently)
- Any test that was modified after my approval (this must not have happened — flag it immediately if it did)

If the project has no automated tests, skip to Step 2 and note that verification was manual (per `3_implement.md`).

Do not proceed to step 2 if there are unexpected failures.

---

## Step 2 — Summary of what was done

Write a clear, concise summary covering:

- **What changed** — which services, components, modules, or endpoints were added or modified
- **Why** — the problem this solves or the behavior it introduces, in plain language
- **How** — the approach taken and any architecture decision that shaped it

Keep it readable by someone who wasn't in this task. No implementation details unless they are essential to understand the decision.

---

## Step 3 — Task objective and Epic impact

Answer explicitly:

- Does the implementation fulfill the task's stated goal? If not entirely, what is missing?
- How does this task contribute to the Epic's overall objective?
- Does this change anything that adjacent tasks in the Epic depend on?

---

## Step 4 — Next step

If there is a natural next step in the Epic or a follow-up that this task makes possible or necessary, state it clearly:

- What is the next step?
- Why does it follow from this task?
- Any dependency or prerequisite to be aware of?

If there is no clear next step, say so explicitly.

---

## Optional — Code review

On request, invoke `core/skills/reins-code-review/SKILL.md` against the full diff for this
task before proposing the commit message in Step 5. Its findings are presented to
the user, who decides whether to address anything before proceeding.

---

## Step 5 — Commit message

Propose the final commit message following these rules:

- One subject line — short, imperative, informative
- Describes **what the change does**, not what files were touched
- If the task title is already a good description, use it as the base
- If the task title is too vague, implementation-specific, or ticket-code-only, write a better one
- Optionally: one blank line followed by 2–3 lines of body if the change needs brief context

Format:
```
<subject line>

<optional short body>
```

Present one primary suggestion and one alternative if the scope could be described differently.

---

## Step 6 — Link the PR in the SPEC

Add the PR link to the spec file for the component whose PR this is (or the
single task file, if single-component):
`~/.reins/user/projects/<project-slug>/specs/<type>_<slug>.md` or
`specs/<type>_<slug>_<component>.md`:

1. Identify the highest-numbered `## Step NN` section **in that component's own
   file** — never a sibling component's file.
2. Add the PR URL under a `### PR` subsection at the bottom of that section.
3. Also record it in the context file's frontmatter (`prs`), under that
   component's key.
4. This link is required for Step 9 to determine whether this component's PR
   has merged and this component's spec file can be deleted — a sibling
   component's file is never affected by this.

---

## Step 7 — PR comment review

When I give the order to review PR comments:

1. If a GitHub (or equivalent) MCP/CLI tool is available, use it to fetch all review comments and inline comments from the PR.
2. Analyze the comments in the context of this task, the Epic, and the codebase decisions made.

For each comment, respond with:

- **Valid** — the comment identifies a real problem or improvement that aligns with the task goals and existing architecture
- **Partially valid** — the comment has merit but misses context (explain what it's missing)
- **Not valid** — the comment is incorrect, irrelevant, or conflicts with a deliberate decision made during this task (explain why)

For every **Valid** or **Partially valid** comment, propose how to address it — a code change, a clarification, or a documented decision.

Do not act on any comment before I confirm which ones to address. Comments marked **Not valid** are ignored unless I say otherwise.

---

## Step 8 — Record historic entry (if historic mode is on)

Check `~/.reins/user/config.yaml` for `historic_mode: on`. If it is off, skip this step entirely.

If on:

1. Check `~/.reins/user/historic/` for any existing files or a user-defined template. If the user has established a structure (their own file layout, naming convention, or template), follow it exactly.
2. If no structure exists yet, ask the user: how do you want to organize this entry — what file, what format, what data?
3. Record the entry as the user specifies, using the task context (still active at this point) as the data source.

Do not impose any file structure, naming convention, or template. The organization of `~/.reins/user/historic/` is entirely the user's choice.

Do not skip this step (when historic mode is on) unless I explicitly say to.

---

### Optional — Mini-retrospective (Historic Mode only)

If historic mode is enabled and a task entry was just written in Step 8, ask the
user once: *"Do you want to add a quick retro to this entry? (takes ~2 minutes)"*

If yes, ask these three questions one at a time — wait for each answer before
asking the next:

1. What went well in this task that you want to repeat?
2. What slowed you down or caused friction?
3. What would you do differently next time?

Append the answers to the historic entry in whatever format fits the user's
established structure. If no structure exists, use a simple `## Retro` section.

If the user says no, or does not respond, skip silently. Never block task closure
on the retro.

---

## Step 9 — Close context file and resume

After the PR comments are reviewed and I confirm the task is closed:

1. Check this task's spec file(s):
   - **Before resolving any of these paths**: this step builds *delete* paths
     from `<slug>` and, if multi-component, each `<component>` key in
     `branches`. Confirm each is still a single lowercase word (letters,
     digits, `-` only — see `2_new_task.md` Step 3 / `3_implement.md` Step 1)
     before using it to build a path to delete. The context file is a plain
     user-editable `.md` — never trust a value read from `branches` without
     this check just because it was validated once, earlier, elsewhere.
   - **Single-component**: `~/.reins/user/projects/<project-slug>/specs/<type>_<slug>.md` — if its highest-numbered `## Step NN` section has a `### PR` link, check if the PR is merged (via available tooling).
   - **Multi-component**: one file per component, `specs/<type>_<slug>_<component>.md` — check **every** component's file the same way. Closing the task means every component is done; do not treat one component's merged PR as license to delete the others' files.
   - **Also check for an orphaned pre-multi-component file**: `specs/<type>_<slug>.md` (no component suffix) can hold early steps from before a second component was added mid-task (see `core/templates/task.md`). If it exists alongside per-component files, it is part of this task's history too — include it in the same merged-PR check and deletion list, do not silently skip it because it doesn't match the `_<component>` pattern.
   - **Before deleting anything**, list every file that would be deleted (one line per component, if multi-component, plus the orphaned file if present) and explain why for each — either "PR merged" or "explicitly authorized by you for this component." If any component's PR has not merged and you have not explicitly authorized deleting its file, stop and say which — do not delete any file, including a ready component's, until every component is either merged or individually authorized. Wait for your confirmation before deleting anything.
   - Delete the file(s) once confirmed.

2. Delete the active context file (`<type>_<slug>.md`) for this task.

3. Glob `~/.reins/user/projects/<project-slug>/contexts/*.md` for any files with `status: paused`:
   - If none exist: confirm the workspace is clean and stop.
   - If any exist: list them (type, title, branches, updated_at) and ask: "Which context do you want to resume?"
   - On selection: set the chosen file to `status: active`, update `updated_at`, then run the branch guard (`1_orchestrator.md` §4) before proceeding.

4. If a SPEC has no PR link yet, keep it until the PR is opened and linked.

---

## Permanent constraints

- Do not close a task with a failing test suite unless I explicitly say to proceed anyway
- Do not write a commit message that references internal ticket codes only — it must be human-readable
- Do not skip the Epic impact section if an Epic was provided at task start
- Do not silently fix unrelated failures — flag them and wait for my instruction
- Do not act on any PR comment before I confirm which ones to address
- Do not mark a comment as valid solely because it follows a general best practice — evaluate it against the specific decisions made in this task
- Do not delete the context file before I explicitly confirm the task is closed
- Do not skip the historic entry step (Step 8) when historic mode is on — it must run before context cleanup
- Do not impose any file structure or template on the user's `~/.reins/user/historic/` — follow what the user has defined, or ask
