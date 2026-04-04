---
name: power-stack
description: Use when starting any non-trivial software project from scratch, or resuming one across sessions. Routes to gstack (planning), GSD (project management), Superpowers TDD (implementation), and gstack QA (verification) based on current lifecycle stage.
---

# Power Stack — Full Dev Lifecycle Orchestrator

Combines gstack + GSD + Superpowers into a single pipeline. Each stage uses the optimal tool, model, and agent team. Context stays ≤50% by isolating each phase into a fresh session.

## The 3 Claude Code Harness Features (always active)

| Feature | What it does |
|---------|-------------|
| **CLAUDE.md** | Project rules auto-loaded every session — no re-explaining context |
| **Auto Memory** (`~/.claude/projects/.../memory/power-stack.md`) | Stage state persists between sessions — Claude remembers where you left off |
| **Hooks + settings.json** | Deterministic automation — enforces rules regardless of what Claude decides |

## Tool Registry

Add new tools here as they become available. The pipeline routes to them automatically.

```yaml
plan:    [gstack:autoplan, gstack:office-hours, gstack:plan-ceo-review, gstack:plan-eng-review]
manage:  [gsd, gsd:plan-phase, gsd:execute-phase, gsd:verify-work, gsd:debug]
build:   [superpowers:test-driven-development, superpowers:dispatching-parallel-agents, superpowers:executing-plans]
verify:  [gstack:codex*, gstack:qa, gstack:qa-only, gstack:cso, gstack:review, gstack:investigate]
deploy:  [gstack:ship, gstack:canary, gstack:land-and-deploy]
# * Codex requires: npm install -g @openai/codex && codex auth
# future: [gemini-cli, claude-computer-use, new models, ...]
```

## Model Assignment

Always pass the correct model when spawning agents:

| Task | Model | Why |
|------|-------|-----|
| Orchestrator (this skill) | `opus` | Routing decisions need best reasoning |
| CEO/architecture review | `opus` | Deepest reasoning for architecture |
| Design + eng review | `sonnet` | Speed + quality balance |
| GSD project planning | `sonnet` | Structured, reliable |
| TDD implementation | `sonnet` | Fast code generation |
| Code verification (Codex) | `codex` | Independent model = catches Claude blind spots |
| QA + security audit | `sonnet` | Tool-use heavy |
| Docs, formatting, comments | `haiku` | Simple repetitive work = cheap |

---

## Step 0: Load State (every session)

```bash
cat POWERSTACK.md 2>/dev/null || echo "No state file — starting Stage 1"
```

- **No POWERSTACK.md** → go to Stage 1
- **POWERSTACK.md exists** → announce `stage` + `next_action`, ask "Continue or restart?"

State file format:
```markdown
# Power Stack State
project: <name>
stage: 1-plan | 2-manage | 3-build | 4-verify
phase: <N>
status: pending | in-progress | done
next_action: <exact skill or command to run>
last_session: YYYY-MM-DD
context_at_close: <% used>
notes: <handoff context for next session — keep under 5 bullet points>
```

---

## Stage 1: PLAN — gstack Multi-Persona Review

**Model team:** CEO review → `opus`, design + eng review → `sonnet`
**Context budget:** Fresh session. Stop at 40%, save state, close session.

### 1a. Optional: Brainstorm first
If idea is still rough, run `/gstack:office-hours` before autoplan.
YC-style startup diagnostic — sharpens the idea before committing to architecture.

### 1b. Multi-persona architecture review
Run `/gstack:autoplan` — triggers the full review pipeline:
- **CEO persona** (`opus`): business viability, risks, scope, make-vs-buy decisions
- **Design persona** (`sonnet`): UX flows, component structure, user journeys
- **Eng persona** (`sonnet`): tech stack, implementation feasibility, unknowns

Output: save to `.planning/PROJECT.md`

### 1c. Close session
Update POWERSTACK.md:
```markdown
stage: 2-manage
next_action: /gsd:new-project
notes: [key decisions from planning review]
```
**STOP. Start a new session. Run `/power-stack` to continue.**

---

## Stage 2: MANAGE — GSD Project Setup

**Model:** `sonnet`
**Context budget:** Fresh session. Stop at 50%, save state, close session.

### 2a. Initialize project
Run `/gsd:new-project` — reads PROJECT.md, creates `.planning/` structure:
- `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`
- Domain research via codebase mapping (uses QMD, not Glob/Read)

### 2b. Plan phases
Run `/gsd:plan-phase 1` — creates `phases/01-name/01-PLAN.md`
- Each plan = an executable prompt, not a document
- Break work into waves: Wave 1 = independent tasks, Wave 2+ = dependent
- Verify with user before moving to next phase

Repeat for all phases.

### 2c. Close session
Update POWERSTACK.md:
```markdown
stage: 3-build
phase: 1
next_action: superpowers:test-driven-development for phase 1
```
**STOP. Start a new session. Run `/power-stack` to continue.**

---

## Stage 3: BUILD — Superpowers TDD (loops per phase)

**Model:** `sonnet` (implementers), `opus` only for architecture forks
**Context budget:** Fresh session per phase. Stop at 50%, immediately save + close.

### 3a. Load phase plan
Read `.planning/phases/0N-name/0N-PLAN.md`
Use QMD for all codebase queries: `mcp__qmd__query` / `mcp__qmd__get` — never Glob/Grep/Read for exploration.

### 3b. TDD: tests before code
Invoke `superpowers:test-driven-development`:
1. Write failing tests that define the contract
2. Tests describe WHAT the code must do — not HOW
3. Zero implementation code until tests exist

### 3c. Parallel wave execution
For Wave 1 (independent tasks): invoke `superpowers:dispatching-parallel-agents`
- Spawn `sonnet` sub-agents, one per task
- Each agent: isolated context, one task, returns result
- Agent tool: `Agent(model="sonnet", isolation="worktree")`

For Wave 2+: sequential or parallel based on dependency graph in PLAN.md

### 3d. Context enforcement
When context reaches 50%:
1. Write progress to `.planning/phases/0N-name/0N-CONTEXT.md`
2. Update POWERSTACK.md notes with exact resume point
3. **STOP. New session. `/power-stack` to resume.**

### 3e. Codex verification (if available)
After each wave passes tests, get a second opinion:
```bash
codex review --approval-mode=suggest  # Via /gstack:codex
```
Codex = OpenAI model = independent perspective = catches Claude blind spots.
Setup if needed: `npm install -g @openai/codex && codex auth`

### 3f. Phase completion
Run `/gsd:verify-work N` — goal-backward check:
- Not "did tasks complete?" but "is the goal actually achieved?"
- If issues: fix + re-verify before advancing

Update POWERSTACK.md: `phase: N+1` (or `stage: 4-verify` if all phases done)
**STOP. New session for next phase.**

---

## Stage 4: VERIFY — gstack QA + Security + Ship

**Model:** `sonnet`
**Context budget:** Fresh session.

### 4a. Report-first QA
Run `/gstack:qa-only` — Playwright E2E browser test, report only, no auto-fixes.
Review findings. Fix critical issues manually.

### 4b. Security audit
Run `/gstack:cso` — OWASP Top 10 + STRIDE threat model.
Fix any HIGH or CRITICAL findings before proceeding.

### 4c. Full QA loop
Run `/gstack:qa` — test + fix loop until clean.

### 4d. Code review
Run `/gstack:review` — final PR review before merge.

### 4e. Ship
Run `/gstack:ship` → `/gstack:land-and-deploy` → `/gstack:canary`

Update POWERSTACK.md: `status: done`

---

## Context Efficiency Rules (enforced at all stages)

```
1. QMD first       → mcp__qmd__query/get/multi_get for ALL codebase queries
2. 50% hard stop   → context ≥50%? save POWERSTACK.md + close session immediately
3. Orchestrator thin → this skill routes only, never implements
4. Sub-agents isolated → each agent gets only its task context, not full history
5. State = the brain → POWERSTACK.md + .planning/STATE.md carry continuity
6. Fresh session = peak quality → GSD rule: 0–30% context = best output
7. Haiku for cheap tasks → formatting, docs, comments = haiku model
```

## Pipeline at a Glance

```
Session 1:  gstack:autoplan (opus CEO + sonnet team) → PROJECT.md
Session 2:  gsd:new-project → ROADMAP.md + phase plans
Session 3+: superpowers:tdd + parallel sonnet agents (one per phase)
            └─ After each wave: gstack:codex (independent Codex verify)
Final:      gstack:qa + gstack:cso + gstack:ship
```

## Adding Future Tools

When a new tool appears (Gemini CLI, Claude computer-use, GPT-o3, etc.):
1. Add to Tool Registry under the right category
2. Add a row to Model Assignment with "when to prefer over X"
3. No other changes needed — the pipeline routes naturally

## Setup Checklist

- [x] Superpowers: already installed (Claude Code plugin)
- [x] GSD: `npx skills add ctsstc/get-shit-done-skills@gsd -y -a claude-code`
- [x] gstack: `npx skills add garrytan/gstack@gstack -y -a claude-code`
- [x] QMD: indexed via `qmd update && qmd embed --chunk-strategy auto`
- [ ] Codex CLI (optional): `npm install -g @openai/codex && codex auth`
- [ ] OPENAI_API_KEY: `export OPENAI_API_KEY=sk-...`
