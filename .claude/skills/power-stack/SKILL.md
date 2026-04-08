---
name: power-stack
description: Use when starting any non-trivial software project from scratch, or resuming one across sessions. Routes to gstack (planning), GSD (project management), Superpowers TDD (implementation), and gstack QA (verification) based on current lifecycle stage.
---

# Power Stack

## Step 0: Load State (every session)

```bash
cat POWERSTACK.md 2>/dev/null || echo "No state file — starting Stage 1"
```

- No file → Stage 1
- File exists → announce `stage` + `next_action`, ask "Continue or restart?"

State file schema:
```
project / stage: 1-plan|2-manage|3-build|4-verify / phase: N
status: pending|in-progress|done / next_action / last_session / context_at_close / notes (≤5 bullets)
```

---

## Stage 1: PLAN

Model: `opus` (CEO), `sonnet` (design/eng). Context limit: 40%.

1. Rough idea? → `/gstack:office-hours` first
2. `/gstack:autoplan` → CEO + design + eng personas → `.planning/PROJECT.md`
3. Save state: `stage: 2-manage, next_action: /gsd:new-project` → **new session**

## Stage 2: MANAGE

Model: `sonnet`. Context limit: 50%.

1. `/gsd:new-project` → `REQUIREMENTS.md`, `ROADMAP.md`, `STATE.md`
2. `/gsd:plan-phase N` for each phase → `phases/0N-name/0N-PLAN.md`
3. Save state: `stage: 3-build, phase: 1` → **new session**

## Stage 3: BUILD (one session per phase)

Model: `sonnet`. Context limit: 50%.

1. Read `0N-PLAN.md`. Use QMD for all codebase queries — never Glob/Grep/Read.
2. `superpowers:test-driven-development` — failing tests before any implementation
3. Wave 1 (independent tasks): `superpowers:dispatching-parallel-agents`
   `Agent(model="sonnet", isolation="worktree")` per task
4. Wave 2+: sequential or parallel per dependency graph
5. **After each wave — Codex verify** → see `.claude/rules/codex.md`
6. `/gsd:verify-work N` — goal-backward check, not task-completion check
7. Advance: `phase: N+1` or `stage: 4-verify` → **new session**

## Stage 4: VERIFY

Model: `sonnet`. Context limit: fresh session.

1. `/gstack:qa-only` — E2E report, no auto-fix. Fix criticals manually.
2. `/gstack:cso` — OWASP Top 10 + STRIDE. Fix HIGH/CRITICAL before proceeding.
3. `/gstack:qa` — full fix loop until clean
4. `/gstack:review` → `/gstack:ship` → `/gstack:land-and-deploy` → `/gstack:canary`

---

## Rules

- QMD first for all codebase queries
- 50% context → save POWERSTACK.md + close session immediately
- This skill routes only — never implements
- Sub-agents get only their task context, not full history
- Haiku for docs/formatting/comments

## Tool Registry

```yaml
plan:    [gstack:autoplan, gstack:office-hours, gstack:plan-ceo-review, gstack:plan-eng-review]
manage:  [gsd, gsd:plan-phase, gsd:execute-phase, gsd:verify-work, gsd:debug]
build:   [superpowers:test-driven-development, superpowers:dispatching-parallel-agents, superpowers:executing-plans]
verify:  [gstack:codex, gstack:qa, gstack:qa-only, gstack:cso, gstack:review, gstack:investigate]
deploy:  [gstack:ship, gstack:canary, gstack:land-and-deploy]
```

Model assignment: `opus` = orchestrator/CEO, `sonnet` = all else, `codex` = verification, `haiku` = cheap tasks

## Setup

- [x] Superpowers, GSD, gstack, QMD, Codex CLI (v0.118.0)
- [ ] `export OPENAI_API_KEY=sk-...` then `codex auth`
