---
name: reins-investigate
description: >
  Forensic root-cause investigation before a bugfix breakdown. Establishes what
  is actually broken and why before implementation begins. Ends with a confirmed
  finding statement — never a fix proposal.
allowed-tools: [read, bash]
tags: [investigate, bugfix, root-cause]
---

# Investigate

Forensic root-cause analysis skill. Runs before breakdown on any `bugfix` task.
Investigation ends with a finding — not a solution.

## Trigger

- Task context type is `bugfix`, or the user describes broken behaviour
- Explicit user request: "investigate this", "what's actually happening here",
  "before we fix this"
- Mid-task when symptoms don't match the initial hypothesis

## Context

Load the active task context file. Read every file the user identifies as relevant.
Do **not** propose a fix during this skill — investigation ends at a confirmed
finding statement. Hand off to `core/workflow/2_new_task.md` Step 3 (breakdown) only
after the user confirms the finding.

## Steps

1. **Symptom statement** — restate the reported symptom in one sentence. Confirm
   with the user before proceeding: *"Is this an accurate description of what you're
   seeing?"*

2. **Reproduction** — identify the minimal conditions that trigger the bug:
   - What input, state, or sequence causes it?
   - Is it deterministic or intermittent?
   - What environment (dev / staging / prod, specific tenant, specific data)?

3. **Evidence gathering** — read the relevant files, logs, and test output. Cite
   every finding as `file:line`. Do not summarise without evidence. Label each
   finding explicitly:
   - **Confirmed:** directly observed in code or output
   - **Deduced:** logically follows from confirmed evidence
   - **Hypothesised:** plausible but not yet supported by evidence

4. **Causal chain** — trace the symptom back to a root cause. Stop at the earliest
   point in the chain where a fix would prevent all downstream symptoms. If multiple
   root causes are plausible, list each with its supporting evidence.

5. **Scope boundary** — state explicitly what is **not** broken. This prevents the
   fix from expanding into unrelated areas.

6. **Finding statement** — one sentence summarising the root cause. Present it to
   the user and wait for confirmation before handing off to breakdown.

## Output

Structured finding presented to the user before breakdown:

**Evidence log**
- Confirmed: `<evidence>` (`file:line`)
- Deduced: `<inference and its basis>`
- Hypothesised: `<hypothesis and why it's plausible>`

**Causal chain**
`<symptom>` ← `<intermediate cause>` ← `<root cause>`

**Scope boundary**
Not broken: `<list what was checked and confirmed working>`

**Finding statement**
`<one sentence: root cause>`

Do not propose a fix. The finding feeds directly into `2_new_task.md` Step 3
(breakdown) — breakdown begins only after the user confirms the finding.
