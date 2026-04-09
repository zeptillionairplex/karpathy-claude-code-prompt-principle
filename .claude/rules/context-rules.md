# Context Rules

Loading unnecessary files wastes tokens and degrades performance. Never read, search, or load the following.

## Never Read

- **Dependencies:** `node_modules/`, `vendor/`, `.venv/`, `venv/`, `__pycache__/`, `dist/`, `build/`, `out/`, `.next/`, `.nuxt/`, `*.min.js`, `*.min.css`, `*.map`, lock files (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `go.sum`, `poetry.lock`)
- **Secrets:** `.env`, `.env.*`, `*.pem`, `*.key`, `*.crt`, `settings.local.json`, `*.local.*`
- **Editor/OS noise:** `.git/`, `.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/` (unless task is IDE config), `*.log`, `*.tmp`, `*.swp`
- **Generated/binary:** `coverage/`, `.nyc_output/`, `*.lcov`, `*.png`, `*.jpg`, `*.gif`, `*.ico`, `*.woff*`, `*.ttf`, `*.sqlite`, `*.db`

When Glob/Grep might hit these: filter before running. If a result comes from a forbidden path, skip it. If unsure, check `.gitignore` first.

| You want to know… | Read this instead |
|---|---|
| Packages used | `package.json`, `go.mod`, `pyproject.toml` |
| DB schema | migration files or schema definitions |
| App config | `.env.example` or config type definitions |
| Build behavior | `vite.config.ts`, `next.config.js`, etc. |

## /clear vs /compact

| Situation | Command |
|---|---|
| Task fully done, switching to a new task | `/clear` |
| Mid-task milestone (research done, before implementation) | `/compact` |
| Mid-implementation | ❌ never `/compact` — loses variable names, file paths, partial state |

- **`/clear`** — wipes context completely. Free, instant. Use only when switching tasks.
- **`/compact`** — summarizes and compresses. Preserves key state. Use only at milestones between distinct work phases.

**Context Monitor signals** (fired by `context-monitor` Stop hook):
- **60%** → consider `/compact` if at a milestone
- **80%** → run `/clear` or `/compact` immediately
