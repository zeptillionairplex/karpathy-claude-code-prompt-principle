# Evolution Rules & Integration

## Rules

1. **Code change = doc change.** Any skill that adds/removes/renames a file in a domain
   SHOULD call `/evolving-docs {folder}` at the end — or manually update the Files table.

2. **Drift detection.** File exists but has no row in CLAUDE.md → drift.
   CLAUDE.md lists a file that no longer exists → drift. Fix immediately.

3. **No duplication.** Folder CLAUDE.md describes THIS folder only.

4. **No speculation.** Only document what currently exists. No "planned" sections.

5. **80-line budget.** If CLAUDE.md grows past 80 lines, extract verbose content
   to `_DECISIONS.md` in the same folder and link to it.

## Integration with Other Skills

| Event | Action |
|-------|--------|
| `/new-domain` creates folder | Run `/evolving-docs {folder}` immediately after |
| `/implement` adds a new file | Update Files table in folder's CLAUDE.md |
| `/refactor` moves a file | Update source and destination folder CLAUDE.md |

## Exceptions

1. **`shared/ui/` and `shared/lib/`** — Many small files. A single "utility functions"
   entry is acceptable instead of one row per file.
2. **Test folders** — Do NOT list test files in the Files table.
3. **Root-level `CLAUDE.md`** — This skill does not touch the project root CLAUDE.md.
4. **Auto-generated files** (`*.pb.go`, `schema.gen.ts`) — Skip in Files table.
   One line in Constraints: "Contains generated files — do not edit."
