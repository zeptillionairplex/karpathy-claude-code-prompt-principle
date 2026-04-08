# Context Hygiene — What NOT to Read

Never read, search, or load the following into context. These add tokens with no benefit.

## Dependency trees (installable, not authored)

- `node_modules/`, `vendor/`, `.venv/`, `venv/`, `__pycache__/`
- `dist/`, `build/`, `out/`, `.next/`, `.nuxt/`
- Any file matching `*.min.js`, `*.min.css`, `*.map`
- Lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `go.sum`, `poetry.lock`
  → These encode dependency trees. Use `package.json` / `go.mod` / `pyproject.toml` instead.

## Secrets and local config

- `.env`, `.env.*`, `*.pem`, `*.key`, `*.crt`
- `settings.local.json`, `*.local.*`

## Editor and OS noise

- `.git/`, `.DS_Store`, `Thumbs.db`
- `.idea/`, `.vscode/` (unless the task is about IDE config)
- `*.log`, `*.tmp`, `*.swp`

## Generated and binary

- `coverage/`, `.nyc_output/`, `*.lcov`
- `*.png`, `*.jpg`, `*.gif`, `*.ico`, `*.woff`, `*.woff2`, `*.ttf`
- `*.sqlite`, `*.db` (read schema files instead)

## When Glob or Grep might hit these

- Before running Glob with a broad pattern (e.g. `**/*`), mentally filter the above.
- If a Grep result comes from one of these paths, skip it — do not open the file.
- If unsure whether a file is generated, check if it is listed in `.gitignore` first.

## What to read instead

| You want to know… | Read this, not that |
|---|---|
| What packages are used | `package.json`, `go.mod`, `pyproject.toml` |
| DB schema | migration files or schema definition files |
| App config | `.env.example` or config type definitions |
| Build output behavior | `vite.config.ts`, `next.config.js`, etc. |
