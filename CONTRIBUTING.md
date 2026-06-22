# Contributing to REINS Method

REINS Method is a bash CLI + Node.js installer + a set of Markdown workflow files.
This document is for contributors who want to understand the internals, report issues,
or submit pull requests.

---

## Project structure

```
reins-method/
├── core/
│   ├── workflow/          ← 1_orchestrator, 2_new_task, 3_implement, 4_close_task
│   ├── templates/         ← context, spec, plan, adapter, skill templates
│   ├── evaluation/        ← historic mode docs + templates
│   └── skills/            ← built-in skills (reins-skill-creator, reins-party-mode,
│                              reins-code-review, reins-business-analyst,
│                              reins-technical-writer, reins-product-manager,
│                              reins-ux-designer, reins-system-architect,
│                              reins-senior-engineer, reins-investigate,
│                              reins-correct-course, reins-faq, reins-config,
│                              reins-remind)
├── agents/                ← generated bridge file templates (README inside)
├── bin/reins              ← the CLI (bash, no runtime dependencies)
├── tools/
│   └── installer/
│       └── cli.js         ← `npx reins-method install` (Node, @clack/prompts)
├── install.sh             ← curl | bash entry point (no Node required)
├── package.json           ← npm package for the installer
├── VERSION                ← single source of truth for the version number
├── ADAPTERS.md            ← adapter pack contract and authoring guide
├── SKILLS.md              ← skill authoring guide
├── HISTORIC_MODE.md       ← historic mode documentation
└── MIGRATION.md           ← upgrade notes between versions
```

---

## How the CLI works (`bin/reins`)

`bin/reins` is a single bash script with no external dependencies beyond `git`
and standard POSIX utilities. Key sections:

### Configuration

All user state lives under `~/.reins/` — never inside project repos.

```bash
REINS_HOME="${REINS_HOME:-$HOME/.reins}"
CORE_DIR="$REINS_HOME/core"
USER_DIR="$REINS_HOME/user"
AGENTS_DIR="$REINS_HOME/agents"
```

`config_get` / `config_set` read and write `~/.reins/user/config.yaml` using
`grep` and `sed` (no YAML parser required).

### Bridge generation (`generate_bridges`)

Called by `reins install`, `reins update`, and `reins sync`. Reads the current
config (agents, adapters, historic mode, language) and writes identical content
to all four bridge files:

- `~/.reins/agents/CLAUDE.md`
- `~/.reins/agents/GEMINI.md`
- `~/.reins/agents/AGENTS.md`
- `~/.reins/agents/copilot-instructions.md`

Then calls `wire_all_agents` to link each bridge into the corresponding agent's
native config directory, and `sync_skills` to register skills with Claude Code's
native skill discovery.

Bridge content includes: orchestrator reference, user standards references, active
adapters, historic mode, language settings, and the registered skill list.

### Skill registration (`sync_skills`)

`collect_skills` walks `core/skills/`, `user/skills/`, and any installed adapter's
`skills/` directories. Each skill is identified by its `SKILL.md` frontmatter
(`name:`, `description:`). The registered list is written into every bridge file
and symlinked into the relevant agent skill directories for native skill discovery.

Each sync performs a clean refresh: `cleanup_skill_links` removes all existing
`reins-*` symlinks before recreating them. There is no risk of skill duplication
across multiple syncs.

### Agent wiring (`wire_all_agents`)

Wires each agent the user has configured (stored in `config.yaml` via
`config_get_agents`). Only configured agents are wired — not all agents
installed on the machine. For each configured agent, writes an import or inline
reference into its native config file:

- `import` mode (Claude Code, Gemini): native config contains `@~/.reins/agents/AGENT.md`
- `inline` mode (Copilot, Codex, Aider): native config contains the full bridge
  content, because these agents do not support file imports

### Version management

`VERSION` is the single source of truth. `package.json` must match. The release
pipeline is tag-based:

```bash
# bump VERSION and package.json manually, then:
git tag v<version>
git push origin main --tags
# GitHub Actions publishes to npm on tag push
```

---

## How skills work

A skill is a directory containing a single `SKILL.md` file. The frontmatter
declares `name:`, `description:`, optional `allowed-tools:` and `tags:`.

```
core/skills/reins-<function>/
└── SKILL.md
```

Skills are **never loaded proactively** — the agent loads them only when the user
explicitly invokes them (by name or slash command). The bridge file lists all
registered skills so the agent knows they exist without loading their content.

To add a built-in skill, create a directory under `core/skills/reins-<function>/`
with a `SKILL.md`. Run `reins sync` to register it. Follow the template in
`core/templates/skill.md`.

Use `reins-skill-creator` (invoke `/reins-skill-creator` in your agent) for
guided authoring.

---

## How adapters work

An adapter pack is a directory under `~/.reins/user/adapters/<name>/` containing:

```
<name>/
├── ADAPTER.md             ← declares name, stacks[], author, version, description
├── standards/
│   └── floor.md           ← non-negotiable stack conventions (highest precedence)
├── workflow/
│   └── 3_implement.md     ← optional override of the implementation phase
└── skills/                ← optional adapter-specific skills
    └── <function>/
        └── SKILL.md
```

The orchestrator matches `stacks:` in `ADAPTER.md` against project marker files.
Multi-stack projects load all matching adapters. Adapter skills are registered
with a `reins-<adapter>-<function>` prefix.

See [ADAPTERS.md](ADAPTERS.md) for the full contract.

---

## Standards precedence

Three layers, enforced in this order:

1. **Adapter floor** (`<adapter>/standards/floor.md`) — stack/framework
   non-negotiables, set by the adapter author
2. **Company** (`~/.reins/user/standards/company.md`) — team or project behavioral
   rules, set by the user; mandatory
3. **Personal** (`~/.reins/user/standards/personal.md`) — individual style
   preferences, additive; must never conflict with company

Conflicts between layers are flagged by the orchestrator before implementation
starts.

---

## Workflow files

The four core workflow files are plain Markdown instructions the agent reads:

| File | Phase |
|---|---|
| `core/workflow/1_orchestrator.md` | Session start — stack detection, adapter loading, context lookup |
| `core/workflow/2_new_task.md` | New task — understand, propose breakdown, flag decisions, confirm |
| `core/workflow/3_implement.md` | Implementation — SPEC → implement → verify (adapter can override) |
| `core/workflow/4_close_task.md` | Close — summary, commit, historic entry, context cleanup |

Adapters may override `3_implement.md` to inject stack-specific TDD/SDD cycles.
They may not override `1_orchestrator.md`, `2_new_task.md`, or `4_close_task.md`.

---

## User data and privacy

Everything inside `~/.reins/user/` — standards, adapters, skills, task contexts,
specs, and historic records — lives exclusively on the user's machine. REINS
makes no network requests and sends no data anywhere. Contributor code must not
introduce any telemetry, remote calls, or data collection of any kind.

---

## Submitting changes

- Open an issue before large changes to align on direction.
- PRs should be focused — one concern per PR.
- Changes to `core/workflow/*.md` or `core/skills/*/SKILL.md` affect every user's
  installed workflow on their next `reins update`. Treat them carefully.
- Changes to `bin/reins` must work with bash 3.2+ (macOS default).
- Changes to `tools/installer/cli.js` require Node ≥ 18.
- Bump `VERSION` and `package.json` together. Do not push tags manually —
  the release pipeline handles npm publish on tag push via GitHub Actions.

---

## Companion tools (optional)

REINS works without additional dependencies. Two optional tools integrate with it:

- **[headroom](https://github.com/chopratejas/headroom)** — token-efficient context
  compression for AI agents (works best with Claude Code; known Copilot limitations
  — [#1](https://github.com/gustavodiasp/reins-method/issues/1))
- **[graphify](https://github.com/safishamsi/graphify)** — codebase knowledge graph;
  `reins graphify` generates and stores the output outside the repo (code-only
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
