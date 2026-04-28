---
name: parallel-dev
description: Spec-first parallel backend/frontend development with subagents — contract location, layered CLAUDE.md, late-dependency mitigation. Trigger when user mentions parallel dev, contracts, openapi.yaml placement, or splitting backend/frontend work.
---

# Parallel Dev (Spec-First, Contract-Centric)

Use this skill when starting or restructuring a project with parallel
backend/frontend work driven by Claude Code subagents.

## Core thesis
**AI agents work best with explicit contracts.** An OpenAPI spec at the repo
neutral zone (`contracts/`) is the single source of truth; backend and frontend
agents generate code from it independently and never drift.

## When to apply
- Project has (or will have) a backend API + a frontend that consumes it.
- You plan to run subagents/teams in parallel.
- You expect mid-project mention of new libs (TanStack, zod, etc.) and want
  to absorb that without retrofit cost.

## Reference docs
→ Strategy & rationale (the original Q&A): `../../../docs/research/parallel-dev-strategy.md`
→ Repo layout & layered CLAUDE.md: `docs/01-layout.md`
→ Spec-first workflow with `oapi-codegen` + `openapi-typescript`: `docs/02-spec-workflow.md`
→ Subagent orchestration rules: `docs/03-subagents.md`
→ Planning checklist (kickoff): `docs/04-planning-checklist.md`
→ Tech-stack registry template: `docs/05-tech-stack-registry.md`
→ Late-dependency mitigation patterns: `docs/06-late-dependency.md`
→ Legal & compliance (KR + global): `docs/07-legal-compliance.md`
→ Security, incident response, DR: `docs/08-security-incident.md`
→ Admin action console (UI for action, not display): `docs/09-admin-action-console.md`
→ Glossary & operator handoff: `docs/10-glossary-and-handoff.md`
→ Stack security defaults (Go Gin / FastAPI / Caddy / EC2 / React): `docs/11-stack-security-defaults.md`
→ Strategy archive (regulated services): `../../../docs/research/regulated-service-strategy.md`

## Quick start
1. Read `docs/04-planning-checklist.md`. Fill in capability decisions before any
   code is written. Defer items explicitly — never silently.
2. Initialize the registry from `docs/05-tech-stack-registry.md`. Commit it to
   `contracts/STACK.md`.
3. Draft `contracts/openapi.yaml` (human + Claude). Freeze it.
4. Spawn backend + frontend subagents per `docs/03-subagents.md`. Each only
   sees its own `CLAUDE.md`.
5. On any "we need lib X" surprise, run `docs/06-late-dependency.md` triage
   before adding it.
