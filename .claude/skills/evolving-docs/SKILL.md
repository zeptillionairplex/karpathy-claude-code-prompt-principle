---
name: evolving-docs
description: Creates or updates CLAUDE.md in a domain/feature folder so documentation evolves automatically with the code. Use when creating a new domain, adding/removing files in a domain, or when asked to document a folder.
argument-hint: "[folder-path] (defaults to current domain being worked on)"
---

# Evolving Docs

## Purpose

This skill generates and maintains `CLAUDE.md` files **inside each domain/feature folder**.

Claude Code automatically loads `CLAUDE.md` from every parent directory of the current file.
This means a `features/auth/CLAUDE.md` is loaded when working on `features/auth/api/authApi.ts`
— giving any AI or human contributor instant, zero-search context for that slice.

**The contract:** documentation lives next to code. When code changes, the doc changes.
No separate wiki. No stale README. No "what does this folder do?" questions.

---

## When to Run

- After `/new-domain` creates a folder (run immediately after)
- After adding or deleting files inside a domain
- After renaming or moving a module
- After the Public API (index.ts exports / handler routes) changes
- Periodically before a PR to catch drift

---

## Folder CLAUDE.md Template

```markdown
# {Folder Name}

## Layer
{FSD: app | pages | widgets | features | entities | shared}
{Clean Arch: entities | use_cases | interfaces | infrastructure}

## Purpose
{Why this folder exists — 1–2 sentences. What user problem does it solve?}

## Files
| File | Role |
|------|------|
| {filename} | {one-line description} |

## Public API
{What this slice exposes to the outside world}
- For frontend: exports from index.ts
- For backend: HTTP routes / service methods / exported functions

## Depends On
- {Other slices or packages this imports from}

## Must NOT Depend On
- {Sibling slices at same layer that would create circular deps}
- {Higher layers that would violate dependency direction}

## Constraints
- {Layer-specific rules, e.g. "no DB calls here", "no business logic here"}
- {Any non-obvious invariants or team decisions}
```

---

## Workflow

### Step 1: Identify Target Folder

If an argument was given, use that path. Otherwise, determine from current session context
(the folder being worked on). Confirm with user if ambiguous.

### Step 2: Scan the Folder

```bash
ls -la {folder-path}
```

Read every non-test file in the folder (skip `__tests__/`, `*.test.ts`, `*_test.go`).
Identify:
- What files exist
- What they export / what functions/routes they define
- What they import from (dependency scan)

Use `grep` for import lines:
```bash
# TypeScript
grep -n "^import" {folder-path}/**/*.ts 2>/dev/null | head -60

# Go
grep -n "^import\|\"" {folder-path}/*.go 2>/dev/null | head -60

# Python
grep -n "^from\|^import" {folder-path}/*.py 2>/dev/null | head -60
```

### Step 3: Determine Layer

**Frontend (FSD)** — match by folder path segment:
| Path contains | Layer |
|---------------|-------|
| `/app/` | app |
| `/pages/` | pages |
| `/widgets/` | widgets |
| `/features/` | features |
| `/entities/` | entities |
| `/shared/` | shared |

**Backend (Clean Architecture)** — match by file names present:
| Files present | Layer |
|---------------|-------|
| `entities.go`, `model.go`, `models.py` only | entities |
| `service.go`, `use_case.go`, `service.py` | use_cases |
| `handler.go`, `router.py`, `controller.go` | interfaces |
| `repository.go`, `repository.py`, `db.go` | infrastructure |

If the folder contains multiple layer files (e.g., `handler.go` + `service.go`), note it as
a mixed domain slice — all Clean Architecture layers for one domain in one folder.

### Step 4: Check for Existing CLAUDE.md

```bash
cat {folder-path}/CLAUDE.md 2>/dev/null
```

- **Exists** → UPDATE: preserve existing content, only change what differs.
  Never remove a Constraint or Dependency entry without checking it's truly gone.
- **Does not exist** → CREATE from template.

### Step 5: Write CLAUDE.md

Fill the template from Step 2 data:
- **Files table**: one row per non-test file. Role = what it does in one clause.
- **Public API**: read `index.ts` exports or route definitions.
- **Depends On**: list unique top-level import paths (not relative `./` — those are internal).
- **Must NOT Depend On**: apply layer rules from `react.md` / `go.md` / `python.md`.
- **Constraints**: copy relevant rules from the layer's rule file.

Write with the Write tool if new, Edit tool if updating.

### Step 6: Check Parent CLAUDE.md

If the folder is a new slice (just created), check if the parent layer folder has its own
`CLAUDE.md`. If yes, add a reference row to its **Sub-slices** section:

```markdown
## Sub-slices
| Slice | Purpose |
|-------|---------|
| [auth](./auth/CLAUDE.md) | User authentication and session management |
```

If the parent has no `CLAUDE.md`, skip — don't cascade upward uninvited.

### Step 7: Verify

Re-read the written `CLAUDE.md`. Check:
- [ ] Layer is correctly identified
- [ ] Every file in the folder has a row in Files table
- [ ] Public API matches actual exports/routes (grep-verify if uncertain)
- [ ] No placeholder text remains (`{...}`)
- [ ] Constraints reference the actual rule (not copy-paste generic text)

---

## Evolution Rules

These rules keep docs alive as the project grows:

1. **Code change = doc change.** Any skill that adds/removes/renames a file in a domain
   SHOULD call `/evolving-docs {folder}` at the end — or manually update the Files table.

2. **Drift detection.** If a file exists in the folder but has no row in CLAUDE.md → drift.
   If CLAUDE.md lists a file that no longer exists → drift. Fix immediately.

3. **No duplication.** Folder `CLAUDE.md` describes THIS folder only.
   Do not duplicate content from parent or sibling CLAUDE.md files.

4. **No speculation.** Only document what currently exists. No "planned" sections.
   Planned features belong in a task list, not in documentation.

5. **80-line budget.** If CLAUDE.md grows past 80 lines, extract verbose content
   to a separate `_DECISIONS.md` in the same folder and link to it.

---

## Integration with Other Skills

| Event | Action |
|-------|--------|
| `/new-domain` creates folder | Run `/evolving-docs {folder}` immediately after |
| `/implement` adds a new file | Update Files table in folder's CLAUDE.md |
| `/refactor` moves a file | Update source and destination folder CLAUDE.md |
| `/manage-skills` runs | Also check for CLAUDE.md drift in changed folders |

---

## Related Files

| File | Purpose |
|------|---------|
| `.claude/rules/react.md` | FSD layer rules (source of Must NOT Depend On for frontend) |
| `.claude/rules/go.md` | Clean Architecture layer rules (source for backend constraints) |
| `.claude/rules/python.md` | Clean Architecture layer rules for Python |
| `.claude/skills/new-domain/SKILL.md` | New domain creation (triggers this skill) |
| `.claude/skills/manage-skills/SKILL.md` | Skill drift detection |

---

## Exceptions

1. **`shared/ui/` and `shared/lib/`** — These may have many small files. A single-row
   "utility functions" entry is acceptable instead of one row per file.
2. **Test folders** (`__tests__/`, `*_test.go`) — Do NOT list test files in the Files table.
   Note their existence in Constraints only if coverage expectation matters.
3. **Root-level `CLAUDE.md`** — This skill does not touch the project root `CLAUDE.md`.
   That file is managed by the project owner, not by this skill.
4. **Auto-generated files** — `*.pb.go`, `schema.gen.ts`, migration files — skip these in
   the Files table. One line in Constraints: "Contains generated files — do not edit."
