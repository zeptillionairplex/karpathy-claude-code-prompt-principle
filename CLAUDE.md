# CLAUDE.md

## Search Priority
If QMD MCP is connected (`mcp__qmd__*` tools available): always use QMD query/get before Glob/Grep/Read.
If QMD is not connected: follow the Setup section in `.claude/rules/tools-rules.md` before doing anything else.

## Core Rules (always apply)
→ Coding principles & architecture: `.claude/rules/coding-principles.md`  
→ Context hygiene & /clear vs /compact: `.claude/rules/context-rules.md`  
→ QMD / Codex / Gemini / OMC:         `.claude/rules/tools-rules.md`  

## Domain Rules (read when relevant)
→ React/TS:      `docs/rules/react.md`  
→ Go:            `docs/rules/go.md`  
→ Python:        `docs/rules/python.md`  
→ Database:      `docs/rules/database.md`  
→ Testing:       `docs/rules/testing.md`  
→ Docker:        `docs/rules/docker.md`  
→ Authorization: `docs/rules/authorization.md`  
→ Celery:        `docs/rules/celery.md`  
→ DI patterns:   `docs/rules/dependency-injection.md`  
→ Error handling: `docs/rules/error-handling.md`  

## Evolution Rules
- Add rules only when recurring mistakes are discovered.
- Details go in `.claude/rules/` or skills. Keep this file minimal.

## Parallel Dev (Spec-First, Layered)
This repo follows a contract-centric layout for any project that grows a real
API surface (backend + frontend, possibly both in subagents):

- API contract lives at `contracts/openapi.yaml` (single source of truth).
- Locked tech decisions live at `contracts/STACK.md` — adding a library
  requires an ADR and a STACK.md update.
- Generated files (`backend/api/api.gen.*`, `frontend/src/types/api.ts`) are
  read-only.
- Each subtree owns its own `CLAUDE.md`:
  → contract rules: `contracts/CLAUDE.md`
  → backend rules:  `backend/CLAUDE.md`
  → frontend rules: `frontend/CLAUDE.md`
- Operational guide: `.claude/skills/parallel-dev/SKILL.md`
- Strategy / Q&A archive: `docs/research/parallel-dev-strategy.md`

Late-dependency surprises (mid-task "we need TanStack / zod / …") flow
through `.claude/skills/parallel-dev/docs/06-late-dependency.md` — never
add an import that isn't registered in `contracts/STACK.md`.

## Regulated Service Build (KR baseline + global)
For any service that touches users, payments, or regulated data, the
parallel-dev skill includes engineering guidance for legal, security,
admin operations, and operator handoff. KR statutes are the baseline
(PIPA, ICN Act, location-info, e-commerce, credit, cloud); GDPR / CCPA /
PIPL covered as global expansion sections. **Not legal advice** — every
user-facing or regulator-bound output requires real legal sign-off.

→ Legal / consents / cross-border basis: `.claude/skills/parallel-dev/docs/07-legal-compliance.md`
→ Security baseline + IR runbook + DR + recent attack-pattern defences: `.claude/skills/parallel-dev/docs/08-security-incident.md`
→ Action-oriented admin dashboard contract: `.claude/skills/parallel-dev/docs/09-admin-action-console.md`
→ Inline glossary + new-operator onboarding: `.claude/skills/parallel-dev/docs/10-glossary-and-handoff.md`
→ Strategy / Q&A archive: `docs/research/regulated-service-strategy.md`

Volatile resource data (authority URLs, hotlines, form templates) lives
in DB (`admin_resources`), never inlined in code or docs. Statute text is
cached from `law.go.kr` OpenAPI. Rarely-changing global metadata lives in
`contracts/legal-resources.json`.

## Multi-Agent Orchestration
This project uses oh-my-claudecode (OMC).
- Parallel execution: use `ultrawork` or `team` keywords
- Planning: /oh-my-claudecode:omc-plan
- Autonomous execution: `autopilot` keyword
- Multi-model: /ccg (Claude + Codex + Gemini)

## Development Pipeline
Run the full pipeline with /power-stack:
deep-interview → omc-plan → ultrawork/team + TDD → /ccg (codex+gemini review) → ultraqa → ship
