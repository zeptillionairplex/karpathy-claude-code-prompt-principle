# Architecture

## Context Boundary Principle
Every folder is a self-contained context boundary. One feature = one folder. All related code lives there.
A contributor (human or AI) working on a feature MUST NOT need to read unrelated folders.

## Frontend: Feature-Sliced Design (FSD)
```
app → pages → widgets → features → entities → shared
```
Dependency flows downward only. Each slice exports only via `index.ts`.
→ See docs/rules/react.md for layer rules.

## Backend: Clean Architecture
```
infrastructure → interfaces → use_cases → entities
```
Dependency points inward (toward domain). Interfaces injected, never concrete.
→ See docs/rules/go.md or docs/rules/python.md for layer rules.

## Self-Describing Folders
Every domain/feature folder has a `CLAUDE.md` (auto-loaded by Claude Code).
→ Run `/evolving-docs` to create or update a folder's `CLAUDE.md`.
→ **Automated:** `doc-guardian.py` (Stop hook) detects missing/stale `CLAUDE.md` after each session and prompts you to run `/evolving-docs`.

## Navigation Rules
- Read the folder's `CLAUDE.md` first. Never explore unrelated folders.
- If exploration requires 4+ tool calls without a `CLAUDE.md` to guide you, stop and ask.
- One-way dependency: higher layers import lower. Never reverse.
