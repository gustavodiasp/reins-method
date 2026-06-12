# Current Task — Working Notes

This file is an optional companion to the active context file (`core/templates/context.md`).
Use it when a task benefits from a more detailed surface map than the context's `## Breakdown`
provides — e.g. a feature touching many files or layers. Adapters may extend this template
with stack-specific sections (e.g. a frontend adapter might add a "Components affected"
or "i18n keys" section) — see `core/templates/adapter.md`.

---

## User value
<!-- Written by the agent. What becomes easier, faster, safer, or clearer for the user. -->

---

## Surface map
<!-- Filled by the agent. List the modules, files, endpoints, or components this task touches. -->
- [ ] ...

---

## Constraints and non-negotiables
<!-- Filled by the agent at task start, from the active adapter's standards. -->
- [ ] Existing behavior preserved unless SPEC says otherwise

---

## Verification checklist
<!-- Filled by the agent before marking a step as done. Adapters may append stack-specific items. -->
- [ ] Main flow works
- [ ] Empty / loading / error states handled (if applicable)
- [ ] No unintended regressions found

---

## My notes
<!-- Written by me only. The agent never modifies this field. -->
