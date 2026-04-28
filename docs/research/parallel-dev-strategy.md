# Parallel Dev Strategy — Q&A Archive

Curated questions and answers that drove the `parallel-dev` skill and the
`contracts/` + `backend/` + `frontend/` skeleton in this repo.

Cross-references:
- Skill (operational guide): `.claude/skills/parallel-dev/`
- Skeleton: `contracts/CLAUDE.md`, `backend/CLAUDE.md`, `frontend/CLAUDE.md`
- Original raw notes: `memo.md`

---

## Q1. Code-first vs Spec-first for AI-paired development

**Decision: Spec-first.**

Why AI changes the calculus:
1. **Single source of truth** — `openapi.yaml` is one file the agent points
   at; code-first scatters truth across handlers, comments, DTOs, and FE
   types. Drift is the default.
2. **Compile-time verification** — codegen produces interfaces. If the AI
   writes a handler that doesn't satisfy the contract, the build fails.
   Code-first lets the AI invent shapes that pass build but break the FE.
3. **FE/BE consistency by construction** — `oapi-codegen` (Go) and
   `openapi-typescript` (TS) generate from the same yaml. Field rename in
   spec → both sides update; type errors highlight every call site.
4. **Smaller, more accurate context** — point the agent at one path of
   `openapi.yaml`, not several handler files.
5. **Refactor safety** — "unify error responses" is a yaml edit + regen,
   not a hunt across handlers.

The historical downsides of spec-first (yaml verbosity, OpenAPI fluency,
setup overhead) all relax in an AI-paired environment, because authoring
and editing the spec is itself an AI task.

**Recommended workflow** (Claude Code + Go Gin + React):
```
1. Spec design     — natural-language requirements → openapi.yaml
2. Codegen (BE)    — oapi-codegen → Go interfaces + types
3. BE implement    — agent implements the generated interface
4. Codegen (FE)    — openapi-typescript → TS types
5. FE hooks        — TanStack Query hooks against generated types
6. Spec change     — edit yaml, re-run 2 + 4
```

---

## Q2. Where to keep `openapi.yaml`?

**Decision: `contracts/` at the repo root, not inside `backend/` or `frontend/`.**

- `contracts/` is a neutral zone. The name signals contract, not docs — agents
  and humans treat it more carefully than another file under `docs/`.
- Inside `backend/`, ownership reads as "backend's file", and the FE agent
  may miss it when its CWD is `frontend/`.
- Permissions and CODEOWNERS are clean when the contract is a top-level dir.

Layout:
```
project-root/
├── contracts/
│   ├── openapi.yaml        # the contract
│   ├── CLAUDE.md           # rules for spec edits
│   ├── STACK.md            # tech-stack registry (locked decisions)
│   └── examples/           # sample request/response payloads
├── backend/                # Go Gin / FastAPI / …
├── frontend/               # React / Next / …
├── docs/                   # ADRs, research, internal docs
└── CLAUDE.md               # root rules
```

Root CLAUDE.md must enforce:
- All API changes start with `contracts/openapi.yaml`.
- After spec change, run codegen on both sides before commit.
- Generated files (`*.gen.go`, `src/types/api.ts`) are read-only.
- New libraries land via ADR + `contracts/STACK.md`.

---

## Q3. Sequential vs parallel BE/FE? Where does the human step in?

**Decision: spec freeze first, then **parallel** BE + FE.**

- **FE-first (sequential)** — UX clarity, but mock dependence creates rework
  when real API arrives.
- **BE-first (sequential)** — solid data model, but FE blocks; over-built
  endpoints accrue.
- Both sequential modes also bleed context: AI agents lose state across long
  gaps. Stale context degrades consistency.

Parallel works **iff the spec is stable**. With a frozen `openapi.yaml`:
- BE agent: spec → codegen → handlers → tests.
- FE agent: spec → codegen → hooks → components (Prism mock fills the gap
  until real BE is up: `prism mock contracts/openapi.yaml`).

Mandatory human checkpoints:
- Requirements → spec translation (domain knowledge).
- Major spec changes (new resource, auth model, pagination, error format).
- Security decisions (JWT vs session, CORS, validation depth, sensitive
  data handling).
- Performance tradeoffs (N+1, caching, page size, chunking).

Recommended cadence (small project, 1 day):
```
AM 30m   human: requirements + spec freeze
AM 2-3h  agents: parallel implementation
Noon 15m human: PR-style midpoint review
PM 2-3h  agents: integration + tests
EOD 30m  human: smoke + tomorrow's priorities
```

Conflict prevention rules:
- Only the main agent edits `contracts/openapi.yaml`; subagents read.
- Generated files are read-only (header marker + CLAUDE.md note).
- CI runs `redocly lint contracts/openapi.yaml` and contract tests.

---

## Q4. Where do shared `CLAUDE.md` and skills live? Copy, link, or layer?

**Decision: **layered/distributed**, not copied.**

Claude Code auto-loads `CLAUDE.md` and `.claude/` walking upward from the
working directory. Layered placement gives each subagent the minimum
relevant context.

- **Copy** — bad. Two sources of truth drift; agents see redundant context.
- **Symlink to a master `~/dev-knowledge`** — fine on Linux/WSL, fragile on
  Windows native, awkward to commit.
- **Layered** — best. Root `CLAUDE.md` thin (overview, absolute rules);
  domain `CLAUDE.md` per folder.

Layout:
```
~/dev-knowledge/                     # master (out-of-tree)
├── CLAUDE.md                        # base coding principles
├── skills/                          # canonical skills
└── templates/{root,backend,frontend}-claude.md

project-root/
├── CLAUDE.md                        # thin (≤ 100 lines)
├── .claude/{commands,settings.json}
├── contracts/CLAUDE.md              # spec-edit rules
├── backend/
│   ├── CLAUDE.md                    # BE conventions
│   └── .claude/skills/              # BE-only skills
├── frontend/
│   ├── CLAUDE.md                    # FE conventions
│   └── .claude/skills/              # FE-only skills
└── docs/
```

Skill placement rule: put a skill at the **closest** folder that needs it.
Token budget is per-load; an unused skill in scope is wasted budget.

| Skill | Location |
|---|---|
| Go Gin handler patterns | `backend/.claude/skills/` |
| React component patterns | `frontend/.claude/skills/` |
| OpenAPI authoring | `contracts/.claude/skills/` (or root) |
| Generic git/commit | root `.claude/skills/` |

Master-to-project bootstrap script — run at `git init`, not by hand:
```bash
# ~/dev-knowledge/init-project.sh
PROJECT=$1
KNOWLEDGE=~/dev-knowledge

cp $KNOWLEDGE/templates/root-claude.md     $PROJECT/CLAUDE.md
mkdir -p $PROJECT/{backend,frontend}/.claude/skills
cp $KNOWLEDGE/templates/backend-claude.md  $PROJECT/backend/CLAUDE.md
cp $KNOWLEDGE/templates/frontend-claude.md $PROJECT/frontend/CLAUDE.md
cp $KNOWLEDGE/skills/go-gin.md             $PROJECT/backend/.claude/skills/
cp $KNOWLEDGE/skills/openapi.md            $PROJECT/backend/.claude/skills/
cp $KNOWLEDGE/skills/react-typescript.md   $PROJECT/frontend/.claude/skills/
cp $KNOWLEDGE/skills/tanstack-query.md     $PROJECT/frontend/.claude/skills/
```

QMD interaction: keep a thin `.claude/index.qmd` per scope. Root `CLAUDE.md`
points at it. Agents read the index first and pull only the docs they need —
that's the token-efficient path.

---

## Q5. Context7 MCP vs local `optional/` skills, and Context7 CLI status

Sourced 2026-04: independent benchmarks + upstash/context7 GitHub.

**Token cost.** Context7 MCP averages ~3,300 tokens/query (vs ~9,700 raw
doc insertion); local `.claude/skills/optional/` is 0 tokens at query time
(already in scope when loaded).

**Accuracy.** A 2025 benchmark put Context7 contextual accuracy at ~65%
across 20 real-world SDK scenarios. It struggles with very fresh APIs in
fast-moving frameworks. Local docs are stale by definition but under our
control — no third-party drift.

**Offline.** Context7 needs network; local docs always available.

**Subagent fit.** Context7 is a generic MCP server. Local skills under
`.claude/` propagate to subagents naturally without extra wiring.

**Decision: hybrid.** Keep `.claude/skills/optional/` for vetted core
patterns (auth, error handling, hooks). Use `ctx7` for live upstream
discovery on fast-moving libs (TanStack, Next, Supabase). When `ctx7`
turns up a pattern we expect to use repeatedly, promote it into
`optional/<lang>/` and stop paying its query cost.

**CLI status.** `ctx7` CLI exists and is stable (v0.4.0, 2025-04). Same
repo as the MCP server (`upstash/context7`); CLI and MCP are dual-packaged.
Commands: `ctx7 setup`, `ctx7 docs --research <q>`, `ctx7 remove <pkg>`.
No separate "upcoming CLI" — install with `npm install -g @upstash/context7`.

Setup steps in this repo: `.claude/skills/setup/docs/10-context7.md`.

---

## Q6. Late-arriving dependencies (mid-conversation lib surprises)

Five layered defenses; full detail in
`.claude/skills/parallel-dev/docs/06-late-dependency.md`.

| Layer | Mechanism | What it prevents |
|---|---|---|
| 1 Planning checklist | enumerate auth/cache/state/log/error/queue/etc. | most omissions |
| 2 Stack registry | `contracts/STACK.md` is the only place libs live | stealth additions |
| 3 ADR template | 5-min template for every new lib | unjustified additions |
| 4 Mid-task triage | STOP → in registry? → existing stack covers? → defer or ADR | impulse adds |
| 5 Spec-first contracts | spec covers pagination/auth/errors → libs are picked at spec time | scope creep |
| 6 CI gate | diff `package.json`/`go.mod` against STACK.md | ADR-skipping merges |

Templates ship in:
- `.claude/skills/parallel-dev/docs/04-planning-checklist.md`
- `.claude/skills/parallel-dev/docs/05-tech-stack-registry.md`
