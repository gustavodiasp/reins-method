---
scope: always
role: master — read first every session, defines stack detection and routing
---

# REINS Orchestrator

**Read this first.** Detects project stack, loads adapter (if any), locates active task context, routes workflow phase.

**Filesystem structure:** REINS lives at `~/.reins/` (never in project repo). Core (`core/`) is updated via `reins update`. State lives in `~/.reins/user/projects/<project-slug>/` (user-owned, never touched by updates).

---

## 1 — Identify the project

- [ ] Determine project root (directory containing `.git`, or current directory)
- [ ] Compute `<project-slug>` — stable filesystem identifier (repo name or absolute path with `/` → `-`)
- [ ] Create `~/.reins/user/projects/<project-slug>/` if not exists (with `contexts/` and `specs/` subdirs)

---

## 2 — Stack detection

Inspect the project root for marker files to detect the stack(s) in play:

| Marker | Stack |
|---|---|
| `Gemfile` | `ruby` |
| `package.json` | `node` (inspect `dependencies`/`devDependencies` for framework hints, e.g. React, Angular, Vue) |
| `pyproject.toml`, `requirements.txt`, `setup.py` | `python` |
| `go.mod` | `go` |
| `pom.xml`, `build.gradle` | `jvm` |
| `Cargo.toml` | `rust` |
| `composer.json` | `php` |
| More than one marker present | multi-stack (e.g. `ruby` + `node` = backend + frontend) |
| Nothing recognizable | ask the user explicitly |

If the active context file (see §4) already declares a `stack`, trust it instead of re-detecting — but flag a mismatch if detection now disagrees.

---

## 3 — Load adapter (if any)

1. Read `~/.reins/user/config.yaml` for `adapters:` list
2. For each adapter: read its `ADAPTER.md` and check `stack:` field
3. Load only adapters whose `stack:` matches stack(s) detected in §2:
   - [ ] Load `<adapter>/standards/floor.md` (non-negotiable, highest precedence)
   - [ ] Load `<adapter>/standards/*.md` (additional standards, must never conflict with floor)
   - [ ] Load `<adapter>/workflow/3_implement.md` if present (overrides `core/workflow/3_implement.md`)
4. If no adapter matches: use generic conventions in `~/.reins/user/standards/company.md` + `personal.md`
5. If multiple stacks detected: load all matching adapters; label breakdown steps by adapter/stack
6. **Always also check** for
   `~/.reins/user/projects/<project-slug>/standards.md` — project-level
   standards, scoped to this one project regardless of stack or adapter match.
   If it exists, load it additively on top of whichever branch above applied
   (non-negotiable, same precedence tier as `floor.md`). Use this for rules
   tied to a specific project's identity rather than its stack — e.g. "this
   project is REINS's own source, changes here need extra scrutiny" — not
   something an adapter (which matches by stack marker, not by repo) can
   express. Create one by hand at that path, or via `reins-config` (see
   `core/skills/reins-config/SKILL.md`).

**Conflict rule:** if `personal.md` or `standards.md` (project-level)
contradicts `floor.md`, stop and ask user to resolve before proceeding.

## 4 — Active context

Context files at `~/.reins/user/projects/<project-slug>/contexts/<type>_<slug>.md` track work state.

**Invariant:** exactly one context per project has `status: active`.

- [ ] On session start: glob contexts, read frontmatter, find `status: active`
- [ ] On interrupt (new task while active): set current to `status: paused`, create new with `status: active`
- [ ] On close: delete active context, list paused contexts, ask which to resume

**Multi-component guard (before developing any step):** if `branches` has >1 entry, verify each branch is correct before proceeding (run `git branch --show-current` per component, compare to context frontmatter). If mismatch: ask user to switch branch, update context, or cancel.

**Running sessions in parallel:** this is how to run two or more sessions at once
on one task's different components (e.g. a backend session and a frontend session
on the same feature): `## Breakdown` steps labeled per component (`(backend)`,
`(frontend)` — see `2_new_task.md` Step 3); `## Current step` holding one line
per component (see `core/templates/context.md`); and each component's SPEC+PLAN
in its own file, `specs/<type>_<slug>_<component>.md`, never shared with another
component (see `core/templates/task.md`). The **spec files are isolated by
construction** — no two components ever touch the same path, nothing to
coordinate there. The **context file is not** — `branches`, `## Breakdown`,
`## Current step`, and `## SPEC status` all live in one shared
`<type>_<slug>.md` that every component's session reads and writes. This *is*
coordinated, not merely isolated: every session wraps its update in a
short-lived `mkdir`-based lock and makes a targeted change scoped to exactly
its own line while holding it (see `3_implement.md`'s "After confirmation —
update the context file"). An earlier version of this fix used
re-read-then-recheck with no real lock ("optimistic concurrency") and passed
review, but re-testing at a stricter standard found it still silently
corrupted the file in roughly 1 of 20 runs under stress — re-checking right
before a write isn't atomic with the write itself, so another session can
land in that gap. The mutex closes it: re-tested at 0 lost updates and 0
silent collisions across 60+ runs (`tools/tests/context_concurrency_test.py`).
Writing the whole file from memory, or doing a targeted edit without the
lock, is exactly the bug this mechanism exists to prevent — both were
measured, not theoretical.

## 5 — What gets loaded when

**Session start (always):**
- `1_orchestrator.md` (this file)
- Active context file (§4)

**Under demand (lazy):**
- `2_new_task.md` → when starting new task
- `3_implement.md` (adapter or core) → when entering development phase
  - Adapter standards (§3) + user standards / generic standards +
    project-level `standards.md` (§3.6, if present) → load at this point, not
    before
- `core/skills/reins-code-review` → when invoked
  - Applicable standards (same resolution as §3, project-level included) →
    load at this point
- `4_close_task.md` → when closing task
- Skills (`core/skills/`, `<adapter>/skills/`, `user/skills/`) → never proactively, only when explicitly invoked

A session that never enters the development or review phase (a question answered by
reading code, a one-off lookup) never pays the token cost of loading standards —
§3's matching procedure itself is unchanged, only *when in the session* it runs.

## 6 — Workflow

```
Task arrives → 2_new_task.md
  - Identify project + detect stack(s)
  - Load adapter/generic standards
  - Understand task + epic
  - Optional: party-mode discussion
  - Propose breakdown, confirm
  - Create context file
      ↓
For each step → 3_implement.md
  - Implement + test (use adapter-specific workflow if present)
  - Save SPEC+PLAN to a `## Step NN` section in specs/<type>_<slug>.md
    (or that component's own specs/<type>_<slug>_<component>.md, if multi-component)
      ↓
On close → 4_close_task.md
  - Run tests
  - Code review (optional)
  - Propose commit message(s)
  - Record historic entry (if enabled)
  - Delete context file, resume paused task (if any)
```

## Essential rules

- [ ] Never implement before SPEC is confirmed
- [ ] Never make architecture decisions silently — surface trade-offs, wait for input
- [ ] Apply adapter + user standards (not optional; flag conflicts immediately)
- [ ] When SPEC is written: record PR URL in context frontmatter + every SPEC file
- [ ] At session start: glob `~/.reins/user/projects/<project-slug>/contexts/*.md`, find `status: active`
- [ ] Run multi-agent tasks in parallel when no dependencies exist

**Reference (on-demand):** See `2_new_task.md` (new task), `3_implement.md` (development), `4_close_task.md` (close task).
