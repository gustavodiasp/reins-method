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

On request, invoke `core/skills/paw-code-review/SKILL.md` against the full diff for this
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

Add the PR link to this task's spec directory at
`~/.paw/user/projects/<project-slug>/specs/<type>_<slug>/`:

1. Identify the highest-numbered `step-NN-spec.md` for this task.
2. Add the PR URL under a `## PR` section at the bottom of that file.
3. Also record it in the context file's frontmatter (`prs`).
4. This link is required for Step 9 to determine whether the PR has merged and the
   `specs/<type>_<slug>/` directory can be deleted.

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

Check `~/.paw/user/config.yaml` for `historic_mode: on`. If it is off, skip this step entirely.

If on, follow `~/.paw/core/evaluation/README.md` (Mode A — record task entry at close), using:
- `~/.paw/core/evaluation/templates/monthly.md` to create the current month's file if it doesn't exist
- `~/.paw/core/evaluation/templates/task-entry.md` to build the entry

This step runs while the task context is still active — that context is the source of data for the entry.

Do not skip this step (when historic mode is on) unless I explicitly say to.

---

## Step 9 — Close context file and resume

After the PR comments are reviewed and I confirm the task is closed:

1. Check `~/.paw/user/projects/<project-slug>/specs/<type>_<slug>/` for this task:
   - If the highest-numbered `step-NN-spec.md` has a `## PR` link, check if the PR is merged (via available tooling).
   - **Before deleting anything**, list every file that would be deleted and explain why (PR merged, or explicitly authorized by you). Wait for your confirmation.
   - Delete only the files (or the whole `specs/<type>_<slug>/` directory) you confirm.

2. Delete the active context file (`<type>_<slug>.md`) for this task.

3. Glob `~/.paw/user/projects/<project-slug>/contexts/*.md` for any files with `status: paused`:
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
