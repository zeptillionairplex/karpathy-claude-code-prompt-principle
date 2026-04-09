# Tools Rules

## QMD (Codebase Search)

**Priority:** QMD → Glob/Grep/Read. Use Glob/Grep/Read only when QMD results are insufficient.

**Check first:** If `mcp__qmd__status` is callable → QMD is active. If not → run Setup below.

**Tools:**
- `query` — hybrid search (BM25 + vector + reranking). Use for conceptual searches: "user auth flow", "error handling patterns"
- `get` — retrieve a specific file by path or `#docid`
- `multi_get` — retrieve multiple files via glob or comma-separated list
- `status` — check index state

**Strategy:** Finding code → `query` · Opening a file from results → `get` (not Read) · Multiple related files → `multi_get`

**Worktree:** Unchanged files → QMD · Files you modified/created → Grep/Read (index may lag) · Diff → Grep/Read only. Worktrees registered as `worktree-<dirname>` (BM25 only). If missing: `python .claude/scripts/qmd-worktree-sync.py`

**Index maintenance:** After major structure changes: `qmd update && qmd embed --chunk-strategy auto`

### Setup (run only when QMD is not connected)

```bash
# 1. Install
which qmd || npm install -g @tobilu/qmd   # requires Node.js >= 22

# 2. Register collections
DIR=$(basename "$PWD")
qmd collection add . --name "$DIR" --mask "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}"
qmd collection add .claude/rules --name rules --mask "**/*.md"

# 3. Add context
qmd context add "qmd://$DIR" "<brief project description>"
qmd context add "qmd://rules" "Claude Code behavioral and architecture rules"

# 4. Index and embed
qmd update && qmd embed --chunk-strategy auto

# 5. Configure MCP — add to ~/.claude/.mcp.json
# { "mcpServers": { "qmd": { "command": "qmd", "args": ["mcp"] } } }
# Then restart Claude Code.
```

---

## Codex (Independent Code Verification)

Codex (OpenAI) uses a different training corpus — catches blind spots Claude-only review misses. Mandatory second opinion after non-trivial implementation.

**When required:** After each implementation wave where tests pass · Before opening a PR · When something feels wrong but tests still pass.
**Not required:** Documentation-only or config/infra-only changes with no logic.

**How to run:**
```bash
codex                                          # interactive review of current diff
codex "Review src/foo.ts for bugs"             # target specific files
git diff HEAD~1 | codex "Review for bugs, security issues, logic errors"
```

**Output handling:**
1. Save findings to `.planning/phases/0N-name/0N-CODEX.md`
2. Fix HIGH/CRITICAL before advancing to the next wave
3. WARN-level: record in file, address before Stage 4 QA

Setup: `/plugin install codex@openai-codex` or `npm install -g @openai/codex` + `OPENAI_API_KEY`

---

## Gemini CLI

- Use for UI/UX review, large-context analysis, and document summarization
- Parallel execution: `omc team N:gemini`
- CCG mode (`/ccg`): Claude synthesizes combined Codex + Gemini results

---

## OMC (oh-my-claudecode)

- Multi-agent orchestration runs through OMC
- Simple tasks are auto-delegated to Haiku agents (cost reduction)
- Parallel execution: use `ultrawork` or `team` keywords
- Planning: `/oh-my-claudecode:omc-plan`
