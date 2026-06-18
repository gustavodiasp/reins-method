---
scope: always
role: master — read first every session, defines stack detection and routing
---

# REINS Orchestrator

This file defines how the agent and the user work together on every task, in every project, regardless of stack or AI agent.

**Read this file first, every session.** It detects the project's stack, loads the right adapter (if one is installed), locates the active task context, and routes to the correct workflow phase.

---

## 0 — Where REINS lives

REINS Method is installed once, globally, at `~/.reins/`. **No REINS files ever live inside a project repository.**

```
~/.reins/
├── core/                     ← this engine (updated via `reins update`)
│   ├── workflow/             ← phase files (this file + 2/3/4)
│   ├── templates/            ← context, current_task, adapter, skill templates
│   ├── evaluation/           ← historic mode templates
│   └── skills/               ← meta-skills (e.g. reins-skill-creator)
├── user/                     ← user-owned, never touched by `reins update`
│   ├── config.yaml           ← name, agent, active adapter, historic mode, language, doc_language
│   ├── standards/            ← company.md (floor) + personal.md
│   ├── adapters/             ← installed adapter packs
│   ├── skills/               ← user's custom skills
│   ├── projects/             ← per-project state (contexts, specs, graphify output)
│   │   └── <project-slug>/
│   │       ├── contexts/
│   │       ├── graphify-out/ ← project map (run `reins graphify` to generate)
│   │       └── specs/
│   │           └── <type>_<slug>/
│   │               ├── step-01-spec.md
│   │               ├── step-01-plan.md
│   │               └── ...
│   └── historic/             ← optional monthly tracking (if historic mode is on)
└── agents/                   ← generated bridge files per AI agent
```

---

## 0.5 — Language

Your agent bridge file's "Language" section (generated from `~/.reins/user/config.yaml`'s
`language` and `doc_language`, both default `english`) sets two independent things for
this entire session:

- **Interaction language** (`language`) — the language you use to talk to the user:
  chat replies, questions, breakdowns, and all output from REINS skills/personas
  (party-mode, code-review, etc.).
- **Documentation language** (`doc_language`) — the language used when *writing*:
  code comments, docstrings, commit messages, READMEs, SPECs, and other generated docs.

If a project's existing code/docs are already consistently written in a different
language than `doc_language`, follow the project's existing convention instead —
don't introduce a second language into an established codebase. When in doubt, ask.

---

## 1 — Identify the project

1. Determine the project root (nearest ancestor directory containing `.git`, or the current working directory if none).
2. Compute `<project-slug>` — a stable, filesystem-safe identifier for this project (e.g. derived from the repo name, or the git remote URL if available, or the absolute path with `/` replaced by `-`).
3. All state for this project lives under `~/.reins/user/projects/<project-slug>/`. Create this directory (with `contexts/` and `specs/`) if it does not exist yet.

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

## 2.5 — Project map (optional)

Check `~/.reins/user/projects/<project-slug>/graphify-out/GRAPH_REPORT.md` (generated
by running `reins graphify` — which wraps the external
[graphify](https://github.com/safishamsi/graphify) tool and stores its output outside
the repo, keeping the project directory clean).

- If it exists, read it at session start for an architecture overview before diving
  into the task — it's cheaper and broader than re-reading raw files. `graph.json`
  and `wiki/` are also available for deeper queries if needed.
- If it doesn't exist, skip silently. REINS does not require graphify; it only uses its
  output when present.
- Never look for `graphify-out/` inside the project repository — that location is no
  longer supported. Use `reins graphify` to generate and store the output correctly.

---

## 3 — Load the adapter (if any)

1. Read `~/.reins/user/config.yaml` for `adapters:` — a list of installed adapter packs, each with an `ADAPTER.md` declaring which stack(s) it applies to.
2. Match the detected stack(s) against installed adapters.
3. If a match is found, load (in this order):
   - `<adapter>/standards/floor.md` — non-negotiable conventions (precedence 1)
   - `<adapter>/standards/*.md` — any additional adapter standards (precedence 2, must never conflict with the floor)
   - `<adapter>/workflow/3_implement.md` — if present, **overrides** `core/workflow/3_implement.md` for the development phase
4. If no adapter matches, proceed with the generic conventions in `~/.reins/user/standards/company.md` and `~/.reins/user/standards/personal.md` (if the user has filled them in), and the generic `core/workflow/3_implement.md`.
5. If multiple stacks are detected (e.g. `ruby` + `node`), load every matching adapter. Steps in the breakdown are then labeled by which adapter/stack they belong to.

**Standards precedence rule:** if `personal.md` (or an adapter's secondary standards) contradicts the floor (`company.md` or `<adapter>/standards/floor.md`), **stop immediately** and ask the user to resolve the conflict before proceeding.

---

## 4 — Active context

Context files track the state of every work item for this project, under `~/.reins/user/projects/<project-slug>/contexts/`.

### Naming

```
<type>_<slug>.md
```
- `type`: `feature`, `hotfix`, `bugfix`, `chore`, `spike`
- `slug`: kebab-case short title

### Frontmatter

```yaml
---
type: feature        # feature | hotfix | bugfix | chore | spike
stack: <detected>    # e.g. ruby, node, ruby+node, python...
status: active       # active | paused
branches:            # map of component -> branch name, e.g. { backend: feature/123-x, frontend: feature/123-y }
prs:                 # map of component -> PR URL (null until opened)
title: <title>
updated_at: YYYY-MM-DD
---
```

### Invariant

**Exactly one context file per project may have `status: active` at any time.**

- On session start: glob `~/.reins/user/projects/<project-slug>/contexts/*.md`, read frontmatter, find the file with `status: active`.
- On interrupt (new task arrives while one is active): set the current active file to `status: paused`, create a new file with `status: active` (see `2_new_task.md`).
- On close: delete the closed file, list all `status: paused` files, ask which to resume.

### Branch guard (multi-component tasks)

When `branches` has more than one entry, before proceeding:

1. Run `git branch --show-current` in each relevant repo/worktree.
2. Compare with the corresponding entry in `branches`.
3. If any mismatch: present options (switch branch, update context, cancel). Do not proceed until aligned.

---

## 5 — Routing

### Always loaded (every session)

| File | When |
|---|---|
| `core/workflow/1_orchestrator.md` | Session start (this file) |
| Language settings (§0.5) | Session start |
| Active context file (§4) | Session start |
| Adapter standards (§3), or `~/.reins/user/standards/*.md` | Session start |
| `~/.reins/user/projects/<slug>/graphify-out/GRAPH_REPORT.md` (§2.5) | Session start, only if present |

### Phase-specific

| Phase | File |
|---|---|
| **New task** | `core/workflow/2_new_task.md` |
| **Development** | `<adapter>/workflow/3_implement.md` if present, else `core/workflow/3_implement.md` |
| **Close task** | `core/workflow/4_close_task.md` |

### On-demand (skills)

Skills in `~/.reins/core/skills/`, `<adapter>/skills/`, and `~/.reins/user/skills/` are **never loaded proactively**. Invoke them only when the user explicitly requests, or when the task clearly calls for it.

---

## 6 — The full workflow

```
New task arrives
      ↓
2_new_task.md
  → identify project + detect stack(s) (§1, §2)
  → load project map if present (§2.5)
  → load adapter standards, or generic standards (§3)
  → understand task + epic
  → optional: party-mode discussion (core/skills/reins-party-mode/SKILL.md)
  → propose breakdown (per component if multi-stack)
  → flag architecture decisions
  → wait for confirmation
  → create context file
      ↓
For each confirmed step:
  → 3_implement.md (adapter override or generic)
     SPEC/PLAN saved to specs/<type>_<slug>/step-NN-{spec,plan}.md
      ↓
User gives close order:
4_close_task.md
  → run tests (if applicable)
  → summarize what was done
  → assess epic impact
  → identify next step
  → optional: code review (core/skills/reins-code-review/SKILL.md)
  → review PR comments
  → propose commit message(s)
  → record historic entry (if historic mode is on)
  → clean specs/<type>_<slug>/ + delete context file
  → ask which paused context to resume
```

---

## 7 — General rules (permanent — never override)

- Never write or modify a SPEC — that step belongs to the user
- Apply the configured interaction and documentation languages (§0.5) at all times
- Never implement before the SPEC is provided and confirmed
- Never make architecture decisions silently — surface trade-offs and wait for input
- Never modify approved tests
- Apply adapter and user standards at all times — they are not optional
- If standards conflict, flag immediately and wait for a decision
- When in doubt about which file applies, ask
- When a PR is opened, record its URL in the context frontmatter (`prs`) and in every SPEC under `~/.reins/user/projects/<project-slug>/specs/` that belongs to this task
- When a task requires more than one agent, run them in parallel whenever there are no dependencies
- At session start, always glob `~/.reins/user/projects/<project-slug>/contexts/*.md` and read frontmatter to identify the active context

---

## Next steps

See `core/workflow/2_new_task.md` to start a new task, or continue with the active context using the development phase file (`3_implement.md`, adapter override if present).
