---
name: implement
description: Implement or modify a feature. Use when the user asks to add, change, or build functionality.
---

## Steps

1. Run /explore to build the work plan (target files, verification method).
2. Define success criteria before writing any code:
   a. **Testable change** → Write failing tests first that define "done."
   b. **Untestable change** (UI, config) → State the expected outcome explicitly.
3. Implement the change:
   - Follow the work plan from /explore. Do not expand scope mid-implementation.
   - Only modify files listed in the plan. If you discover additional files need changes,
     update the plan and inform the user before proceeding.
   - Follow existing style. Match naming, formatting, and patterns of surrounding code.
4. Run tests. All must pass (existing + new).
5. Update _NODE.md if needed (see CLAUDE.md > _NODE.md Rules for criteria).
6. Commit with a message that describes what was implemented and why.

## Constraints
- If 200 lines can be 50, rewrite.
- No unrequested abstractions, flexibility, or configurability.
- If implementation requires a new domain, use /new-domain instead.
- If implementation requires changes across 3+ domains, propose a plan to the user first.
