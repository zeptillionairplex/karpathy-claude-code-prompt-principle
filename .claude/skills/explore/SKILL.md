---
name: explore
description: Identify the target area for a task and load only the necessary context. Use when starting any new task to understand which files to read.
---

## Steps

1. Extract keywords from the user's request to identify the likely domain folder.
2. Navigate to the target area using this priority:
   a. `_NODE.md` exists → read it. This gives you Purpose, Public API, Dependencies, Files.
   b. No `_NODE.md` → `ls` the folder only. Do NOT read individual files yet.
   c. If the target area is unclear, `ls` the `domains/` (or `src/`) root to find candidates.
3. From _NODE.md, decide what to read next:
   - Need to understand the public interface? → read `index.ts`/`index.js`
   - Need to understand a dependency? → read that dependency's `_NODE.md`, not its source
   - Need implementation details? → read only the specific file listed in _NODE.md > Files
4. Output a work plan:
   - Target files to modify (with line-level precision if possible)
   - Files that will NOT be touched (explicit exclusion)
   - Verification method for the change

## Constraints
- Maximum 4 tool calls for exploration. If you need more, stop and ask the user to narrow scope.
- Never read a file that isn't referenced by _NODE.md or directly requested by the user.
- Never `ls` more than 2 directories in a single explore.
- If no _NODE.md exists and the project has no CNA structure, fall back to standard exploration.

---

## _NODE.md Update Rules

> Migrated from CLAUDE.md

- Structural summary file in domain/feature folders.
- Update Files section on file add/delete/rename.
- Update Public API section on index.js changes.
- Update Dependencies section on new external imports.
- Do NOT touch _NODE.md for internal logic-only changes.
