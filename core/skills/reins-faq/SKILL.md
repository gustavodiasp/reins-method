---
name: reins-faq
description: >
  Answers questions about REINS Method — what it is, how it works, where things
  live, and how to get the most out of each feature. Curated knowledge, not a
  docs redirect. Concrete examples over abstract descriptions.
allowed-tools: [read]
tags: [meta, faq, help]
---

# REINS FAQ

Answers questions about REINS Method directly from curated knowledge. Reads
current config when state-specific answers are needed. Never redirects to docs —
answers inline with examples.

## Trigger

- User asks "what is X in REINS?", "how does Y work?", "where does Z live?"
- Any question about REINS features, configuration, skills, or concepts
- Invoked by `reins-config` when a user needs explanation before deciding on a setting

## Context

Read `~/.reins/user/config.yaml` when the question is about current state (e.g.
"is historic mode on?"). Otherwise answer from the knowledge base below.

---

## Knowledge base

### What is REINS?

A global, agent-agnostic AI pair-programming workflow. Installed once at `~/.reins/`,
it wires itself into every AI agent's global config — so every project you open with
Claude, Copilot, Gemini, or Codex automatically gets the REINS orchestrator. No REINS
files ever live inside a project repository.

The core workflow:
```
New task → 2_new_task.md  (understand → breakdown → confirm → context file)
         → 3_implement.md (SPEC → PLAN → implement → verify → confirm)
         → 4_close_task.md (summary → epic impact → PR → historic entry → cleanup)
```

### Where does everything live?

```
~/.reins/
├── core/          ← the engine (updated by reins update — do not edit directly)
│   ├── workflow/  ← orchestrator + the 4 phase files
│   ├── skills/    ← built-in skills
│   └── templates/ ← context, spec, plan, adapter templates
├── user/          ← yours (never touched by reins update)
│   ├── config.yaml        ← language, historic mode, agents
│   ├── standards/         ← company.md + personal.md
│   ├── adapters/          ← installed adapter packs
│   ├── skills/            ← your custom skills
│   ├── projects/          ← per-project context files and specs
│   └── historic/          ← monthly performance entries
└── agents/        ← generated bridge files per AI agent
```

`user/` is yours. `core/` is updated by `reins update`. Changes to core behaviour
belong in a GitHub issue — not in local edits.

### What are adapter packs?

Adapter packs teach REINS your stack's specific conventions. A `my-company` adapter
for Rails + React can: enforce TDD cycles in the implement phase, add coding standards
(use Turbo, no `find_by`, always write request specs), and add custom skills for your
team's patterns.

Create one: `reins new-adapter my-company`
Edit one: `reins edit adapters`

The orchestrator matches an adapter's declared `stacks:` against your project's marker
files (`Gemfile`, `package.json`, etc.) and loads it automatically on every session.

### What are skills?

On-demand procedures loaded only when invoked — never proactively. Each skill is a
`SKILL.md` file with a clear trigger, steps, and output format.

Built-in skills:

| Skill | When |
|---|---|
| `reins-party-mode` | Multi-perspective discussion before a breakdown |
| `reins-code-review` | Adversarial parallel review before a commit |
| `reins-investigate` | Root-cause analysis before a bugfix breakdown |
| `reins-correct-course` | Mid-implementation divergence from confirmed spec |
| `reins-business-analyst` | Business/stakeholder perspective on a task |
| `reins-product-manager` | User value and jobs-to-be-done framing |
| `reins-system-architect` | Architecture decisions and trade-offs |
| `reins-senior-engineer` | TDD-first implementation lens — also standalone for a full session |
| `reins-ux-designer` | User flow, friction points, edge cases |
| `reins-technical-writer` | Documentation clarity and audience calibration |
| `reins-config` | Guided configuration wizard |
| `reins-faq` | This skill |

Create your own: `reins new-skill my-skill`

### What is Historic Mode?

Historic Mode records a short entry for each closed task in a monthly file at
`~/.reins/user/historic/YYYY-MM.md`. It runs automatically at task close. An optional
mini-retrospective (3 questions, ~2 minutes) can be appended to each entry.

Enable: `reins historic on` — Disable: `reins historic off`

**Why enable it?** People use it for very different things:

- **Track where your time goes.** Each entry records the task type and key decisions.
  After a month you can see whether you're spending most time on bugfixes, features,
  or chores — and whether that matches your actual goals.

- **Evidence for performance reviews.** Ask for a Monthly Summary at the end of each
  month: a structured breakdown of what you shipped, decisions made, and patterns
  observed. Paste it directly into a self-assessment.

- **Find your friction patterns.** The mini-retrospective captures what slowed you
  down per task. After 4–6 weeks, ask: "what appears most often in Friction?" — you
  get a real pattern you can act on (e.g. "I consistently underestimate scope on
  tasks touching the auth layer").

- **Measure workflow changes.** Ran without an adapter for 2 weeks, then added one?
  Historic entries let you compare task friction before and after with actual data.

- **Accountability.** Writing one sentence per closed task creates a lightweight
  forcing function to reflect rather than just ship.

### What are context files?

One `.md` file per active task, at `~/.reins/user/projects/<project-slug>/contexts/`.
Exactly one context can be `status: active` at a time.

It tracks: task type, stack, branches, breakdown steps, current step, decisions made,
and PR link. When a task is interrupted, it becomes `status: paused`. At resume, the
branch guard runs (checks you're on the right git branch before continuing).

### What are specs and plans?

For each step in a breakdown, two files are saved:

- `step-NN-spec.md` — written by **you**, saved by the agent. Expected behaviour,
  edge cases, guarantees.
- `step-NN-plan.md` — written by the **agent**. Confirms understanding and states
  how the step will be verified.

Both live at `~/.reins/user/projects/<slug>/specs/<type>_<slug>/`. They're deleted at
task close after the PR is merged — with your explicit confirmation.

### What CLI commands are available?

```
reins install           First-time setup (interactive wizard)
reins update            Pull latest core, regenerate bridges
reins sync              Regenerate bridges + skills (no download)
reins agents            Update which AI agents you use and re-wire
reins status            Show installed version, agents, historic mode
reins doctor            Validate the installation
reins edit standards    Edit company/personal coding standards
reins edit config       Edit REINS configuration
reins edit adapters     Edit adapter packs
reins edit skills       Edit custom skills
reins historic on|off   Enable/disable historic mode
reins new-adapter       Scaffold a new adapter pack
reins new-skill         Scaffold a new skill
reins uninstall         Remove REINS from agents and shell
```

---

## Steps

1. If the question is about current config state, read `~/.reins/user/config.yaml`.
2. Answer directly from the knowledge base — no "see the docs" redirects.
3. If the answer involves a configuration change, offer to hand off to `reins-config`.

## Output

Direct answers with concrete examples. If the question reveals a configuration gap,
name it and offer: *"Want me to walk you through configuring that? I can invoke
`reins-config` for a guided setup."*
