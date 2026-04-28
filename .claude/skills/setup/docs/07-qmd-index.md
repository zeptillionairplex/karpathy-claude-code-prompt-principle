# Step 7: QMD Index

```bash
DIR=$(basename "$PWD")
qmd collection add . --name "$DIR" --mask "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}" 2>/dev/null || true
qmd collection add .claude/rules --name rules --mask "**/*.md" 2>/dev/null || true
qmd context add "qmd://$DIR" "Claude Code prompt engineering principles and workflow setup" 2>/dev/null || true
qmd context add "qmd://rules" "Claude Code behavioral and architecture rules" 2>/dev/null || true
qmd update && qmd embed --chunk-strategy auto
```

Note: first `qmd embed` downloads a ~2GB local model. Expected.

Register the QMD MCP server in `~/.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

Restart Claude Code so the MCP server is picked up.
