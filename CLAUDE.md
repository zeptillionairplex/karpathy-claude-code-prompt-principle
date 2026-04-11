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

## Multi-Agent Orchestration
This project uses oh-my-claudecode (OMC).
- Parallel execution: use `ultrawork` or `team` keywords
- Planning: /oh-my-claudecode:omc-plan
- Autonomous execution: `autopilot` keyword
- Multi-model: /ccg (Claude + Codex + Gemini)

## Development Pipeline
Run the full pipeline with /power-stack:
deep-interview → omc-plan → ultrawork/team + TDD → /ccg (codex+gemini review) → ultraqa → ship
