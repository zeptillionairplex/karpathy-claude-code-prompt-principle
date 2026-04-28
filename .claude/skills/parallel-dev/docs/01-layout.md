# 1. Repo Layout & Layered CLAUDE.md

Claude Code auto-loads `CLAUDE.md` and `.claude/` walking upward from the
working directory. Layered placement gives each subagent only the context it
needs, with shared rules at the root.

## Recommended layout

```
project-root/
├── CLAUDE.md                 # thin: stack, folder map, absolute rules
├── .claude/
│   ├── skills/
│   └── settings.json
├── contracts/                # neutral zone — the API contract lives here
│   ├── openapi.yaml          # single source of truth
│   ├── CLAUDE.md             # rules for editing the spec
│   ├── STACK.md              # tech-stack registry (locked decisions)
│   └── examples/             # request/response samples
├── backend/                  # e.g. Go Gin / FastAPI
│   ├── CLAUDE.md             # backend-only conventions
│   ├── .claude/skills/       # backend-only skills
│   └── api/api.gen.go        # generated from openapi.yaml — do not edit
├── frontend/                 # e.g. React + TS
│   ├── CLAUDE.md             # frontend-only conventions
│   ├── .claude/skills/       # frontend-only skills
│   └── src/types/api.ts      # generated — do not edit
└── docs/
    └── research/             # decisions, ADRs, Q&A archives
```

## Why `contracts/` and not `backend/openapi.yaml`?
- A spec inside `backend/` signals ownership to the backend; the frontend agent
  drifts. Neutrality matters for parallel work.
- Git ownership/permissions can be split cleanly when the contract is its own dir.
- Subagents working in `backend/` or `frontend/` don't pull contract context
  unless they reference `../contracts/` explicitly — that's a feature.

## Why layered CLAUDE.md?
- Root: shared rules ("contract is sacred", "generated files are read-only").
- `contracts/`: spec-editing rules (versioning, examples, lint).
- `backend/`: language/framework conventions.
- `frontend/`: component/state/styling conventions.

Each subagent's working dir determines what it sees. No copy-paste of common
rules across folders — root inherits naturally.

## Absolute rules to put in root CLAUDE.md
- All API changes start in `contracts/openapi.yaml`.
- After spec change, run codegen on both sides before committing.
- Generated files (`*.gen.*`, `api.ts`) are read-only.
- Locked tech decisions live in `contracts/STACK.md`. Add a library only by
  amending STACK.md with a brief rationale.
