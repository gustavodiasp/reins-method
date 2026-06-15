```
      ,~~_              ____  ___________   _______
      |/\ =_ _ ~       / __ \/ ____/  _/ | / / ___/
       _( )_( )\~~    / /_/ / __/  / //  |/ /\__ \
       \,\  _|\ \~~~ / _, _/ /____/ // /|  /___/ /
          \`   \    /_/ |_/_____/___/_/ |_//____/
          `    `

  Structured AI pair programming method
  ──────────────────────────────────────────────────
  Agent-agnostic · stack-agnostic · globally installed
```

<p align="center">
  <a href="#quick-start"><img alt="Install" src="https://img.shields.io/badge/install-npx%20reins--method-orange?style=flat-square"></a>
  <a href="#supported-agents"><img alt="Agents" src="https://img.shields.io/badge/agents-Claude%20%7C%20Gemini%20%7C%20Copilot%20%7C%20Codex%20%7C%20Aider-8A2BE2?style=flat-square"></a>
  <a href="#"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-bash%20%2B%20git%20(installer%3A%20node)-4EAA25?style=flat-square&logo=gnu-bash&logoColor=white"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square"></a>
</p>

# REINS Method

A universal, agent-agnostic AI pair-programming workflow. Install it once, globally,
and use it in every project — without ever adding files to a project repository.

---

## Why

Most AI coding workflows end up either:
- copy-pasted into every repo (drifts out of sync, leaks into commits), or
- tightly coupled to one company's stack and conventions (can't be shared or open-sourced)

REINS Method solves both: a small, **stack-agnostic core** that defines how you and your
AI agent move through a task (new task → implement → close task, with an optional
historic/performance-tracking mode), plus **user-owned adapter packs** that teach it
your company's or project's specific conventions and skills.

---

## What it looks like

```
you:    Add a password reset endpoint to the API

agent:  Detected stack: ruby (Gemfile) + node (package.json)
        Loading adapter: acme-rails (matches `ruby`)

        This looks like a new feature. Proposed breakdown:
          1. POST /password_resets        — request a reset token
          2. POST /password_resets/:token — consume token, set new password
          3. Wire up email delivery via existing Mailer

        Architecture decision needed: store reset tokens in the DB or Redis
        with a TTL? Flagging this before we proceed.

        Create a context file and start on step 1?
```

The orchestrator instructions live in your AI agent's global config — every
project you open gets this behavior automatically, with no REINS files added to
the repo.

---

## Quick start

```bash
npx reins-method@latest install
```

This clones REINS Method to `~/.reins/` and runs the setup wizard — arrow-key
menus for:
- pick your AI agent (Claude Code, GitHub Copilot CLI, Codex CLI, Gemini CLI, Aider, OpenCode, Cursor, other)
- optionally fill in your company/personal coding standards
- optionally enable Historic Mode (performance tracking)
- optionally install an adapter pack
- choose your interaction language (default: English)
- choose your documentation language (default: English)

Then restart your terminal/agent and run:

```bash
reins status
```

Open any project with your AI agent — REINS's orchestrator is now part of its
instructions and will detect the project's stack automatically.

No Node.js? Use the plain bash installer instead — same questions, numbered
prompts instead of arrow-key menus:

```bash
curl -fsSL https://raw.githubusercontent.com/gustavodiasp/reins-method/main/install.sh | bash
```

### Where should I install this?

**Install once, in your home directory — not inside or next to your projects.**
`reins install` always installs to `~/.reins/`, regardless of where you run it from.

There's no need to create a parent folder containing all your projects, and no
need to install REINS per-project or per-workspace: REINS wires itself into each AI
agent's *global* config (`~/.claude/CLAUDE.md`, `~/.gemini/GEMINI.md`, etc. — see
"Supported agents" below), so every project you open with that agent
automatically gets REINS's orchestrator instructions and stack detection. One
global install covers every project on the machine, in every supported agent.

### Why does the installer need Node, if REINS is a bash CLI?

Only the *installer* (`npx reins-method install`) uses Node, for the arrow-key
menus. Everything you run afterwards — `reins update`, `reins sync`, `reins
new-adapter`, etc. — is plain bash with no runtime dependencies. No Node? `install.sh`
runs the same wizard with `read -p` prompts instead of menus.

---

## How it works

```
~/.reins/
├── core/        ← the workflow engine (updated via `reins update`)
├── user/        ← your config, standards, adapters, skills, project state, historic data
└── agents/      ← generated bridge files, one per AI agent
```

- **`core/`** defines the workflow phases: `1_orchestrator.md` (read first every
  session — detects stack, loads adapters, locates the active task), `2_new_task.md`
  (understand → breakdown → confirm), `3_implement.md` (SPEC → implement → verify),
  `4_close_task.md` (summary → commit → optional historic entry → cleanup).
- **`user/`** is yours. `reins update` never touches it. It holds your standards, your
  adapters, your custom skills, per-project task contexts/specs, and (optionally)
  monthly historic records.
- **`agents/`** holds generated files that each AI agent's native config imports or
  references — see [agents/README.md](agents/README.md).

No REINS file is ever written into a project repository. `.gitignore` hacks aren't
needed because there's nothing to ignore.

---

## The workflow

```
New task arrives
      ↓
2_new_task.md   — understand task & epic, propose breakdown, flag decisions, create context
      ↓
3_implement.md  — SPEC → implement → verify, per confirmed step
                  (adapters can override this with TDD/SDD-style cycles)
      ↓
4_close_task.md — summary, epic impact, commit message, PR review,
                  optional historic entry, context cleanup
```

Context files (one per active task, per project) live at
`~/.reins/user/projects/<project-slug>/contexts/`. See `core/workflow/1_orchestrator.md`
for the full model, including the "exactly one active context" invariant and the
multi-component branch guard.

---

## Adapters — teaching REINS your stack

An adapter pack is a folder with conventions (`standards/floor.md`), an optional
override of the implement phase (`workflow/3_implement.md`), and optional on-demand
skills (`skills/<name>/SKILL.md`). The orchestrator matches an adapter's declared
`stacks:` against marker files it finds in your project (`Gemfile`, `package.json`,
`pyproject.toml`, `go.mod`, ...).

```bash
reins new-adapter my-company
```

See [ADAPTERS.md](ADAPTERS.md) for the full contract. Adapters are **user-owned** —
keep them local, share them privately within your team, or publish them if there's
nothing proprietary inside.

---

## Skills — on-demand procedures

Skills are single `SKILL.md` files the agent loads only when relevant — never
proactively. Use the built-in meta-skill to create one:

```bash
reins new-skill my-skill
```

or invoke `reins-skill-creator` for guided creation. See [SKILLS.md](SKILLS.md).

---

## Personas, Party Mode & Code Review

Six built-in persona skills give you BMAD-style perspectives natively, with no
external install:

| Skill | Lens |
|---|---|
| `reins-business-analyst` | Methodical, evidence-based (Porter, Minto Pyramid), represents every stakeholder — including the inconvenient ones — never takes sides |
| `reins-technical-writer` | CommonMark/DITA/OpenAPI, writes for the reader with zero context, diagrams over walls of text |
| `reins-product-manager` | Jobs-to-be-Done, pragmatic and people-focused, skeptical of complexity that doesn't earn its cost |
| `reins-ux-designer` | Deeply empathetic, thinks in user flows and friction points, every decision serves a genuine user need |
| `reins-system-architect` | Calm and strategic, favors proven tech, developer productivity, ties decisions to business value |
| `reins-senior-engineer` | Test-first (red/green/refactor), 100% passing before review, no shortcuts |

Each is callable individually (e.g. "give me the system architect's take on
this"). Before a breakdown, ask for **`reins-party-mode`** — a facilitator picks the
relevant personas (always the business analyst) and announces the lineup, each
speaks in turn, then a synthesizer distills it into what matters for the
breakdown. Before proposing a commit message, ask for **`reins-code-review`** — it
launches independent subagents (logic, security, and requirements if a SPEC
exists) for adversarial, parallel review, then closes with a plain-language
summary of what needs fixing before merge.

---

## Historic Mode — optional performance tracking

```bash
reins historic on
```

Each closed task can leave a short entry in a monthly file under
`~/.reins/user/historic/`. On request, REINS compiles a Monthly Summary to support
self-assessment and check-ins. All data is local and user-owned. See
[HISTORIC_MODE.md](HISTORIC_MODE.md).

---

## Companion tools (optional)

REINS has no required dependencies, but its workflow is designed to take advantage of
these tools if you choose to install them separately:

- **[headroom](https://github.com/chopratejas/headroom)** — token-efficient context
  compression for AI agents. Wrap your agent to cut context usage without losing
  comprehension:
  ```bash
  pip install "headroom-ai[all]"
  headroom wrap <agent>
  ```
  Every session must be started through the wrapper (`headroom wrap claude`
  instead of `claude`). To avoid typing that every time, alias it in your shell
  rc file (e.g. `~/.zshrc`):
  ```bash
  alias claude="headroom wrap claude"
  ```
  This is fully optional — REINS works the same with or without headroom.
- **[graphify](https://github.com/safishamsi/graphify)** — generates a knowledge
  graph of your codebase (code, docs, SQL, PDFs, images) at `graphify-out/`. REINS's
  orchestrator (`1_orchestrator.md` §2.5) automatically reads
  `graphify-out/GRAPH_REPORT.md` at session start if present:
  ```bash
  pip install graphifyy && graphify install
  # then, in a project:
  /graphify .
  ```

---

## CLI reference

```
reins install              First-time setup (interactive wizard)
reins update                Pull latest core, regenerate agent bridge files
reins new-adapter <name>    Scaffold a new adapter pack
reins new-skill <name>      Scaffold a new skill
reins sync                  Regenerate agent bridges + skill registration (no git pull)
reins link-agents           Wire any newly-installed AI agents into existing bridges
reins historic on|off       Enable/disable historic mode
reins status                Show installed version, agent, adapters, historic mode
reins doctor                Validate the installation
reins uninstall             Unhook REINS from your agent/shell, optionally delete ~/.reins
```

---

## Supported agents

REINS doesn't just wire the one agent you pick during `reins install` — every `reins
update`/`reins sync` run wires **every agent it finds installed on the machine**
(detected by the presence of that agent's config directory), plus a generic
`~/AGENTS.md` fallback used by tools without a dedicated config directory:

| Agent | Bridge mechanism | Detected via |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` imports `~/.reins/agents/CLAUDE.md` | `~/.claude/` exists |
| Gemini CLI | `~/.gemini/GEMINI.md` imports `~/.reins/agents/GEMINI.md` | `~/.gemini/` exists |
| GitHub Copilot CLI | `~/.copilot/instructions.md` references `~/.reins/agents/copilot-instructions.md` | `~/.copilot/` exists |
| Codex CLI | `~/.codex/AGENTS.md` references `~/.reins/agents/AGENTS.md` | `~/.codex/` exists |
| Aider / OpenCode / Cursor / other | `~/AGENTS.md` references `~/.reins/agents/AGENTS.md` | always wired |

The agent you pick during `reins install` is just your *default* for `reins
status`/`reins doctor` — it doesn't limit which agents get REINS's instructions.
If you install a new AI agent later, run `reins link-agents` to wire it in
without a full `reins update`. Run `reins doctor` to check your default agent's
bridge is wired correctly.

---

## Project structure (this repo)

```
reins-method/
├── core/
│   ├── workflow/        ← 1_orchestrator, 2_new_task, 3_implement, 4_close_task
│   ├── templates/        ← context, current_task, adapter, skill, spec, plan templates
│   ├── evaluation/        ← historic mode docs + templates
│   └── skills/            ← reins-skill-creator, reins-party-mode, reins-code-review,
│                              reins-business-analyst, reins-technical-writer,
│                              reins-product-manager, reins-ux-designer,
│                              reins-system-architect, reins-senior-engineer
├── agents/                ← generated bridge file templates
├── bin/reins                ← the CLI
├── tools/installer/cli.js ← `npx reins-method install` (Node wizard, @clack/prompts)
├── install.sh             ← curl | bash entry point (no Node required)
├── package.json           ← npm package for the installer (`reins-method`)
├── ADAPTERS.md
├── SKILLS.md
├── HISTORIC_MODE.md
└── MIGRATION.md
```

---

## Inspiration

REINS Method's design borrows specific ideas from these projects (full credit to their
authors — nothing here is a fork or a dependency):

- **[spec-kit](https://github.com/github/spec-kit)** (GitHub) — the per-feature
  `specs/<feature>/{spec,plan}.md` artifact separation that shaped
  `specs/<type>_<slug>/step-NN-{spec,plan}.md` and `core/templates/{spec,plan}.md`.
- **[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** — the
  multi-persona "Party Mode" discussion and the adversarial, parallel code-review
  pattern, reimplemented natively as `reins-party-mode`, `reins-code-review`, and the six
  `reins-business-analyst`/`reins-technical-writer`/`reins-product-manager`/
  `reins-ux-designer`/`reins-system-architect`/`reins-senior-engineer` persona skills.
- **[headroom](https://github.com/chopratejas/headroom)** — token-efficient context
  compression; documented as an optional companion tool (see "Companion tools"
  above).
- **[graphify](https://github.com/safishamsi/graphify)** — codebase knowledge-graph
  generation; the orchestrator (`1_orchestrator.md` §2.5) reads its
  `graphify-out/GRAPH_REPORT.md` output if present (see "Companion tools" above).
- **[ruflo](https://github.com/ruvnet/ruflo)** — informed thinking on fluid
  interlinking of workflow phases; no dedicated subsystem was added, but it shaped
  how `1_orchestrator.md` surfaces optional steps (project map, reins-party-mode,
  reins-code-review) inline in the workflow diagram.

---

## License

MIT — see [LICENSE](LICENSE).
