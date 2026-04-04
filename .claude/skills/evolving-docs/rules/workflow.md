# Workflow

## Step 1: Identify Target Folder

If an argument was given, use that path. Otherwise, determine from current session context
(the folder being worked on). Confirm with user if ambiguous.

## Step 2: Scan the Folder

Read every non-test file in the folder (skip `__tests__/`, `*.test.ts`, `*_test.go`).
Identify what files exist, what they export, and what they import.

Use Grep for import lines:
- TypeScript: `^import` in `**/*.ts`
- Go: `^import` in `*.go`
- Python: `^from|^import` in `*.py`

## Step 3: Determine Layer

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

If the folder contains multiple layer files, note it as a mixed domain slice.

## Step 4: Check for Existing CLAUDE.md

- **Exists** → UPDATE: preserve existing content, only change what differs.
  Never remove a Constraint or Dependency entry without checking it's truly gone.
- **Does not exist** → CREATE from `rules/template.md`.

## Step 5: Write CLAUDE.md

Fill the template from Step 2 data:
- **Files table**: one row per non-test file. Role = what it does in one clause.
- **Public API**: read `index.ts` exports or route definitions.
- **Depends On**: list unique top-level import paths (not relative `./`).
- **Must NOT Depend On**: apply layer rules from `react.md` / `go.md` / `python.md`.
- **Constraints**: copy relevant rules from the layer's rule file.

Write with the Write tool if new, Edit tool if updating.

## Step 6: Check Parent CLAUDE.md

If the folder is a new slice, check if the parent layer folder has its own CLAUDE.md.
If yes, add a reference row to its **Sub-slices** section:

```markdown
## Sub-slices
| Slice | Purpose |
|-------|---------|
| [auth](./auth/CLAUDE.md) | User authentication and session management |
```

If the parent has no CLAUDE.md, skip — don't cascade upward uninvited.

## Step 7: Verify

- [ ] Layer is correctly identified
- [ ] Every file in the folder has a row in Files table
- [ ] Public API matches actual exports/routes
- [ ] No placeholder text remains (`{...}`)
- [ ] Constraints reference the actual rule
