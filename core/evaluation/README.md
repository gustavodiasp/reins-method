# Historic Mode

Historic Mode turns daily work into a clear, evidence-based record of monthly progress.
It is **optional** — enable it with `paw historic on`. All data it produces is
**user-owned** and lives at `~/.paw/user/historic/`, never inside a project repo and
never touched by `paw update`.

---

## Purpose

Each closed task leaves a short, objective trace. At the end of a period (or before a
performance check-in / 1:1), that trace is compiled into a **Monthly Summary** that
supports self-assessment and the conversation with a manager or lead. It typically
helps answer questions like:

1. What were the priorities for this period?
2. What progress was made on previous priorities?
3. What are the expectations/priorities for the upcoming period?
4. What support is needed?
5. How can strengths be leveraged further?
6. How is performance overall?

---

## Structure

```text
~/.paw/user/historic/
└── YYYY-MM.md          ← one file per month
```

Templates used to create these files live at:
```
~/.paw/core/evaluation/templates/
├── monthly.md           ← empty monthly file template
└── task-entry.md        ← empty task entry template
```

---

## Mode A — Record task entry at close

**When:** invoked automatically from `core/workflow/4_close_task.md` Step 8, when
historic mode is on.

### Step 1 — Identify the target month

Use today's date to determine `YYYY-MM`.

### Step 2 — Open or create the monthly file

- Check if `~/.paw/user/historic/YYYY-MM.md` exists.
- If it does **not** exist:
  - Create it from `core/evaluation/templates/monthly.md`.
  - Fill in the header (period, month).
  - **Ask the user to fill in the priorities and "punch back" sections** before proceeding — these set the context for the whole period.
- If it already exists: open it.

### Step 3 — Check for duplicates

Before adding an entry, verify the task/PR/branch is not already recorded in the
"Task entries" section. Dedupe key: branch name, PR number, or task title. If a
duplicate is found, skip and inform the user.

### Step 4 — Enrich with available tooling (optional)

If a GitHub (or equivalent) MCP/CLI tool is available, fetch from the PR associated
with this task: PR number, title, URL, state, merged date, files changed,
additions/deletions, commit count, and review comment themes (summarized, not
transcribed verbatim). If unavailable, proceed without it — do not block the entry.

### Step 5 — Build the entry

Use `core/evaluation/templates/task-entry.md` as the structure. Fill in date, title,
type, context, what was done, and impact from the task summary (`4_close_task.md`
Step 2). Ask the user for the difficulty dimensions and any notes worth highlighting
at the next check-in.

### Step 6 — Insert the entry

Append the entry to the "Task entries" section of the monthly file, in chronological
order.

### Step 7 — Done

Confirm the entry was added. Show the entry title and the file path.

---

## Mode B — Monthly summary (`paw historic summary`)

Generated only when explicitly requested. The agent reads the entries for the
specified month, optionally enriches with PR/commit metrics from available tooling,
and produces a summary covering: main deliveries, progress against priorities,
impact, skills demonstrated, evolution signals, areas to improve, and a one-line
takeaway.

---

## Rules

- **One file per period** — `historic/YYYY-MM.md`
- **Record at close, not at the end of the period** — don't let entries pile up
- **Summary only on request** — never generated automatically
- **Enrichment is additive, never blocking** — if data isn't available, the entry still gets recorded
- **No duplicates** — dedupe key: branch / PR / date

---

## Difficulty scale (0–10, optional)

Each entry can optionally rate three dimensions:

| Dimension | What it measures |
|---|---|
| **Size** | Volume of work / effort |
| **Complexity** | Technical difficulty / ambiguity |
| **Impact** | Importance of the result / risk / relevance |

| Score | Reading |
|---|---|
| 0–2 | Very simple, direct execution |
| 3–4 | Simple, with some context |
| 5–6 | Intermediate, required analysis or coordination |
| 7–8 | Complex, significant risk or ambiguity |
| 9–10 | Exceptionally demanding or critical |

---

## Guiding principle

This system isn't about "looking productive". It exists to make real work, real
growth, and real needs visible — to the user themselves, first.
