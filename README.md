# Claude Code Prompt Principles

A production-ready Claude Code workspace setup based on Andrej Karpathy's four coding principles — with a full AI-assisted development pipeline, automated hooks, and dual-model code verification (Claude + Codex).

## What You Get

- **Power Stack pipeline** — Plan → Manage → Build → Verify using gstack, GSD, and Superpowers TDD
- **Dual-model verification** — Codex (OpenAI) reviews every implementation wave, catching Claude's blind spots
- **Automated hooks** — context hygiene, doc drift detection, skill analysis, QMD worktree sync
- **Karpathy's 4 principles** enforced via `CLAUDE.md` rules: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution
- **QMD codebase search** — hybrid BM25 + vector search so Claude never explores blindly with Glob/Grep
- **One-command setup** — `/setup` installs everything from a fresh clone

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Node.js 18.18 or later
- Python 3.10 or later
- Git
- An OpenAI API key (for Codex verification) — [get one here](https://platform.openai.com/api-keys)

## Quick Start

```bash
git clone <this-repo>
cd <this-repo>
```

Open Claude Code in this directory, then run:

```
/setup
```

That's it. `/setup` checks your environment, installs all plugins and CLI tools, and walks you through the two manual steps (API key + MCP config).

## Project Structure

```
.
├── CLAUDE.md                    # Project rules — auto-loaded every session
├── .claude/
│   ├── settings.json            # Hooks configuration
│   ├── rules/                   # Behavioral rules (loaded on demand)
│   │   ├── behavior.md          # Karpathy's 4 principles
│   │   ├── architecture.md      # Context boundaries, FSD, Clean Architecture
│   │   ├── code-style.md        # Naming, commits, documentation
│   │   ├── codex.md             # Codex verification — when and how
│   │   ├── context-hygiene.md   # What NOT to read (node_modules, etc.)
│   │   ├── context-management.md # /clear vs /compact — when to use each
│   │   └── qmd.md               # QMD search rules and setup
│   ├── skills/                  # Custom slash commands
│   │   ├── setup/               # /setup — environment installer
│   │   ├── power-stack/         # /power-stack — full dev lifecycle
│   │   ├── explore/             # /explore — targeted codebase navigation
│   │   ├── implement/           # /implement — feature implementation
│   │   ├── fix-bug/             # /fix-bug — minimal bug fixes
│   │   ├── refactor/            # /refactor — behavior-preserving refactors
│   │   └── ...                  # Additional domain skills
│   └── scripts/                 # Hook scripts (Python)
│       ├── guard-file-read.py   # Blocks context-hygiene violations
│       ├── guard-bash.py        # Blocks dangerous shell commands
│       ├── doc-guardian.py      # Detects stale CLAUDE.md on session end
│       ├── context-monitor.py   # Warns when context approaches 50%
│       ├── skill-hook-analyzer.py # Analyzes new skills for hook patterns
│       ├── sync-skills.py       # Keeps skills registry up to date
│       ├── qmd-worktree-sync.py # Registers/removes git worktrees in QMD
│       └── notify.py            # Session-end desktop notification
└── docs/
    └── rules/                   # Domain-specific rules (React, Go, Python, etc.)
```

## How It Works

### Layer 1 — Rules (`CLAUDE.md` + `.claude/rules/`)

Rules are plain Markdown files that Claude reads when relevant. `CLAUDE.md` is loaded automatically every session; domain rules are loaded on demand via pointers in `CLAUDE.md`.

Key rules:
| File | Purpose |
|------|---------|
| `behavior.md` | Karpathy's 4 principles — the foundation of every decision |
| `codex.md` | When to run Codex, how to classify findings, what to do with them |
| `context-hygiene.md` | Explicit list of paths Claude must never load (node_modules, dist, etc.) |
| `context-management.md` | `/clear` vs `/compact` — when each is appropriate, what's forbidden |
| `qmd.md` | QMD search-first discipline — Glob/Grep only as fallback |

### Layer 2 — Skills (`.claude/skills/`)

Skills are slash commands that give Claude structured workflows. Each lives in its own folder as `SKILL.md`.

Key skills:
| Command | Purpose |
|---------|---------|
| `/setup` | Install all plugins, CLI tools, and skills from scratch |
| `/power-stack` | Orchestrate the full Plan → Build → Verify pipeline |
| `/explore` | Navigate to a target area in max 4 tool calls |
| `/fix-bug` | Minimal bug fix with test-first discipline |

Third-party skills installed by `/setup`:
- **Superpowers** — TDD, parallel agents, plan writing, code review workflows
- **GSD** — Project planning, phase management, goal-backward verification
- **gstack** — Multi-persona architecture review, QA, security audit, ship

### Layer 3 — Hooks (`.claude/settings.json`)

Hooks run Python scripts automatically on Claude Code events. They enforce rules regardless of what Claude decides.

| Event | Script | What it does |
|-------|--------|-------------|
| `PreToolUse(Read/Grep/Glob)` | `guard-file-read.py` | Blocks reads of `node_modules`, `dist`, lock files, etc. |
| `PreToolUse(Bash)` | `guard-bash.py` | Blocks destructive shell patterns |
| `PostToolUse(Write/Edit)` | `skill-hook-analyzer.py` | Suggests hooks when new skills are added |
| `PostToolUse(Bash: git worktree)` | `qmd-worktree-sync.py` | Keeps QMD index in sync with worktrees |
| `Stop` | `doc-guardian.py` | Detects missing/stale `CLAUDE.md` at session end |
| `Stop` | `context-monitor.py` | Warns at 60% (consider `/compact`) and 80% (urgent: `/clear` or `/compact`) |

### Layer 4 — Dual-Model Verification

Every implementation wave goes through two models:

1. **Claude** writes and tests the code
2. **Codex (OpenAI)** reviews the diff independently

```bash
# After each wave passes tests:
git diff HEAD~1 | codex "Review this diff for bugs, security issues, and logic errors."

# Or use the plugin slash command:
/codex:review
/codex:adversarial-review
```

Findings are saved to `.planning/phases/0N-name/0N-CODEX.md` and gated:
- **HIGH** → fix before next wave
- **WARN** → fix before Stage 4 QA
- **INFO** → optional

### Layer 5 — QMD Search

[QMD](https://github.com/tobias-luedtke/qmd) indexes the codebase with hybrid BM25 + vector search. Claude queries it before opening any file, keeping context usage minimal.

```
mcp__qmd__query  →  conceptual search ("user auth flow")
mcp__qmd__get    →  fetch a specific file by path
mcp__qmd__multi_get → fetch several files at once
```

## The Power Stack Pipeline

For non-trivial projects, run `/power-stack`:

```
Session 1: /gstack:autoplan  → architecture review → .planning/PROJECT.md
Session 2: /gsd:new-project  → phase plans
Session 3+: superpowers:tdd + parallel agents (one per wave)
            └─ After each wave: /codex:review (Codex verify)
Final:      /gstack:qa + /gstack:cso + /gstack:ship
```

State persists across sessions in `POWERSTACK.md`. Context is capped at 50% per session for peak output quality.

## Manual Setup

If you prefer not to use `/setup`, install each piece manually:

**Claude Code plugins:**
```bash
claude plugin install superpowers@claude-plugins-official
claude plugin install commit-commands@claude-plugins-official
claude plugin install frontend-design@claude-plugins-official
claude plugin install skill-creator@claude-plugins-official
claude plugin install typescript-lsp@claude-plugins-official
claude plugin install gopls-lsp@claude-plugins-official
claude plugin install pyright-lsp@claude-plugins-official
claude plugin marketplace add openai/codex-plugin-cc
claude plugin install codex@openai-codex
```

**CLI tools:**
```bash
npm install -g @openai/codex
npm install -g @tobilu/qmd
```

**Skills:**
```bash
npx skills add ctsstc/get-shit-done-skills@gsd -y -a claude-code
npx skills add garrytan/gstack@gstack -y -a claude-code
```

**QMD index:**
```bash
DIR=$(basename "$PWD")
qmd collection add . --name "$DIR" --mask "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}"
qmd collection add .claude/rules --name rules --mask "**/*.md"
qmd update && qmd embed --chunk-strategy auto
```

**MCP server** — add to `~/.claude/.mcp.json`:
```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

**API key:**
```bash
export OPENAI_API_KEY=sk-...   # add to shell profile
codex login
```

## Principles

This setup is built around four principles from Andrej Karpathy's approach to working with AI coding assistants:

1. **Think Before Coding** — State assumptions, ask when uncertain, push back on overcomplicated requests
2. **Simplicity First** — No features, abstractions, or error handling beyond what was asked
3. **Surgical Changes** — Only modify code directly related to the request; never "improve" adjacent code
4. **Goal-Driven Execution** — Transform tasks into verifiable goals; write tests before implementation

These are enforced via `.claude/rules/behavior.md`, which Claude loads automatically.

## Contributing

Rules and skills improve over time. When you find a recurring mistake:

1. Add a rule to `.claude/rules/` (or update an existing one)
2. If it's workflow-related, update the relevant skill in `.claude/skills/`
3. Keep `CLAUDE.md` minimal — it's a pointer file, not a documentation file

## License

MIT
