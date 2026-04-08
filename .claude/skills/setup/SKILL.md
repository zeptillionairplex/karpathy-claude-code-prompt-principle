---
name: setup
description: Use when the user runs /setup — checks the current environment and installs all required Claude Code plugins, CLI tools, and skills for this project.
---

# Setup — Environment Installer

Checks what is already installed and installs what is missing. Run this once after cloning the repo.

## Step 1: Check current state

Run these checks and report what is installed (✔) vs missing (✗):

```bash
# Plugins
claude plugin list 2>/dev/null

# CLI tools
codex --version 2>/dev/null && echo "codex ok" || echo "codex missing"
qmd --version 2>/dev/null && echo "qmd ok" || echo "qmd missing"
node --version 2>/dev/null && echo "node ok" || echo "node missing"

# Skills
npx skills list 2>/dev/null | grep -E "gsd|gstack" || echo "check manually"

# API key
[ -n "$OPENAI_API_KEY" ] && echo "OPENAI_API_KEY set" || echo "OPENAI_API_KEY not set"
```

Show the user a summary table, then ask:

> "The following items need to be installed: [list]. Proceed with installation? (yes/no)"

If the user says **no**, stop here and show the Manual Setup section of README.md.

## Step 2: Install Claude Code plugins

Install in this exact order. Skip any already installed.

```bash
# 1. Superpowers (skills framework)
claude plugin install superpowers@claude-plugins-official

# 2. Commit helpers
claude plugin install commit-commands@claude-plugins-official

# 3. Frontend design skill
claude plugin install frontend-design@claude-plugins-official

# 4. Skill creator
claude plugin install skill-creator@claude-plugins-official

# 5. LSP plugins
claude plugin install typescript-lsp@claude-plugins-official
claude plugin install gopls-lsp@claude-plugins-official
claude plugin install pyright-lsp@claude-plugins-official

# 6. Codex plugin (needs marketplace first)
claude plugin marketplace add openai/codex-plugin-cc 2>/dev/null || true
claude plugin install codex@openai-codex
```

Verify:
```bash
claude plugin list
```
Expected: all 8 plugins show `Status: ✔ enabled`

## Step 3: Install CLI tools

```bash
# Codex CLI
npm install -g @openai/codex
codex --version   # expected: codex-cli 0.118.x

# QMD (codebase search)
npm install -g @tobilu/qmd
qmd --version
```

## Step 4: Install skills (GSD + gstack)

```bash
npx skills add ctsstc/get-shit-done-skills@gsd -y -a claude-code
npx skills add garrytan/gstack@gstack -y -a claude-code
```

## Step 5: Index codebase with QMD

```bash
DIR=$(basename "$PWD")
qmd collection add . --name "$DIR" --mask "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}" 2>/dev/null || true
qmd collection add .claude/rules --name rules --mask "**/*.md" 2>/dev/null || true
qmd context add "qmd://$DIR" "Claude Code prompt engineering principles and workflow setup" 2>/dev/null || true
qmd context add "qmd://rules" "Claude Code behavioral and architecture rules" 2>/dev/null || true
qmd update
qmd embed --chunk-strategy auto
```

Note: `qmd embed` downloads ~2GB of local models on first run. This is expected.

## Step 6: Manual steps (cannot be automated)

Tell the user clearly:

> **Two things require manual action:**
>
> 1. **OPENAI_API_KEY** — Get one at platform.openai.com, then:
>    ```bash
>    # Add to ~/.bashrc or ~/.zshrc (Mac/Linux)
>    export OPENAI_API_KEY=sk-...
>    # Windows: set via System Environment Variables
>    ```
>    Then restart your terminal and run:
>    ```bash
>    codex login
>    ```
>
> 2. **QMD MCP server** — Add to `~/.claude/.mcp.json`:
>    ```json
>    {
>      "mcpServers": {
>        "qmd": { "command": "qmd", "args": ["mcp"] }
>      }
>    }
>    ```
>    Then restart Claude Code.

## Step 7: Verify

```bash
claude plugin list          # 8 plugins enabled
codex --version             # codex-cli 0.118.x
qmd status                  # shows indexed collection
```

Tell the user: "Setup complete. Restart Claude Code to activate plugins and MCP server."
