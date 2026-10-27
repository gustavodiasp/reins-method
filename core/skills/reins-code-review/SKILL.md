---
name: reins-code-review
description: >
  Adversarial, parallel code review orchestrating independent reviewer
  skills — not role-play. Michael (Facilitator) announces the session and
  selects which of `reins-logic-reviewer` (Dwight), `reins-security-reviewer`
  (Creed), and `reins-acceptance-reviewer` (Oscar) are worth calling for this
  diff — always as separate, individual subagents, never merged into one; after
  triage, Jim (Synthesizer) summarizes what needs fixing before merge. Use
  before proposing a commit message, on PRs, or whenever the user asks to
  "review this code"/"review this diff"/"review this PR".
allowed-tools: Agent
tags: [review, quality, multi-agent]
---

# Code Review — Selector + Independent Reviewer Skills

This skill **decides which reviewer skills are worth calling**, then spawns
each selected one as a **real, independent subagent** via the `Agent` tool —
genuine independence, no groupthink, each subagent only sees its own lens
(from its own `SKILL.md`: `reins-logic-reviewer`, `reins-security-reviewer`,
`reins-acceptance-reviewer`) and the diff. **Never merge two lenses into one
subagent's prompt** — if a diff's scope only warrants one lens, call that one
lens alone; the adversarial-independence property (no groupthink) only holds
when each subagent's view is genuinely its own. Michael (opening) and Jim
(closing) are framing roles *you* adopt directly — they don't get their own
subagent, don't become their own skill, and contribute no findings of their
own.

## Trigger

- The user asks to "review this code", "review this diff", "review this PR", or
  equivalent
- Optionally referenced from `core/workflow/4_close_task.md` near Step 5 (commit
  message), on request

## Context

- Requires the `Agent` tool (or equivalent subagent-spawning capability of the
  active AI coding agent) — real parallel subagents, not a simulated substitute.
  If unavailable, state plainly that this skill cannot run in this runtime; do not
  proceed with a single-model simulation.
- The three reviewer lenses are separate skills, read when selected (never
  inlined here): `core/skills/reins-logic-reviewer/SKILL.md`,
  `core/skills/reins-security-reviewer/SKILL.md`,
  `core/skills/reins-acceptance-reviewer/SKILL.md`.
- If a context file is active (`1_orchestrator.md` §4), its spec file's
  `## Step NN` → `### SPEC` sections are the source for
  `reins-acceptance-reviewer` —
  `specs/<type>_<slug>.md` (single-component) or every relevant component's own
  `specs/<type>_<slug>_<component>.md` (multi-component; resolve the component
  from the changed files' paths, not from guessing). **Multi-component tasks
  can also have an orphaned pre-split `specs/<type>_<slug>.md` (no suffix)
  holding steps from before a second component existed** (see
  `core/templates/task.md`) — if the changed files include steps recorded
  there, that file is a SPEC source too, not just the per-component files.

## Steps

### Step 1 — Gather context

1. Determine what to review: branch diff against the base branch, staged changes,
   a specific PR, or a commit range — ask the user if ambiguous.
2. Construct the unified diff for that scope.
3. Look for a SPEC: if a context file is active, check
   `~/.reins/user/projects/<project-slug>/specs/<type>_<slug>.md` (or, for a
   multi-component task, every component's own `specs/<type>_<slug>_<component>.md`
   **plus the same unsuffixed `specs/<type>_<slug>.md`, if it still exists
   alongside them, for any pre-split steps** — do not skip it just because it
   doesn't match the `_<component>` pattern)
   for the `## Step NN` sections covering the changed steps. If none found, Oscar
   is skipped (note this in the output).
4. Resolve applicable standards file paths — same resolution as
   `1_orchestrator.md` §3: active adapter's `standards/floor.md` + `standards/*.md`
   if one matched, otherwise `~/.reins/user/standards/company.md` +
   `personal.md`, plus this project's `~/.reins/user/projects/<project-slug>/standards.md`
   if it exists. These paths (not their content) are passed to each reviewer
   below — each subagent reads them itself.
5. Select which reviewer skills are worth calling — always as separate
   individual subagents, never merged:
   - `reins-logic-reviewer` (Dwight) — **always called.**
   - `reins-security-reviewer` (Creed) — called unless the diff is **small**
     (roughly under 50 changed lines) **and** touches no security-sensitive
     surface (auth, payments, access control, secrets handling). When unsure,
     call it.
   - `reins-acceptance-reviewer` (Oscar) — called only if a SPEC was found in
     Step 1.3.
   **Before applying the size-based skip for the security lens, check whether
   this project's `standards.md` (from step 4, if it exists) specifies its
   own review-mode rule** (e.g. "always use three-reviewer mode for this
   project") — honor it over the generic size heuristic, i.e. call
   `reins-security-reviewer` regardless of size. This lets one project opt
   into stricter review without hardcoding that project's name or paths into
   this shared skill.

### Step 2 — Review (parallel subagents)

**Michael (Facilitator) opens the session.** Read the diff context and the
selection from Step 1 and announce the review, in Michael's voice, before
launching anything — e.g. *"Okay everyone, we are doing a code review. This is
serious. I'm bringing in Dwight and Creed."* (add *"...and Oscar"* if a SPEC
was found), or, when the security lens was skipped: *"This one's small and
low-risk — Dwight alone covers it."* Michael does not review anything himself.

**Launch every selected reviewer skill via `Agent` in a single message**
(parallel, no dependencies between them — even when only one was selected,
spawn it the same way). For each: read that skill's `SKILL.md`
(`reins-logic-reviewer`, `reins-security-reviewer`, `reins-acceptance-reviewer`)
and pass the subagent exactly what its own `## Execution` section specifies —
the full diff, the standards file paths from Step 1, and (for
`reins-acceptance-reviewer` only) the relevant `### SPEC` section(s). Do not
let one subagent see another's instructions, and never combine two skills'
content into a single subagent's prompt — call fewer of them instead.

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
