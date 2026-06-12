```
 @@@@@@@    @@@@@@   @@@  @@@  @@@
@@@@@@@@  @@@@@@@@  @@@  @@@  @@@
@@!  @@@  @@!  @@@  @@!  @@!  @@!
!@!  @!@  !@!  @!@  !@!  !@!  !@!
@!@@!@!   @!@!@!@!  @!!  !!@  @!@
!!@!!!    !!!@!!!!  !@!  !!!  !@!
!!:       !!:  !!!  !!:  !!:  !!:
:!:       :!:  !:!  :!:  :!:  :!:
 ::       ::   :::   :::: :: :::
 :         :   : :    :: :  : :

  Purposeful AI Workflow Method
  ──────────────────────────────────────────
  agent-agnostic · stack-agnostic
  globally installed · customizable
  ──────────────────────────────────────────
```

<p align="center">
  <a href="#quick-start"><img alt="Install" src="https://img.shields.io/badge/install-curl%20%7C%20bash-orange?style=flat-square"></a>
  <a href="#supported-agents"><img alt="Agents" src="https://img.shields.io/badge/agents-Claude%20%7C%20Gemini%20%7C%20Copilot%20%7C%20Codex%20%7C%20Aider-8A2BE2?style=flat-square"></a>
  <a href="#"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-bash%20%2B%20git-4EAA25?style=flat-square&logo=gnu-bash&logoColor=white"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square"></a>
</p>

# PAW Method — Purposeful Workflow Method

A universal, agent-agnostic AI pair-programming workflow. Install it once, globally,
and use it in every project — without ever adding files to a project repository.

---

## Why

Most AI coding workflows end up either:
- copy-pasted into every repo (drifts out of sync, leaks into commits), or
- tightly coupled to one company's stack and conventions (can't be shared or open-sourced)

PAW Method solves both: a small, **stack-agnostic core** that defines how you and your
AI agent move through a task (new task → implement → close task, with an optional
historic/performance-tracking mode), plus **user-owned adapter packs** that teach it
your company's or project's specific conventions and skills.

---

## Quick start

```bash
curl -fsSL https://raw.githubusercontent.com/gustavodiasp/paw-method/main/install.sh | bash
```

This clones PAW Method to `~/.paw/` and runs the setup wizard:
- pick your AI agent (Claude Code, GitHub Copilot CLI, Codex CLI, Gemini CLI, Aider, OpenCode, Cursor, other)
- optionally fill in your company/personal coding standards
- optionally enable Historic Mode (performance tracking)
- optionally install an adapter pack

Then restart your terminal/agent and run:

```bash
paw status
```

Open any project with your AI agent — PAW's orchestrator is now part of its
instructions and will detect the project's stack automatically.

### Where should I install this?

**Install once, in your home directory — not inside or next to your projects.**
`paw install` always installs to `~/.paw/`, regardless of where you run it from.

There's no need to create a parent folder containing all your projects, and no
need to install PAW per-project or per-workspace: PAW wires itself into each AI
agent's *global* config (`~/.claude/CLAUDE.md`, `~/.gemini/GEMINI.md`, etc. — see
"Supported agents" below), so every project you open with that agent
automatically gets PAW's orchestrator instructions and stack detection. One
global install covers every project on the machine, in every supported agent.

### Why `curl | bash` and not `npx`?

PAW is a bash CLI with no runtime dependencies — `npx` would mean publishing an
npm package and requiring Node.js just to run a shell script, which works
against the "no required dependencies" design goal. `curl | bash` (or `git
clone <repo> ~/.paw && ~/.paw/bin/paw install`) keeps the install footprint
minimal and matches how the CLI is actually distributed (`bin/paw`, a single
executable script).

---

## How it works

```
~/.paw/
├── core/        ← the workflow engine (updated via `paw update`)
├── user/        ← your config, standards, adapters, skills, project state, historic data
└── agents/      ← generated bridge files, one per AI agent
```

- **`core/`** defines the workflow phases: `1_orchestrator.md` (read first every
  session — detects stack, loads adapters, locates the active task), `2_new_task.md`
  (understand → breakdown → confirm), `3_implement.md` (SPEC → implement → verify),
  `4_close_task.md` (summary → commit → optional historic entry → cleanup).
- **`user/`** is yours. `paw update` never touches it. It holds your standards, your
  adapters, your custom skills, per-project task contexts/specs, and (optionally)
  monthly historic records.
- **`agents/`** holds generated files that each AI agent's native config imports or
  references — see [agents/README.md](agents/README.md).

No PAW file is ever written into a project repository. `.gitignore` hacks aren't
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
`~/.paw/user/projects/<project-slug>/contexts/`. See `core/workflow/1_orchestrator.md`
for the full model, including the "exactly one active context" invariant and the
multi-component branch guard.

---

## Adapters — teaching PAW your stack

An adapter pack is a folder with conventions (`standards/floor.md`), an optional
override of the implement phase (`workflow/3_implement.md`), and optional on-demand
skills (`skills/<name>/SKILL.md`). The orchestrator matches an adapter's declared
`stacks:` against marker files it finds in your project (`Gemfile`, `package.json`,
`pyproject.toml`, `go.mod`, ...).

```bash
paw new-adapter my-company
```

See [ADAPTERS.md](ADAPTERS.md) for the full contract. Adapters are **user-owned** —
keep them local, share them privately within your team, or publish them if there's
nothing proprietary inside.

---

## Skills — on-demand procedures

Skills are single `SKILL.md` files the agent loads only when relevant — never
proactively. Use the built-in meta-skill to create one:

```bash
paw new-skill my-skill
```

or invoke `skill-creator` for guided creation. See [SKILLS.md](SKILLS.md).

---

## Personas, Party Mode & Code Review

Six built-in persona skills give you BMAD-style perspectives natively, with no
external install — each named after its role (`paw-<role>`), with a character
identity for flavor:

| Skill | Persona | Lens |
|---|---|---|
| `paw-business-analyst` | Toby | Methodical, evidence-based (Porter, Minto Pyramid), represents every stakeholder — including the inconvenient ones — never takes sides |
| `paw-technical-writer` | Pam | CommonMark/DITA/OpenAPI, writes for the reader with zero context, diagrams over walls of text |
| `paw-product-manager` | Jim | Jobs-to-be-Done, pragmatic and people-focused, skeptical of complexity that doesn't earn its cost |
| `paw-ux-designer` | Erin | Deeply empathetic, thinks in user flows and friction points, every decision serves a genuine user need |
| `paw-system-architect` | David | Calm and strategic, favors proven tech, developer productivity, ties decisions to business value |
| `paw-senior-engineer` | Angela | Test-first (red/green/refactor), 100% passing before review, no shortcuts |

Each is callable individually ("give me David's take on this"). Before a
breakdown, ask for **`paw-party-mode`** — Michael (Facilitator) picks the relevant
personas (always Toby) and announces the lineup, each speaks in turn, then Jim
(Synthesizer) distills it into what matters for the breakdown. Before proposing a
commit message, ask for **`paw-code-review`** — Michael opens the session and
launches independent subagents (Dwight for logic, Creed for security, and Oscar for
requirements if a SPEC exists) for adversarial, parallel review; Jim then closes
with a plain-language summary of what needs fixing before merge.

---

## Historic Mode — optional performance tracking

```bash
paw historic on
```

Each closed task can leave a short entry in a monthly file under
`~/.paw/user/historic/`. On request, PAW compiles a Monthly Summary to support
self-assessment and check-ins. All data is local and user-owned. See
[HISTORIC_MODE.md](HISTORIC_MODE.md).

---

## Companion tools (optional)

PAW has no required dependencies, but its workflow is designed to take advantage of
these tools if you choose to install them separately:

- **[headroom](https://github.com/chopratejas/headroom)** — token-efficient context
  compression for AI agents. Wrap your agent to cut context usage without losing
  comprehension:
  ```bash
  pip install "headroom-ai[all]"
  headroom wrap <agent>
  ```
- **[graphify](https://github.com/safishamsi/graphify)** — generates a knowledge
  graph of your codebase (code, docs, SQL, PDFs, images) at `graphify-out/`. PAW's
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
paw install              First-time setup (interactive wizard)
paw update                Pull latest core, regenerate agent bridge files
paw new-adapter <name>    Scaffold a new adapter pack
paw new-skill <name>      Scaffold a new skill
paw sync                  Regenerate agent bridges + skill registration (no git pull)
paw link-agents           Wire any newly-installed AI agents into existing bridges
paw historic on|off       Enable/disable historic mode
paw status                Show installed version, agent, adapters, historic mode
paw doctor                Validate the installation
paw uninstall             Unhook PAW from your agent/shell, optionally delete ~/.paw
```

---

## Supported agents

PAW doesn't just wire the one agent you pick during `paw install` — every `paw
update`/`paw sync` run wires **every agent it finds installed on the machine**
(detected by the presence of that agent's config directory), plus a generic
`~/AGENTS.md` fallback used by tools without a dedicated config directory:

| Agent | Bridge mechanism | Detected via |
|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` imports `~/.paw/agents/CLAUDE.md` | `~/.claude/` exists |
| Gemini CLI | `~/.gemini/GEMINI.md` imports `~/.paw/agents/GEMINI.md` | `~/.gemini/` exists |
| GitHub Copilot CLI | `~/.copilot/instructions.md` references `~/.paw/agents/copilot-instructions.md` | `~/.copilot/` exists |
| Codex CLI | `~/.codex/AGENTS.md` references `~/.paw/agents/AGENTS.md` | `~/.codex/` exists |
| Aider / OpenCode / Cursor / other | `~/AGENTS.md` references `~/.paw/agents/AGENTS.md` | always wired |

The agent you pick during `paw install` is just your *default* for `paw
status`/`paw doctor` — it doesn't limit which agents get PAW's instructions.
If you install a new AI agent later, run `paw link-agents` to wire it in
without a full `paw update`. Run `paw doctor` to check your default agent's
bridge is wired correctly.

---

## Project structure (this repo)

```
paw-method/
├── core/
│   ├── workflow/        ← 1_orchestrator, 2_new_task, 3_implement, 4_close_task
│   ├── templates/        ← context, current_task, adapter, skill, spec, plan templates
│   ├── evaluation/        ← historic mode docs + templates
│   └── skills/            ← paw-skill-creator, paw-party-mode, paw-code-review,
│                              paw-business-analyst, paw-technical-writer,
│                              paw-product-manager, paw-ux-designer,
│                              paw-system-architect, paw-senior-engineer
├── agents/                ← generated bridge file templates
├── bin/paw                ← the CLI
├── install.sh             ← curl | bash entry point
├── ADAPTERS.md
├── SKILLS.md
├── HISTORIC_MODE.md
└── MIGRATION.md
```

---

## Inspiration

PAW Method's design borrows specific ideas from these projects (full credit to their
authors — nothing here is a fork or a dependency):

- **[spec-kit](https://github.com/github/spec-kit)** (GitHub) — the per-feature
  `specs/<feature>/{spec,plan}.md` artifact separation that shaped
  `specs/<type>_<slug>/step-NN-{spec,plan}.md` and `core/templates/{spec,plan}.md`.
- **[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** — the
  multi-persona "Party Mode" discussion and the adversarial, parallel code-review
  pattern, reimplemented natively as `paw-party-mode`, `paw-code-review`, and the six
  `paw-business-analyst`/`paw-technical-writer`/`paw-product-manager`/
  `paw-ux-designer`/`paw-system-architect`/`paw-senior-engineer` persona skills.
- **[headroom](https://github.com/chopratejas/headroom)** — token-efficient context
  compression; documented as an optional companion tool (see "Companion tools"
  above).
- **[graphify](https://github.com/safishamsi/graphify)** — codebase knowledge-graph
  generation; the orchestrator (`1_orchestrator.md` §2.5) reads its
  `graphify-out/GRAPH_REPORT.md` output if present (see "Companion tools" above).
- **[ruflo](https://github.com/ruvnet/ruflo)** — informed thinking on fluid
  interlinking of workflow phases; no dedicated subsystem was added, but it shaped
  how `1_orchestrator.md` surfaces optional steps (project map, party-mode,
  code-review) inline in the workflow diagram.

---

## License

MIT (or your choice — update before publishing).
