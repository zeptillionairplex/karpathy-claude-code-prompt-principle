# QMD Codebase Search

## Check first: is QMD connected?

At the start of any session, check whether the QMD MCP server is available.
If `mcp__qmd__status` is callable → QMD is active. Apply the search rules below.
If not → follow the **Setup** section at the bottom of this file before proceeding.

---

## Mandatory: Search with QMD before reading any file.

Always use QMD MCP tools to search for relevant information before exploring the codebase or reading files.
Glob, Grep, and Read are only permitted when QMD results are insufficient.

## Available QMD MCP Tools

1. **query** — Hybrid search (BM25 + vector + reranking). Use for complex or conceptual searches.
   - e.g. "user auth flow", "error handling patterns", "database connection logic"

2. **get** — Retrieve a specific document by path or docid.
   - e.g. fetch a file path or `#docid` returned from search results

3. **multi_get** — Retrieve multiple documents at once via glob pattern or comma-separated list.
   - e.g. `src/api/*.ts` or `file1.ts, file2.ts, #abc123`

4. **status** — Check index state and collection info.

## Search Strategy

- Finding code locations: use `query`
- Opening a specific file from search results: use `get` (not Read)
- Viewing several related files at once: use `multi_get`
- Fall back to Grep/Glob/Read only when QMD results are insufficient

## Worktree Search Strategy

When working inside a git worktree (PWD contains `.git` as a file, not a directory):

| What you're searching for | Use |
|---------------------------|-----|
| Existing codebase location (unchanged files) | QMD (worktree collection registered automatically) |
| Files you modified or created in this worktree | Grep / Read (QMD index may lag) |
| Diff vs original branch | Grep / Read only |

Worktrees are registered as `worktree-<dirname>` collections via hook (BM25 only, no vector search).
If a worktree collection is missing, run manually:
```bash
python .claude/scripts/qmd-worktree-sync.py
```

## Index Maintenance

After major file structure changes:
```bash
qmd update && qmd embed --chunk-strategy auto
```
When index state is suspect: verify with the `status` tool.

---

## Setup (run only when QMD is not installed or MCP is not connected)

### Step 1 — Install

```bash
which qmd || npm install -g @tobilu/qmd
qmd --version   # requires Node.js >= 22
```

### Step 2 — Register this project as a collection

```bash
# From the project root
DIR=$(basename "$PWD")
qmd collection add . --name "$DIR" --mask "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}"
qmd collection add .claude/rules --name rules --mask "**/*.md"
qmd collection list
```

### Step 3 — Add context

```bash
qmd context add "qmd://$DIR" "<brief project description>"
qmd context add "qmd://rules" "Claude Code behavioral and architecture rules"
```

### Step 4 — Index and embed

```bash
qmd update
qmd embed --chunk-strategy auto   # downloads ~2GB of local models on first run
qmd status
```

### Step 5 — Configure MCP server

Add to `~/.claude/.mcp.json` (create if it does not exist, preserve existing entries):

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

Restart Claude Code. The `mcp__qmd__*` tools will be available from the next session.

### Step 6 — Verify

```bash
qmd search "main" --json -n 3
qmd query "project entry point" -n 3
```
