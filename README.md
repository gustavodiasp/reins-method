```
      ,~~_              ____  ___________   _______
      |/\ =_ _ ~       / __ \/ ____/  _/ | / / ___/
       _( )_( )\~~    / /_/ / __/  / //  |/ /\__ \
       \,\  _|\ \~~~ / _, _/ /____/ // /|  /___/ /
          \`   \    /_/ |_/_____/___/_/ |_//____/
          `    `

  Structured AI Pair Programming Method
  ──────────────────────────────────────────────────
  Agent-agnostic · Stack-agnostic · Globally installed
```

<p align="center">
  <a href="#quick-start"><img alt="Install" src="https://img.shields.io/badge/install-npx%20reins--method-orange?style=flat-square"></a>
  <a href="#supported-agents"><img alt="Agents" src="https://img.shields.io/badge/agents-Claude%20%7C%20Gemini%20%7C%20Copilot%20%7C%20Codex%20%7C%20Aider-8A2BE2?style=flat-square"></a>
  <a href="#"><img alt="Dependencies" src="https://img.shields.io/badge/dependencies-bash%20%2B%20git%20(installer%3A%20node)-4EAA25?style=flat-square&logo=gnu-bash&logoColor=white"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/license-MIT-yellow?style=flat-square"></a>
</p>

# REINS Method

**One install. Every project. Any AI agent.**

A structured, SPEC-first AI pair programming workflow that lives in your home
directory — never inside your repos — and activates automatically in every
project you open, with any supported AI agent.

---

## The problem with AI pair programming today

Most AI coding setups break down in one of three ways:

- **Config drift** — `CLAUDE.md`, `.github/copilot-instructions.md`, `AGENTS.md`
  scattered across every repo. Out of sync, leaked into commits, duplicated endlessly.
- **Agent lock-in** — your workflow is tied to one tool. Switching agents means
  rebuilding your setup from scratch.
- **No structure** — the agent runs ahead of you. It skips planning, jumps to
  implementation, and ignores your standards. You spend more time correcting than
  coding.

REINS solves all three.

---

## What you get

- **Automatic wiring, zero per-project setup** — install once in `~/.reins/` and
  every project you open gets the full workflow automatically. Nothing is added to
  your repos.
- **Truly agent-agnostic** — Claude Code, GitHub Copilot CLI, Gemini CLI, Codex
  CLI, Aider, OpenCode, Cursor. Switch agents anytime. Your workflow, standards,
  and task history follow you.
- **Context that persists across sessions and agents** — active tasks, specs, and
  decisions are saved between sessions in `~/.reins/user/projects/`. Open a project
  days later with a different agent and pick up exactly where you left off.
- **SPEC-first workflow** — the agent proposes a breakdown, flags architecture
  decisions, and waits for your confirmation before writing a single line of code.
  You stay in control.
- **Company + personal standards, properly weighted** — define your team's
  non-negotiable rules in `company.md` and your personal style in `personal.md`.
  Both are enforced. Neither overrides the other. Conflicts are caught before they
  happen.
- **Built-in expert panel** — six on-demand AI personas (Business Analyst, Product
  Manager, UX Designer, System Architect, Senior Engineer, Technical Writer) for
  multi-angle task discussion and adversarial code review. No external tools needed.
- **Fully customizable** — adapter packs teach REINS your stack's conventions.
  Custom skills add on-demand procedures. Override any workflow phase without
  touching the core.
- **Session reliability** — if your agent drifts mid-session, one skill invocation
  re-anchors it on your configured standards and workflow. No manual context
  reconstruction.
- **Historic mode** — optional monthly tracking of closed tasks for self-assessment
  and check-ins. All data local and user-owned.

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
project you open gets this behavior automatically, with no REINS files in the repo.

---

## Quick start

```bash
npx reins-method@latest install
```

The setup wizard guides you through:
- Pick your AI agent (Claude Code, GitHub Copilot CLI, Codex CLI, Gemini CLI,
  Aider, OpenCode, Cursor, or other)
- Set your company and personal coding standards (optional — defaults work out of
  the box)
- Enable Historic Mode for performance tracking (optional)
- Install an adapter pack for your stack (optional)
- Choose interaction and documentation languages (default: English)

Restart your terminal/agent, then:

```bash
reins status
```

Open any project — REINS is already active.

No Node.js? Use the plain bash installer instead:

```bash
curl -fsSL https://raw.githubusercontent.com/gustavodiasp/reins-method/main/install.sh | bash
```

### Install once, not per project

`reins install` always installs to `~/.reins/`. REINS wires itself into each
AI agent's *global* config (`~/.claude/CLAUDE.md`, `~/.gemini/GEMINI.md`, etc.),
so every project you open automatically gets the workflow. One install covers
every project on the machine, with every supported agent.

### Why does the installer need Node?

Only the *installer* uses Node, for the arrow-key menus. Everything you run
afterwards — `reins update`, `reins sync`, `reins new-adapter`, etc. — is plain
bash with no runtime dependencies. No Node? `install.sh` runs the same wizard
with `read -p` prompts.

---

## How it works

```
~/.reins/
├── core/    ← workflow engine (updated via `reins update`)
├── user/    ← your config, standards, adapters, skills, project contexts, historic data
└── agents/  ← generated bridge files, one per AI agent
```

- **`core/`** defines the workflow phases: `1_orchestrator.md` (read first every
  session — detects stack, loads adapters, locates the active task),
  `2_new_task.md` (understand → breakdown → confirm), `3_implement.md`
  (SPEC → implement → verify), `4_close_task.md` (summary → commit → cleanup).
- **`user/`** is yours. `reins update` never touches it. Holds your standards,
  adapters, custom skills, per-project task contexts/specs, and optional historic
  records.
- **`agents/`** holds the generated files that each AI agent's native config
  imports or references.

No REINS file is ever written into a project repository.

---

## The workflow

```
New task arrives
      ↓
Detect stack · load adapter · locate active context
      ↓
Understand task · propose breakdown · flag architecture decisions
      ↓
Wait for your confirmation
      ↓
For each confirmed step: SPEC → implement → verify
      ↓
Summary · commit message · optional historic entry · context cleanup
```

Task context (one active context per project) persists at
`~/.reins/user/projects/<project-slug>/contexts/` across sessions and agents.

---

## Standards — three layers, clear responsibilities

| Layer | File | What goes here |
|---|---|---|
| **Adapter floor** | `<adapter>/standards/floor.md` | Stack/framework non-negotiables: framework conventions, tooling, file structure |
| **Company** | `~/.reins/user/standards/company.md` | Team or project behavioral rules — mandatory: testing philosophy, PR standards, documentation conventions |
| **Personal** | `~/.reins/user/standards/personal.md` | Your individual style — additive, never overriding company |

Precedence is enforced: adapter floor → company → personal. Conflicts between
layers are caught before any implementation starts.

**Example:**
- Company: *"Tests must describe system behavior, not implementation."*
- Personal: *"Group all expectations for one behavior in a single `it` block
  using `aggregated_failures`."*

Both applied. No conflict. Both mandatory.

---

## Adapters — teach REINS your stack

An adapter pack adds your stack's non-negotiable conventions (`floor.md`), an
optional implementation phase override for TDD/SDD cycles, and optional on-demand
skills.

```bash
reins new-adapter my-company
```

The orchestrator matches adapter `stacks:` against marker files in your project
(`Gemfile` → ruby, `package.json` → node, `pyproject.toml` → python, `go.mod` →
go, etc.). Multi-stack projects load multiple adapters simultaneously.

Adapters are user-owned — keep them local, share privately within your team, or
publish them. See [ADAPTERS.md](ADAPTERS.md).

---

## Skills — on-demand procedures

Skills are `SKILL.md` files the agent loads only when invoked — never
proactively. Each `reins sync` / `reins update` refreshes skill registration
cleanly (removes stale entries before re-registering), so there is no risk of
skill duplication across syncs. Create your own with:

```bash
reins new-skill my-skill
```

Or invoke `reins-skill-creator` for guided creation. See [SKILLS.md](SKILLS.md).

---

## Expert personas, Party Mode & Code Review

Six built-in persona skills give you a multi-angle expert panel natively:

| Skill | Perspective |
|---|---|
| `reins-business-analyst` | Methodical, evidence-based — represents every stakeholder, never takes sides |
| `reins-product-manager` | Jobs-to-be-Done, pragmatic — skeptical of complexity that doesn't earn its cost |
| `reins-ux-designer` | Deeply empathetic — thinks in user flows and friction points |
| `reins-system-architect` | Calm and strategic — favors proven tech, ties decisions to business value |
| `reins-senior-engineer` | Test-first — red/green/refactor, 100% passing before review, no shortcuts |
| `reins-technical-writer` | CommonMark/DITA/OpenAPI — writes for the reader with zero assumed context |

**`reins-party-mode`** — before a breakdown, bring the relevant personas together.
Each speaks independently, a synthesizer distills what actually matters for your
decision.

**`reins-code-review`** — before a commit, spawn independent subagents for
adversarial parallel review (logic, security, requirements). Closes with a
plain-language summary of what needs fixing before merge.

**`reins-remind`** — if your agent drifts mid-session and stops applying your
configured standards, invoke this. Output: *"Ops! Let me focus again!"* — the
agent re-reads your standards and re-anchors on the workflow.

---

## Historic Mode

```bash
reins historic on
```

When enabled, a hook fires at the end of every closed task and records a short
entry under `~/.reins/user/historic/`. What you do with that data is entirely
up to you — track your own velocity, feed it into a review process, build a
personal knowledge base, or anything else. REINS provides the hook and the
storage; you decide the purpose. All data is local and user-owned.
See [HISTORIC_MODE.md](HISTORIC_MODE.md).

---

## CLI reference

```
reins install              First-time setup (interactive wizard)
reins update               Pull latest core, regenerate agent bridge files
reins sync                 Regenerate agent bridges + skill registration (no git pull)
reins new-adapter <name>   Scaffold a new adapter pack
reins new-skill <name>     Scaffold a new skill
reins link-agents          Wire any newly-installed AI agents into existing bridges
reins historic on|off      Enable/disable historic mode
reins graphify             Run graphify and store output in ~/.reins (not the repo)
reins status               Show installed version, agent, adapters, historic mode
reins doctor               Validate the installation
reins edit home            Open all of ~/.reins/ in your IDE
reins edit standards       Your company and personal code standards
reins edit adapters        Your adapter packs
reins edit skills          Your custom skills
reins edit config          Your REINS configuration
reins uninstall            Unhook REINS from your agent/shell, optionally delete ~/.reins
```

---

## Supported agents

During `reins install` you can configure one or more agents at once — pick
everything you use. Every `reins update` / `reins sync` re-wires all configured
agents automatically:

| Agent | Bridge mechanism |
|---|---|
| Claude Code | `~/.claude/CLAUDE.md` imports `~/.reins/agents/CLAUDE.md` |
| Gemini CLI | `~/.gemini/GEMINI.md` imports `~/.reins/agents/GEMINI.md` |
| GitHub Copilot CLI | `~/.copilot/instructions.md` references `~/.reins/agents/copilot-instructions.md` |
| Codex CLI | `~/.codex/AGENTS.md` references `~/.reins/agents/AGENTS.md` |
| Aider / OpenCode / Cursor / other | `~/AGENTS.md` references `~/.reins/agents/AGENTS.md` |

The agent you mark as *primary* during setup is used by `reins status` and
`reins doctor` — it doesn't restrict which agents get the workflow. If you
install a new agent later, run `reins link-agents` to add it without a full
`reins update`.

---

## Your data stays on your machine

Everything inside `~/.reins/user/` — your standards, adapters, skills, task
contexts, specs, and historic records — lives exclusively on your machine.
REINS is a local tool: it reads and writes local files, makes no network
requests, and sends no data anywhere. The authors of REINS have no access to
any of your configuration or history.

---

## Uninstalling

```bash
reins uninstall
```

This unwires REINS from all configured agents and removes the CLI. By default,
`~/.reins/` is left intact — your standards, adapters, skills, and project
contexts are preserved. If you choose to delete `~/.reins/`, you are offered
the option to back up your `user/` folder first.

---

## Companion tools (optional)

REINS works without additional dependencies. Two optional tools integrate with it
if you choose to set them up:

- **[headroom](https://github.com/chopratejas/headroom)** — token-efficient context
  compression for AI agents (works best with Claude Code; known Copilot limitations
  — [#1](https://github.com/gustavodiasp/reins-method/issues/1))
- **[graphify](https://github.com/safishamsi/graphify)** — codebase knowledge graph;
  use `reins graphify` to generate and store it outside the repo (code-only
  extraction works without an API key; docs/papers require a separate LLM key
  — [#2](https://github.com/gustavodiasp/reins-method/issues/2))

---

## Inspiration

REINS borrows specific ideas from these projects — full credit to their authors,
nothing here is a fork or a dependency:

- **[spec-kit](https://github.com/github/spec-kit)** (GitHub) — the per-feature
  `specs/<feature>/{spec,plan}.md` artifact separation that shaped
  `specs/<type>_<slug>/step-NN-{spec,plan}.md` and the spec/plan templates.
- **[BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD)** — the
  multi-persona discussion and adversarial parallel code-review pattern,
  reimplemented natively as `reins-party-mode`, `reins-code-review`, and the six
  persona skills.
- **[ruflo](https://github.com/ruvnet/ruflo)** — informed thinking on fluid
  interlinking of workflow phases; shaped how `1_orchestrator.md` surfaces optional
  steps inline in the workflow diagram.

---

## License

MIT — see [LICENSE](LICENSE).
