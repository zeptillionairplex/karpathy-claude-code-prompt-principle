# Claude Code Prompt Principles v2

Claude Code workspace setup based on Andrej Karpathy's four coding principles.
OMC multi-agent orchestration + Superpowers TDD + triple-model verification.

## What You Get

- **OMC Multi-Agent** — 29 specialized agents, parallel execution, smart model routing (30–50% cost reduction)
- **Superpowers TDD** — test first → implement → verify, strict execution loop
- **Triple-Model Verification** — Claude (implementation) + Codex (review) + Gemini (UI/large-context analysis)
- **Context Optimization** — 44% fixed overhead reduction vs v1 (21.5K → ~12K)
- **Karpathy's 4 Principles** — enforced via rules (Think / Simplicity / Surgical / Goal-Driven)
- **QMD Semantic Search** — BM25 + vector search instead of Glob/Grep
- **One-Command Setup** — `/setup` configures the full environment automatically

## Requirements

- [Claude Code](https://claude.ai/code) CLI
- Node.js 18.18+
- Python 3.10+
- Git
- tmux (for OMC team mode — optional)
- OpenAI API key (for Codex verification) — [get one here](https://platform.openai.com/api-keys)
- Google account (for Gemini CLI OAuth)

## Quick Start

```bash
git clone https://github.com/zeptillionairplex/karpathy-claude-code-prompt-principle.git
cd karpathy-claude-code-prompt-principle
```

Open Claude Code in this directory, then run:

```
/setup
```

`/setup` handles environment checks, CLI installation, plugin installation, OMC initialization, and QMD indexing.

## Project Structure

```
.
├── CLAUDE.md                        # Project rules — auto-loaded every session
├── .claude/
│   ├── settings.json                # Hooks configuration
│   ├── CLAUDE.md                    # OMC orchestration config
│   ├── rules/                       # Behavioral rules (3 files)
│   │   ├── coding-principles.md     # Karpathy's 4 principles + architecture + code style
│   │   ├── context-rules.md         # Paths to never read + /clear vs /compact
│   │   └── tools-rules.md           # QMD / Codex / Gemini / OMC usage rules
│   ├── skills/                      # Core slash commands
│   │   ├── setup/                   # /setup — environment installer
│   │   ├── power-stack/             # /power-stack — full dev lifecycle
│   │   ├── explore/                 # /explore — codebase navigation
│   │   ├── implement/               # /implement — feature implementation
│   │   ├── fix-bug/                 # /fix-bug — minimal bug fixes
│   │   ├── refactor/                # /refactor — behavior-preserving refactors
│   │   ├── verify-implementation/   # /verify-implementation — implementation verification
│   │   ├── manage-skills/           # /manage-skills — skill management
│   │   ├── omc-reference/           # /omc-reference — OMC agent catalog
│   │   └── optional/                # Language-specific skills (auto-detected)
│   │       ├── react/               # React/TypeScript
│   │       ├── python/              # Python
│   │       ├── python-structure/    # Python project structure
│   │       ├── supabase/            # Supabase
│   │       └── n8n/                 # n8n workflows
│   └── scripts/                     # Hook scripts (Python)
│       ├── guard-file-read.py       # Blocks context-rules violations
│       ├── guard-bash.py            # Blocks dangerous shell commands
│       ├── bash-output-limiter.py   # Limits Bash output size
│       ├── guard-golang-best-practices.py  # Go best practices guard
│       ├── doc-guardian.py          # Detects stale CLAUDE.md at session end
│       ├── context-monitor.py       # Warns at 60% (compact) and 80% (urgent)
│       ├── skill-hook-analyzer.py   # Suggests hooks when new skills are added
│       ├── sync-skills.py           # Keeps skills registry up to date
│       ├── qmd-worktree-sync.py     # Syncs git worktrees with QMD index
│       └── notify.py                # Session-end desktop notification
└── docs/
    └── rules/                       # Domain-specific rules (loaded on demand)
        ├── react.md
        ├── go.md
        ├── python.md
        ├── database.md
        ├── testing.md
        ├── docker.md
        ├── authorization.md
        ├── celery.md
        ├── dependency-injection.md
        └── error-handling.md
```

## How It Works

### Layer 1 — Rules (3 files)

`CLAUDE.md` is auto-loaded every session. Domain rules are loaded on demand via pointers.

| File | Purpose |
|------|---------|
| `coding-principles.md` | Karpathy's 4 principles · architecture boundaries · code style |
| `context-rules.md` | Paths Claude must never read · `/clear` vs `/compact` criteria |
| `tools-rules.md` | QMD-first search · Codex verification · Gemini · OMC usage |

### Layer 2 — Skills (core + optional)

Slash commands that give Claude structured workflows.

Core skills:

| Command | Purpose |
|---------|---------|
| `/setup` | CLI install · plugins · OMC init · QMD indexing |
| `/power-stack` | Full lifecycle orchestration |
| `/explore` | Navigate to a target area in max 4 tool calls |
| `/fix-bug` | Write test first, then minimal fix |
| `/implement` | Feature implementation with TDD |
| `/refactor` | Behavior-preserving refactor |

Optional skills (`optional/`) — `/setup` auto-detects project language and activates:

| Detection | Activated skill |
|-----------|----------------|
| package.json with "react" or tsconfig.json | `optional/react/` |
| requirements.txt or pyproject.toml | `optional/python/`, `optional/python-structure/` |
| go.mod | `optional/golang/` |
| supabase/ directory or SUPABASE in .env | `optional/supabase/` |
| n8n config files | `optional/n8n/` |

External skills (auto-installed by `/setup`):
- **Superpowers** — TDD, parallel agents, plan writing, code review workflows
- **oh-my-claudecode (OMC)** — 29 specialized agents, ultrawork, team, autopilot, and more

### Layer 3 — Hooks

Hooks run Python scripts automatically on Claude Code events, enforcing rules regardless of Claude's decisions.

| Event | Script | What it does |
|-------|--------|-------------|
| `PreToolUse(Read/Grep/Glob)` | `guard-file-read.py` | Blocks reads of `node_modules`, `dist`, lock files, etc. |
| `PreToolUse(Bash)` | `guard-bash.py` | Blocks destructive shell patterns |
| `PreToolUse(Bash)` | `bash-output-limiter.py` | Limits Bash output size |
| `PreToolUse(Bash)` | `guard-golang-best-practices.py` | Detects Go best practice violations |
| `PostToolUse(Write/Edit)` | `skill-hook-analyzer.py` | Suggests hooks when new skills are added |
| `PostToolUse(Bash: git worktree)` | `qmd-worktree-sync.py` | Keeps QMD index in sync with worktrees |
| `Stop` | `doc-guardian.py` | Detects missing/stale `CLAUDE.md` at session end |
| `Stop` | `context-monitor.py` | 60% (consider `/compact`) · 80% (urgent `/clear` or `/compact`) |

### Layer 4 — OMC Multi-Agent Orchestration

oh-my-claudecode (OMC) coordinates specialized agents for each task type.

| Keyword | Behavior |
|---------|----------|
| `autopilot` | Autonomous single-task execution |
| `ultrawork` / `ulw` | Parallel high-throughput execution |
| `ralph` | Self-referential loop until goal is met |
| `team N:executor` | N parallel agents on a shared task list |
| `deep interview` | Socratic requirements interview |
| `ccg` | Claude + Codex + Gemini triple verification |
| `ultraqa` | Autonomous QA cycling until all goals pass |

### Layer 5 — Triple-Model Verification

| Model | Role |
|-------|------|
| Claude | Implementation · test writing |
| Codex (OpenAI) | Independent diff review · security · logic errors |
| Gemini | UI/UX review · large-context analysis |

```bash
# Codex review
git diff HEAD~1 | codex "Review this diff for bugs, security issues, and logic errors."
# Or: /codex:review

# Triple verification (CCG mode)
/ccg "Review implemented feature"
```

Findings are gated by severity:
- **HIGH** → fix before next wave
- **WARN** → fix before QA
- **INFO** → optional

### Layer 6 — QMD Semantic Search

[QMD](https://github.com/tobias-luedtke/qmd) indexes the codebase with hybrid BM25 + vector search. Claude always queries QMD before opening any file.

```
mcp__qmd__query     →  conceptual search ("user auth flow")
mcp__qmd__get       →  fetch a specific file by path
mcp__qmd__multi_get →  fetch multiple files at once
```

## The Power Stack Pipeline v2

For non-trivial projects, run `/power-stack`:

```
deep-interview → omc-plan → ultrawork/team + TDD → codex:review → ultraqa → ship
```

| Stage | Command | Purpose |
|-------|---------|---------|
| Plan | `/oh-my-claudecode:deep-interview` | Socratic requirements clarification |
| Architect | `/oh-my-claudecode:omc-plan --consensus` | Consensus-based plan |
| Implement | `ultrawork` / `team N:executor` | TDD + parallel execution |
| Verify | `/codex:review` + `/ccg` | Independent triple-model review |
| QA | `/oh-my-claudecode:ultraqa` | Autonomous cycling until goals pass |
| Ship | `/commit-commands:commit-push-pr` | Commit · push · open PR |

State persists across sessions in `.omc/`. Keep context under 50% per session.

## Migrating from v1

If you need the full v1 stack (gstack + GSD + Superpowers):

```bash
git checkout v1-full-stack
```

v2 changes summary:
- Rules: 7 files → 3 files (44% overhead reduction)
- State: `.planning/` → `.omc/`
- Pipeline: gstack/GSD → OMC multi-agent
- Verification: dual → triple (Gemini added)

## Manual Setup

If you prefer not to use `/setup`:

**1. CLI tools:**

```bash
# Codex CLI (OpenAI code review)
npm install -g @openai/codex

# Gemini CLI (UI/UX review and large-context analysis)
npm install -g @google/gemini-cli

# QMD (codebase semantic search)
npm install -g @tobilu/qmd
```

**2. Claude Code plugins:**

```bash
# OMC — install first (multi-agent orchestration core)
claude plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
claude plugin install oh-my-claudecode

# Superpowers (TDD and execution discipline)
claude plugin install superpowers@claude-plugins-official

# Codex plugin (dual verification)
claude plugin marketplace add openai/codex-plugin-cc
claude plugin install codex@openai-codex

# Utilities
claude plugin install commit-commands@claude-plugins-official
claude plugin install skill-creator@claude-plugins-official
```

**3. OMC initialization:**

```
/oh-my-claudecode:omc-setup --local
```

**4. QMD index:**

```bash
DIR=$(basename "$PWD")
qmd collection add . --name "$DIR" --mask "**/*.{ts,tsx,js,jsx,py,go,rs,md,json,yaml,yml,toml}"
qmd collection add .claude/rules --name rules --mask "**/*.md"
qmd update && qmd embed --chunk-strategy auto
```

> First run of `qmd embed` downloads a ~2GB local model.

**5. MCP server** — add to `~/.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "qmd": { "command": "qmd", "args": ["mcp"] }
  }
}
```

Restart Claude Code after adding.

**6. API keys and authentication:**

```bash
# OpenAI (Codex)
export OPENAI_API_KEY=sk-...   # add to shell profile
codex login

# Gemini (Google OAuth)
gemini   # opens browser for authentication
```

## Principles

Four principles from Andrej Karpathy's approach to AI-assisted coding:

1. **Think Before Coding** — state assumptions, ask when uncertain, push back on overcomplicated requests
2. **Simplicity First** — no features, abstractions, or error handling beyond what was asked
3. **Surgical Changes** — only modify code directly related to the request; never "improve" adjacent code
4. **Goal-Driven Execution** — transform tasks into verifiable goals; write tests before implementation

Enforced automatically via `.claude/rules/coding-principles.md`.

## License

MIT
