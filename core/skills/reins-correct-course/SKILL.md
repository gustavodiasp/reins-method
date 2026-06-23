---
name: reins-correct-course
description: >
  Structured pause when implementation diverges from the confirmed spec. Diagnoses
  whether the spec is wrong or the implementation drifted before either is updated.
  Never resumes implementation without explicit user confirmation.
allowed-tools: [read]
tags: [correct-course, divergence, spec]
---

# Correct Course

Mid-implementation divergence handler. Invoked when implementation cannot satisfy
the confirmed spec as written, or when the user signals a mismatch.

## Trigger

- User signals divergence: "this isn't going as expected", "the spec doesn't match
  reality", "we need to rethink this", "correct course"
- Agent detects a contradiction between the confirmed spec and what the
  implementation requires to proceed

Do not invoke proactively — only when divergence is explicit.

## Execution

Spawn a fork for the diagnostic phase — the fork reads spec and implementation
files and builds the divergence report without blocking the main thread. The main
agent handles the options confirmation with the user.

1. Announce: "Diagnosing divergence..."
2. Spawn a fork with this SKILL.md content, the active spec file path, and the
   relevant implementation files. Instruct the fork to execute Steps 1–3 and return
   the structured divergence report.
3. When the fork returns, present the options (Step 4) and wait for user confirmation
   before updating the spec or resuming implementation.

Never use ScheduleWakeup to wait for the fork — it completes and returns directly.

## Context

Load the active task context and the current step's spec file at
`~/.reins/user/projects/<project-slug>/specs/<type>_<slug>/step-NN-spec.md`. Read the
current implementation state. Do not resume implementation until the divergence is
resolved and the spec is updated if needed.

## Steps

1. **State the divergence** — one sentence describing exactly where implementation
   and spec contradict each other. Cite `spec-file:line` and `implementation-file:line`.

2. **Classify the divergence** — one of three types:
   - **Spec is wrong** — the spec made an assumption that reality has invalidated.
     The implementation direction is correct; the spec needs updating.
   - **Implementation drifted** — the implementation departed from the spec without
     a justified reason. The spec is correct; the implementation needs correcting.
   - **New information** — neither is wrong; something emerged during implementation
     that the spec could not have anticipated. Both need updating.

3. **Impact assessment** — what has already been built that depends on the divergent
   assumption? List affected files and steps.

4. **Options** — present two or three concrete paths forward with trade-offs. Apply
   David's Rule of Three: do not propose a new abstraction unless three independent
   cases justify it. Wait for user confirmation before proceeding.

## Output

**Divergence:** `<one sentence, spec:line vs implementation:line>`

**Classification:** Spec is wrong / Implementation drifted / New information

**Impact**
- Affected files: `<list>`
- Affected steps: `<list>`

**Options**
1. `<option>` — `<trade-off>`
2. `<option>` — `<trade-off>`
3. `<option if applicable>` — `<trade-off>`

**Chosen path:** `<filled after user confirmation>`

Update the spec file to reflect the chosen path before resuming `3_implement.md`.
Do not continue implementing until the user explicitly confirms the chosen path.
