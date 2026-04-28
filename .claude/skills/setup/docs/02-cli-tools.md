# Step 2: CLI Tools

Install via npm globals. Skip any tool that is already on PATH.

```bash
# Codex CLI (dual-review)
which codex || npm install -g @openai/codex

# Gemini CLI (UI/UX review, large-context)
which gemini || npm install -g @google/gemini-cli

# QMD (codebase search, MCP-backed)
which qmd || npm install -g @tobilu/qmd

# Playwright CLI (E2E, browser automation) — installed globally so `playwright`
# is callable without a per-project devDependency
which playwright || npm install -g playwright

# Context7 CLI (live SDK/framework docs, dual MCP + CLI modes)
# Provides `ctx7 docs --research`, `ctx7 setup`, `ctx7 remove`.
# Pairs with curated `.claude/skills/optional/` (hybrid pattern, see
# docs/research/parallel-dev-strategy.md).
which ctx7 || npm install -g @upstash/context7
```

Browser binaries and OS-level deps are handled in Step 3.
Context7 first-time setup (auth + index registration) is in Step 10.
