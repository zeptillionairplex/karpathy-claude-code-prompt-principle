# Codex — Independent Code Verification

Codex (OpenAI) is a different model family from Claude. Running it on code you wrote catches
blind spots that Claude-only review misses. Use it as a mandatory second opinion after any
non-trivial implementation wave.

## Setup (one-time)

### Option A — Claude Code plugin (recommended)

```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
/codex:setup
```

Gives you `/codex:review`, `/codex:adversarial-review`, `/codex:rescue` slash commands
inside Claude Code in addition to the CLI.

### Option B — CLI only

```bash
npm install -g @openai/codex   # already installed: v0.118.0
codex auth                     # requires OPENAI_API_KEY
```

### API key (required for both options)

```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, or Windows environment variables)
export OPENAI_API_KEY=sk-...
# Then authenticate:
codex login        # ChatGPT account or API key
```

> Run `/setup` in Claude Code to install all tools at once.

## When to run Codex

**Required** after every implementation wave where tests pass:
- After each Build stage wave in power-stack (`/power-stack` Stage 3e)
- After completing a feature branch before opening a PR
- When something feels wrong but tests still pass

**Not required** for:
- Documentation-only changes
- Config/infra-only changes with no logic

## How to run

```bash
# Interactive review — Codex reads the diff and suggests improvements
codex

# Point it at changed files explicitly
codex "Review the changes in src/foo.ts and src/bar.ts for bugs and logic issues"

# Or scope to a git diff
git diff HEAD~1 | codex "Review this diff for bugs, security issues, and logic errors"
```

## What to do with the output

1. Save findings to `.planning/phases/0N-name/0N-CODEX.md`
2. Fix any HIGH/CRITICAL issues before advancing to the next wave
3. WARN-level findings: record in the file, address before Stage 4 QA
4. Update POWERSTACK.md notes with a one-line summary of findings

## Why this matters

Claude writes code and reviews it with the same mental model — shared blind spots.
Codex uses a different training corpus and different reasoning patterns.
The combination catches ~10x more issues than single-model review alone.
