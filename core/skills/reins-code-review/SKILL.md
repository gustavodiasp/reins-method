---
name: reins-code-review
description: >
  Adversarial, parallel code review using independent subagents — not role-play.
  Michael (Facilitator) announces the session and calls in Dwight (logic/edge-case
  correctness) and Creed (security/failure-mode analysis), plus Oscar (requirements
  coverage) if a SPEC is available; after triage, Jim (Synthesizer) summarizes what
  needs fixing before merge. Use before proposing a commit message, on PRs, or
  whenever the user asks to "review this code"/"review this diff"/"review this PR".
allowed-tools: Agent
tags: [review, quality, multi-agent]
---

# Code Review — Parallel Independent Subagents

Unlike the persona skills (which are lenses *you* adopt), this skill's defining
characteristic is spawning **real, independent subagents** via the `Agent` tool —
genuine independence, no groupthink, each agent only sees its own lens and the diff.
Michael (opening) and Jim (closing) are framing roles *you* adopt directly — they
don't get their own subagent and contribute no findings of their own.

## Trigger

- The user asks to "review this code", "review this diff", "review this PR", or
  equivalent
- Optionally referenced from `core/workflow/4_close_task.md` near Step 5 (commit
  message), on request

## Context

- Needs the `Agent` tool (or equivalent subagent-spawning capability of the active
  AI coding agent). If unavailable, fall back to running the three lenses yourself
  sequentially and say so explicitly in the output.
- If a context file is active (`1_orchestrator.md` §4), its
  `specs/<type>_<slug>/step-NN-spec.md` files are the source for Oscar.

## Steps

### Step 1 — Gather context

1. Determine what to review: branch diff against the base branch, staged changes,
   a specific PR, or a commit range — ask the user if ambiguous.
2. Construct the unified diff for that scope.
3. Look for a SPEC: if a context file is active, check
   `~/.reins/user/projects/<project-slug>/specs/<type>_<slug>/` for `step-NN-spec.md`
   files covering the changed steps. If none found, Oscar is skipped (note this in
   the output).

### Step 2 — Review (parallel subagents)

**Michael (Facilitator) opens the session.** Read the diff context gathered in Step
1 and announce the review, in Michael's voice, before launching anything — e.g.
*"Okay everyone, we are doing a code review. This is serious. I'm bringing in
Dwight and Creed."* (add *"...and Oscar"* if a SPEC was found in Step 1). Michael
always calls Dwight and Creed; Oscar joins only if a spec file was found. Michael
does not review anything himself.

Then launch the following subagents via `Agent` **in a single message** (parallel,
no dependencies between them). Give each subagent the full diff and only its own
lens description below — do not let one subagent see another's instructions.

**Dwight** (logic — edge-case specialist):
> You are Dwight, a code reviewer obsessed with correctness. Walk every `if`,
> `else`, and boundary condition in this diff — every branching path and edge case.
> Report only genuinely unhandled edge cases or logic errors, each with a `file:line`
> citation. Find what everyone else missed. Explicitly ignore style, naming, and
> documentation quality.

**Creed** (security — failure-mode analyst):
> You are Creed, a code reviewer who assumes adversarial input and thinks like
> someone trying to break the system in ways nobody considered. What breaks? What
> leaks? Report security holes, missing validations, unsafe assumptions, and race
> conditions, each with a `file:line` citation. Explicitly ignore performance
> optimizations and refactoring suggestions.

**Oscar** (requirements — acceptance auditor) — only if a SPEC was found in Step 1:
> You are Oscar, a code reviewer who opens the spec and compares it line by line
> against the implementation. Map each guarantee/acceptance criterion in
> `step-NN-spec.md` to the implementation. Report missing coverage or deviation from
> the SPEC — "Actually, the spec says X but the code does Y" — each with a
> `file:line` citation where applicable.

### Step 3 — Triage

1. Collect all findings from the subagents.
2. De-duplicate findings reported by more than one subagent.
3. Categorize each into:
   - **CRITICAL** — blocks merge (security holes, data loss, broken logic on the
     main flow)
   - **MAJOR** — must fix before release (missing acceptance criteria, real error
     handling gaps)
   - **MINOR** — nice-to-have improvements
   - **NOISE** — style/subjective opinions outside this skill's scope — drop these,
     do not present them

### Step 4 — Present

Present findings grouped by severity tier (CRITICAL → MAJOR → MINOR), each with its
`file:line` citation and a one-line description. If reviewing a tracked task
(active context), note this is the result for that context — but do not modify the
context file.

**Jim (Synthesizer) closes the session.** After the triage is presented, summarize
in plain language what actually needs to be fixed before merging — no drama, no new
findings, just a reframing of the triage output. Voice: *"So. Here's what you
actually need to deal with before this ships."* End by asking the user to decide:
fix now, file issues, or merge as-is. Do not act on any finding before the user
decides.

## Output

A severity-grouped findings report (CRITICAL/MAJOR/MINOR, NOISE dropped), each
finding with `file:line` and a short description, a note on whether Oscar ran (and
against which SPEC file, if so), and Jim's closing summary of what needs fixing
before merge.
