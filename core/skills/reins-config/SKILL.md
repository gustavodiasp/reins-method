---
name: reins-config
description: >
  Guided configuration wizard for REINS Method. Shows current state, explains
  each option before asking, and writes only to ~/.reins/user/ — never to core.
  Invokes reins-faq for deeper explanations when needed.
allowed-tools: [bash, read]
tags: [meta, config, setup]
---

# REINS Config

Guided configuration wizard. Shows what's configured, explains the "why" of each
option, and helps you extract maximum value from REINS — without touching core files.

## Trigger

- User asks to "configure REINS", "set up my REINS", "review my REINS setup",
  "change language", "configure historic mode", or similar
- Explicitly invoked as `reins-config`

## Context

Read `~/.reins/user/config.yaml` for current state. All changes go to `~/.reins/user/`
only. Core (`~/.reins/core/`) is never modified under any circumstances — if the user
wants to change core behaviour, direct them to open a GitHub issue at the REINS repo.

Run `reins sync` at the end of any session that made changes.

## Steps

### 1 — Read and present current state

Run `cat ~/.reins/user/config.yaml` and present a clear summary before asking anything:

```
Current REINS configuration:
  ✓ Interaction language: Portuguese
  ✓ Documentation language: English
  ✓ Historic mode: ON
  ✓ Agents: claude-code, copilot
  ○ Company standards: not configured
  ○ Personal standards: not configured
  ○ Adapter packs: none installed
```

### 2 — Ask what the user wants to do

Present three options:
1. **Full walkthrough** — review and update all settings one by one
2. **Specific option** — configure one thing (user names it)
3. **Gap analysis** — show what's available but not yet configured

### 3 — Configure each option (explain before asking)

#### Language (`language`, `doc_language`)

Explain first: *"These are two independent settings. Interaction language controls how
the agent talks to you in chat. Documentation language controls what's written in code
comments, commit messages, and READMEs. You can mix them freely — for example, chat in
Portuguese but write docs in English."*

Then ask each one with its current value shown.

To update, edit `~/.reins/user/config.yaml` directly (these have no dedicated CLI command).

#### Historic Mode (`historic_mode`)

Before asking to enable, present 2–3 concrete use cases and ask which resonates:

*"Historic mode records a short entry per closed task. People use it for: (1) tracking
where time goes across a month, (2) generating evidence for performance reviews, or
(3) finding recurring friction patterns. Does any of these match what you'd want?"*

If yes: enable with `reins historic on`, and mention the optional mini-retrospective
(3 questions at task close, always skippable).

If the user wants more detail before deciding: *"For a fuller picture of what historic
mode can do, I can answer specific questions — or you can ask `reins-faq` directly
about historic mode."*

#### Agents (`agents`)

Show current configured agents. If the list needs changing, say: *"Run `reins agents`
in your terminal — it opens an interactive selector that also re-wires all agent
bridges automatically."* Do not attempt to edit the agents list manually.

#### Company standards (`~/.reins/user/standards/company.md`)

Read the file. If it contains only the template placeholder text, explain:
*"Company standards are non-negotiable coding conventions the agent follows in every
session — things like 'always write tests', 'no raw SQL', 'use the repository pattern'.
The agent reads this file at session start."*

Offer to open it: *"I can open it with `reins edit standards` — you fill in your
team's conventions and run `reins sync` after."*

If already filled: show the first few non-empty lines and confirm it's still current.

#### Personal standards (`~/.reins/user/standards/personal.md`)

Same approach as company standards. Note that personal standards layer on top of
company standards — any conflict is flagged by the orchestrator and must be resolved
before proceeding.

#### Adapter packs (`~/.reins/user/adapters/`)

Check if any adapters exist. If none: explain *"Adapter packs teach REINS your stack's
conventions — TDD cycles, framework-specific rules, custom skills. If you work
consistently on one or two stacks, an adapter is the single highest-leverage
configuration you can add."*

Offer to scaffold: *"Run `reins new-adapter my-company` to create the scaffold —
then fill in your stack's conventions."*

If adapters exist: list them and confirm they're still relevant to the user's current work.

### 4 — Gap analysis (if requested or at end of full walkthrough)

Summarise what's configured vs what could add value:

```
You're using:     language settings, historic mode, 2 agents
Not yet using:    company standards, adapter packs

Highest-value next step: adapter packs — they enforce your stack's TDD/coding
conventions automatically on every project that matches the stack marker files.
```

### 5 — Apply and sync

For each change made, apply via CLI command if one exists:
- `reins historic on` / `reins historic off`
- Direct edit to `~/.reins/user/config.yaml` for language settings
- `reins edit standards` / `reins edit adapters` for file-based config

Run `reins sync` after any changes to refresh agent bridges.

## Constraints

- Never modify `~/.reins/core/` for any reason. If the user asks to change core
  behaviour, say: *"Core changes go through GitHub issues at the REINS repo — local
  edits to core get overwritten by `reins update`. Open an issue and it'll be picked
  up in a future release."*
- Always show current state before proposing changes.
- For complex explanations, offer `reins-faq` rather than going deep inline:
  *"I can explain further here, or `reins-faq` has a fuller answer on this."*
- Never overwrite parts of config the user didn't explicitly ask to change.

## Output

A session summary at the end:

```
Changes made:
  ✓ Historic mode: ON
  ✓ Company standards: opened for editing
  ✓ reins sync: run

No changes needed:
  - Language settings already correct
  - Agents list up to date
```
