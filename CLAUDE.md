# CLAUDE.md

## Search Priority
If QMD MCP is connected (`mcp__qmd__*` tools available): always use QMD query/get before Glob/Grep/Read.
If QMD is not connected: follow the Setup section in `.claude/rules/qmd.md` before doing anything else.

## Domain Rules (read when relevant)
→ Architecture:  `.claude/rules/architecture.md`
→ React/TS:      `docs/rules/react.md`
→ Go:            `docs/rules/go.md`
→ Python:        `docs/rules/python.md`
→ Database:      `docs/rules/database.md`
→ Testing:       `docs/rules/testing.md`
→ Code style:    `docs/rules/code-style.md`
→ Docker:        `docs/rules/docker.md`
→ Authorization: `docs/rules/authorization.md`
→ Codex verify:  `.claude/rules/codex.md`

## Evolution Rules
- Add rules only when recurring mistakes are discovered.
- Details go in `.claude/rules/` or skills. Keep this file minimal.
